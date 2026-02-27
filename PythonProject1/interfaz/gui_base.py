import tkinter as tk
from tkinter import ttk, messagebox

from ventana_iter import VentanaIteraciones
from graficas import graficas

from metodos import (
    bhaskara,
    biseccion,
    falsa_posicion,
    newton_raphson,
    secante,
    punto_fijo
)


class InterfazBase:

    def __init__(self):
        self.root = None

    def crear_ventana(self):

        self.root = tk.Tk()
        self.root.title("Métodos Numéricos")

        self.configuracion_general()
        self.root.mainloop()

    def configuracion_general(self):

        tk.Label(self.root, text="Por favor elija el Método Numérico", font=("Arial", 14)).pack(pady=10)

        self.metodo = ttk.Combobox(
            self.root,
            values=[
                "Bisección",
                "Falsa Posición",
                "Punto Fijo",
                "Newton-Raphson",
                "Secante",
                "Fórmula General"
            ],
            state="readonly"
        )
        self.metodo.pack()
        self.metodo.bind("<<ComboboxSelected>>", self.actualizar_interfaz)

        self.label_ecuacion = tk.Label(self.root, text="Ingrese la Ecuación")
        self.ecuacion = tk.Entry(self.root, width=40)

        self.label_iteracion = tk.Label(self.root, text="Número de Iteraciones")
        self.iteracion = tk.Entry(self.root)

        self.label_mostrariteraciones = tk.Label(self.root, text="Mostrar Iteraciones")
        self.mostrariteraciones = ttk.Combobox(self.root, values=["Si", "No"], state="readonly")

        self.label_tolerancia = tk.Label(self.root, text="Tolerancia")
        self.tolerancia = tk.Entry(self.root)

        self.label_grafica = tk.Label(self.root, text="Mostrar Gráfica")
        self.grafica = ttk.Combobox(self.root, values=["Si", "No"], state="readonly")

        self.label_procedimiento = tk.Label(self.root, text="¿Ver Procedimiento?")
        self.procedimiento = ttk.Combobox(self.root, values=["Si", "No"], state="readonly")

        self.btn_calcular = tk.Button(self.root, text="Calcular", command=self.calcular)

    def actualizar_interfaz(self, event):

        metodo = self.metodo.get()
        self.ocultar_todo()

        if metodo == "Fórmula General":

            self.label_procedimiento.pack()
            self.procedimiento.pack()

        else:

            self.label_ecuacion.pack()
            self.ecuacion.pack()

            self.label_iteracion.pack()
            self.iteracion.pack()

            self.label_mostrariteraciones.pack()
            self.mostrariteraciones.pack()

            self.label_tolerancia.pack()
            self.tolerancia.pack()

            self.label_grafica.pack()
            self.grafica.pack()

        self.btn_calcular.pack(pady=20)

    def ocultar_todo(self):

        widgets = [
            self.label_ecuacion, self.ecuacion,
            self.label_iteracion, self.iteracion,
            self.label_mostrariteraciones, self.mostrariteraciones,
            self.label_tolerancia, self.tolerancia,
            self.label_grafica, self.grafica,
            self.label_procedimiento, self.procedimiento,
            self.btn_calcular
        ]

        for w in widgets:
            w.pack_forget()

    def calcular(self):

        metodo = self.metodo.get()

        try:

            if metodo == "Fórmula General":

                a = float(self.ecuacion.get())
                b = float(self.iteracion.get())
                c = float(self.tolerancia.get())

                resultado = bhaskara(a, b, c)

            else:

                ecuacion = self.ecuacion.get()
                tol = float(self.tolerancia.get())
                it = int(self.iteracion.get())

                if metodo == "Bisección":
                    resultado = biseccion(ecuacion, tol, it)

                elif metodo == "Falsa Posición":
                    resultado = falsa_posicion(ecuacion, tol, it)

                elif metodo == "Newton-Raphson":
                    resultado = newton(ecuacion, tol, it)

                elif metodo == "Secante":
                    resultado = secante(ecuacion, tol, it)

                elif metodo == "Punto Fijo":
                    resultado = punto_fijo(ecuacion, tol, it)

            self.mostrar_resultado(resultado)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_resultado(self, resultado):

        texto = ""

        if "raices" in resultado:
            texto += "\nRaíces:\n"
            for i, r in enumerate(resultado["raices"], start=1):
                texto += f"X{i} = {r}\n"

        if "ea" in resultado:
            texto += f"\nEa Final = {resultado['ea']}"

        if "iteraciones" in resultado:
            texto += f"\nIteraciones = {resultado['iteraciones']}"

        messagebox.showinfo("Resultado", texto)

        if self.mostrariteraciones.get() == "Si" and "historial" in resultado:
            VentanaIteraciones(resultado["historial"])

        if self.grafica.get() == "Si":
            VentanaGrafica(resultado)

if __name__ == "__main__":
    interfaz = InterfazBase()
    interfaz.crear_ventana()