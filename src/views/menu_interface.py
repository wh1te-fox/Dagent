"""Dashboard module providing main application navigation."""
import flet as ft


def dash_board(page: ft.Page):
    """Renders the dashboard interface with navigation rail and dynamic view loading."""
    from services.database import crear_bd
    from page import main as profile_view
    from views.add_client import customer_page
    from views.add_product import main as add_product_view
    from views.report_view import list_report
    from views.page_sale import input_sale
    from views.search_client import search as search_client_view
    from views.components.navigation_rail import NavigationBar
    from views.ui_settings import dark_mode

    page.title = "Dagent"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()
    crear_bd()

    def on_change(e):
        index = e.control.selected_index
        print(f"Selected destination: {index}")

        page.controls.clear()
        page.update()

        execute_function = {
            0: profile_view,
            1: input_sale,
            2: add_product_view,
            3: customer_page,
            4: search_client_view,
            5: list_report,
            6: dark_mode,
        }

        func = execute_function.get(index)
        if func:
            func(page)
        else:
            print(f"No function assigned for index {index}")

    nav = NavigationBar(on_change=on_change)
    page.add(nav.build())
