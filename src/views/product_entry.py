import flet as ft
import sqlite3


# Product Entry Page
def entry_product(page: ft.Page):

    from views.components.modelButton import Control_b
    from views.components.model_alignment import Column
    from views.menu_interface import dash_board
    page.controls.clear()

    save_button = Control_b("Guardar", data, page)
    exit_button = Control_b("Sailr", dash_board, page)


    # revisar 
    name = ft.TextField(label="Product Name", width=300, border_radius=10)
    product = ft.TextField(label=f"{e}", width=300, border_radius=10)



    buttons = Column(save_button, exit_button)
    tickets = buttons.view_column()
    
    page.add(tickets, buttons)
      #entradas






    '''
        page.add(
        save_button.view(),
        exit_button.view()
        )

    '''












    #from Code.SQL.insertar import data


    # en la pagina, de forma vertical
    page.vertical_alignment= ft.MainAxisAlignment.CENTER # alinearlo en el centro
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.controls.clear()
    page.title = "Register Product"

    e = "precio"

 



    entries = ft.Row (
        controls= [
            ft.Column ([name]),
            ft.Column([product])
        ], alignment=ft.MainAxisAlignment.CENTER # en las entradas, se posicionan en el centro
    )


    page.add( ft.Text("Agrega producto", size=30, 
        weight=ft.FontWeight.W_900),
        entries, buttons)
    page.update()

    def data():
        print("esperando funcion....")
ft.app(target=entry_product)

print("entrada.py")