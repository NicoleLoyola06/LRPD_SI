import pandas as pd
import os

print("\n=== AGENTE INTELIGENTE ===")

os.makedirs("outputs/reportes", exist_ok=True)

df = pd.read_csv(
    "data/dataset_modelado.csv"
)

recomendaciones = []

for _, fila in df.iterrows():

    accion = "Monitorear"

    # Regla 1
    if (
        fila["nivel_rotacion"] == "Alta"
        and fila["stock_actual"] < fila["stock_minimo"]
    ):

        accion = "Reabastecimiento urgente"

    # Regla 2
    elif (
        fila["nivel_rotacion"] == "Baja"
        and fila["stock_actual"] >
        fila["stock_minimo"] * 3
    ):

        accion = "Alerta de sobrestock"

    # Regla 3
    elif fila["dias_para_vencer"] < 15:

        accion = "Promocionar producto"

    recomendaciones.append({

        "codigo_producto":
        fila["codigo_producto"],

        "nombre_producto":
        fila["nombre_producto"],

        "accion":
        accion

    })

resultado = pd.DataFrame(
    recomendaciones
)

resultado.to_csv(
    "outputs/reportes/recomendaciones.csv",
    index=False
)

print("recomendaciones.csv generado")