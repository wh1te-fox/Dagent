import flet as ft
from views.menu_interface import dash_board
    

# Settings Page
def dark_mode(page: ft.Page):

    page.controls.clear()
    page.title = "Configuraciones"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()    

    #page.theme_mode = ft.ThemeMode.DARK

    theme_swith = ft.Switch( 
        label_position=ft.LabelPosition.LEFT, 
        on_change=theme_changed
        )

    settings_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PALETTE_OUTLINED, size=24, color=ft.Colors.BLUE_400),
                    ft.Text("Apariencia y Tema", size=18, weight=ft.FontWeight.BOLD)
                ], spacing=10),
                ft.Divider(),
                ft.Row([
                    ft.Text("Cambiar entre modo claro y oscuro", size=14),
                    theme_swith
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], spacing=15),
            padding=25,
            width=450
        )
    )

    btn = ft.Button(
        content=ft.Row([ft.Icon(ft.Icons.ARROW_BACK, size=18), ft.Text("Volver")], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        on_click=lambda _: dash_board(page),
        width=160,
        height=45
    )

    header_row = ft.Row([
        ft.Text("Configuraciones", size=30, weight=ft.FontWeight.W_900, selectable=True)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    page.add(
        header_row,
        ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
        settings_card,
        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
        btn
    )
    page.update()