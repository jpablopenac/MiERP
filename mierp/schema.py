from mierp.database import get_connection

TABLES = (
    '''
    CREATE TABLE IF NOT EXISTS OrdenesCompra (
        id_oc INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_oc TEXT NOT NULL UNIQUE,
        cliente TEXT NOT NULL,
        fecha_oc DATE NOT NULL,
        fecha_entrega DATE,
        monto INTEGER NOT NULL
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS GuiasDespacho (
        id_gd INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_gd TEXT NOT NULL UNIQUE,
        id_oc INTEGER,
        fecha_gd DATE NOT NULL,
        FOREIGN KEY (id_oc) REFERENCES OrdenesCompra(id_oc)
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Facturas (
        id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_factura TEXT NOT NULL UNIQUE,
        id_gd INTEGER,
        fecha_factura DATE NOT NULL,
        monto INTEGER NOT NULL,
        FOREIGN KEY (id_gd) REFERENCES GuiasDespacho(id_gd)
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Pagos (
        id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
        id_factura INTEGER NOT NULL,
        monto INTEGER NOT NULL,
        fecha_pago_esperada DATE NOT NULL,
        fecha_pago_real DATE,
        estado_pago TEXT DEFAULT 'Pendiente',
        FOREIGN KEY (id_factura) REFERENCES Facturas(id_factura)
    )
    ''',
)


def crear_tablas(db_path=None):
    with get_connection(db_path) as conn:
        for ddl in TABLES:
            conn.execute(ddl)
