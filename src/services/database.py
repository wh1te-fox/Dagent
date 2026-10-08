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


def obtener_ventas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
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
        ORDER BY id DESC
    """)

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
