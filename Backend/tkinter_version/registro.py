import tkinter as tk 
import sqlite3
from tkinter import messagebox

ventana = tk.Tk()
ventana.title("Ingreso de Datos")

texto = tk.Label (ventana, text= "Registro de ventas")

dato1 = tk.Label(ventana, text="fecha: ")
dato2 = tk.Label(ventana, text="producto: ")
dato3 = tk.Label(ventana, text="precio unitario: ")
dato4 = tk.Label(ventana, text="total: ")

entrada1 = tk.Entry(ventana)
entrada2 = tk.Entry(ventana)
entrada3 = tk.Entry(ventana)
entrada4 = tk.Entry(ventana)

dato5 = tk.Label (ventana, text="fecha de credito: ")
dato6 = tk.Label (ventana, text="Nombre: ")
dato7 = tk.Label (ventana, text="apellido: ")
dato8 = tk.Label (ventana, text="productos: ")
dato9 = tk.Label (ventana, text= "total")

entrada5 = tk.Entry(ventana)
entrada6 = tk.Entry(ventana)
entrada7 = tk.Entry(ventana)
entrada8 = tk.Entry(ventana)
entrada9 = tk.Entry(ventana)

mensaje = tk.Label (ventana, text="Total")
dato10 = tk.Entry (ventana)

mensaje2 = tk.Label (ventana, text= "Nombre del cliente:")
dato11 = tk.Entry (ventana)

texto.grid(column=0, row=0, padx=10, pady=10)


dato1.grid(row=1, column=0, padx=10, pady=10)
entrada1.grid(row=1, column=1, padx=10, pady=10)

dato2.grid(row=1, column=2, padx=10, pady=10)
entrada2.grid(row=1, column=3, padx=10, pady=10)

dato3.grid(row=2, column=0, padx=10, pady=10)
entrada3.grid(row=2, column=1, padx=10, pady=10)

dato4.grid(row=2, column=2, padx=10, pady=10)
entrada4.grid(row=2, column=3, padx=10, pady=10)

#

dato5.grid(row=4, column=0, padx=10, pady=10)
entrada5.grid(row=4, column=1, padx=10, pady=10)

dato6.grid(row=5, column=0, padx=10, pady=10)
entrada6.grid(row=5, column=1, padx=10, pady=10)

dato7.grid(row=5, column=2, padx=10, pady=10)
entrada7.grid(row=5, column=3, padx=10, pady=10)

dato8.grid(row=8, column=0, padx=10, pady=10)
entrada8.grid(row=8, column=1, padx=10, pady=10)

dato9.grid(row=8, column=2, padx=10, pady= 10)
entrada9.grid(row=8, column=3, padx=10, pady=10)


mensaje.grid (row = 11, column=0, padx= 10, pady= 10)
dato10.grid (row= 11, column= 1, padx= 10, pady= 10)

mensaje2.grid ( row= 10, column= 0, padx= 10, pady=10)
dato11.grid (row= 10, column=1, padx= 10, pady= 10)



# funcional

conectaBaseDatos = sqlite3.connect("data.db")
cur = conectaBaseDatos.cursor()

# Crear la tabla si no existe
cur.execute('''
    CREATE TABLE IF NOT EXISTS registro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        producto TEXT,
        precio_unitario REAL,
        total REAL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        nombre TEXT,
        apellido TEXT,
        producto TEXT,
        total REAL
    )
''')



conectaBaseDatos.commit()

def input_b():
    conectaBaseDatos.execute('''
        INSERT INTO registro (fecha, producto, precio_unitario, total)
        VALUES (?, ?, ?, ?)                     
        ''', (entrada1.get(), entrada2.get(), entrada3.get(), entrada4.get()))
    conectaBaseDatos.commit()
    # No cerrar la conexión aquí
    messagebox.showinfo("notificacion", "Los datos ha sido guardados correctamrnte")

def input_c():
    conectaBaseDatos.execute('''
    INSERT INTO clientes (fecha, nombre, apellido, producto, total)
    VALUES (?,?,?,?,?)
    ''', (entrada5.get(), entrada6.get(), entrada7.get(), entrada8.get(), entrada9.get()))
    conectaBaseDatos.commit()

    messagebox.showinfo("Alerta", "Cliente anadido correctamente")

def contulta_r():
    rows = cur.execute('SELECT fecha, producto, total FROM registro;').fetchall()
    result = '\n'.join([f"Fecha: {row[0]}  Producto: {row[1]} Valor: {row[2]}" for row in rows])
    messagebox.showinfo("Consulta", result if result else "No data found!")

def consulta_c():
    rows = cur.execute('SELECT fecha, nombre, apellido, total FROM clientes;').fetchall()
    result = '\n'.join([f"Fecha: {row[0]}  Nombre: {row[1]} Apellido: {row[2]} Total: {row[3]}" for row in rows])
    messagebox.showinfo("Consulta", result if result else "No data found!")

def cerrar_d():
    conectaBaseDatos.close()
    messagebox.showinfo("Advertencia", "Base de datos cerrada correctamente")

def actualizar_c():
    conectaBaseDatos.execute('''
        UPDATE clientes
            SET total = ?
            WHERE nombre = ? ;
                ''', (dato10.get(), dato11.get()))
    
    # nombre = cur.execute('SELECT nombre, apellido FROM clientes').fetchall()
    messagebox.showinfo("Actilizacion", f"Cuenta de actializada")
    conectaBaseDatos.commit()

def borrar_c():
    conectaBaseDatos.execute('''


''')
    pass

boton_registrar = tk.Button(ventana, text="Registrar", command=input_b,)
boton_registrar.grid(row=3, column=3, padx=10, pady=10)


boton_registrar = tk.Button(ventana, text="Registrar cliente", command=input_c,)
boton_registrar.grid(row=9, column=3, padx=10, pady=10)

b_consulta = tk.Button (ventana, text="consulta", command= contulta_r)
b_consulta.grid(column=0, row= 3, padx= 10, pady=10)

c_consulta = tk.Button (ventana, text= "Consultar Clientes", command= consulta_c)
c_consulta.grid(column=0, row=9, padx=10, pady=10)

boton_c = tk.Button (ventana, text= "Aceptar", command = actualizar_c)
boton_c.grid (column= 1, row= 12, padx= 10, pady=10)

# Cerrar la base de datos al salir de la ventana
ventana.protocol("WM_DELETE_WINDOW", lambda: (cerrar_d(), ventana.destroy()))


ventana.mainloop()

