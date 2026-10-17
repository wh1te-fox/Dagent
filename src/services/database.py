import sqlite3


DB_NAME = "ventas.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def crear_bd():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL DEFAULT 0,
            existencia INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            codigo TEXT NOT NULL,
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            subtotal REAL NOT NULL,
            descuento REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (producto_id)
                REFERENCES productos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS creditos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            monto REAL NOT NULL,
            descripcion TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            pagado REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (cliente_id)
                REFERENCES clientes(id)
        )
    """)

    cursor.execute("PRAGMA table_info(creditos)")
    columnas = [col[1] for col in cursor.fetchall()]
    if "pagado" not in columnas:
        cursor.execute("ALTER TABLE creditos ADD COLUMN pagado REAL NOT NULL DEFAULT 0")

    conn.commit()
    conn.close()


def guardar_producto(codigo, nombre, categoria, precio, existencia):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO productos (
            codigo,
            nombre,
            categoria,
            precio,
            existencia
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        codigo,
        nombre,
        categoria,
        precio,
        existencia
    ))

    conn.commit()
    conn.close()


def obtener_producto_por_codigo(codigo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            codigo,
            nombre,
            categoria,
            precio,
            existencia
        FROM productos
        WHERE codigo = ?
    """, (codigo,))

    producto = cursor.fetchone()

    conn.close()

    return producto


def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            codigo,
            nombre,
            categoria,
            precio,
            existencia
        FROM productos
        ORDER BY nombre
    """)

    productos = cursor.fetchall()

    conn.close()

    return productos


def buscar_productos(termino=""):
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT
            id,
            codigo,
            nombre,
            categoria,
            precio,
            existencia
        FROM productos
        WHERE codigo LIKE ? OR nombre LIKE ? OR categoria LIKE ?
        ORDER BY nombre
    """
    param = f"%{termino}%"
    cursor.execute(query, (param, param, param))
    productos = cursor.fetchall()

    conn.close()

    return productos


def actualizar_producto_stock(producto_id, existencia):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE productos
        SET existencia = ?
        WHERE id = ?
    """, (existencia, producto_id))

    conn.commit()
    conn.close()


def guardar_venta(
    producto_id,
    codigo,
    producto,
    cantidad,
    precio,
    subtotal,
    descuento,
    total
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT existencia FROM productos WHERE id = ?", (producto_id,))
    row = cursor.fetchone()
    if not row or row[0] < cantidad:
        conn.close()
        raise ValueError("Stock insuficiente para realizar la venta")

    cursor.execute("""
        INSERT INTO ventas (
            producto_id,
            codigo,
            producto,
            cantidad,
            precio,
            subtotal,
            descuento,
            total
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        producto_id,
        codigo,
        producto,
        cantidad,
        precio,
        subtotal,
        descuento,
        total
    ))

    cursor.execute("""
        UPDATE productos
        SET existencia = existencia - ?
        WHERE id = ?
    """, (cantidad, producto_id))

    conn.commit()
    conn.close()


def obtener_ventas(filtro="todos", valor=None, valor_hasta=None):
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT
            codigo,
            producto,
            cantidad,
            precio,
            subtotal,
            descuento,
            total,
            fecha
        FROM ventas
        WHERE 1=1
    """
    params = []

    if filtro == "fecha" and valor:
        query += " AND DATE(fecha) = ?"
        params.append(valor)
    elif filtro == "personalizada" and valor and valor_hasta:
        query += " AND DATE(fecha) BETWEEN ? AND ?"
        params.extend([valor, valor_hasta])
    elif filtro == "semana":
        query += " AND fecha >= datetime('now', '-7 days')"
    elif filtro == "mes":
        query += " AND strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')"

    query += " ORDER BY id DESC"

    cursor.execute(query, params)
    ventas = cursor.fetchall()

    conn.close()

    return ventas


def guardar_cliente(nombre, apellido):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clientes (
            nombre,
            apellido
        )
        VALUES (?, ?)
    """, (
        nombre,
        apellido
    ))

    conn.commit()
    conn.close()


