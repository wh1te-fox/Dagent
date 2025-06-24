import sqlite3

# Inicializar base de datos SQLite
def inicializar_base_datos():
    
    conn = sqlite3.connect('information.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS sale (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            product TEXT NOT NULL,
            valor REAL NOT NULL,
            Total REAL NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS inputs (
            product TEXT NOT NULL,
            valor REAL NOT NULL
        )
    ''')
    print("good")
    conn.commit()
    conn.close()

inicializar_base_datos()
