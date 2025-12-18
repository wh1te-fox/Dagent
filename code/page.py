import flet as ft 

# Ventana normal
def controll(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add (ft.Text ("depuracion lista"))

    from views.menu import dash_board
    from views.components.modelButton import Control_b

    use_class = Control_b("Cambiar vista", dash_board, page)
    page.add(use_class.view())
    page.update()
    
if __name__ == "__main__": # solo ejecutara si estas en page.py
    ft.app(target=controll)
    