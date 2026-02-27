import math
import matplotlib.pyplot as plt
import  tkinter as tk

def bhaskara_visualmente(a,b,c):
    discriminante= b**2-4*a*c

    if discriminante < 0:
        ecuaciones = [
            r"$\Delta = b^2 - 4ac$",
            rf"$\Delta = {b}^2 - 4({a})({c})$",
            rf"$\Delta = {discriminante}$",
            r"$\text{No existen raíces reales}$"
        ]
    else:
        raiz = math.sqrt(discriminante)

        x1 = (-b + raiz) / (2 * a)
        x2 = (-b - raiz) / (2 * a)

        ecuaciones = [
            r"$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$",

            rf"$x_1 = {x1}$",
            rf"$x_2 = {x2}$"
        ]

    plt.figure(figsize=(6, 8))
    plt.axis("off")

    y = 0.9

    for eq in ecuaciones:
        plt.text(0.1, y, eq, fontsize=18)
        y -= 0.12

    plt.show()

    if mostrar_procedimiento:
        procedimiento=(
        "Fórmula General:\n"
        "X = (-({b}) ±  "
        )