def obtener_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            apellido
        FROM clientes
        ORDER BY nombre
    """)

    clientes = cursor.fetchall()
    conn.close()

    return clientes


def buscar_clientes(nombre="", apellido=""):
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT
            id,
            nombre,
            apellido
        FROM clientes
        WHERE 1=1
    """
    params = []

    if nombre:
        query += " AND nombre LIKE ?"
        params.append(f"%{nombre}%")
    if apellido:
        query += " AND apellido LIKE ?"
        params.append(f"%{apellido}%")

    query += " ORDER BY nombre"

    cursor.execute(query, params)
    clientes = cursor.fetchall()
    conn.close()

    return clientes


def cliente_existe(nombre, apellido):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM clientes WHERE LOWER(nombre) = LOWER(?) AND LOWER(apellido) = LOWER(?)
    """, (nombre.strip(), apellido.strip()))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def actualizar_cliente(id, nombre, apellido):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nombre = ?, apellido = ?
        WHERE id = ?
    """, (nombre, apellido, id))
    conn.commit()
    conn.close()


def guardar_credito(cliente_id, monto, descripcion, pagado=0):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO creditos (cliente_id, monto, descripcion, pagado)
        VALUES (?, ?, ?, ?)
    """, (cliente_id, monto, descripcion, pagado))
    conn.commit()
    conn.close()


def guardar_venta_con_credito(producto_id, codigo, producto, cantidad, precio, subtotal, descuento, total, abono, cliente_id, descripcion_credito):
    """Saves the sale and, when the cash payment does not cover the total,
    registers the remaining balance as a credit for the client in one transaction."""
    if abono < 0 or abono > total + 1e-9:
        raise ValueError("El abono debe estar entre 0 y el total de la venta")
    if abono < total - 1e-9 and cliente_id is None:
        raise ValueError("Se requiere un cliente para registrar la venta a crédito")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT existencia FROM productos WHERE id = ?", (producto_id,))
    row = cursor.fetchone()
    if not row or row[0] < cantidad:
        conn.close()
        raise ValueError("Stock insuficiente para realizar la venta")

    cursor.execute("""
        INSERT INTO ventas (
            producto_id,
            codigo,
            producto,
            cantidad,
            precio,
            subtotal,
            descuento,
            total
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        producto_id,
        codigo,
        producto,
        cantidad,
        precio,
        subtotal,
        descuento,
        total
    ))

    cursor.execute("""
        UPDATE productos
        SET existencia = existencia - ?
        WHERE id = ?
    """, (cantidad, producto_id))

    pendiente = total - abono
    if pendiente > 1e-9:
        cursor.execute("""
            INSERT INTO creditos (cliente_id, monto, descripcion, pagado)
            VALUES (?, ?, ?, 0)
        """, (cliente_id, pendiente, descripcion_credito))

    conn.commit()
    conn.close()


def obtener_creditos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            c.id,
            c.cliente_id,
            cli.nombre,
            cli.apellido,
            c.monto,
            c.descripcion,
            c.fecha,
            c.pagado
        FROM creditos c
        LEFT JOIN clientes cli ON c.cliente_id = cli.id
        ORDER BY c.id DESC
    """)
    creditos = cursor.fetchall()
    conn.close()
    return creditos


def registrar_abono(credito_id, monto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT monto, pagado FROM creditos WHERE id = ?", (credito_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError("El crédito no existe")

    total, pagado = row
    saldo = total - pagado

    if monto <= 0:
        conn.close()
        raise ValueError("El abono debe ser mayor que cero")
    if monto > saldo + 1e-9:
        conn.close()
        raise ValueError(f"El abono excede el saldo pendiente (${saldo:.2f})")

    cursor.execute("UPDATE creditos SET pagado = pagado + ? WHERE id = ?", (monto, credito_id))
    conn.commit()
    conn.close()


def obtener_resumen_creditos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            COALESCE(SUM(monto), 0),
            COALESCE(SUM(pagado), 0),
            COALESCE(SUM(monto - pagado), 0),
            COALESCE(SUM(CASE WHEN monto - pagado > 0.009 THEN 1 ELSE 0 END), 0)
        FROM creditos
    """)
    resumen = cursor.fetchone()
    conn.close()
    return resumen
