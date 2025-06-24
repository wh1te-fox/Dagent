import flet as ft
import sqlite3

# lista de clientes
def search(page: ft.Page):

    #from controlador.busqueda_c import search_c
    #from Testing.controlador.menu import main

    page.controls.clear()
    page.update()

    entry_name = ft.TextField(label="name client", width = 150, border_radius=10)
    entry_nick = ft.TextField(label="nickname client", width = 150, border_radius=10)

    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    #cur.execute("SELECT name, lastname, date FROM customer")
    products = cur.fetchall()
    conn.close()

    product_list = [
        ft.Text(f"{prod[0]} - {prod[1]} : {prod[2]}") for prod in products
    ]

    #exit_btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))

    search_e = ft.Row(
        controls=[
            ft.Column(
                [
                    ft.IconButton(
                        icon=ft.Icons.SEARCH_OUTLINED,
                        icon_color = ft.Colors.GREEN_300,
                        on_click= lambda _: print("esperando funcion"),
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

    #page.add(*product_list, exit_btn)
    
    
    page.update()

ft.app(target=search)