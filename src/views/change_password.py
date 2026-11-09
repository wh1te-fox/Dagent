"""Change-password view module: dedicated screen for updating the password."""
import flet as ft

from services.auth import active_session, change_password
from views.components import section


def _go_back(page):
    """Returns to the settings section (only when the app shell is mounted)."""
    layout = getattr(page, "_app_layout", None)
    if layout is not None:
        layout.open_section("settings")


def show(page: ft.Page):
    """Renders the change-password screen inside the application layout."""
    section.setup(page, "Cambiar contraseña")

    active_user = active_session(page)

    header_row = section.header(
        ft.Icons.PASSWORD,
        "Cambiar contraseña",
        "Actualiza la contraseña de tu cuenta",
    )

    current_field = ft.TextField(
        label="Contraseña actual",
        password=True,
        can_reveal_password=True,
        width=340,
        border_radius=10,
    )
    new_field = ft.TextField(
        label="Nueva contraseña",
        password=True,
        can_reveal_password=True,
        width=340,
        border_radius=10,
    )
    confirm_field = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=340,
        border_radius=10,
    )
    result_label = ft.Text("", size=13)

    def save_password(e):
        new_field.error_text = None
        confirm_field.error_text = None
        result_label.value = ""
        page.update()

        if len(new_field.value or "") < 6:
            new_field.error_text = "Debe tener al menos 6 caracteres"
            page.update()
            return
        if new_field.value != confirm_field.value:
            confirm_field.error_text = "Las contraseñas no coinciden"
            page.update()
            return

        success, message = change_password(
            page, current_field.value or "", new_field.value or ""
        )
        if success:
            current_field.value = ""
            new_field.value = ""
            confirm_field.value = ""

        result_label.value = message
        result_label.color = (
            ft.Colors.GREEN_600 if success else ft.Colors.RED_400
        )
        page.update()

    save_button = section.primary_button(
        ft.Button(
            content=ft.Text("Actualizar contraseña"),
            on_click=save_password,
            width=340,
        )
    )

    back_button = section.secondary_button(
        ft.Button(
            content=ft.Row(
                [ft.Icon(ft.Icons.ARROW_BACK, size=18), ft.Text("Volver a configuración")],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5,
            ),
            on_click=lambda _: _go_back(page),
            width=220,
        )
    )

    password_card = section.card(
        ft.Column(
            [
                ft.Text(
                    f"Sesión activa: {active_user}" if active_user else "Sin sesión activa",
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(),
                current_field,
                new_field,
                confirm_field,
                result_label,
                section.buttons_row([save_button]),
            ],
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=section.FORM_WIDTH,
    )

    page.add(
        header_row,
        section.spacer(20),
        password_card,
        section.spacer(16),
        section.buttons_row([back_button]),
    )
    page.update()


if __name__ == "__main__":
    ft.run(show)
