import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class VentanaParametros:

    def __init__(self, parent, metodo, config_parametros):

        self.valores = {}

        self.window = tk.Toplevel(parent)
        self.window.title(f"Parámetros - {metodo}")
        self.window.geometry("400x400")
        self.window.resizable(False, False)

        ttk.Label(
            self.window,
            text=f"Configuración - {metodo}",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        self.entries = {}

        for param in config_parametros:

            frame = ttk.Frame(self.window)
            frame.pack(pady=5, padx=15, fill="x")

            ttk.Label(frame, text=param["label"], width=15).pack(side="left")

            entry = ttk.Entry(frame)
            entry.pack(side="right", fill="x", expand=True)

            if "default" in param:
                entry.insert(0, str(param["default"]))

            self.entries[param["label"]] = (entry, param)

        ttk.Button(
            self.window,
            text="Aceptar",
            command=self.obtener_valores
        ).pack(pady=20)

        self.window.grab_set()
        parent.wait_window(self.window)

    def obtener_valores(self):

        try:
            for label, (entry, param) in self.entries.items():

                valor = entry.get()

                if param["tipo"] == float:
                    valor = float(valor)

                elif param["tipo"] == int:
                    valor = int(valor)

                self.valores[label] = valor

            self.window.destroy()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Verifique los parámetros numéricos"
            )

    def get_valores(self):
        return self.valores