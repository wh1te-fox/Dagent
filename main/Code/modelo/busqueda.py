import flet as ft
import sqlite3
from flet import SnackBar

# lista de clientes
def search(page: ft.Page):

    from Code.controlador.menu import dash_board

    page.update()
    page.controls.clear()
    
    name = ft.TextField(label="first name", width = 150, border_radius=10)
    last = ft.TextField(label="last name", width = 150, border_radius=10)
    exi = ft.ElevatedButton(text="Exit", on_click= lambda e: dash_board(page))
  


    search_e = ft.Row(
        controls=[
            ft.Column(
                [
                    ft.IconButton(
                        icon=ft.Icons.SEARCH_OUTLINED,
                        icon_color = ft.Colors.GREEN_300,
                        on_click= lambda _: s(),
                        tooltip="search"
                    )
                ]
            )
        ],
    )
    search_setting = ft.Row(
        controls=[
            ft.Column([name]),
            ft.Column([last]),
            ft.Column([search_e])

            ],
            spacing= 50,
            alignment=ft.MainAxisAlignment.CENTER
        )
    buttons = ft.Row (
        controls= [
            ft.Column([exi])
        ], alignment= ft.MainAxisAlignment.CENTER
    )
    
    page.add (ft.Text("Clientes", 
        size=30, weight=ft.FontWeight.W_900, 
        selectable=True), 
        search_setting, buttons)

    #page.add(*product_list)
             
             #,exit_btn)

    def s():
        print("esperando...")

        page.controls.clear()
    
    
    page.update()

print("busqueda.py")