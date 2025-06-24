import flet as ft

# Settings Page
def sett(page: ft.Page):
    page.controls.clear()
    page.title = "Settings"


    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()    
    # def app():
    
    from Testing.controlador.menu import main

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


    
    btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))
    page.add(theme_swith, btn)
    page.update()

#ft.app(target=sett)