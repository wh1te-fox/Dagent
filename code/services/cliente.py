import flet as ft
import sqlite3

def client(page: ft.Page):

    from Code.controlador.menu import dash_board

    page.controls.clear()
    page.title = "New Client"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    name = ft.TextField(label="First Name", width=200)
    last = ft.TextField(label="last name", width=200)
    product = ft.TextField (label= "product", width= 100)
    product = ft.Dropdown (label="producto", width=200)

    exi = ft.Button(text="Exit", on_click= lambda e: dash_board(page))
    save = ft.ElevatedButton(text= "guardar", on_click= lambda e: data, )
                             #bgcolor=ft.colors.GREEN_400, color=ft.colors.WHITE)
    
    campos = ft.Row (
        controls= [
            ft.Column ([name]),
            ft.Column ([last]),
            ft.Column ([product]),

        ], alignment= ft.MainAxisAlignment.CENTER, spacing= 100
    )

    botton = ft.Row (
        controls= [
            ft.Column ([exi]),
            ft.Column([save])
        ], alignment= ft.MainAxisAlignment.CENTER, spacing = 300
    )

    page.add( ft.Text ("Agregar clientes Nuevos", size=30, 
        weight=ft.FontWeight.W_900),
        campos, botton)
print("cliente.py")