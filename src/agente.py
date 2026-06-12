import pandas as pd
import sqlite3
import os

print("\n=== AGENTE INTELIGENTE ===")

os.makedirs("outputs/reportes", exist_ok=True)

conn = sqlite3.connect("data/inventario.db")
df = pd.read_sql("SELECT * FROM dataset_modelado", conn)
conn.close()

# ====================================================
# MÓDULO 1: RECOMENDACIONES POR PRODUCTO (reglas IF-THEN)
# ====================================================

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
        "codigo_producto": fila["codigo_producto"],
        "nombre_producto": fila["nombre_producto"],
        "categoria":       fila["categoria"],
        "nivel_rotacion":  fila["nivel_rotacion"],
        "accion":          accion
    })

resultado = pd.DataFrame(recomendaciones)

resultado.to_csv(
    "outputs/reportes/recomendaciones.csv",
    index=False
)

print("recomendaciones.csv generado")

# ====================================================
# MÓDULO 2: ANÁLISIS DE TENDENCIAS POR CATEGORÍA
# ¿Qué importar más? ¿Qué reducir?
# ====================================================

print("\n=== ANÁLISIS DE IMPORTACIÓN POR CATEGORÍA ===")

resumen_categoria = df.groupby("categoria").agg(
    total_productos     = ("codigo_producto",  "count"),
    ventas_promedio     = ("cantidad_vendida",  "mean"),
    rotacion_promedio   = ("indice_rotacion",   "mean"),
    pct_alta_rotacion   = ("nivel_rotacion",
                           lambda x: (x == "Alta").sum() / len(x) * 100),
    pct_baja_rotacion   = ("nivel_rotacion",
                           lambda x: (x == "Baja").sum() / len(x) * 100),
    stock_promedio      = ("stock_actual",      "mean"),
).reset_index()

def decision_importacion(fila):
    if fila["pct_alta_rotacion"] >= 40:
        return "Aumentar importación"
    elif fila["pct_baja_rotacion"] >= 50:
        return "Reducir importación"
    elif fila["ventas_promedio"] >= df["cantidad_vendida"].quantile(0.66):
        return "Mantener y evaluar expansión"
    else:
        return "Mantener importación actual"

resumen_categoria["decision_importacion"] = resumen_categoria.apply(
    decision_importacion, axis=1
)

resumen_categoria = resumen_categoria.sort_values(
    "rotacion_promedio", ascending=False
)

resumen_categoria.to_csv(
    "outputs/reportes/tendencias_importacion.csv",
    index=False
)

print("tendencias_importacion.csv generado")

# ====================================================
# MÓDULO 3: TOP PRODUCTOS A IMPORTAR MÁS
# Alta rotación + stock bajo de forma recurrente
# ====================================================

productos_importar = df[
    (df["nivel_rotacion"] == "Alta") &
    (df["urgencia_stock"] >= 0.5)        # stock cerca del mínimo
].groupby(["categoria", "nombre_producto"]).agg(
    veces_stock_critico = ("codigo_producto", "count"),
    ventas_promedio     = ("cantidad_vendida", "mean"),
    stock_promedio      = ("stock_actual",     "mean"),
).reset_index().sort_values(
    ["veces_stock_critico", "ventas_promedio"], ascending=False
)

# ----------------------------------------------------------
# Cálculo de cantidad sugerida de importación
#
# demanda_proyectada: estima la demanda esperada para el
# siguiente periodo a partir de las ventas promedio, aplicando
# un margen de seguridad del 20% (MARGEN_SEGURIDAD = 1.2) para
# evitar quiebres de stock por variabilidad de la demanda.
#
# cantidad_sugerida_importar: diferencia entre la demanda
# proyectada y el stock promedio actual. Si el resultado es
# negativo (ya hay suficiente stock), se ajusta a 0 con clip().
# ----------------------------------------------------------

MARGEN_SEGURIDAD = 1.2

productos_importar["demanda_proyectada"] = (
    productos_importar["ventas_promedio"] * MARGEN_SEGURIDAD
)

productos_importar["cantidad_sugerida_importar"] = (
    productos_importar["demanda_proyectada"]
    - productos_importar["stock_promedio"]
).clip(lower=0).round().astype(int)

productos_importar["recomendacion"] = productos_importar[
    "cantidad_sugerida_importar"
].apply(
    lambda cantidad:
        f"Importar aprox. {cantidad} unidades"
        if cantidad > 0
        else "Mantener nivel actual"
)

productos_importar.to_csv(
    "outputs/reportes/productos_a_importar.csv",
    index=False
)

print("productos_a_importar.csv generado")

# ====================================================
# MÓDULO 4: PRODUCTOS A DESCONTINUAR O REDUCIR
# Baja rotación + sobrestock persistente
# ====================================================

productos_reducir = df[
    (df["nivel_rotacion"] == "Baja") &
    (df["stock_actual"] > df["stock_minimo"] * 2)
].groupby(["categoria", "nombre_producto"]).agg(
    veces_sobrestock    = ("codigo_producto", "count"),
    ventas_promedio     = ("cantidad_vendida", "mean"),
    stock_promedio      = ("stock_actual",     "mean"),
).reset_index().sort_values(
    "veces_sobrestock", ascending=False
)

productos_reducir["recomendacion"] = "Reducir o no reimportar"

productos_reducir.to_csv(
    "outputs/reportes/productos_a_reducir.csv",
    index=False
)

print("productos_a_reducir.csv generado")

# ====================================================
# RESUMEN EN CONSOLA
# ====================================================

print("\n--- DECISIONES DE IMPORTACIÓN POR CATEGORÍA ---")
print(resumen_categoria[[
    "categoria", "pct_alta_rotacion", "pct_baja_rotacion", "decision_importacion"
]].to_string(index=False))

print(f"\nProductos recomendados para aumentar importación: {len(productos_importar)}")
print(f"Productos recomendados para reducir/no reimportar: {len(productos_reducir)}")