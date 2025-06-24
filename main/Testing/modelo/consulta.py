import flet as ft
import sqlite3

# Placeholder for consultation page
def consult_sale(page: ft.Page):
    page.controls.clear()

    conn = sqlite3.connect("information.db")
    cur = conn.cursor()

    lis = cur.execute('''
    SELECT product, valor FROM sale''').fetchall()

    #page.add(*lis)
    conn.close()

    exit_btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))
    page.add(exit_btn)

    page.update()