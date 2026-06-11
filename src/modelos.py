import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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

os.makedirs("outputs/reportes", exist_ok=True)
os.makedirs("outputs/graficos", exist_ok=True)

# ====================================================
# MODELO 1: REGRESIÓN LINEAL
# Objetivo: predecir indice_rotacion
# (cantidad_vendida / stock_actual — tiene relación
#  lógica con los features seleccionados)
# ====================================================

print("\n=== REGRESIÓN LINEAL ===")

X_reg = df[[
    "stock_actual",
    "stock_minimo",
    "cantidad_vendida",
    "dias_para_vencer",
    "urgencia_stock"
]]

y_reg = df["indice_rotacion"]

X_train, X_test, y_train, y_test = train_test_split(
    X_reg, y_reg,
    test_size=0.20,
    random_state=42
)

# Escalado de features (mejora convergencia y comparabilidad)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

modelo_regresion = LinearRegression()
modelo_regresion.fit(X_train_s, y_train)

predicciones = modelo_regresion.predict(X_test_s)

mse = mean_squared_error(y_test, predicciones)
r2  = r2_score(y_test, predicciones)

print("MSE:", mse)
print("R2: ", r2)

# ==========================
# GRÁFICO REGRESIÓN
# ==========================

plt.figure(figsize=(8, 5))
plt.scatter(y_test, predicciones, alpha=0.6)
plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--", label="Predicción perfecta"
)
plt.xlabel("Índice de rotación real")
plt.ylabel("Índice de rotación predicho")
plt.title(f"Demanda real vs predicha  (R² = {r2:.3f})")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/graficos/demanda_real_vs_predicha.png")
plt.close()

# ====================================================
# MODELO 2: ÁRBOL DE DECISIÓN
# max_depth=3 para evitar sobreajuste
# ====================================================

print("\n=== ÁRBOL DE DECISIÓN ===")

X_clf = df[[
    "stock_actual",
    "stock_minimo",
    "dias_para_vencer",
    "urgencia_stock"
]]

y_clf = df["nivel_rotacion"]

X_train, X_test, y_train, y_test = train_test_split(
    X_clf, y_clf,
    test_size=0.20,
    random_state=42
)

# max_depth=3 limita la profundidad para evitar que el árbol
# memorice el conjunto de entrenamiento (sobreajuste).
# min_samples_leaf=5 exige al menos 5 muestras en cada hoja,
# lo que también mejora la generalización.
modelo_arbol = DecisionTreeClassifier(
    max_depth=3,
    min_samples_leaf=5,
    random_state=42
)

modelo_arbol.fit(X_train, y_train)

pred_train = modelo_arbol.predict(X_train)
pred_test  = modelo_arbol.predict(X_test)

accuracy_train = accuracy_score(y_train, pred_train)
accuracy_test  = accuracy_score(y_test,  pred_test)

precision = precision_score(y_test, pred_test, average="weighted")
recall    = recall_score(   y_test, pred_test, average="weighted")
f1        = f1_score(       y_test, pred_test, average="weighted")

print(f"Accuracy entrenamiento : {accuracy_train:.4f}")
print(f"Accuracy prueba        : {accuracy_test:.4f}")
print("Precision:", precision)
print("Recall:   ", recall)
print("F1:       ", f1)

# ==========================
# MATRIZ DE CONFUSIÓN
# ==========================

cm   = confusion_matrix(y_test, pred_test)
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=modelo_arbol.classes_
)
disp.plot()
plt.title("Matriz de confusión — Árbol de decisión")
plt.savefig("outputs/graficos/matriz_confusion.png")
plt.close()

# ==========================
# GRÁFICO DEL ÁRBOL
# ==========================

plt.figure(figsize=(16, 8))
plot_tree(
    modelo_arbol,
    filled=True,
    feature_names=X_clf.columns,
    class_names=modelo_arbol.classes_,
    impurity=True,
    rounded=True
)
plt.title("Árbol de decisión (max_depth=3)")
plt.tight_layout()
plt.savefig("outputs/graficos/arbol_decision.png", dpi=150)
plt.close()

# ====================================================
# GUARDAR MÉTRICAS
# ====================================================

metricas = pd.DataFrame({
    "Modelo":     ["Regresion Lineal",  "Arbol de Decision"],
    "Metrica_1":  [mse,                 accuracy_test],
    "Metrica_2":  [r2,                  f1],
    "Metrica_3":  ["—",                 f"Train acc: {accuracy_train:.4f}"]
})

metricas.to_csv("outputs/reportes/metricas_modelos.csv", index=False)

print("\nArchivos generados correctamente")