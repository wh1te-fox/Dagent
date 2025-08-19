import flet as ft

from Testing.controlador.menu import dash_board
    

# Settings Page
def sett(page: ft.Page):
    page.controls.clear()
    page.add(ft.Text("Configuraciones", width=300, height=60))
    page.title = "Settings"


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
    '''c2 = ft.Switch(
        label= "sistema de credito\n" \
        "puedes activar o descativar para tener un sistem de creditos"
        label_position= ft.LabelPosition=LEFT,
        on_change=
    )'''


    btn = ft.ElevatedButton(text="Exit", on_click=lambda _: dash_board(page))
    page.add(theme_swith, btn)
    page.update()