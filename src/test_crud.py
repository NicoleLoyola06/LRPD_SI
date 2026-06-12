from crud import agregar_producto, actualizar_stock, registrar_venta, consultar_producto

print("=== ANTES DE LOS CAMBIOS ===")
print(consultar_producto("P0001"))

# Agregar producto nuevo
agregar_producto({
    "codigo_producto": "P0501",
    "nombre_producto": "Snack importado nuevo",
    "categoria": "Comida Asiatica",
    "stock_actual": 100,
    "stock_minimo": 20,
    "cantidad_vendida": 0,
    "fecha_venta": "2026-06-11",
    "dias_para_vencer": 180
})

# Actualizar stock de un producto existente
actualizar_stock("P0001", 50)

# Registrar una venta
registrar_venta("P0001", 5)

print("\n=== DESPUÉS DE LOS CAMBIOS ===")
print(consultar_producto("P0001"))
print(consultar_producto("P0501"))