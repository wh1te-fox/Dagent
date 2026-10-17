"""Placeholder view for sections that have no real implementation yet."""
import flet as ft
from views.components import section


def pending_section(page, title, description=None):
    """Renders a clearly marked 'pending' placeholder for a module under construction."""
    section.setup(page, title)

    message = description or (
        "Esta sección aún no cuenta con una implementación real. "
        "Se habilitará cuando el módulo esté disponible."
    )

    placeholder = section.card(
        ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.CONSTRUCTION_OUTLINED, size=40, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.AMBER_600,
                    border_radius=50,
                    padding=16,
                ),
                ft.Row(
                    [
                        ft.Text(title, size=22, weight=ft.FontWeight.W_900),
                        ft.Container(
                            content=ft.Text(
                                "PENDIENTE",
                                size=11,
                                weight=ft.FontWeight.W_700,
                                color=ft.Colors.WHITE,
                            ),
                            bgcolor=ft.Colors.AMBER_600,
                            border_radius=20,
                            padding=ft.Padding.symmetric(vertical=3, horizontal=10),
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(
                    message,
                    size=14,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=460,
    )

    page.add(placeholder)
    page.update()
