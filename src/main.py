import os

print("===================================")
print("SUPERMERCADO ORIENTAL")
print("SISTEMA INTELIGENTE")
print("===================================")

os.makedirs(
    "outputs/graficos",
    exist_ok=True
)

os.makedirs(
    "outputs/reportes",
    exist_ok=True
)

# PREPROCESAMIENTO

exec(
    open(
        "src/preprocesamiento.py",
        encoding="utf-8"
    ).read()
)

# PROCESAMIENTO

exec(
    open(
        "src/procesamiento.py",
        encoding="utf-8"
    ).read()
)

# MODELOS

exec(
    open(
        "src/modelos.py",
        encoding="utf-8"
    ).read()
)

# AGENTE

exec(
    open(
        "src/agente.py",
        encoding="utf-8"
    ).read()
)

# BEST FIRST SEARCH

exec(
    open(
        "src/busqueda.py",
        encoding="utf-8"
    ).read()
)

print("\nPROYECTO FINALIZADO")