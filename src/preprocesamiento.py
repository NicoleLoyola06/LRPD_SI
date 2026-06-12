import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler

print("=== PREPROCESAMIENTO ===")

conn = sqlite3.connect("data/inventario.db")

df = pd.read_sql("SELECT * FROM inventario", conn)

print("Registros originales:", len(df))

# Eliminar duplicados
df = df.drop_duplicates()

# Eliminar nulos
df = df.dropna()

# Eliminar valores negativos
df = df[df["stock_actual"] >= 0]
df = df[df["cantidad_vendida"] >= 0]

# Normalización
scaler = MinMaxScaler()

df["stock_norm"] = scaler.fit_transform(
    df[["stock_actual"]]
)

df["ventas_norm"] = scaler.fit_transform(
    df[["cantidad_vendida"]]
)

# Clasificación de rotación

p33 = df["cantidad_vendida"].quantile(0.33)
p66 = df["cantidad_vendida"].quantile(0.66)

def clasificar_rotacion(x):

    if x >= p66:
        return "Alta"

    elif x >= p33:
        return "Media"

    else:
        return "Baja"

df["nivel_rotacion"] = (
    df["cantidad_vendida"]
    .apply(clasificar_rotacion)
)

df.to_sql(
    "inventario_preprocesado",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Tabla generada en inventario.db:")
print("inventario_preprocesado")