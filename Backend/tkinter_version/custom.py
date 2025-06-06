from argparse import _VersionAction
import sqlite3
from xml.dom import Node
import customtkinter
from CTKessagebox import CTkMessagebox
from setuptools import Command


root = customtkinter.CTk()
root.title("Dagent")
root.geometry("800x500")

input_v = customtkinter.CTkButton(root, text = "Ingresar venta", fg_color= "blue", command = lambda: (ventan()))
input_v.grid(column = 0, row = 1, padx = 10, pady = 10)

input_c = customtkinter.CTkButton(root, text = "Ingresar creditos", fg_color= "blue", command= lambda: (credito()))
input_c.grid(column = 1, row = 1, padx = 10, pady = 10)

act = customtkinter.CTkButton(root, text = "Actualizar cliente", fg_color= "blue", command= lambda : (abonar()))
act.grid(column = 2, row = 1, padx = 10, pady = 10)



# Funcionalidad de la base de datos
conectaBaseDatos = sqlite3.connect("data.db")
cur = conectaBaseDatos.cursor()

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

modo = ["ligth", "dark", "system"] # Modos: "light", "dark", "system"
tema = ["blue", "green", "dark-blue"] # Temas: "blue", "green", "dark-blue"

# Configuración de apariencia
customtkinter.set_appearance_mode(modo[1])  
customtkinter.set_default_color_theme(tema[1])  
 

# Ventana principal
def ventan():

    ventana = customtkinter.CTkToplevel(root)
  # Ajusta el tamaño de la ventana

# Etiquetas y entradas
    texto = customtkinter.CTkLabel(ventana, text="Registro de ventas", font=("Arial", 20))
    dato1 = customtkinter.CTkLabel(ventana, text="Fecha:")
    dato2 = customtkinter.CTkLabel(ventana, text="Producto:")
    dato3 = customtkinter.CTkLabel(ventana, text="Precio unitario:")
    dato4 = customtkinter.CTkLabel(ventana, text="Total:")

    entrada1 = customtkinter.CTkEntry(ventana)
    entrada2 = customtkinter.CTkEntry(ventana)
    entrada3 = customtkinter.CTkEntry(ventana)
    entrada4 = customtkinter.CTkEntry(ventana)

    dato1.grid(row=1, column=0, padx=10, pady=10)
    entrada1.grid(row=1, column=1, padx=10, pady=10)

    dato2.grid(row=1, column=2, padx=10, pady=10)
    entrada2.grid(row=1, column=3, padx=10, pady=10)

    dato3.grid(row=2, column=0, padx=10, pady=10)
    entrada3.grid(row=2, column=1, padx=10, pady=10)

    dato4.grid(row=2, column=2, padx=10, pady=10)
    entrada4.grid(row=2, column=3, padx=10, pady=10)

    def input_b():
        conectaBaseDatos.execute('''
        INSERT INTO registro (fecha, producto, precio_unitario, total)
        VALUES (?, ?, ?, ?)                     
        ''', (entrada1.get(), entrada2.get(), entrada3.get(), entrada4.get()))
        conectaBaseDatos.commit()
        CTkMessagebox(message="Agregado.",
                  icon="check", option_1="Aceptar")

    boton_registrar = customtkinter.CTkButton(ventana, text="Registrar", command=input_b, fg_color="blue")
    boton_registrar.grid(row=3, column=3, padx=10, pady=10)

    def consulta_r():
        rows = cur.execute("SELECT fecha, producto, total FROM registro;").fetchall()
        result = '\n'.join([f"Fecha: {row[0]}  Producto: {row[1]} Valor: {row[2]}" for row in rows]) # variable row alamcena resultado y in rows eslo que itera
# Mostrar mensaje basado en el contenido de result
        if result: # si tiene elementos
            CTkMessagebox(message=result, icon="check", option_1="Thanks")
        else: # si no 
            CTkMessagebox(message="No data found", icon="warning", option_1="OK")

    b_consulta = customtkinter.CTkButton(ventana, text="Consultar", command=consulta_r, fg_color="green")
    b_consulta.grid(column=0, row=3, padx=10, pady=10)

