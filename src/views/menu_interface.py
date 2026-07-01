import flet as ft

def dash_board(page: ft.Page):
    from views.components.model_navrail import NavigationBar
    from views.search_client import search
    from views.ui_settings import dark_mode
    from views.add_product import main
    from views.add_client import customer_page
    

    page.title = "Dagent"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()

    def on_change(e):
        index = e.control.selected_index
        print(f"Destino seleccionado: {index}")

        page.controls.clear()
        page.update()

        execute_function = {
            1:main,
            2:customer_page,
            3:search,
            4:dark_mode
        }

        func = execute_function.get(index)
        if func:
            func(page)
        else:
            print(f"No hay función asignada para index {index}")


    nav = NavigationBar(on_changes=on_change)
    page.add(nav.build())