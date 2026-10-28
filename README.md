# MiERP

Sistema de escritorio para el control del ciclo comercial de una pyme: **orden de compra → guía de despacho → factura → pago**. Su objetivo es centralizar la trazabilidad de cada documento y anticipar pendientes, como entregas sin facturar o facturas vencidas sin pago.

El proyecto se desarrolla de forma incremental. Actualmente cuenta con la capa de datos y la lógica de negocio base; la interfaz gráfica y las notificaciones se encuentran planificadas (ver [Hoja de ruta](#hoja-de-ruta)).

## Funcionalidades actuales

- Modelo relacional en SQLite con cuatro entidades: órdenes de compra, guías de despacho, facturas y pagos.
- Registro de órdenes de compra, con cálculo automático de la fecha de entrega a partir de los días comprometidos.
- Registro de guías de despacho, con vinculación opcional a una orden de compra.
- Registro de facturas, vinculadas a una guía. Cada factura genera automáticamente un pago pendiente con vencimiento a 30 días.
- Actualización del estado de un pago a «Pagado» con su fecha real.
- Operaciones atómicas: la creación de una factura y de su pago se realiza en una única transacción, con integridad referencial activada.

## Modelo de datos

```
OrdenesCompra 1 ──< GuiasDespacho 1 ──< Facturas 1 ──< Pagos
```

| Tabla             | Descripción                                                         |
| ----------------- | -------------------------------------------------------------------- |
| `OrdenesCompra` | Pedido del cliente: número, cliente, fecha, fecha de entrega, monto |
| `GuiasDespacho` | Entrega física, opcionalmente asociada a una orden de compra        |
| `Facturas`      | Documento tributario asociado a una guía                            |
| `Pagos`         | Fecha de pago esperada y real, y estado (`Pendiente` / `Pagado`) |

## Estructura del proyecto

```
MiERP/
├── mierp/
│   ├── database.py      # Conexión SQLite y manejo de transacciones
│   ├── schema.py        # Definición de tablas
│   └── services.py      # Lógica de negocio (altas y actualizaciones)
├── scripts/
│   ├── init_db.py       # Crea la base de datos y las tablas
│   └── seed_demo.py     # Carga datos de ejemplo
├── data/                # Ubicación de la base de datos local (no versionada)
└── README.md
```

## Requisitos

- Python 3.9 o superior. La etapa actual solo utiliza la biblioteca estándar.

## Uso

Desde la raíz del repositorio:

```bash
# 1. Crear la base de datos
python -m scripts.init_db

# 2. (Opcional) Cargar datos de ejemplo
python -m scripts.seed_demo
```

Ejemplo de uso desde Python:

```python
from mierp import services

services.insertar_orden_compra("OC003", "Cliente C", "2025-06-01", 90000, dias_entrega=7)
services.insertar_guia_despacho("GD003", "OC003", "2025-06-08")
services.insertar_factura("F003", "GD003", "2025-06-09", 90000)
services.actualizar_pago("F003", "2025-06-20")
```

## Hoja de ruta

| Etapa | Descripción                                                                                                                  | Estado      |
| ----- | ----------------------------------------------------------------------------------------------------------------------------- | ----------- |
| 1     | Base de datos SQLite y funciones de alta, actualización y consulta                                                           | Completada  |
| 2     | Interfaz gráfica mínima (PySimpleGUI) para registrar guías, facturas y pagos                                               | Planificada |
| 3     | Validaciones: una guía no puede facturarse dos veces ni una factura pagarse más de una vez; alertas por vínculos faltantes | Planificada |
| 4     | Notificaciones de escritorio (plyer) para entregas sin facturar y facturas vencidas                                           | Planificada |
| 5     | Reportes con filtros (facturas pendientes, entregas próximas) y exportación a Excel                                         | Planificada |
| 6     | Empaquetado como ejecutable con PyInstaller y pruebas en un equipo sin Python                                                 | Planificada |

## Mejoras futuras

**Calidad y mantenibilidad**

- Suite de pruebas automatizadas con `pytest` sobre una base de datos en memoria.
- Validación de entradas (formato de fechas, montos positivos, números de documento únicos) con mensajes de error propios en lugar de `print`.
- Sistema de migraciones del esquema, para evolucionar la base sin perder datos.
- Integración continua con GitHub Actions (pruebas y análisis estático con `ruff`).
- Tipado estático y documentación de las funciones públicas.

**Funcionalidad**

- Soporte de pagos parciales y de múltiples facturas por guía.
- Plazo de pago configurable por cliente, en lugar del valor fijo de 30 días.
- Gestión de clientes como entidad propia, con historial de documentos.
- Cálculo de IVA y manejo de notas de crédito.
- Dashboard con indicadores: facturación mensual, antigüedad de saldos y cumplimiento de plazos de entrega.
- Importación de documentos desde archivos CSV o Excel.

**Arquitectura**

- Separación en capas (repositorio, servicios, interfaz) para facilitar el cambio de motor de base de datos.
- Migración opcional a PostgreSQL para uso multiusuario.
- Exposición de la lógica mediante una API REST (FastAPI) y una interfaz web como alternativa a la de escritorio.
- Autenticación y registro de auditoría de cambios.
