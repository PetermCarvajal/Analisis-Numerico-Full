from typing import Callable, Dict, List, Union
import time

class Secante:
    def __init__(self, funcion: Callable[[float], float], tolerancia: float = 1e-9, max_iter: int = 100):
        self.funcion = funcion
        self.tolerancia = tolerancia
        self.max_iter = max_iter
        self.evaluaciones_funcion = 0

    def calcular(self, x0: float, x1: float) -> Dict[str, Union[float, int, List[Dict[str, float]], str]]:
        self.evaluaciones_funcion = 0
        iteraciones_data = []
        inicio_tiempo = time.perf_counter()

        fx0 = self.funcion(x0)
        fx1 = self.funcion(x1)
        self.evaluaciones_funcion += 2

        for n in range(1, self.max_iter + 1):
            if fx1 - fx0 == 0:
                return {
                    'exito': False, 'raiz': x1, 'iteraciones_totales': n,
                    'evaluaciones': self.evaluaciones_funcion, 'historial': iteraciones_data,
                    'mensaje': f"Falla del método: División por cero en iteración {n}."
                }

            # Fórmula del método de la secante
            x_siguiente = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            fx_siguiente = self.funcion(x_siguiente)
            self.evaluaciones_funcion += 1

            error_absoluto = abs(x_siguiente - x1)
            error_relativo = abs(x_siguiente - x1) / abs(x_siguiente) if x_siguiente != 0 else 0.0

            iteraciones_data.append({
                'n': n, 'x_n-1': x0, 'c': x1, 'f(x_n-1)': fx0, 'f(c)': fx1,
                'x_n+1': x_siguiente, 'error_absoluto': error_absoluto, 'error_relativo': error_relativo * 100
            })

            if error_absoluto < self.tolerancia:
                return {
                    'exito': True, 'raiz': x_siguiente, 'iteraciones_totales': n,
                    'evaluaciones': self.evaluaciones_funcion, 'historial': iteraciones_data,
                    'mensaje': "Convergencia exitosa."
                }

            x0, fx0 = x1, fx1
            x1, fx1 = x_siguiente, fx_siguiente

        return {
            'exito': False, 'raiz': x1, 'iteraciones_totales': self.max_iter,
            'evaluaciones': self.evaluaciones_funcion, 'historial': iteraciones_data,
            'mensaje': "Máximo de iteraciones alcanzado sin convergir."
        }