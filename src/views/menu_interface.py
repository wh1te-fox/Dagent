import flet as ft

def dash_board(page: ft.Page):
    from views.components.model_navrail import NavigationBar
    from views.search_client import search
    from views.ui_settings import dark_mode


    page.title = "Dagent"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()

    def on_change(e):
        index = e.control.selected_index
        print(f"Destino seleccionado: {index}")

        execute_function = {
            0:search,
            4:dark_mode
        }

        execute_function.get(index)(page)

    nav = NavigationBar(on_changes=on_change)
    page.add(nav.build())