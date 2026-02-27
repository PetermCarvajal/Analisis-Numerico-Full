"""Método de Punto Fijo para resolución de ecuaciones no lineales.

Transforma la ecuación f(x) = 0 en la forma iterativa x = g(x).
El método converge si la magnitud de la derivada |g'(x)| < 1 en la región.

Fórmula: x_{n+1} = g(x_n)

Ejercicio 3 de la guía: Crecimiento de Base de Datos.
"""

from __future__ import annotations

import math
import time
from typing import Any, Callable, Dict, List, Tuple


class PuntoFijoError(Exception):
    """Excepción para errores en el método de Punto Fijo."""
    pass


def derivada_numerica(g: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Calcula la derivada numérica de g en x usando diferencias centrales.

    Args:
        g: Función iterativa g(x).
        x: Punto a evaluar.
        h: Tamaño del paso.

    Returns:
        Aproximación del valor de g'(x).
    """
    return (g(x + h) - g(x - h)) / (2.0 * h)


def verificar_condicion_convergencia(g: Callable[[float], float], x: float) -> Tuple[bool, float]:
    """Verifica si se cumple la condición suficiente de convergencia |g'(x)| < 1.

    Args:
        g: Función iterativa g(x).
        x: Punto de evaluación (usualmente el x0 inicial).

    Returns:
        Tupla con (cumple_condicion: bool, valor_derivada_absoluta: float).
    """
    gp_abs = abs(derivada_numerica(g, x))
    return gp_abs < 1.0, gp_abs


def punto_fijo(
        g: Callable[[float], float],
        x0: float,
        tol: float = 1e-8,
        max_iter: int = 100,
        limite_divergencia: float = 1e6
) -> Tuple[float, List[Dict[str, Any]], bool, str, float]:
    """Encuentra el punto fijo de g empezando en x0.

    Algoritmo:
        1. Calcular x_nuevo = g(x_actual)
        2. Evaluar error y divergencia.
        3. Repetir hasta que el error absoluto sea menor a 'tol'.

    Args:
        g: Función iterativa g(x).
        x0: Aproximación inicial.
        tol: Tolerancia para el criterio de parada.
        max_iter: Número máximo de iteraciones.
        limite_divergencia: Umbral para abortar si la función explota.

    Returns:
        Tupla con:
            - Raíz encontrada (float)
            - Historial de iteraciones (List[Dict])
            - Convergido (bool)
            - Mensaje de estado (str)
            - Tiempo de ejecución en segundos (float)

    Raises:
        PuntoFijoError: Si los parámetros son inválidos.
    """
    # ── Validaciones ───────────────────────────────────────────────────
    if not callable(g):
        raise PuntoFijoError("El argumento 'g' debe ser callable.")
    if not math.isfinite(x0):
        raise PuntoFijoError(f"Valor inicial inválido (infinito o NaN): {x0}")
    if tol <= 0:
        raise PuntoFijoError(f"La tolerancia debe ser positiva. Recibido: {tol}.")
    if max_iter < 1:
        raise PuntoFijoError(f"Máximo de iteraciones debe ser al menos 1. Recibido: {max_iter}.")

    t_inicio = time.perf_counter()

    historial: List[Dict[str, Any]] = []
    x_actual = x0
    convergido = False
    mensaje = f"No convergió en {max_iter} iteraciones."

    for n in range(1, max_iter + 1):
        try:
            x_next = float(g(x_actual))
        except Exception as e:
            raise PuntoFijoError(f"Error matemático al evaluar g(x): {e}")

        # Detección de divergencia
        if not math.isfinite(x_next) or abs(x_next) > limite_divergencia:
            mensaje = f"Divergencia detectada en la iteración {n}. El valor excedió el límite."
            break

        abs_err = abs(x_next - x_actual)
        rel_err = abs_err / abs(x_next) if x_next != 0.0 else float("inf")

        # Se guardan las llaves exactamente como las piden las pruebas del profesor
        historial.append({
            "iter": n,
            "x_n": x_actual,
            "g_xn": x_next,
            "error_abs": abs_err,
            "error_rel": rel_err
        })

        if abs_err < tol:
            convergido = True
            mensaje = "Convergencia exitosa."
            x_actual = x_next
            break

        x_actual = x_next

    tiempo_total = time.perf_counter() - t_inicio
    return x_actual, historial, convergido, mensaje, tiempo_total


# ====================================================================================
# ADAPTADOR PARA LA INTERFAZ GRÁFICA (WRAPPER)
# ====================================================================================
class PuntoFijo:
    """Clase envoltura para mantener compatibilidad 100% con nuestra Interfaz Gráfica."""

    def __init__(self, funcion_g: Callable[[float], float], tolerancia: float = 1e-8, max_iter: int = 100,
                 limite_divergencia: float = 1e6):
        self.funcion_g = funcion_g
        self.tolerancia = tolerancia
        self.max_iter = max_iter
        self.limite_divergencia = limite_divergencia

    def calcular(self, x0: float) -> Dict[str, Any]:
        """Ejecuta el método y empaqueta los resultados en el formato que espera nuestra GUI."""
        raiz, historial_prof, convergido, mensaje, elapsed = punto_fijo(
            self.funcion_g, x0, self.tolerancia, self.max_iter, self.limite_divergencia
        )

        # Mapeamos las llaves del profesor a las que usa nuestra tabla en Tkinter
        historial_gui = []
        for rec in historial_prof:
            historial_gui.append({
                'n': rec['iter'],
                'c': rec['x_n'],
                'f(c)': rec['g_xn'],
                'error_absoluto': rec['error_abs'],
                'error_relativo': rec['error_rel'] * 100  # La GUI lo espera como porcentaje
            })

        return {
            'exito': convergido,
            'raiz': raiz,
            'iteraciones_totales': len(historial_prof),
            'historial': historial_gui,
            'mensaje': mensaje,
            'tiempo': elapsed * 1000  # La GUI lo espera en milisegundos
        }