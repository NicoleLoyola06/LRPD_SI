import pandas as pd
from sklearn.preprocessing import MinMaxScaler

print("=== PREPROCESAMIENTO ===")

df = pd.read_csv("data/inventario_oriental.csv")

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

df.to_csv(
    "data/inventario_preprocesado.csv",
    index=False
)

print("Archivo generado:")
print("inventario_preprocesado.csv")