import pandas as pd
import tkinter as tk
from tkinter import ttk
class Iteracion:

    def __init__(self, n, x=None, fx=None, error=None, a=None, b=None):
        self.n = n              # Número de iteración
        self.x = x              # Aproximación actual
        self.fx = fx            # f(x)
        self.error = error      # Error relativo / absoluto
        self.a = a              # Extremo izquierdo (si aplica)
        self.b = b              # Extremo derecho (si aplica)

    def to_dict(self):
        return {
            "Iteración": self.n,
            "x": self.x,
            "f(x)": self.fx,
            "Error": self.error,
            "a": self.a,
            "b": self.b
        }

class RegistroIteraciones:
    def __init__(self):
        self.iteraciones = []

    def agregar(self, iteracion):
        self.iteraciones.append(iteracion)

    def obtener_tabla(self):
        return [it.to_dict() for it in self.iteraciones]

    def ultima(self):
        return self.iteraciones[-1] if self.iteraciones else None

    def limpiar(self):
        self.iteraciones = []

    def externo(self):
        tabla = registro.obtener_tabla()

        for fila in tabla:
            print(fila)

        df = pd.DataFrame(registro.obtener_tabla())
        df.to_csv("iteraciones.csv", index=False)
