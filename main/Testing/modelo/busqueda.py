import flet as ft
import sqlite3
from flet import SnackBar

# lista de clientes
def search(page: ft.Page):

    #from controlador.busqueda_c import search_c
    #from Testing.controlador.menu import main
    page.update()
    page.controls.clear()

    entry_name = ft.TextField(label="name client", width = 150, border_radius=10)
    entry_nick = ft.TextField(label="nickname client", width = 150, border_radius=10)

  


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
            ft.Column([entry_name]),
            ft.Column([entry_nick]),
            ft.Column([search_e])

            ],
            spacing= 50,
            alignment=ft.MainAxisAlignment.CENTER
        )
    
    page.add (ft.Text("Clientes", size=30, weight=ft.FontWeight.W_900, selectable=True), search_setting)

    #page.add(*product_list)
             
             #,exit_btn)

    def s():
        print("esperando...")

        page.controls.clear()
    
    
    page.update()
