import flet as ft

def dash_board(page: ft.Page):
    from views.components.model_navrail import NavigationBar
    from page import main as perfil
    from views.search_client import search
    from views.ui_settings import dark_mode
    from views.add_product import main
    from views.add_client import customer_page
    from views.page_sale import input_sale
    from views.FrmReporte import list_report
    from services.database import crear_bd
    

    page.title = "Dagent"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()
    crear_bd()

    def on_change(e):
        index = e.control.selected_index
        print(f"Destino seleccionado: {index}")

        page.controls.clear()
        page.update()

        execute_function = {
            0:perfil,
            1:input_sale,
            2:main,
            3:customer_page,
            4:search,
            5:list_report,
            6:dark_mode,
        } # refactorizar el orden de seleccion

        func = execute_function.get(index)
        if func:
            func(page)
        else:
            print(f"No hay función asignada para index {index}")

    nav = NavigationBar(on_changes=on_change)
    page.add(nav.build())