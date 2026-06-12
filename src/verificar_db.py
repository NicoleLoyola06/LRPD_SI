import sqlite3
import pandas as pd

conn = sqlite3.connect("data/inventario.db")

# Ver qué tablas existen
tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
print("Tablas en la base de datos:")
print(tablas)

# Ver los primeros registros
df = pd.read_sql("SELECT * FROM inventario LIMIT 5", conn)
print("\nPrimeros 5 registros:")
print(df)

# Contar registros totales
total = pd.read_sql("SELECT COUNT(*) as total FROM inventario", conn)
print("\nTotal de registros:")
print(total)

conn.close()