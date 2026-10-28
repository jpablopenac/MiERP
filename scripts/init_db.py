"""Crea la base de datos y sus tablas. Ejecutar desde la raíz: python -m scripts.init_db"""
from mierp.database import DB_PATH
from mierp.schema import crear_tablas

if __name__ == "__main__":
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    crear_tablas()
    print(f"Base de datos y tablas creadas correctamente en {DB_PATH}")
