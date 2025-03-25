import sqlite3

# Inicializar base de datos SQLite
def inicializar_base_datos():
    conn = sqlite3.connect('ventas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            Producto TEXT NOT NULL,
            precio REAL NOT NULL,
            Total REAL NOT NULL,
        )
    ''')
    conn.commit()
    conn.close()