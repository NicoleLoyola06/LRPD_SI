import pandas as pd
import sqlite3

print("=== PROCESAMIENTO ===")

conn = sqlite3.connect("data/inventario.db")

df = pd.read_sql("SELECT * FROM inventario_preprocesado", conn)

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

df.to_sql(
    "dataset_modelado",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Tabla generada en inventario.db:")
print("dataset_modelado")