import pandas as pd
import sqlite3
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/inventario.db")

df = pd.read_csv("data/inventario_oriental.csv")

df.to_sql("inventario", conn, if_exists="replace", index=False)

conn.close()

print(f"Base de datos creada: data/inventario.db")
print(f"Registros cargados en tabla 'inventario': {len(df)}")