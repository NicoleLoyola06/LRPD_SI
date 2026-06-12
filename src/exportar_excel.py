import pandas as pd
import sqlite3

conn = sqlite3.connect("data/inventario.db")
df = pd.read_sql("SELECT * FROM inventario", conn)
conn.close()

df.to_excel("data/inventario_editable.xlsx", index=False, sheet_name="inventario")

print("Archivo generado: data/inventario_editable.xlsx")
print(f"Filas exportadas: {len(df)}")