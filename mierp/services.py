from datetime import datetime, timedelta

from mierp.database import get_connection

DIAS_PLAZO_PAGO = 30


def calcular_fecha(dias, fecha_base):
    fecha_dt = datetime.strptime(fecha_base, "%Y-%m-%d")
    nueva_fecha = fecha_dt + timedelta(days=dias)
    return nueva_fecha.strftime("%Y-%m-%d")


def _buscar_id(conn, tabla, columna_id, columna_numero, numero):
    fila = conn.execute(
        f'SELECT {columna_id} FROM {tabla} WHERE {columna_numero} = ?', (numero,)
    ).fetchone()
    return fila[0] if fila else None


def buscar_id_oc(numero_oc):
    with get_connection() as conn:
        return _buscar_id(conn, 'OrdenesCompra', 'id_oc', 'numero_oc', numero_oc)


def buscar_id_gd(numero_gd):
    with get_connection() as conn:
        return _buscar_id(conn, 'GuiasDespacho', 'id_gd', 'numero_gd', numero_gd)


def buscar_id_factura(numero_factura):
    with get_connection() as conn:
        return _buscar_id(conn, 'Facturas', 'id_factura', 'numero_factura', numero_factura)


def insertar_orden_compra(numero_oc, cliente, fecha_oc, monto, dias_entrega=None):
    fecha_entrega = calcular_fecha(dias_entrega, fecha_oc) if dias_entrega else None

    with get_connection() as conn:
        conn.execute('''
            INSERT INTO OrdenesCompra (numero_oc, cliente, fecha_oc, fecha_entrega, monto)
            VALUES (?, ?, ?, ?, ?)
        ''', (numero_oc, cliente, fecha_oc, fecha_entrega, monto))

    print(f"Orden de Compra {numero_oc} insertada correctamente.")


def insertar_guia_despacho(numero_gd, numero_oc=None, fecha_gd=None):
    with get_connection() as conn:
        id_oc = (
            _buscar_id(conn, 'OrdenesCompra', 'id_oc', 'numero_oc', numero_oc)
            if numero_oc else None
        )
        conn.execute('''
            INSERT INTO GuiasDespacho (numero_gd, id_oc, fecha_gd)
            VALUES (?, ?, ?)
        ''', (numero_gd, id_oc, fecha_gd))

    print(f"Guía de Despacho {numero_gd} insertada correctamente.")


def insertar_factura(numero_factura, numero_gd, fecha_factura, monto):
    """Registra la factura y genera su pago pendiente en una sola transacción."""
    with get_connection() as conn:
        id_gd = _buscar_id(conn, 'GuiasDespacho', 'id_gd', 'numero_gd', numero_gd)

        cursor = conn.execute('''
            INSERT INTO Facturas (numero_factura, id_gd, fecha_factura, monto)
            VALUES (?, ?, ?, ?)
        ''', (numero_factura, id_gd, fecha_factura, monto))

        fecha_pago_esperada = calcular_fecha(DIAS_PLAZO_PAGO, fecha_factura)
        conn.execute('''
            INSERT INTO Pagos (id_factura, monto, fecha_pago_esperada)
            VALUES (?, ?, ?)
        ''', (cursor.lastrowid, monto, fecha_pago_esperada))

    print(f"Factura {numero_factura} insertada correctamente y pago registrado.")


def actualizar_pago(numero_factura, fecha_pago_real):
    with get_connection() as conn:
        id_factura = _buscar_id(conn, 'Facturas', 'id_factura', 'numero_factura', numero_factura)
        if not id_factura:
            print(f"No se encontró factura {numero_factura}")
            return

        conn.execute('''
            UPDATE Pagos
            SET fecha_pago_real = ?, estado_pago = 'Pagado'
            WHERE id_factura = ?
        ''', (fecha_pago_real, id_factura))

    print(f"Pago actualizado para factura {numero_factura}.")
