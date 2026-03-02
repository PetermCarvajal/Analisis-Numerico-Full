from typing import Callable, Dict, List, Union

class NewtonRaphson:
    """
    Clase que implementa el método numérico de Newton-Raphson.
    """

    def __init__(self, funcion: Callable[[float], float], derivada: Callable[[float], float], tolerancia: float = 1e-10, max_iter: int = 100):
        """
        Inicializa el configurador del método de Newton-Raphson.

        Args:
            funcion: La función matemática a evaluar f(x).
            derivada: La primera derivada de la función f'(x).
            tolerancia: El criterio de parada para el error (10^-10 para este ejercicio).
            max_iter: Número máximo de iteraciones.
        """
        self.funcion = funcion
        self.derivada = derivada
        self.tolerancia = tolerancia
        self.max_iter = max_iter

    def calcular(self, x0: float) -> Dict[str, Union[float, int, List[Dict[str, float]], str]]:
        """
        Ejecuta la iteración de Newton-Raphson a partir del valor inicial x0.

        Args:
            x0: Aproximación inicial (ej: n0 = 3.0).

        Returns:
            Un diccionario con los resultados estandarizados para la interfaz gráfica.
        """
        iteraciones_data = []
        x_actual = x0

        for n in range(1, self.max_iter + 1):
            fx = self.funcion(x_actual)
            dfx = self.derivada(x_actual)

            # Validación exigida: evitar división por cero si la tangente es completamente horizontal
            if dfx == 0:
                if abs(fx) < 1e-15:
                    # Ya estamos en la raíz exacta, pero la derivada es 0 (multiplicidad > 1)
                    return {
                        'exito': True,
                        'raiz': x_actual,
                        'iteraciones_totales': n - 1 if n > 1 else 1,
                        'historial': iteraciones_data,
                        'mensaje': "Convergencia exitosa (raíz múltiple)."
                    }
                else:
                    return {
                        'exito': False,
                        'raiz': x_actual,
                        'iteraciones_totales': n,
                        'historial': iteraciones_data,
                        'mensaje': f"Falla del método: La derivada f'(x) se hizo cero en la iteración {n}."
                    }

            # Fórmula central de Newton-Raphson (calculamos X_siguiente ANTES de guardar el historial)
            x_siguiente = x_actual - (fx / dfx)

            # Cálculo de errores de esta iteración
            error_absoluto = abs(x_siguiente - x_actual)
            error_relativo = abs(x_siguiente - x_actual) / abs(x_siguiente) if x_siguiente != 0 else 0.0

            # Se evalúa la función en el nuevo X calculado para mostrar los datos reales de esta iteración
            fx_sig = self.funcion(x_siguiente)
            dfx_sig = self.derivada(x_siguiente)

            # Se guardan los datos de X_1 en n=1
            iteraciones_data.append({
                'n': n,
                'c': x_siguiente,
                'f(c)': fx_sig,
                'f_prima(c)': dfx_sig,
                'error_absoluto': error_absoluto,
                'error_relativo': error_relativo * 100
            })

            # Criterio de parada
            if error_absoluto < self.tolerancia or abs(fx_sig) < 1e-15:
                return {
                    'exito': True,
                    'raiz': x_siguiente,
                    'iteraciones_totales': n,
                    'historial': iteraciones_data,
                    'mensaje': "Convergencia exitosa."
                }

            x_actual = x_siguiente

        return {
            'exito': False,
            'raiz': x_actual,
            'iteraciones_totales': self.max_iter,
            'historial': iteraciones_data,
            'mensaje': "Máximo de iteraciones alcanzado sin convergir."
        }