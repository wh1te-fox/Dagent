import flet as ft
import sqlite3
from flet import SnackBar

# lista de clientes
def search(page: ft.Page):

    from views.menu_interface import dash_board
    from views.components.model_textfield import InputModel
    from views.components.modelButton import Control_b, ButtonIcon
    from views.components.model_alignment import Column

    page.update()
    page.controls.clear()

    page.add (ft.Text("Clientes", 
        size=30, weight=ft.FontWeight.W_900, 
        selectable=True))
    
    def hi():
        print('hola')


    parameter_name = InputModel('nombre')
    execute_entry = parameter_name.entry_style()

    last_name = InputModel('apellido')
    execute_entry1 = last_name.entry_style()

    exit_button = Control_b("Salir", dash_board, page)
    execute_button = exit_button.view()
  
    element_column = Column(execute_entry, execute_entry1)
    execute_column = element_column.view_column()

    search_button = ButtonIcon(ft.Icons.SEARCH_OUTLINED, ft.Colors.GREEN_300, hi, "Buscar")
    add_search = search_button.model_icon()

    page.add(
    ft.Row(
        controls=[
            execute_column,
            add_search
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
)

print("search_client")