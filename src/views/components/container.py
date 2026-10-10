"""Container component module."""
import flet as ft


class ContainerComponent:
    """Encapsulates reusable container configurations."""

    @staticmethod
    def create_container(content, width=300, padding=20):
        return ft.Container(
            bgcolor=ft.Colors.SURFACE_TINT,
            padding=padding,
            width=width,
            content=content,
        )
