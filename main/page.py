import flet as ft 

# Ventana normal
def controll(page: ft.Page):
    page.add (ft.Text ("depuracion lista"))

    from Testing.controlador.menu import dash_board

    page.controls.append(ft.ElevatedButton("Cambiar vista", on_click=lambda e: dash_board(page)))
    page.update()
    
if __name__ == "__main__": # solo ejecutara si estas en page.py
    ft.app(target=controll)