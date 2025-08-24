import flet as ft

def client(page: ft.Page):
    page.controls.clear()
    page.title = "New Client"

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    name_field = ft.TextField(label="First Name", width=200)
    nickname_field = ft.TextField(label="Nickname", width=200)
    product = ft.TextField (label= "product", width= 100)
    num = ft.TextField (label="precio", width= 100)

    page.add(name_field, nickname_field, product, num)


    from Code.controlador.menu import dash_board
    page.add(ft.ElevatedButton(text= "guardar"))
    page.add(ft.ElevatedButton (text = "Salir", on_click = lambda e: dash_board))