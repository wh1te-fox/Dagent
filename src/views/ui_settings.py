"""Settings view module for application configuration."""
import flet as ft

from services.auth import active_session
from views.components import section


def _open_change_password(page):
    """Opens the change-password section (only when the app shell is mounted)."""
    layout = getattr(page, "_app_layout", None)
    if layout is not None:
        layout.open_section("password")


def dark_mode(page: ft.Page):
    """Renders the settings view for theme configuration and appearance."""
    section.setup(page, "Configuración")

    active_user = active_session(page)

    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()

    theme_switch = ft.Switch(
        label_position=ft.LabelPosition.LEFT,
        on_change=theme_changed
    )

    settings_card = section.card(
        ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PALETTE_OUTLINED, size=24, color=section.ACCENT),
                ft.Text("Apariencia y Tema", size=18, weight=ft.FontWeight.BOLD)
            ], spacing=10),
            ft.Divider(),
            ft.Row([
                ft.Text("Cambiar entre modo claro y oscuro", size=14),
                theme_switch
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=15),
        width=section.FORM_WIDTH
    )

    header_row = section.header(
        ft.Icons.SETTINGS,
        "Configuración",
        "Personaliza el comportamiento y aspecto de la aplicación"
    )

    user_chip = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.PERSON, size=16, color=section.ACCENT),
            ft.Text(
                active_user if active_user else "Sin sesión activa",
                size=12,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.GREY_700,
            ),
        ], spacing=6, tight=True),
        padding=ft.Padding.symmetric(vertical=6, horizontal=12),
        border_radius=20,
        bgcolor=ft.Colors.with_opacity(0.06, section.ACCENT),
    )

    change_button = section.primary_button(
        ft.Button(
            content=ft.Row(
                [ft.Icon(ft.Icons.PASSWORD, size=18), ft.Text("Cambiar")],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5,
            ),
            on_click=lambda _: _open_change_password(page),
            width=150,
        )
    )

    password_card = section.card(
        ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PASSWORD, size=24, color=section.ACCENT),
                ft.Text("Contraseña", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                user_chip,
            ], spacing=10),
            ft.Row([
                ft.Text(
                    "Necesitarás tu contraseña actual para confirmar el cambio.",
                    size=12,
                    color=ft.Colors.GREY_600,
                    expand=True,
                ),
                change_button,
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ], spacing=12),
        padding=20,
        width=section.FORM_WIDTH
    )

    page.add(
        header_row,
        section.spacer(20),
        settings_card,
        section.spacer(16),
        password_card,
    )
    page.update()
