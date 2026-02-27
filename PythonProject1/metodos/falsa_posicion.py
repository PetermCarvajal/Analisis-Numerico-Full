from typing import Callable, Dict, List, Union


class FalsaPosicion:
    """
    Clase que implementa el método numérico de Falsa Posición (Regula Falsi).
    """

    def __init__(self, funcion: Callable[[float], float], tolerancia: float = 1e-7, max_iter: int = 100):
        """
        Inicializa el configurador del método.

        Args:
            funcion: La función matemática a evaluar f(x).
            tolerancia: El criterio de parada para el error relativo/absoluto.
            max_iter: Número máximo de iteraciones permitidas.
        """
        self.funcion = funcion
        self.tolerancia = tolerancia
        self.max_iter = max_iter

    def calcular(self, a: float, b: float) -> Dict[str, Union[float, int, List[Dict[str, float]], str]]:
        """
        Ejecuta el método de falsa posición para encontrar la raíz en el intervalo [a, b].

        Args:
            a: Límite inferior del intervalo.
            b: Límite superior del intervalo.

        Returns:
            Un diccionario con el estado de la convergencia, la raíz, iteraciones y errores.
        """
        # Validación del intervalo: f(a) y f(b) deben tener signos opuestos [cite: 225]
        fa = self.funcion(a)
        fb = self.funcion(b)

        if fa * fb > 0:
            raise ValueError("El intervalo no contiene una raíz (f(a) y f(b) tienen el mismo signo).")

        iteraciones_data = []
        c_anterior = a

        for n in range(1, self.max_iter + 1):
            fa = self.funcion(a)
            fb = self.funcion(b)

            # Manejo de caso de división por cero [cite: 93, 222]
            if fb - fa == 0:
                raise ZeroDivisionError("División por cero detectada: f(b) - f(a) es 0.")

            # Fórmula del método de falsa posición [cite: 92]
            c = b - fb * (b - a) / (fb - fa)
            fc = self.funcion(c)

            # Cálculo de errores
            error_absoluto = abs(c - c_anterior)
            error_relativo = abs(c - c_anterior) / abs(c) if c != 0 else 0.0

            iteraciones_data.append({
                'n': n,
                'a': a,
                'b': b,
                'c': c,
                'f(c)': fc,
                'error_absoluto': error_absoluto,
                'error_relativo': error_relativo * 100  # Porcentaje
            })

            # Criterio de parada
            if error_absoluto < self.tolerancia or abs(fc) < 1e-15:
                return {
                    'exito': True,
                    'raiz': c,
                    'iteraciones_totales': n,
                    'historial': iteraciones_data,
                    'mensaje': "Convergencia exitosa."
                }

            # Actualización del intervalo
            if fa * fc < 0:
                b = c
            else:
                a = c

            c_anterior = c

        # No convergencia tras iteraciones máximas [cite: 223]
        return {
            'exito': False,
            'raiz': c,
            'iteraciones_totales': self.max_iter,
            'historial': iteraciones_data,
            'mensaje': "Máximo de iteraciones alcanzado sin convergir."
        }