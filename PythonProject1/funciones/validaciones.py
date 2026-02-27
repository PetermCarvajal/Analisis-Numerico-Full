import numpy as np


class ValidadorEntradas:
    @staticmethod
    def validar_datos(funcion_str, tol_str, iter_str, x0_str, x1_str=None, derivada_str=None):
        """Limpia y valida las entradas de la GUI."""
        datos = {}

        if not funcion_str.strip():
            raise ValueError("La función no puede estar vacía.")
        datos['funcion_str'] = funcion_str

        try:
            datos['tol'] = float(tol_str)
            if datos['tol'] <= 0:
                raise ValueError("La tolerancia debe ser mayor a 0.")
        except ValueError:
            raise ValueError("Tolerancia inválida. Usa formato numérico (ej. 1e-7).")

        try:
            datos['max_iter'] = int(iter_str)
            if datos['max_iter'] <= 0:
                raise ValueError("Las iteraciones deben ser un entero positivo.")
        except ValueError:
            raise ValueError("Las iteraciones deben ser un número entero.")

        try:
            datos['x0'] = float(x0_str)
            if x1_str:
                datos['x1'] = float(x1_str)
        except ValueError:
            raise ValueError("Los valores iniciales deben ser numéricos.")

        if derivada_str is not None:
            if not derivada_str.strip():
                raise ValueError("La derivada no puede estar vacía para Newton-Raphson.")
            datos['derivada_str'] = derivada_str

        return datos

    @staticmethod
    def crear_evaluador(expresion: str):
        """Convierte un string matemático en una función evaluable."""

        def f(x_val):
            # Se inyecta __builtins__ para que numpy no colapse al calcular logaritmos o exponenciales
            entorno = {"x": x_val, "np": np, "e": np.e, "pi": np.pi, "__builtins__": __builtins__}
            try:
                expr_segura = expresion.replace("^", "**")
                resultado = eval(expr_segura, entorno, entorno)

                if np.isnan(resultado) or np.isinf(resultado):
                    raise ValueError(f"La función evaluó a un valor no válido en x={x_val}")
                return float(resultado)
            except ZeroDivisionError:
                raise ZeroDivisionError(f"División por cero al evaluar f({x_val})")
            except Exception as e:
                raise ValueError(f"Error matemático al evaluar la función: {e}")

        return f