def credito():
    ventana = customtkinter.CTkToplevel(root)
    ventana.title("Credito")

    dato5 = customtkinter.CTkLabel(ventana, text="Fecha de crédito:")
    dato6 = customtkinter.CTkLabel(ventana, text="Nombre:")
    dato7 = customtkinter.CTkLabel(ventana, text="Apellido:")
    dato8 = customtkinter.CTkLabel(ventana, text="Productos:")
    dato9 = customtkinter.CTkLabel(ventana, text="Total:")

    entrada5 = customtkinter.CTkEntry(ventana)
    entrada6 = customtkinter.CTkEntry(ventana)
    entrada7 = customtkinter.CTkEntry(ventana)
    entrada8 = customtkinter.CTkEntry(ventana)
    entrada9 = customtkinter.CTkEntry(ventana)

    dato5.grid(row=4, column=0, padx=10, pady=10)
    entrada5.grid(row=4, column=1, padx=10, pady=10)

    dato6.grid(row=5, column=0, padx=10, pady=10)
    entrada6.grid(row=5, column=1, padx=10, pady=10)

    dato7.grid(row=5, column=2, padx=10, pady=10)
    entrada7.grid(row=5, column=3, padx=10, pady=10)

    dato8.grid(row=8, column=0, padx=10, pady=10)
    entrada8.grid(row=8, column=1, padx=10, pady=10)

    dato9.grid(row=8, column=2, padx=10, pady=10)
    entrada9.grid(row=8, column=3, padx=10, pady=10)

    if entrada5 and entrada6 and entrada7 and entrada8 and entrada9 is Node:
        CTkMessagebox(message="Hay un valor nulo, verifique las entradas", icon="warning", option_1="verificar")
    else:
        def input_c():
            conectaBaseDatos.execute('''
    INSERT INTO clientes (fecha, nombre, apellido, producto, total)
    VALUES (?, ?, ?, ?, ?)
    ''', (entrada5.get(), entrada6.get(), entrada7.get(), entrada8.get(), entrada9.get()))
            CTkMessagebox(message="Cliente añadido correctamente", icon="check", option_1="Finalizar")
            conectaBaseDatos.commit()
    

    boton_registrar_cliente = customtkinter.CTkButton(ventana, text="Registrar Cliente", command=input_c, fg_color="blue")
    boton_registrar_cliente.grid(row=9, column=3, padx=10, pady=10)
    
   

    

def abonar():

    ventana = customtkinter.CTkToplevel(root)
    ventana.title("abonar")
    mensaje = customtkinter.CTkLabel (ventana, text="Total")
    dato10 = customtkinter.CTkEntry (ventana)

    mensaje2 = customtkinter.CTkLabel (ventana, text= "Nombre del cliente:")
    dato11 = customtkinter.CTkEntry (ventana)

    mensaje.grid (row = 0, column=0, padx= 10, pady= 10)
    dato10.grid (row= 0, column= 1, padx= 10, pady= 10)

    mensaje2.grid ( row= 1, column= 0, padx= 10, pady=10)
    dato11.grid (row= 1, column=1, padx= 10, pady= 10)

    conectaBaseDatos.commit()
    boton_c = customtkinter.CTkButton (ventana, text= "Aceptar", command = lambda: (actualizar_c()), fg_color="blue")
    boton_c.grid (column= 1, row= 2, padx= 10, pady=10)

    def actualizar_c():
        conectaBaseDatos.execute('''
        UPDATE clientes
            SET total = ?
            WHERE nombre = ? ;
                ''', (dato10.get(), dato11.get()))
         # nombre = cur.execute('SELECT nombre, apellido FROM clientes').fetchall()
        CTkMessagebox(message="Cuenta Actilizada",
                  icon="check", option_1="Thanks")
        

    def consulta_c():
        # Ejecutar la consulta y obtener los resultados
        rows = cur.execute('SELECT fecha, nombre, apellido, total FROM clientes;').fetchall()
    
    # Construir el resultado en un formato legible
        result = '\n'.join([f"Fecha: {row[0]}  Nombre: {row[1]} Apellido: {row[2]} Total: {row[3]}" for row in rows])
    
    # Mostrar mensaje basado en el contenido de result
        if result:
                CTkMessagebox(message=result, icon="check", option_1="Thanks")
        else:
                CTkMessagebox(message="No data found", icon="warning", option_1="OK")
    c_consulta = customtkinter.CTkButton(ventana, text="Consultar Clientes", command= lambda : (consulta_c()), fg_color="blue")
    c_consulta.grid(column=0, row=2, padx=10, pady=10)
        


def cerrar_d():
    conectaBaseDatos.close()
    # Función para mostrar un cuadro de diálogo personalizado

    # Crear un nuevo CTkToplevel como cuadro de confirmación
    confirmacion = customtkinter.CTkToplevel()
    confirmacion.geometry("300x150")
    confirmacion.title("Advertencia")
    # Etiqueta para el mensaje
    etiqueta = customtkinter.CTkLabel(confirmacion, text="¿Estás seguro de que deseas cerrar?", font=("Arial", 14),)
    etiqueta.pack(pady=10)

    # Botón para confirmar
    boton_si = customtkinter.CTkButton(confirmacion, fg_color= "blue", text="Sí", command=lambda: (cerrar_d(), root.destroy()))
    boton_si.pack(side="left", padx=10, pady=10)

    # Botón para cancelar
    boton_no = customtkinter.CTkButton(confirmacion, fg_color= "blue", text="No", command=confirmacion.destroy)
    boton_no.pack(side="right", padx=10, pady=10)


    

    
   
    
def borrar_c():
    pass

# Cerrar la ventana y la base de datos

root.protocol("WM_DELETE_WINDOW", cerrar_d)

root.mainloop()
