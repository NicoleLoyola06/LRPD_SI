import pandas as pd
import numpy as np
import os

np.random.seed(42)

productos_catalogo = {

    "Mascotas": [
        "Arena para gato",
        "Correa retractil",
        "Plato para mascotas",
        "Juguete para perro",
        "Shampoo canino"
    ],

    "Hogar": [
        "Organizador plastico",
        "Caja multiuso",
        "Escoba plegable",
        "Repisa modular"
    ],

    "Cocina": [
        "Palillos chinos",
        "Vaporizador de bambu",
        "Sarten antiadherente",
        "Taza termica"
    ],

    "Comida Asiatica": [
        "Ramen coreano",
        "Fideos udon",
        "Salsa de soya",
        "Mochi",
        "Te verde japones"
    ],

    "Decoracion": [
        "Incienso japones",
        "Farol decorativo",
        "Figura Feng Shui"
    ],

    "Electronica": [
        "Mini ventilador USB",
        "Luz LED USB",
        "Cable Tipo C",
        "Audifonos Bluetooth"
    ],

    "Belleza": [
        "Mascarilla coreana",
        "Crema hidratante",
        "Cepillo facial"
    ],

    "Papeleria": [
        "Cuaderno kawaii",
        "Lapicero gel",
        "Stickers decorativos"
    ],

    "Ropa": [
        "Polo basico",
        "Medias termicas",
        "Pijama"
    ]
}

registros = []

for i in range(500):

    categoria = np.random.choice(
        list(productos_catalogo.keys())
    )

    producto = np.random.choice(
        productos_catalogo[categoria]
    )

    registros.append({

        "codigo_producto": f"P{i+1:04}",

        "nombre_producto": producto,

        "categoria": categoria,

        "stock_actual": np.random.randint(10,300),

        "stock_minimo": np.random.randint(5,80),

        "cantidad_vendida": np.random.randint(1,150),

        "fecha_venta":
            pd.Timestamp("2025-01-01")
            + pd.Timedelta(days=np.random.randint(0,365)),

        "dias_para_vencer":
            np.random.randint(1,365)

    })

df = pd.DataFrame(registros)

os.makedirs("data", exist_ok=True)

df.to_csv(
    "data/inventario_oriental.csv",
    index=False
)

print("Dataset generado correctamente")
print(df.head())