import flet as ft
import sqlite3


# Product Entry Page
def entry_product(page: ft.Page):
    page.controls.clear()
    from Code.controlador.menu import dash_board


    # en la pagina, de forma vertical
    page.vertical_alignment= ft.MainAxisAlignment.CENTER # alinearlo en el centro
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.controls.clear()
    page.title = "Register Product"

    name = ft.TextField(label="Product Name", width=300, border_radius=10)
    product = ft.TextField(label="Price", width=300, border_radius=10)

    save = ft.ElevatedButton(text="Save", on_click=lambda _: save_product())
    exi = ft.ElevatedButton(text="Exit", on_click=lambda _: dash_board(page))

    entries = ft.Row (
        controls= [
            ft.Column ([name]),
            ft.Column([product])
        ], alignment=ft.MainAxisAlignment.CENTER # en las entradas, se posicionan en el centro
    )

    buttons = ft.Row (
        controls= [
            ft.Column ([save]),
            ft.Column ([exi])
        ],  alignment=ft.MainAxisAlignment.CENTER,
    )
    page.add( ft.Text("Agrega producto", size=30, 
        weight=ft.FontWeight.W_900),
        entries, buttons)
    page.update()

    def data():
        print("esperando funcion....")
    

print("entrada.py")