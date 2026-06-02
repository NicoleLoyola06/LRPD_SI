import pandas as pd
import os

print("\n=== BEST FIRST SEARCH ===")

os.makedirs(
    "outputs/reportes",
    exist_ok=True
)

df = pd.read_csv(
    "data/dataset_modelado.csv"
)

rotacion_map = {

    "Alta": 1.0,
    "Media": 0.5,
    "Baja": 0.0

}

df["rotacion_num"] = (
    df["nivel_rotacion"]
    .map(rotacion_map)
)

max_demanda = (
    df["cantidad_vendida"]
    .max()
)

df["demanda_norm"] = (
    df["cantidad_vendida"]
    /
    max_demanda
)

# h(n)

df["prioridad"] = (

    0.5 * df["rotacion_num"]

    +

    0.3 * df["demanda_norm"]

    +

    0.2 * df["urgencia_stock"]

)

priorizados = (

    df.sort_values(
        by="prioridad",
        ascending=False
    )

)

priorizados.to_csv(

    "outputs/reportes/productos_priorizados.csv",

    index=False

)

print(
    "productos_priorizados.csv generado"
)