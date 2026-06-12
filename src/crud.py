import sqlite3
import pandas as pd

DB_PATH = "data/inventario.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def agregar_producto(producto: dict):
    """
    producto debe tener las mismas columnas que la tabla 'inventario':
    codigo_producto, nombre_producto, categoria, stock_actual,
    stock_minimo, cantidad_vendida, fecha_venta, dias_para_vencer
    """
    conn = conectar()
    pd.DataFrame([producto]).to_sql(
        "inventario", conn, if_exists="append", index=False
    )
    conn.close()
    print(f"Producto {producto['codigo_producto']} agregado")


def actualizar_stock(codigo_producto: str, nuevo_stock: int):
    conn = conectar()
    conn.execute(
        "UPDATE inventario SET stock_actual = ? WHERE codigo_producto = ?",
        (nuevo_stock, codigo_producto)
    )
    conn.commit()
    conn.close()
    print(f"Stock de {codigo_producto} actualizado a {nuevo_stock}")


def registrar_venta(codigo_producto: str, cantidad: int):
    conn = conectar()
    conn.execute(
        """
        UPDATE inventario
        SET cantidad_vendida = cantidad_vendida + ?,
            stock_actual = stock_actual - ?
        WHERE codigo_producto = ?
        """,
        (cantidad, cantidad, codigo_producto)
    )
    conn.commit()
    conn.close()
    print(f"Venta registrada: {cantidad} unidades de {codigo_producto}")


def eliminar_producto(codigo_producto: str):
    conn = conectar()
    conn.execute(
        "DELETE FROM inventario WHERE codigo_producto = ?",
        (codigo_producto,)
    )
    conn.commit()
    conn.close()
    print(f"Producto {codigo_producto} eliminado")


def consultar_producto(codigo_producto: str):
    conn = conectar()
    resultado = pd.read_sql(
        "SELECT * FROM inventario WHERE codigo_producto = ?",
        conn, params=(codigo_producto,)
    )
    conn.close()
    return resultado