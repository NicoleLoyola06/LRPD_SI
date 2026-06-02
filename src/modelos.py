import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

# REGRESIÓN
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ÁRBOL
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ==========================
# CARGAR DATASET
# ==========================

df = pd.read_csv("data/dataset_modelado.csv")

# Crear carpeta outputs si no existe
import os

os.makedirs("outputs/reportes", exist_ok=True)
os.makedirs("outputs/graficos", exist_ok=True)

# ====================================================
# MODELO 1: REGRESIÓN LINEAL
# ====================================================

print("\n=== REGRESIÓN LINEAL ===")

# Variable objetivo:
# predecir cantidad_vendida

X_reg = df[
    [
        "stock_actual",
        "stock_minimo",
        "dias_para_vencer"
    ]
]

y_reg = df["cantidad_vendida"]

X_train, X_test, y_train, y_test = train_test_split(
    X_reg,
    y_reg,
    test_size=0.20,
    random_state=42
)

modelo_regresion = LinearRegression()

modelo_regresion.fit(
    X_train,
    y_train
)

predicciones = modelo_regresion.predict(X_test)

mse = mean_squared_error(
    y_test,
    predicciones
)

r2 = r2_score(
    y_test,
    predicciones
)

print("MSE:", mse)
print("R2:", r2)

# ==========================
# GRAFICO REGRESIÓN
# ==========================

plt.figure(figsize=(8,5))

plt.scatter(
    y_test,
    predicciones
)

plt.xlabel("Ventas reales")
plt.ylabel("Ventas predichas")

plt.title(
    "Demanda real vs predicha"
)

plt.tight_layout()

plt.savefig(
    "outputs/graficos/demanda_real_vs_predicha.png"
)

plt.close()

# ====================================================
# MODELO 2: ÁRBOL DE DECISIÓN
# ====================================================

print("\n=== ÁRBOL DE DECISIÓN ===")

X_clf = df[
    [
        "stock_actual",
        "stock_minimo",
        "cantidad_vendida",
        "dias_para_vencer"
    ]
]

y_clf = df["nivel_rotacion"]

X_train, X_test, y_train, y_test = train_test_split(
    X_clf,
    y_clf,
    test_size=0.20,
    random_state=42
)

modelo_arbol = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

modelo_arbol.fit(
    X_train,
    y_train
)

pred = modelo_arbol.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    pred
)

precision = precision_score(
    y_test,
    pred,
    average="weighted"
)

recall = recall_score(
    y_test,
    pred,
    average="weighted"
)

f1 = f1_score(
    y_test,
    pred,
    average="weighted"
)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)

# ==========================
# MATRIZ DE CONFUSIÓN
# ==========================

cm = confusion_matrix(
    y_test,
    pred
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=modelo_arbol.classes_
)

disp.plot()

plt.savefig(
    "outputs/graficos/matriz_confusion.png"
)

plt.close()

# ==========================
# GRAFICO DEL ÁRBOL
# ==========================

plt.figure(figsize=(14,8))

plot_tree(
    modelo_arbol,
    filled=True,
    feature_names=X_clf.columns,
    class_names=modelo_arbol.classes_
)

plt.savefig(
    "outputs/graficos/arbol_decision.png"
)

plt.close()

# ====================================================
# GUARDAR MÉTRICAS
# ====================================================

metricas = pd.DataFrame({

    "Modelo": [
        "Regresion Lineal",
        "Arbol de Decision"
    ],

    "Metrica_1": [
        mse,
        accuracy
    ],

    "Metrica_2": [
        r2,
        f1
    ]
})

metricas.to_csv(
    "outputs/reportes/metricas_modelos.csv",
    index=False
)

print("\nArchivos generados correctamente")