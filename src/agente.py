# Dentro del bloque MÓDULO 3, después de agrupar:

# Asumimos que cantidad_vendida representa ventas en un periodo de referencia (ej. 30 días)
PERIODO_DIAS = 30
MARGEN_SEGURIDAD = 1.2  # 20% extra de colchón

productos_importar["demanda_proyectada"] = (
    productos_importar["ventas_promedio"] * MARGEN_SEGURIDAD
)

productos_importar["cantidad_sugerida_importar"] = (
    productos_importar["demanda_proyectada"] - productos_importar["stock_promedio"]
).clip(lower=0).round().astype(int)

productos_importar["recomendacion"] = productos_importar.apply(
    lambda r: f"Importar aprox. {r['cantidad_sugerida_importar']} unidades"
    if r["cantidad_sugerida_importar"] > 0
    else "Mantener nivel actual",
    axis=1
)