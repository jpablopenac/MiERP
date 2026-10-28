"""Carga datos de ejemplo. Ejecutar desde la raíz: python -m scripts.seed_demo"""
from mierp import services
from mierp.database import DB_PATH
from mierp.schema import crear_tablas

if __name__ == "__main__":
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    crear_tablas()

    services.insertar_orden_compra("OC001", "Cliente A", "2025-05-02", 50000, dias_entrega=7)
    services.insertar_orden_compra("OC002", "Cliente B", "2025-05-03", 75000, dias_entrega=10)

    services.insertar_guia_despacho("GD001", "OC001", "2025-05-09")
    services.insertar_guia_despacho("GD002", fecha_gd="2025-05-10")

    services.insertar_factura("F001", "GD001", "2025-05-10", 50000)
    services.insertar_factura("F002", "GD002", "2025-05-11", 30000)

    services.actualizar_pago("F001", "2025-05-15")
