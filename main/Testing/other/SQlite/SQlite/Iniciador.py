import sqlite3

# Inicializar base de datos SQLite
def inicializar_base_datos():
    conn = sqlite3.connect('information.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            Producto TEXT NOT NULL,
            precio REAL NOT NULL,
            Total REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

""""

def create_table():
    conn = sqlite3.connect('information.db')
    cur = conn.cursor()

    # N:N Relationship between sale and product
    cur.execute('''
    CREATE TABLE IF NOT EXISTS sale (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        total REAL NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS sale_product (
        sale_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (sale_id) REFERENCES sale(id),
        FOREIGN KEY (product_id) REFERENCES product(id),
        PRIMARY KEY (sale_id, product_id)
    )
    ''')

    # 1:N Relationship between customer and shopping
    cur.execute('''
    CREATE TABLE IF NOT EXISTS customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        name TEXT NOT NULL,
        nickname TEXT NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS shopping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        total REAL NOT NULL,
        customer_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customer(id)
    )
    ''')

    conn.commit()
    conn.close()

"""