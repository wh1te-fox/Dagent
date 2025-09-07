import sqlite3 as sql

conn = sql.connect("informatio.db")
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTIS productos (
            )
''')