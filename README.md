# Sistema Inteligente de Gestión de Inventario — Supermercado Oriental

Sistema de análisis y predicción de inventario que combina modelos de Machine Learning con algoritmos de búsqueda inteligente para optimizar la gestión de productos de un supermercado oriental.

---

## Estructura del proyecto

```
LRPD_sI/
├── data/
│   ├── inventario_oriental.csv       # Dataset base generado
│   ├── inventario_preprocesado.csv   # Dataset limpio y normalizado
│   └── dataset_modelado.csv          # Dataset con variables derivadas
├── outputs/
│   ├── graficos/
│   │   ├── demanda_real_vs_predicha.png
│   │   ├── matriz_confusion.png
│   │   └── arbol_decision.png
│   └── reportes/
│       ├── metricas_modelos.csv
│       ├── recomendaciones.csv
│       └── productos_priorizados.csv
├── src/
│   ├── generar_dataset.py     # Generación del dataset sintético
│   ├── preprocesamiento.py    # Limpieza, normalización y clasificación
│   ├── procesamiento.py       # Cálculo de variables derivadas
│   ├── modelos.py             # Regresión lineal y árbol de decisión
│   ├── agente.py              # Agente de reglas para recomendaciones
│   ├── busqueda.py            # Best-First Search para priorización
│   └── main.py                # Punto de entrada principal
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python 3.10 o superior
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecución

### 1. Generar el dataset base (solo la primera vez)

```bash
python src/generar_dataset.py
```

Esto crea `data/inventario_oriental.csv` con 500 registros de productos sintéticos distribuidos en 9 categorías (Mascotas, Hogar, Cocina, Comida Asiática, Decoración, Electrónica, Belleza, Papelería, Ropa).

### 2. Ejecutar el sistema completo

```bash
python src/main.py
```

Esto corre en orden:
1. **Preprocesamiento** — limpieza, normalización y clasificación de nivel de rotación
2. **Procesamiento** — cálculo de índice de rotación, urgencia de stock y riesgo de vencimiento
3. **Modelos ML** — entrenamiento de regresión lineal y árbol de decisión
4. **Agente inteligente** — generación de recomendaciones por reglas
5. **Best-First Search** — priorización de productos por reposición

---

## Modelos utilizados

### Regresión Lineal
- **Objetivo:** predecir el `indice_rotacion` de cada producto
- **Features:** `stock_actual`, `stock_minimo`, `cantidad_vendida`, `dias_para_vencer`, `urgencia_stock`
- **Preprocesamiento:** escalado con `StandardScaler`
- **Resultado:** R² ≈ 0.62
- **¿Por qué regresión lineal y no red neuronal?** El dataset tiene 500 registros y las relaciones entre variables son aproximadamente lineales. Una red neuronal requeriría miles de registros para generalizar bien y añadiría complejidad innecesaria sin mejora significativa en este contexto.

### Árbol de Decisión
- **Objetivo:** clasificar el `nivel_rotacion` (Alta / Media / Baja)
- **Features:** `stock_actual`, `stock_minimo`, `dias_para_vencer`, `urgencia_stock`
- **Parámetros:** `max_depth=3`, `min_samples_leaf=5`
- **Resultado:** Accuracy ≈ 0.38, F1 ≈ 0.35
- **¿Por qué árbol de decisión y no SVM?** El árbol produce reglas interpretables (ej. "si stock_actual ≤ 44.5 entonces..."), lo cual es clave para que el negocio entienda y confíe en las decisiones. Un SVM es una caja negra que no permite esa interpretabilidad.

### Best-First Search
- **Objetivo:** priorizar productos para reposición
- **Función heurística h(n):** `0.5 × rotación + 0.3 × demanda_norm + 0.2 × urgencia_stock`
- **¿Por qué Best-First y no A\*?** A\* requiere un grafo con costos reales de transición g(n). En este problema no existe un grafo de nodos, solo una lista de productos a ordenar por prioridad. Best-First Search con h(n) es suficiente y más eficiente para este caso.

---

## Outputs generados

| Archivo | Descripción |
|---|---|
| `metricas_modelos.csv` | MSE, R² de regresión y Accuracy, F1 del árbol |
| `recomendaciones.csv` | Acción recomendada por producto (reabastecimiento, sobrestock, promoción) |
| `productos_priorizados.csv` | Productos ordenados por score de prioridad |
| `demanda_real_vs_predicha.png` | Gráfico de dispersión real vs predicho (regresión) |
| `matriz_confusion.png` | Matriz de confusión del árbol de decisión |
| `arbol_decision.png` | Visualización del árbol de decisión |

---

## Agente inteligente

El agente aplica 3 reglas de negocio sobre cada producto:

| Condición | Acción |
|---|---|
| Rotación Alta + stock < stock mínimo | Reabastecimiento urgente |
| Rotación Baja + stock > 3× stock mínimo | Alerta de sobrestock |
| Días para vencer < 15 | Promocionar producto |
| Ninguna condición anterior | Monitorear |
