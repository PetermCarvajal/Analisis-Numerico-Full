import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


class InterfazEjercicio5:
    def __init__(self, root):
        self.root = root
        self.root.title("Ejercicio 5: Predicción de Escalabilidad (Secante)")
        self.root.configure(bg="#2d2d44")

        # Variables GUI
        self.var_funcion = tk.StringVar(value="x * np.exp(-x/2) - 0.3")
        self.var_x0 = tk.StringVar(value="0.5")
        self.var_x1 = tk.StringVar(value="1.0")
        self.var_tol = tk.StringVar(value="1e-9")

        self.mostrar_graf = tk.BooleanVar(value=True)
        self.mostrar_iter = tk.BooleanVar(value=True)

        self.construir_gui()

    def construir_gui(self):
        # Frame Principal
        main_frame = tk.Frame(self.root, bg="#2d2d44")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === PANEL IZQUIERDO (Controles) ===
        panel_izq = tk.Frame(main_frame, bg="#353550", padx=15, pady=15)
        panel_izq.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(panel_izq, text="PARÁMETROS DEL MÉTODO", font=("Arial", 12, "bold"), bg="#353550", fg="white").pack(
            pady=(0, 10))

        def crear_input(texto, variable):
            f = tk.Frame(panel_izq, bg="#353550")
            f.pack(fill="x", pady=5)
            tk.Label(f, text=texto, bg="#353550", fg="#b0b0d0", width=15, anchor="w").pack(side="left")
            tk.Entry(f, textvariable=variable, bg="#2d2d44", fg="white", insertbackground="white").pack(side="right",
                                                                                                        fill="x",
                                                                                                        expand=True)

        crear_input("Función P(x):", self.var_funcion)
        crear_input("x0 (n-1):", self.var_x0)
        crear_input("x1 (n):", self.var_x1)
        crear_input("Tolerancia:", self.var_tol)

        # Checkboxes
        tk.Checkbutton(panel_izq, text="Mostrar Gráfica", variable=self.mostrar_graf, bg="#353550", fg="white",
                       selectcolor="#2d2d44", command=self.gestionar_paneles).pack(anchor="w", pady=(10, 0))
        tk.Checkbutton(panel_izq, text="Mostrar Iteraciones", variable=self.mostrar_iter, bg="#353550", fg="white",
                       selectcolor="#2d2d44", command=self.gestionar_paneles).pack(anchor="w")

        tk.Button(panel_izq, text="CALCULAR Y COMPARAR", bg="#5c7cfa", fg="white", font=("Arial", 10, "bold"),
                  command=self.calcular).pack(fill="x", pady=20)

        # Panel de Resultados Generales
        self.lbl_resultados = tk.Label(panel_izq, text="Esperando cálculo...", font=("Consolas", 11, "bold"),
                                       bg="#1a1a2e", fg="#40c057", justify="left", padx=10, pady=10)
        self.lbl_resultados.pack(fill="x")

        # Tabla Comparativa (Oculta por defecto, se muestra si es el Ej 5)
        self.frame_comparativa = tk.LabelFrame(panel_izq, text="Comparativa vs Newton-Raphson", bg="#353550",
                                               fg="#f9e2af")
        self.tree_comp = ttk.Treeview(self.frame_comparativa, columns=("Metrica", "Sec", "New"), show="headings",
                                      height=3)
        self.tree_comp.heading("Metrica", text="Métrica");
        self.tree_comp.heading("Sec", text="Secante");
        self.tree_comp.heading("New", text="Newton")
        self.tree_comp.column("Metrica", width=100);
        self.tree_comp.column("Sec", width=80, anchor="center");
        self.tree_comp.column("New", width=80, anchor="center")
        self.tree_comp.pack(fill="x", padx=5, pady=5)

        # === PANEL DERECHO (Gráficas y Tablas) ===
        self.panel_der = tk.Frame(main_frame, bg="#2d2d44")
        self.panel_der.pack(side="right", fill="both", expand=True)

        # Gráfica
        self.viz = VisualizadorGrafico(self.panel_der)

        # Tabla Iteraciones
        columnas = ("n", "x_n-1", "x_n", "f(x_n-1)", "f(x_n)", "x_n+1", "Error")
        self.tree_iter = ttk.Treeview(self.panel_der, columns=columnas, show="headings")
        for col in columnas:
            self.tree_iter.heading(col, text=col)
            self.tree_iter.column(col, width=90, anchor="center")

        self.gestionar_paneles()

    def gestionar_paneles(self):
        if self.mostrar_graf.get():
            self.viz.widget.pack(fill="both", expand=True, pady=(0, 5))
        else:
            self.viz.widget.pack_forget()

        if self.mostrar_iter.get():
            self.tree_iter.pack(fill="both", expand=True)
        else:
            self.tree_iter.pack_forget()

    def calcular(self):
        try:
            # Configurar Evaluador Seguro
            entorno = {"np": np, "x": 0}  # Dummy x
            funcion_str = self.var_funcion.get()
            f = lambda x_val: eval(funcion_str.replace("^", "**"), {"np": np, "x": x_val})

            tol = float(self.var_tol.get())
            x0, x1 = float(self.var_x0.get()), float(self.var_x1.get())

            # Ejecutar Secante
            secante = SecanteEj5(f, tol)
            res_sec = secante.calcular(x0, x1)

            # Actualizar GUI: Tabla Iteraciones
            self.tree_iter.delete(*self.tree_iter.get_children())
            for fila in res_sec['historial']:
                self.tree_iter.insert("", "end", values=(
                    fila['n'], f"{fila['x_n-1']:.6f}", f"{fila['x_n']:.6f}",
                    f"{fila['f(x_n-1)']:.2e}", f"{fila['f(x_n)']:.2e}",
                    f"{fila['x_n+1']:.6f}", f"{fila['error']:.2e}"
                ))

            # Actualizar GUI: Gráfica
            self.viz.graficar_metodo(f, res_sec['raiz'], res_sec['historial'], "Convergencia Secante",
                                     mostrar_secantes=True)

            # Actualizar GUI: Resultados
            self.lbl_resultados.config(
                text=f"RAÍZ: {res_sec['raiz']:.8f}\nITER: {res_sec['iteraciones']}\nTIEMPO: {res_sec['tiempo']:.2f} ms")

            # === COMPARACIÓN CON NEWTON (Punto 20 y 21) ===
            # Detectamos si es la fórmula por defecto del Ejercicio 5
            if "np.exp(-x/2)" in funcion_str and "0.3" in funcion_str:
                self.frame_comparativa.pack(fill="x", pady=10)

                # Ejecutamos Newton en segundo plano con la derivada exigida
                df = lambda x_val: np.exp(-x_val / 2) * (1 - x_val / 2)

                # Lógica rápida de Newton para sacar métricas
                import time
                t_ini = time.perf_counter()
                xn = x1;
                iter_n = 0;
                eval_n = 0
                for i in range(1, 100):
                    fxn = f(xn);
                    dfxn = df(xn)
                    eval_n += 2
                    x_next = xn - fxn / dfxn
                    if abs(x_next - xn) < tol:
                        iter_n = i
                        break
                    xn = x_next
                t_newton = (time.perf_counter() - t_ini) * 1000

                # Llenar tabla comparativa
                self.tree_comp.delete(*self.tree_comp.get_children())
                self.tree_comp.insert("", "end", values=("Iteraciones", res_sec['iteraciones'], iter_n))
                self.tree_comp.insert("", "end", values=("Evals. Función", res_sec['evaluaciones'], eval_n))
                self.tree_comp.insert("", "end", values=("Tiempo (ms)", f"{res_sec['tiempo']:.3f}", f"{t_newton:.3f}"))
            else:
                self.frame_comparativa.pack_forget()  # Ocultar si cambian la fórmula

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazEjercicio5(root)
    root.mainloop()