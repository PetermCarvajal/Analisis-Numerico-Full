import tkinter as tk
from tkinter import ttk

class VentanaIteraciones:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Iteraciones del Método")
        self.window.geometry("750x400")

        columnas = ("iter", "a", "b", "xr", "fxr", "ea")

        self.tree = ttk.Treeview(
            self.window,
            columns=columnas,
            show="headings"
        )

        # Encabezados
        self.tree.heading("iter", text="Iter")
        self.tree.heading("a", text="a")
        self.tree.heading("b", text="b")
        self.tree.heading("xr", text="xr")
        self.tree.heading("fxr", text="|f(xr)|")
        self.tree.heading("ea", text="%Ea")

        self.tree.column("iter", width=60, anchor="center")
        self.tree.column("a", width=120, anchor="center")
        self.tree.column("b", width=120, anchor="center")
        self.tree.column("xr", width=140, anchor="center")
        self.tree.column("fxr", width=140, anchor="center")
        self.tree.column("ea", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def insertar_iteracion(self, n, a, b, xr, fxr, ea):

        self.tree.insert(
            "",
            "end",
            values=(
                n,
                f"{a:.6f}",
                f"{b:.6f}",
                f"{xr:.6f}",
                f"{abs(fxr):.6e}",
                f"{ea:.6f}" if ea is not None else "-"
            )
        )

    def limpiar(self):
        for fila in self.tree.get_children():
            self.tree.delete(fila)