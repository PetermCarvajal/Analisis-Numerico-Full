import tkinter as tk
from tkinter import ttk, messagebox
import time
import math

from utils.validaciones import ValidadorEntradas
from interfaz.graficas import VisualizadorGrafico
from metodos.biseccion import Biseccion
from metodos.falsa_posicion import FalsaPosicion
from metodos.secante import Secante
from metodos.punto_fijo import PuntoFijo
from metodos.newton_raphson import NewtonRaphson

# --- TEMA OSCURO PASTEL ---
ESTILO = {
    "bg_principal": "#1e1e2b", "bg_paneles": "#242436", "bg_entradas": "#1a1a26",
    "texto": "#c8c8d8", "texto_sec": "#8a8a9b", "btn_calc": "#6284ff",
    "btn_limpiar": "#404059", "exito": "#50fa7b", "alerta": "#ff5555"
}


def formatear_valor(valor):
    """
    Formatea el número a 8 decimales fijos.
    Si el valor es muy pequeño o muy grande, aplica notación científica con 8 decimales.
    """
    if valor is None or valor == '-' or valor == '--------':
        return valor
    if isinstance(valor, str):
        return valor
    try:
        val = float(valor)
        if val == 0.0:
            return "0.00000000"
        if abs(val) < 1e-4 or abs(val) >= 1e8:
            return f"{val:.8e}"
        else:
            return f"{val:.8f}"
    except (ValueError, TypeError):
        return str(valor)


# --- FUNCIÓN DE VALIDACIÓN IMPORTADA DEL PROYECTO DE LA PROFESORA ---
def validar_intervalo_signo(f, a, b):
    fa, fb = float(f(a)), float(f(b))
    if math.isnan(fa) or math.isnan(fb):
        raise ValueError(f"Evaluación produjo NaN en los extremos: f({a})={fa}, f({b})={fb}.")
    if fa * fb > 0:
        raise ValueError(f"No hay cambio de signo en [{a}, {b}]: f(a)={fa:.6g}, f(b)={fb:.6g}.")


