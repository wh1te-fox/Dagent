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

    page.add (ft.Text("solo falta la funcion"))


    page.add(name_field, nickname_field, product, num)

    page.add(ft.ElevatedButton(text= "guardar"))