from ventana_iter import VentanaIteraciones

METODOS = {

    "Bhaskara": [
        {"label": "a", "tipo": float},
        {"label": "b", "tipo": float},
        {"label": "c", "tipo": float},
    ],

    "Bisección": [
        {"label": "a", "tipo": float},
        {"label": "b", "tipo": float},
        {"label": "Tolerancia", "tipo": float, "default": 0.0001},
        {"label": "Número de Iteraciones", "tipo": int, "default": 100},
    ],

    "Falsa Posición": [
        {"label": "a", "tipo": float},
        {"label": "b", "tipo": float},
        {"label": "Tolerancia", "tipo": float, "default": 0.0001},
        {"label": "Número de Iteraciones", "tipo": int, "default": 100},
    ],

    "Newton": [
        {"label": "x0", "tipo": float},
        {"label": "Tolerancia", "tipo": float, "default": 0.0001},
        {"label": "Número de Iteraciones", "tipo": int, "default": 100},
    ],

    "Secante": [
        {"label": "x0", "tipo": float},
        {"label": "x1", "tipo": float},
        {"label": "Tolerancia", "tipo": float, "default": 0.0001},
        {"label": "Número de Iteraciones", "tipo": int, "default": 100},
    ],

    "Punto Fijo": [
        {"label": "x0", "tipo": float},
        {"label": "Tolerancia", "tipo": float, "default": 0.0001},
        {"label": "Número de Iteraciones", "tipo": int, "default": 100},
    ]
}

ventana_iters = VentanaIteraciones(root)

for n in range(1, max_iter + 1):

    xr = ...
    fxr = f(xr)
    ea = ...

    ventana_iters.insertar_iteracion(
        n=n,
        a=a,
        b=b,
        xr=xr,
        fxr=fxr,
        ea=ea
    )