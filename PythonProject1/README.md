# Resolución Numérica de Ecuaciones No Lineales - Ingeniería de Software

Este repositorio contiene la implementación de cinco métodos numéricos clásicos aplicados a la resolución de problemas específicos en el ámbito de la Ingeniería de Software, desarrollados en Python con una interfaz gráfica interactiva (Tkinter + Matplotlib).

## Métodos Implementados y Casos de Estudio
1. **Método de la Bisección:** Optimización de tiempo de búsqueda en una Hash Table (Caché).
2. **Método de Falsa Posición (Regula Falsi):** Cálculo de balanceo de carga en servidores distribuidos.
3. **Método de Punto Fijo:** Predicción de crecimiento de almacenamiento en Bases de Datos.
4. **Método de Newton-Raphson:** Análisis de overhead y concurrencia (Threads).
5. **Método de la Secante:** Predicción de escalabilidad y costos en infraestructura Cloud.

## Estructura del Proyecto
```text
proyecto_metodos_numericos/
├── metodos/              # Lógica algorítmica de cada método
├── interfaz/             # Componentes visuales y ventanas
├── funciones/            # Funciones adicionales y validador de entradas
├── tests/                # Pruebas unitarias para verificar la matemática
├── main.py               # Archivo de arranque principal
├── requirements.txt      # Dependencias externas
└── README.md             # Documentación del proyecto