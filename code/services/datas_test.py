import sqlite3

def init_base():
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()

    # Tabla de clientes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        ID_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL
    );
    """)

    # Tabla de estados del cliente
    cur.execute("""
    CREATE TABLE IF NOT EXISTS estados (
        ID_estado INTEGER PRIMARY KEY AUTOINCREMENT,
        estado TEXT NOT NULL
    );
    """)

    # Tabla de productos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        ID_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    );
    """)

    # Tabla de precios de productos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS precios (
        ID_precio INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_producto INTEGER NOT NULL,
        precio REAL NOT NULL,
        FOREIGN KEY (ID_producto) REFERENCES productos(ID_producto)
    );
    """)

    # Tabla de ventas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS venta (
        ID_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        fecha TEXT DEFAULT CURRENT_TIMESTAMP,
        total REAL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(ID_cliente)
    );
    """)

    conn.commit()
    conn.close()

def agregar_cliente(nombre, apellido):
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO clientes (nombre, apellido) VALUES (?, ?)", (nombre, apellido))
    conn.commit()
    conn.close()

def agregar_estado(estado):
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO estados (estado) VALUES (?)", (estado,))
    conn.commit()
    conn.close()

def agregar_producto(nombre, precio):
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO productos (nombre) VALUES (?)", (nombre,))
    producto_id = cur.lastrowid
    cur.execute("INSERT INTO precios (ID_producto, precio) VALUES (?, ?)", (producto_id, precio))
    conn.commit()
    conn.close()

def registrar_venta(cliente_id, total):
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO venta (cliente_id, total) VALUES (?, ?)", (cliente_id, total))
    conn.commit()
    conn.close()

def ver_clientes():
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM clientes")
    clientes = cur.fetchall()
    conn.close()
    return clientes

def ver_productos_con_precios():
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute("""
    SELECT productos.nombre, precios.precio
    FROM productos
    JOIN precios ON productos.ID_producto = precios.ID_producto
    """)
    resultados = cur.fetchall()
    conn.close()
    return resultados

def ver_ventas():
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute("""
    SELECT venta.ID_venta, clientes.nombre, clientes.apellido, venta.fecha, venta.total
    FROM venta
    JOIN clientes ON venta.cliente_id = clientes.ID_cliente
    """)
    ventas = cur.fetchall()
    conn.close()
    return ventas

# Bloque principal
if __name__ == "__main__":
    # Inicializar base de datos
    init_base()

    # Insertar datos de prueba
    agregar_cliente("Juan", "Pérez")
    agregar_cliente("Ana", "García")

    agregar_estado("Activo")
    agregar_estado("Inactivo")

    agregar_producto("Camiseta", 19.99)
    agregar_producto("Pantalón", 39.99)
    agregar_producto("Zapatos", 59.99)

    registrar_venta(1, 59.98)  # Juan compra
    registrar_venta(2, 39.99)  # Ana compra

    # Consultas
    clientes = ver_clientes()
    print("Clientes:")
    for cliente in clientes:
        print(cliente)

    productos = ver_productos_con_precios()
    print("\nProductos con precios:")
    for producto in productos:
        print(producto)

    ventas = ver_ventas()
    print("\nVentas:")
    for venta in ventas:
        print(venta)
