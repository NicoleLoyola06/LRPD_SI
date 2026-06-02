import pandas as pd

print("=== PROCESAMIENTO ===")

df = pd.read_csv(
    "data/inventario_preprocesado.csv"
)

# Variables derivadas

df["indice_rotacion"] = (
    df["cantidad_vendida"]
    /
    df["stock_actual"]
)

df["urgencia_stock"] = (
    df["stock_minimo"]
    /
    df["stock_actual"]
)

df["riesgo_vencimiento"] = (
    df["dias_para_vencer"] < 30
).astype(int)

df.to_csv(
    "data/dataset_modelado.csv",
    index=False
)

print("Archivo generado:")
print("dataset_modelado.csv")