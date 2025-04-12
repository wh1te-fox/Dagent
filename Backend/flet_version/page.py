from pydoc import text
import flet as ft
import sqlite3

# Start Data Base (SQLite)
def create_table():
    conexion = sqlite3.connect('information.db')
    cur = conexion.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS inputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        product TEXT NOT NULL,
        valor REAL NOT NULL,
        
    )
        ''')
    cur.commit()
    cur.close()


def main(page: ft.Page):
    
    #page.title("Dagent")
    page.controls.clear()
    b =ft.ElevatedButton(text="data", on_click= lambda _: entry_product(main))
    page.add(b)
    page.controls.clear() 
    
def welcome(page: ft.Page):

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(ft.Text(
        "Bienvenido a Dagent\n "
        "Solución Digital para negocios\n"
        "Registra tus ingresos de manera fácil y sencilla\n",
        text_align=ft.TextAlign.CENTER
    ))

    page.add(
        ft.ElevatedButton(
            text="Comenzar",
            on_click=lambda _: main(page)  # Mostrar los campos de entrada
        )
    )
    
def entry_product (page: ft.Page):
    #page.title("Input")
    #page.geometry("300x400")


    date = ft.TextField (label ="Entry Date", width=100)
    product = ft.TextField (label = "Product", width=100)
    unit = 1 
    content = date, product, unit

    g_buttom = ft.ElevatedButton (text= "Save", on_click= lambda _: save_i())
    
    def save_i(date, product, unit ):
        try:
            conexion = sqlite3.connect("infomation.db")
            cur = conexion.cursor()
            cur.execute(''' INSERT INTO inputs (date, product, valor) VALUES (?,?,?)
                    ''', (date.value, product.value, int(unit)))
            cur.commit()
            cur.clore()
            print("completed!")
            
        except Exception as e:
            print ("error")

    page.add = (
        [
            content, g_buttom
        ]
    )


ft.app(target=main)