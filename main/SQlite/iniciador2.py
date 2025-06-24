import sqlite3

def iniciar_base_datos():
    cur = sqlite3.connect('ventas.db')
    conn = cur.cursor()
    conn.execute ('''
CREATE TABLE customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nickname TEXT UNIQUE,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);''')

    conn.execute ('''
CREATE TABLE sale (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total REAL NOT NULL,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);''')
    
    conn.execute ('''
CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    price REAL NOT NULL
);''')
    
    conn.execute ('''
CREATE TABLE sale_product (
    sale_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (sale_id, product_id),
    FOREIGN KEY (sale_id) REFERENCES sale(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);''')

    cur.commit()
    cur.close()
