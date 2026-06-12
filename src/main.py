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

# INICIALIZAR BASE DE DATOS (solo la primera vez)

if not os.path.exists("data/inventario.db"):
    exec(
        open(
            "src/init_db.py",
            encoding="utf-8"
        ).read()
    )
    
# SINCRONIZAR EXCEL → BASE DE DATOS (si el archivo existe)
import os
if os.path.exists("data/inventario_editable.xlsx"):
    exec(open("src/importar_excel.py", encoding="utf-8").read())
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