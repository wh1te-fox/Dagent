"""Main application entry point module."""
import flet as ft

from views.components import section


def main(page: ft.Page):
    """Renders the home/welcome view with the same aesthetics as login."""
    from views.components.button import Control_b
    from views.login_view import login

    page.title = "Dagent - Bienvenido"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.controls.clear()

    logo_image = ft.Image(
        src="assets/logo.png",
        width=110,
        height=110,
        fit="contain"
    )

    welcome_text = ft.Text(
        "Te damos la bienvenida",
        size=24,
        weight=ft.FontWeight.W_900,
        text_align=ft.TextAlign.CENTER
    )

    subtitle_text = ft.Text(
        "Sistema de Gestión de Ventas, Productos y Clientes",
        size=13,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER
    )

    enter_button = Control_b("Ingresar al Sistema", login, page).view()
    section.primary_button(enter_button)

    welcome_card = section.card(
        ft.Column(
            [
                logo_image,
                welcome_text,
                subtitle_text,
                ft.Divider(height=12, color=ft.Colors.TRANSPARENT),
                enter_button,
            ],
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=420,
        padding=32,
    )

    page.add(welcome_card)
    page.update()

if __name__ == "__main__":
    ft.run(main)
