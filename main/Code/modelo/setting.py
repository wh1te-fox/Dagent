import flet as ft

from Code.controlador.menu import dash_board
    

# Settings Page
def sett(page: ft.Page):

    page.controls.clear()
    page.add(ft.Text("Configuraciones", width=300, height=60))
    page.title = "Settings"

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()    

    page.theme_mode = ft.ThemeMode.LIGHT

    theme_swith = ft.Switch(
        label="Cambia al modo oscuro", 
        label_position=ft.LabelPosition.LEFT, 
        on_change=theme_changed
        )

    btn = ft.ElevatedButton(text="Exit", on_click=lambda _: dash_board(page))
    page.add(theme_swith, btn)
    page.update()