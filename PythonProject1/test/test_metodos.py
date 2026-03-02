import unittest
import math

# Importamos las clases de nuestros métodos
from metodos.biseccion import Biseccion
from metodos.falsa_posicion import FalsaPosicion
from metodos.punto_fijo import PuntoFijo
from metodos.newton_raphson import NewtonRaphson
from metodos.secante import Secante


class TestMetodosNumericos(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial antes de cada prueba.
        Usaremos funciones matemáticas sencillas con raíces conocidas para verificar los algoritmos.
        """
        # Ecuación de prueba: f(x) = x^2 - 4 (Tiene raíces exactas en x = 2 y x = -2)
        self.f = lambda x: x ** 2 - 4
        self.df = lambda x: 2 * x  # Derivada para Newton-Raphson

        # Función iterativa para Punto Fijo: x = sqrt(x + 2) para resolver x^2 - x - 2 = 0 (Raíz en x = 2)
        self.g = lambda x: math.sqrt(x + 2)

    def test_biseccion(self):
        metodo = Biseccion(self.f, tolerancia=1e-5, max_iter=50)
        # Buscamos la raíz en el intervalo [0, 3]
        resultado = metodo.calcular(0.0, 3.0)
        self.assertTrue(resultado['exito'], "El método de bisección no convergió.")
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=4, msg="Raíz incorrecta en Bisección.")

    def test_falsa_posicion(self):
        metodo = FalsaPosicion(self.f, tolerancia=1e-5, max_iter=50)
        resultado = metodo.calcular(0.0, 3.0)
        self.assertTrue(resultado['exito'], "El método de falsa posición no convergió.")
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=4, msg="Raíz incorrecta en Falsa Posición.")

    def test_punto_fijo(self):
        metodo = PuntoFijo(self.g, tolerancia=1e-5, max_iter=50)
        resultado = metodo.calcular(1.0)
        self.assertTrue(resultado['exito'], "El método de punto fijo no convergió.")
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=4, msg="Raíz incorrecta en Punto Fijo.")

    def test_newton_raphson(self):
        metodo = NewtonRaphson(self.f, self.df, tolerancia=1e-5, max_iter=50)
        resultado = metodo.calcular(3.0)
        self.assertTrue(resultado['exito'], "El método de Newton-Raphson no convergió.")
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=4, msg="Raíz incorrecta en Newton-Raphson.")

    def test_secante(self):
        metodo = Secante(self.f, tolerancia=1e-5, max_iter=50)
        # Requiere dos valores iniciales
        resultado = metodo.calcular(3.0, 2.5)
        self.assertTrue(resultado['exito'], "El método de la secante no convergió.")
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=4, msg="Raíz incorrecta en Secante.")


if __name__ == '__main__':
    unittest.main()