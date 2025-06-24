import flet as ft
import sqlite3

from Testing.controlador.update_client import actualizar

def search_c(entry_name, entry_nick):


    def d(page: ft.Page):
        page.add(controls)


    conn = sqlite3.connect("information.db")
    cur = conn.cursor()

    cont = cur.execute('''
    SELECT name, lastname FROM customer WHERE name=? AND nickname=?''',
    (entry_name.value, entry_nick.value)).fetchall()

    conn.close()

    if cont:
        d()
        """controls = ft.Row(
                controls=[
                    ft.Column([
                        page.add( ft.Text(cont))]),

                    ft.Column([
                        page.add(ft.Button(text="editar", on_click= lambda _: test()))]
                    )
                ],
                alignment= ft.MainAxisAlignment.CENTER
        ) """


        b = ft.Button(text="editar", on_click= lambda _: actualizar(entry_name, entry_nick))
        a = ft.Text(cont)

        controls = ft.Row(
            controls=[
                ft.Column([a]),
                ft.Column([b])
            ], alignment= ft.MainAxisAlignment.CENTER, spacing= 100
        )




        
    else:
        print("intenta de nuevo")