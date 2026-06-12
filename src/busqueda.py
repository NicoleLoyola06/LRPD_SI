import pandas as pd
import sqlite3
import os

# ============================================================
# ALGORITMO: BEST-FIRST SEARCH
#
# ¿Por qué Best-First Search y no A*?
# - A* combina g(n) + h(n): necesita un grafo con costos reales
#   de transición entre estados. En este problema no existe un
#   grafo de nodos; solo hay una lista de productos a priorizar.
# - Best-First Search solo usa h(n) (función heurística), lo que
#   es suficiente cuando el objetivo es ORDENAR por prioridad,
#   no encontrar el camino óptimo entre estados.
# - Complejidad temporal: O(n log n) por el sort, frente a
#   O(b^d) de A* sobre un grafo explícito.
# Conclusión: Best-First Search es la elección correcta para
# ranking de inventario sin estructura de grafo.
# ============================================================

print("\n=== BEST-FIRST SEARCH ===")

os.makedirs("outputs/reportes", exist_ok=True)

conn = sqlite3.connect("data/inventario.db")
df = pd.read_sql("SELECT * FROM dataset_modelado", conn)
conn.close()

rotacion_map = {
    "Alta":  1.0,
    "Media": 0.5,
    "Baja":  0.0
}

df["rotacion_num"] = df["nivel_rotacion"].map(rotacion_map)

max_demanda = df["cantidad_vendida"].max()

df["demanda_norm"] = df["cantidad_vendida"] / max_demanda

# -------------------------------------------------------
# h(n) — función heurística de prioridad
# Pesos elegidos según impacto en el negocio:
#   0.5 · rotación  → factor más importante (mueve el inventario)
#   0.3 · demanda   → señal de mercado
#   0.2 · urgencia  → riesgo de quiebre de stock
# -------------------------------------------------------
df["prioridad"] = (
    0.5 * df["rotacion_num"]
    + 0.3 * df["demanda_norm"]
    + 0.2 * df["urgencia_stock"]
)

priorizados = df.sort_values(by="prioridad", ascending=False)

priorizados.to_csv(
    "outputs/reportes/productos_priorizados.csv",
    index=False
)

print("productos_priorizados.csv generado")
print(f"Top 5 productos priorizados:\n{priorizados[['nombre_producto','nivel_rotacion','prioridad']].head()}")