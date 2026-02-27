"""Método de Bisección para resolución de ecuaciones no lineales.

Basado en el Teorema del Valor Intermedio: si f(a)*f(b) < 0, existe
al menos una raíz en el intervalo [a, b].

Ejercicio 1 de la guía: Optimización de Hash Table.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class IterationRecord:
    """Registro de una iteración del método de bisección."""
    n: int
    a: float
    b: float
    c: float
    fc: float
    abs_error: float
    rel_error: float


class BisectionError(Exception):
    """Excepción para errores en el proceso de bisección."""
    pass


def biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> Dict[str, Any]:
    # ── Validaciones de entrada ────────────────────────────────────────
    if not callable(f):
        raise BisectionError("El argumento 'f' debe ser una función callable.")
    if not (math.isfinite(a) and math.isfinite(b)):
        raise BisectionError("Los extremos 'a' y 'b' deben ser números finitos.")
    if a >= b:
        raise BisectionError(f"Se requiere a < b. Recibido: a={a}, b={b}.")
    if tol <= 0:
        raise BisectionError(f"La tolerancia debe ser positiva. Recibido: {tol}.")
    if max_iter < 1:
        raise BisectionError(f"El número máximo de iteraciones debe ser al menos 1. Recibido: {max_iter}.")

    t_inicio = time.perf_counter()
    fa = float(f(a))
    fb = float(f(b))

    # ── Casos especiales: raíz exacta en los extremos ─────────────────
    if abs(fa) < 1e-15:
        return _build_result(a, [], True, 0, time.perf_counter() - t_inicio, "f(a) = 0. Raíz exacta en el extremo izquierdo.")
    if abs(fb) < 1e-15:
        return _build_result(b, [], True, 0, time.perf_counter() - t_inicio, "f(b) = 0. Raíz exacta en el extremo derecho.")

    # ── Validación de cambio de signo ──────────────────────────────────
    if fa * fb > 0:
        raise BisectionError(f"No hay cambio de signo en [{a}, {b}]: f(a)={fa:.6g}, f(b)={fb:.6g}.")

    iteraciones: List[IterationRecord] = []
    c_prev: Optional[float] = None
    c: float = a
    converged = False
    message = f"No convergió en {max_iter} iteraciones."

    for n in range(1, max_iter + 1):
        c = a + (b - a) / 2.0
        fc = float(f(c))

        if c_prev is None:
            abs_err = float("inf")
            rel_err = float("inf")
        else:
            abs_err = abs(c - c_prev)
            rel_err = abs_err / abs(c) if c != 0.0 else float("inf")

        iteraciones.append(IterationRecord(n=n, a=a, b=b, c=c, fc=fc, abs_error=abs_err, rel_error=rel_err))

        # ── Criterios de parada ────────────────────────────────────────
        if abs(fc) < 1e-15:
            converged = True
            message = "Convergencia: f(c) = 0 (raíz exacta)."
            break
        if c_prev is not None and abs_err < tol:
            converged = True
            message = "Convergencia por error absoluto < tolerancia."
            break
        if (b - a) / 2.0 < tol:
            converged = True
            message = "Convergencia por longitud de intervalo < tolerancia."
            break

        # ── Selección del subintervalo ─────────────────────────────────
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        c_prev = c

    tiempo_total = time.perf_counter() - t_inicio
    return _build_result(c, iteraciones, converged, len(iteraciones), tiempo_total, message)


def _build_result(root: float, iterations: List[IterationRecord], converged: bool, n_iter: int, elapsed: float, message: str) -> Dict[str, Any]:
    return {"root": root, "iterations": iterations, "converged": converged, "n_iter": n_iter, "time": elapsed, "message": message}


# ====================================================================================
# ADAPTADOR PARA LA INTERFAZ GRÁFICA (WRAPPER)
# ====================================================================================
class Biseccion:
    """Clase envoltura para mantener compatibilidad 100% con nuestra Interfaz Gráfica."""
    def __init__(self, funcion: Callable[[float], float], tolerancia: float = 1e-6, max_iter: int = 100):
        self.funcion = funcion
        self.tolerancia = tolerancia
        self.max_iter = max_iter

    def calcular(self, a: float, b: float) -> Dict[str, Any]:
        resultado_prof = biseccion(self.funcion, a, b, self.tolerancia, self.max_iter)

        historial_gui = []
        for rec in resultado_prof['iterations']:
            rel_err_porcentaje = rec.rel_error * 100 if rec.rel_error != float('inf') else 0.0
            historial_gui.append({
                'n': rec.n, 'a': rec.a, 'b': rec.b, 'c': rec.c,
                'f(c)': rec.fc, 'error_absoluto': rec.abs_error, 'error_relativo': rel_err_porcentaje
            })

        return {
            'exito': resultado_prof['converged'], 'raiz': resultado_prof['root'],
            'iteraciones_totales': resultado_prof['n_iter'], 'historial': historial_gui,
            'mensaje': resultado_prof['message'], 'tiempo': resultado_prof['time'] * 1000
        }