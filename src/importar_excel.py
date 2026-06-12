import pandas as pd
import sqlite3

conn = sqlite3.connect("data/inventario.db")

df = pd.read_excel("data/inventario_editable.xlsx", sheet_name="inventario")

# Validación básica antes de sobrescribir
columnas_esperadas = [
    "codigo_producto", "nombre_producto", "categoria",
    "stock_actual", "stock_minimo", "cantidad_vendida",
    "fecha_venta", "dias_para_vencer"
]

faltantes = [c for c in columnas_esperadas if c not in df.columns]
if faltantes:
    raise ValueError(f"Faltan columnas en el Excel: {faltantes}")

# Eliminar filas vacías que el usuario pudo dejar
df = df.dropna(subset=["codigo_producto"])

df.to_sql("inventario", conn, if_exists="replace", index=False)
conn.close()

print(f"Base de datos actualizada con {len(df)} registros desde Excel")