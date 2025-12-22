import sqlite3 as sql

def productos(n, p):

    conn = sql.connect("information.db")
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTIS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio TEXT NOT NULL
                );  ''')
    conn.commit()
    conn.close()

productos()