import flet as ft

def ventana(page: ft.Page):
    page.title = "ventana"
    # page.add (ft.Text("Registro de ventas"), size = 40) # Malo
    page.add (ft.Text("Registro de ventas", size = 40))
    page.add (ft.TextField(label="Producto"))
    page.add (ft.TextField(label="Precio"))
    page.add (ft.ElevatedButton("Aceptar"))

ft.app(target=ventana)