class AppMetodosNumericos:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=ESTILO["bg_principal"])

        self.mostrar_grafica_var = tk.BooleanVar(value=True)
        self.mostrar_tabla_var = tk.BooleanVar(value=True)
        self.mostrar_convergencia_var = tk.BooleanVar(value=False)
        self.datos_actuales = None

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TCombobox", fieldbackground=ESTILO["bg_entradas"], background=ESTILO["bg_paneles"],
                        foreground=ESTILO["texto"])
        style.configure("Treeview", background=ESTILO["bg_paneles"], foreground=ESTILO["texto"],
                        fieldbackground=ESTILO["bg_paneles"], rowheight=25, borderwidth=0)
        style.configure("Treeview.Heading", background="#1a1a26", foreground="#6284ff",
                        font=("Arial", 9, "bold"), borderwidth=1, relief="solid")
        style.map("Treeview", background=[("selected", "#3a3a50")], foreground=[("selected", "#ffffff")])

        self.construir_interfaz()

    def construir_interfaz(self):
        self.main_container = tk.Frame(self.root, bg=ESTILO["bg_principal"])
        self.main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # === PANEL IZQUIERDO ===
        self.col_izq = tk.Frame(self.main_container, bg=ESTILO["bg_principal"], width=350)
        self.col_izq.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(self.col_izq, text="Seleccione el Método / Ejercicio:", font=("Arial", 10, "bold"),
                 bg=ESTILO["bg_principal"], fg="#6284ff").pack(anchor="w")
        self.combo_metodo = ttk.Combobox(self.col_izq, values=[
            "Bisección (Ej. 1 - Hash Table)", "Falsa Posición (Ej. 2 - Balanceo)",
            "Punto Fijo (Ej. 3 - BD)", "Newton-Raphson (Ej. 4 - Threads)", "Secante (Ej. 5 - Cloud)"
        ], width=35, state="readonly")
        self.combo_metodo.pack(fill="x", pady=5)
        self.combo_metodo.current(0)
        self.combo_metodo.bind("<<ComboboxSelected>>", self.cambio_de_metodo)

        self.frame_campos = tk.LabelFrame(self.col_izq, text="Parámetros de entrada", bg=ESTILO["bg_principal"],
                                          fg="#6284ff", padx=10, pady=10)
        self.frame_campos.pack(fill="x", pady=10)

        self.var_funcion, self.var_derivada = tk.StringVar(), tk.StringVar()
        self.var_x0, self.var_x1, self.var_tol, self.var_iter = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

        self.var_comparar_fp_bi = tk.BooleanVar(value=False)
        self.var_comparar_multi_pf = tk.BooleanVar(value=True)
        self.var_comparar_ej4 = tk.BooleanVar(value=False)
        self.var_usar_derivada_ej1 = tk.BooleanVar(value=False)

        frame_opciones = tk.Frame(self.col_izq, bg=ESTILO["bg_principal"])
        frame_opciones.pack(fill="x", pady=5)

        tk.Checkbutton(frame_opciones, text="Mostrar Gráfica Principal", variable=self.mostrar_grafica_var,
                       bg=ESTILO["bg_principal"], fg=ESTILO["texto"], selectcolor=ESTILO["bg_principal"],
                       command=self.actualizar_vistas).pack(anchor="w")
        tk.Checkbutton(frame_opciones, text="Mostrar Convergencia (Log)", variable=self.mostrar_convergencia_var,
                       bg=ESTILO["bg_principal"], fg=ESTILO["texto"], selectcolor=ESTILO["bg_principal"],
                       command=self.actualizar_vistas).pack(anchor="w")
        tk.Checkbutton(frame_opciones, text="Mostrar Tabla", variable=self.mostrar_tabla_var, bg=ESTILO["bg_principal"],
                       fg=ESTILO["texto"], selectcolor=ESTILO["bg_principal"], command=self.actualizar_vistas).pack(
            anchor="w")

        frame_btns = tk.Frame(self.col_izq, bg=ESTILO["bg_principal"])
        frame_btns.pack(fill="x", pady=10)
        tk.Button(frame_btns, text="▶ Calcular", bg=ESTILO["btn_calc"], fg="#ffffff", font=("Arial", 10, "bold"),
                  command=self.ejecutar, relief="flat", padx=10, pady=5).pack(side="left", expand=True, fill="x",
                                                                              padx=5)
        tk.Button(frame_btns, text="↺ Limpiar", bg=ESTILO["btn_limpiar"], fg="#ffffff", font=("Arial", 10),
                  command=self.limpiar, relief="flat", padx=10, pady=5).pack(side="right", expand=True, fill="x",
                                                                             padx=5)

        self.frame_resultados = tk.LabelFrame(self.col_izq, text="Resultado Final", bg=ESTILO["bg_principal"],
                                              fg="#6284ff", padx=15, pady=15)
        self.frame_resultados.pack(fill="x", pady=10)

        self.lbl_res_texto = tk.Label(self.frame_resultados,
                                      text="RAÍZ:\nITERACIONES:\nERROR ABS:\nERROR REL:\nTIEMPO:",
                                      font=("Consolas", 11, "bold"), bg=ESTILO["bg_principal"], fg=ESTILO["texto"],
                                      justify="left")
        self.lbl_res_texto.pack(anchor="w")

        self.frame_comparativa = tk.LabelFrame(self.col_izq, text="Comparativa de Métodos", bg=ESTILO["bg_principal"],
                                               fg="#ffb86c")
        self.tree_comp = ttk.Treeview(self.frame_comparativa, columns=("Metrica", "M1", "M2"), show="headings",
                                      height=4)
        self.tree_comp.column("Metrica", width=100, anchor="w")
        self.tree_comp.column("M1", width=110, anchor="center")
        self.tree_comp.column("M2", width=110, anchor="center")
        self.tree_comp.pack(fill="x", padx=5, pady=5)

        # === PANEL DERECHO ===
        self.col_der = tk.Frame(self.main_container, bg=ESTILO["bg_principal"])
        self.col_der.pack(side="right", fill="both", expand=True)

        self.frame_grafica = tk.Frame(self.col_der, bg=ESTILO["bg_paneles"])
        self.viz = VisualizadorGrafico(self.frame_grafica)

        self.frame_tabla = tk.LabelFrame(self.col_der, text="Tabla de Iteraciones", bg=ESTILO["bg_principal"],
                                         fg="#6284ff")
        self.scroll_tabla = ttk.Scrollbar(self.frame_tabla, orient="vertical")
        self.tabla = ttk.Treeview(self.frame_tabla, show="headings", yscrollcommand=self.scroll_tabla.set)
        self.scroll_tabla.config(command=self.tabla.yview)

        self.frame_tabla_sec = tk.LabelFrame(self.col_der, text="Tabla Comparativa Detallada",
                                             bg=ESTILO["bg_principal"], fg="#ffb86c")
        self.scroll_tabla_sec = ttk.Scrollbar(self.frame_tabla_sec, orient="vertical")
        self.tabla_sec = ttk.Treeview(self.frame_tabla_sec, show="headings", height=5,
                                      yscrollcommand=self.scroll_tabla_sec.set)
        self.scroll_tabla_sec.config(command=self.tabla_sec.yview)

        self.cambio_de_metodo()

    def actualizar_vistas(self):
        if self.mostrar_grafica_var.get() or self.mostrar_convergencia_var.get():
            self.frame_grafica.pack(fill="both", expand=True, pady=(0, 5))
        else:
            self.frame_grafica.pack_forget()

        if self.mostrar_tabla_var.get():
            self.frame_tabla.pack(fill="both", expand=True, padx=5, pady=5)
            self.scroll_tabla.pack(side="right", fill="y")
            self.tabla.pack(side="left", fill="both", expand=True)

            if self.datos_actuales and self.datos_actuales.get('historial_secundario'):
                self.frame_tabla_sec.pack(fill="both", expand=True, padx=5, pady=5)
                self.scroll_tabla_sec.pack(side="right", fill="y")
                self.tabla_sec.pack(side="left", fill="both", expand=True)
            else:
                self.frame_tabla_sec.pack_forget()
        else:
            self.frame_tabla.pack_forget()
            self.frame_tabla_sec.pack_forget()

        if self.datos_actuales:
            self.viz.graficar_metodo(
                f=self.datos_actuales['f'],
                raiz=self.datos_actuales['raiz'],
                historial=self.datos_actuales['historial'],
                titulo=f"Convergencia - {self.datos_actuales['metodo']}",
                mostrar_secantes="Secante" in self.datos_actuales['metodo'],
                mostrar_tangentes="Newton" in self.datos_actuales['metodo'],
                mostrar_convergencia=self.mostrar_convergencia_var.get(),
                mostrar_principal=self.mostrar_grafica_var.get(),
                historiales_multiples=self.datos_actuales.get('historiales_multiples', None),
                historial_secundario=self.datos_actuales.get('historial_secundario', None),
                nombre_metodo=self.datos_actuales['metodo']
            )

    def cambio_de_metodo(self, event=None):
        self.datos_actuales = None
        self.frame_comparativa.pack_forget()
        self.frame_tabla_sec.pack_forget()
        self.cargar_valores_defecto()
        self.configurar_columnas_tabla()
        self.viz.fig.clf()
        self.viz.canvas.draw()
        self.actualizar_vistas()

    def toggle_derivada_ej1(self):
        if self.var_usar_derivada_ej1.get():
            self.var_funcion.set("1.6*x - 3.2 + 1/(x+1)")
        else:
            self.var_funcion.set("2.5 + 0.8*x**2 - 3.2*x + np.log(x+1)")

    def dibujar_campos_entrada(self):
        for widget in self.frame_campos.winfo_children(): widget.destroy()
        metodo = self.combo_metodo.get()

        if "Punto Fijo" in metodo:
            self.crear_fila_input("Función g(x):", self.var_funcion)
            self.crear_fila_input("Valor inicial (x0):", self.var_x0)
            chk = tk.Checkbutton(self.frame_campos, text="Comparar x0 (0.5, 1.0, 1.5, 2.0)",
                                 variable=self.var_comparar_multi_pf, bg=ESTILO["bg_principal"], fg="#ffb86c",
                                 selectcolor=ESTILO["bg_principal"])
            chk.pack(anchor="w", pady=4)
        else:
            self.crear_fila_input("Función f(x) / T(λ):", self.var_funcion)

            if "Newton" in metodo:
                self.crear_fila_input("Derivada f'(x):", self.var_derivada)
                tk.Checkbutton(self.frame_campos, text="Iterar Prof (1.0, 2.0, 3.0, 5.0)",
                               variable=self.var_comparar_ej4, bg=ESTILO["bg_principal"], fg="#ffb86c",
                               selectcolor=ESTILO["bg_principal"]).pack(anchor="w", pady=4)
                self.crear_fila_input("Valor inicial (x0):", self.var_x0)

            elif "Bisección" in metodo:
                self.crear_fila_input("Límite a:", self.var_x0)
                self.crear_fila_input("Límite b:", self.var_x1)
                tk.Checkbutton(self.frame_campos, text="Usar Derivada T'(λ) (Encuentra el óptimo)",
                               variable=self.var_usar_derivada_ej1, bg=ESTILO["bg_principal"], fg="#50fa7b",
                               selectcolor=ESTILO["bg_principal"], command=self.toggle_derivada_ej1).pack(anchor="w",
                                                                                                          pady=4)

            elif "Falsa Posición" in metodo:
                self.crear_fila_input("Límite a:", self.var_x0)
                self.crear_fila_input("Límite b:", self.var_x1)
                tk.Checkbutton(self.frame_campos, text="Comparar con Bisección", variable=self.var_comparar_fp_bi,
                               bg=ESTILO["bg_principal"], fg="#ffb86c", selectcolor=ESTILO["bg_principal"]).pack(
                    anchor="w", pady=4)
                tk.Button(self.frame_campos, text="📊 Comparar (F. Posición vs Bisección)",
                          bg="#ffb86c", fg="#1f1d24", font=("Arial", 9, "bold"),
                          command=self.ejecutar_comparativa_manual).pack(fill="x", pady=8)

            elif "Secante" in metodo:
                self.crear_fila_input("Límite a / x(n-1):", self.var_x0)
                self.crear_fila_input("Límite b / x(n):", self.var_x1)

        self.crear_fila_input("Tolerancia:", self.var_tol)
        self.crear_fila_input("Máx. Iteraciones:", self.var_iter)

    def crear_fila_input(self, texto, variable):
        frame = tk.Frame(self.frame_campos, bg=ESTILO["bg_principal"])
        frame.pack(fill="x", pady=4)
        tk.Label(frame, text=texto, bg=ESTILO["bg_principal"], fg=ESTILO["texto_sec"], width=18, anchor="w").pack(
            side="left")
        tk.Entry(frame, textvariable=variable, bg=ESTILO["bg_entradas"], fg=ESTILO["texto"], insertbackground="#ffffff",
                 relief="flat", highlightbackground="#3a3a50", highlightthickness=1).pack(side="right", expand=True,
                                                                                          fill="x", ipady=3)

    def configurar_columnas_especificas(self, tree, metodo):
        tree.delete(*tree.get_children())

        if "Secante" in metodo:
            cols = ("n", "x_n-1", "x_n", "f(x_n-1)", "f(x_n)", "x_n+1", "Error Abs")
        elif "Newton" in metodo:
            cols = ("n", "x_n", "f(x_n)", "f'(x_n)", "Error Abs", "Error Rel")
        elif "Punto Fijo" in metodo:
            cols = ("n", "x_n", "g(x_n)", "|x_n - g(x_n)|", "Error Rel")
        else:
            cols = ("n", "a", "b", "c", "f(c)", "Error Abs", "Error Rel")

        tree["columns"] = cols
        for col in cols:
            tree.heading(col, text=col)
            width = 85 if col in ["Error Abs", "Error Rel"] else 95
            tree.column(col, width=width, anchor="center")

    def configurar_columnas_tabla(self):
        metodo = self.combo_metodo.get()
        self.configurar_columnas_especificas(self.tabla, metodo)

    def cargar_valores_defecto(self):
        self.dibujar_campos_entrada()
        sel = self.combo_metodo.get()

        self.var_comparar_ej4.set(False)
        self.var_comparar_fp_bi.set(False)
        self.var_usar_derivada_ej1.set(False)
        self.mostrar_convergencia_var.set("Newton" in sel or "Punto Fijo" in sel)

        if "Bisección" in sel:
            self.var_funcion.set("2.5 + 0.8*x**2 - 3.2*x + np.log(x+1)")
            self.var_x0.set("0.5")
            self.var_x1.set("2.5")
            self.var_tol.set("1e-6")
        elif "Falsa Posición" in sel:
            self.var_funcion.set("x**3 - 6*x**2 + 11*x - 6.5")
            self.var_x0.set("2.0")
            self.var_x1.set("4.0")
            self.var_tol.set("1e-7")
        elif "Punto Fijo" in sel:
            self.var_funcion.set("0.5 * np.cos(x) + 1.5")
            self.var_x0.set("1.0")
            self.var_tol.set("1e-8")
        elif "Newton" in sel:
            self.var_funcion.set("x**3 - 8*x**2 + 20*x - 16")
            self.var_derivada.set("3*x**2 - 16*x + 20")
            self.var_x0.set("3.0")
            self.var_tol.set("1e-10")
        elif "Secante" in sel:
            self.var_funcion.set("x * np.exp(-x/2) - 0.3")
            self.var_x0.set("0.5")
            self.var_x1.set("1.0")
            self.var_tol.set("1e-9")

        self.var_iter.set("100")

    def limpiar(self):
        self.var_funcion.set("")
        self.var_derivada.set("")
        self.var_x0.set("")
        self.var_x1.set("")
        self.tabla.delete(*self.tabla.get_children())
        self.tabla_sec.delete(*self.tabla_sec.get_children())
        self.lbl_res_texto.config(text="RAÍZ:\nITERACIONES:\nERROR ABS:\nERROR REL:\nTIEMPO:", fg=ESTILO["texto"])
        self.frame_comparativa.pack_forget()
        self.frame_tabla_sec.pack_forget()
        self.datos_actuales = None
        self.viz.fig.clf()
        self.viz.canvas.draw()

    def ejecutar_comparativa_manual(self):
        self.ejecutar(modo_comparativa=True)

    def ejecutar(self, modo_comparativa=False):
        metodo_sel = self.combo_metodo.get()
        try:
            x0_tmp = self.var_x0.get()
            if "Newton" in metodo_sel and self.var_comparar_ej4.get(): x0_tmp = "1.0"
            if "Punto Fijo" in metodo_sel and self.var_comparar_multi_pf.get(): x0_tmp = "1.0"

            datos = ValidadorEntradas.validar_datos(
                self.var_funcion.get(), self.var_tol.get(), self.var_iter.get(),
                x0_tmp, self.var_x1.get() if self.var_x1.get() else None,
                self.var_derivada.get() if "Newton" in metodo_sel else None
            )
            f_eval = ValidadorEntradas.crear_evaluador(datos['funcion_str'])
            if "Newton" in metodo_sel: df_eval = ValidadorEntradas.crear_evaluador(datos['derivada_str'])

            if "Bisección" in metodo_sel or "Falsa Posición" in metodo_sel:
                validar_intervalo_signo(f_eval, datos['x0'], datos['x1'])

        except Exception as e:
            messagebox.showerror("Error de Entrada Matemático",
                                 str(e) + "\n\n💡 TIP: ¿La gráfica cruza por cero en este intervalo?")
            return

        historiales_multiples = None
        historial_secundario = None
        metodo_secundario = None
        tiempo_ms = 0

        try:
            inicio_tiempo = time.perf_counter()

            if ("Newton" in metodo_sel and self.var_comparar_ej4.get()) or (
                    "Punto Fijo" in metodo_sel and self.var_comparar_multi_pf.get()):
                valores_prof = [0.5, 1.0, 1.5, 2.0] if "Punto Fijo" in metodo_sel else [1.0, 2.0, 3.0, 5.0]
                mejor_res = None
                historiales_multiples = {}
                tiempo_total = 0

                for val in valores_prof:
                    t_ini = time.perf_counter()
                    if "Newton" in metodo_sel:
                        res = NewtonRaphson(f_eval, df_eval, datos['tol'], datos['max_iter']).calcular(val)
                    else:
                        res = PuntoFijo(f_eval, datos['tol'], datos['max_iter']).calcular(val)

                    tiempo_total += (time.perf_counter() - t_ini) * 1000
                    historiales_multiples[val] = res['historial']

                    if mejor_res is None or res['iteraciones_totales'] < mejor_res['iteraciones_totales']:
                        res['x0_ganador'] = val
                        mejor_res = res

                resultado = mejor_res
                tiempo_ms = tiempo_total

            elif modo_comparativa or ("Falsa Posición" in metodo_sel and self.var_comparar_fp_bi.get()):
                resultado = FalsaPosicion(f_eval, datos['tol'], datos['max_iter']).calcular(datos['x0'], datos['x1'])
                tiempo_ms = (time.perf_counter() - inicio_tiempo) * 1000

                res_bi = Biseccion(f_eval, datos['tol'], datos['max_iter']).calcular(datos['x0'], datos['x1'])
                historial_secundario = res_bi['historial']
                metodo_secundario = "Bisección"
                metodo_sel = "Falsa Posición"

                self.frame_comparativa.pack(fill="x", pady=10)
                self.frame_comparativa.config(text="Comparativa: F. Posición vs Bisección")
                self.tree_comp.heading("Metrica", text="Métrica")
                self.tree_comp.heading("M1", text="Falsa Posición")
                self.tree_comp.heading("M2", text="Bisección")
                self.tree_comp.delete(*self.tree_comp.get_children())

                self.tree_comp.insert("", "end", values=(
                "Iteraciones", resultado['iteraciones_totales'], res_bi['iteraciones_totales']))
                self.tree_comp.insert("", "end", values=(
                "Raíz Hallada", formatear_valor(resultado['raiz']), formatear_valor(res_bi['raiz'])))
                self.tree_comp.insert("", "end", values=(
                "Error Abs.", formatear_valor(resultado['historial'][-1]['error_absoluto']),
                formatear_valor(res_bi['historial'][-1]['error_absoluto'])))
                self.tree_comp.insert("", "end", values=(
                "Error Rel.", f"{formatear_valor(resultado['historial'][-1]['error_relativo'])}%",
                f"{formatear_valor(res_bi['historial'][-1]['error_relativo'])}%"))

            else:
                if "Bisección" in metodo_sel:
                    resultado = Biseccion(f_eval, datos['tol'], datos['max_iter']).calcular(datos['x0'], datos['x1'])
                elif "Falsa Posición" in metodo_sel:
                    resultado = FalsaPosicion(f_eval, datos['tol'], datos['max_iter']).calcular(datos['x0'],
                                                                                                datos['x1'])
                elif "Punto Fijo" in metodo_sel:
                    resultado = PuntoFijo(f_eval, datos['tol'], datos['max_iter']).calcular(datos['x0'])
                elif "Newton" in metodo_sel:
                    resultado = NewtonRaphson(f_eval, df_eval, datos['tol'], datos['max_iter']).calcular(datos['x0'])
                elif "Secante" in metodo_sel:
                    resultado = Secante(f_eval, datos['tol'], datos['max_iter']).calcular(datos['x0'], datos['x1'])

                tiempo_ms = (time.perf_counter() - inicio_tiempo) * 1000

            color_msj = ESTILO["exito"] if resultado['exito'] else ESTILO["alerta"]

            if resultado['historial']:
                error_abs_final = resultado['historial'][-1].get('error_absoluto', 0)
                error_rel_final = resultado['historial'][-1].get('error_relativo', 0)
            else:
                error_abs_final = 0
                error_rel_final = 0

            if historiales_multiples:
                texto_res = (f"🔥 MÁS RÁPIDO: x0 = {resultado['x0_ganador']}\n"
                             f"RAÍZ: {formatear_valor(resultado['raiz'])}\n"
                             f"ITERACIONES: {resultado['iteraciones_totales']}\n"
                             f"ERROR ABS: {formatear_valor(error_abs_final)}\n"
                             f"ERROR REL: {formatear_valor(error_rel_final)}%\n"
                             f"TIEMPO: {formatear_valor(tiempo_ms)} ms")
            else:
                texto_res = (f"RAÍZ: {formatear_valor(resultado['raiz'])}\n"
                             f"ITERACIONES: {resultado['iteraciones_totales']}\n"
                             f"ERROR ABS: {formatear_valor(error_abs_final)}\n"
                             f"ERROR REL: {formatear_valor(error_rel_final)}%\n"
                             f"TIEMPO: {formatear_valor(tiempo_ms)} ms")

            self.lbl_res_texto.config(text=texto_res, fg=color_msj)

        except Exception as e:
            messagebox.showerror("Error de Cálculo", str(e))
            return

        if not historiales_multiples and not historial_secundario:
            if "Newton" in metodo_sel and "x**3 - 8*x**2" in datos['funcion_str']:
                historial_secundario = self.ejecutar_comparacion_ej4(datos, resultado.get('iteraciones_totales', 0),
                                                                     tiempo_ms)
                metodo_secundario = "Secante"
            elif "Secante" in metodo_sel and "np.exp(-x/2)" in datos['funcion_str']:
                historial_secundario = self.ejecutar_comparacion_ej5(datos, resultado.get('iteraciones_totales', 0),
                                                                     resultado.get('evaluaciones', 0), tiempo_ms)
                metodo_secundario = "Newton"

        self.frame_tabla.config(text=f"Tabla de Iteraciones - {metodo_sel}")
        self.actualizar_tabla(resultado['historial'], metodo_sel, self.tabla)

        if historial_secundario and metodo_secundario:
            self.frame_tabla_sec.config(text=f"Tabla Comparativa Detallada - {metodo_secundario}")
            self.configurar_columnas_especificas(self.tabla_sec, metodo_secundario)
            self.actualizar_tabla(historial_secundario, metodo_secundario, self.tabla_sec)

        self.datos_actuales = {
            'f': f_eval,
            'raiz': resultado['raiz'],
            'historial': resultado['historial'],
            'metodo': metodo_sel,
            'historiales_multiples': historiales_multiples,
            'historial_secundario': historial_secundario
        }
        self.actualizar_vistas()

    def actualizar_tabla(self, historial, metodo, tree=None):
        if tree is None: tree = self.tabla
        tree.delete(*tree.get_children())

        for fila in historial:
            # RESTAURAMOS LA LÓGICA DE PRIMERA ITERACIÓN PARA LOS GUIONES
            es_primera = (fila.get('n', fila.get('iter', 1)) == 1)
            err_abs = fila.get('error_absoluto', fila.get('error_abs', 0))
            err_rel = fila.get('error_relativo', fila.get('error_rel', 0))

            err_abs_str = "--------" if es_primera else formatear_valor(err_abs)
            err_rel_str = "--------" if es_primera else f"{formatear_valor(err_rel)}%"

            n_val = fila.get('n', fila.get('iter', 1))

            if "Secante" in metodo:
                # Secante no tiene columna de error relativo, así que no se pasa err_rel_str
                valores = (n_val, formatear_valor(fila.get('x_n-1')), formatear_valor(fila.get('c')),
                           formatear_valor(fila.get('f(x_n-1)')), formatear_valor(fila.get('f(c)')),
                           formatear_valor(fila.get('x_n+1')), err_abs_str)
            elif "Newton" in metodo:
                valores = (n_val, formatear_valor(fila.get('c')), formatear_valor(fila.get('f(c)')),
                           formatear_valor(fila.get('f_prima(c)')), err_abs_str, err_rel_str)
            elif "Punto Fijo" in metodo:
                valores = (
                n_val, formatear_valor(fila.get('c')), formatear_valor(fila.get('f(c)')), err_abs_str, err_rel_str)
            else:
                valores = (
                n_val, formatear_valor(fila.get('a')), formatear_valor(fila.get('b')), formatear_valor(fila.get('c')),
                formatear_valor(fila.get('f(c)')), err_abs_str, err_rel_str)

            tree.insert("", "end", values=valores)

    def ejecutar_comparacion_ej4(self, datos_newton, iter_newton, tiempo_newton):
        self.frame_comparativa.pack(fill="x", pady=10)
        self.frame_comparativa.config(text="Comparativa vs Secante")
        f_eval = ValidadorEntradas.crear_evaluador(datos_newton['funcion_str'])
        self.tree_comp.heading("Metrica", text="Métrica")
        self.tree_comp.heading("M1", text="Newton")
        self.tree_comp.heading("M2", text="Secante")

        try:
            t_ini = time.perf_counter()
            res_sec = Secante(f_eval, datos_newton['tol'], datos_newton['max_iter']).calcular(datos_newton['x0'] - 0.5,
                                                                                              datos_newton['x0'])
            t_sec = (time.perf_counter() - t_ini) * 1000

            self.tree_comp.delete(*self.tree_comp.get_children())
            self.tree_comp.insert("", "end", values=("Iteraciones", iter_newton, res_sec['iteraciones_totales']))
            self.tree_comp.insert("", "end", values=(
            "Evals. Función", iter_newton * 2, res_sec.get('evaluaciones', res_sec['iteraciones_totales'] + 2)))
            self.tree_comp.insert("", "end",
                                  values=("Tiempo (ms)", formatear_valor(tiempo_newton), formatear_valor(t_sec)))

            return res_sec['historial']
        except:
            pass

    def ejecutar_comparacion_ej5(self, datos_secante, iter_secante, evals_secante, tiempo_secante):
        self.frame_comparativa.pack(fill="x", pady=10)
        self.frame_comparativa.config(text="Comparativa vs Newton")
        f_eval = ValidadorEntradas.crear_evaluador(datos_secante['funcion_str'])
        df_eval = ValidadorEntradas.crear_evaluador("np.exp(-x/2) * (1 - x/2)")
        self.tree_comp.heading("Metrica", text="Métrica")
        self.tree_comp.heading("M1", text="Secante")
        self.tree_comp.heading("M2", text="Newton")

        try:
            t_ini = time.perf_counter()
            res_newton = NewtonRaphson(f_eval, df_eval, datos_secante['tol'], datos_secante['max_iter']).calcular(
                datos_secante['x1'])
            t_newton = (time.perf_counter() - t_ini) * 1000

            self.tree_comp.delete(*self.tree_comp.get_children())
            self.tree_comp.insert("", "end", values=("Iteraciones", iter_secante, res_newton['iteraciones_totales']))
            self.tree_comp.insert("", "end",
                                  values=("Evals. Función", evals_secante, res_newton['iteraciones_totales'] * 2))
            self.tree_comp.insert("", "end",
                                  values=("Tiempo (ms)", formatear_valor(tiempo_secante), formatear_valor(t_newton)))

            return res_newton['historial']
        except:
            pass