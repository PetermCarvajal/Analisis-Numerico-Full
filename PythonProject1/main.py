import tkinter as tk

from interfaz.principal import AppMetodosNumericos


def main():
    root = tk.Tk()
    root.title("Métodos Numéricos - Ingeniería de Software")
    app = AppMetodosNumericos(root)
    root.mainloop()

if __name__ == "__main__":
    main()