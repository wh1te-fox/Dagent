"""Login view module: entry point with username and password validation."""
import flet as ft

from views.components import section


def login(page: ft.Page):
    """Renders the login screen and routes to the dashboard on success."""
    from services.auth import active_session, authenticate, initialize_users
    from views.menu_interface import dash_board

    if active_session(page):
        dash_board(page)
        return

    first_run = initialize_users()

    page.title = "Dagent - Iniciar sesión"
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

    username_field = ft.TextField(
        label="Nombre de usuario",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        width=340,
        border_radius=10,
        autofocus=True,
        on_submit=lambda _: submit(),
    )

    password_field = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        width=340,
        border_radius=10,
        password=True,
        can_reveal_password=True,
        on_submit=lambda _: submit(),
    )

    error_label = ft.Text(
        "",
        size=13,
        color=ft.Colors.RED_400,
        expand=True,
    )

    error_banner = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=20, color=ft.Colors.RED_400),
            error_label,
        ], spacing=10),
        width=340,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.RED_400),
        border_radius=10,
        padding=12,
        visible=False,
    )

    submit_button = section.primary_button(
        ft.Button(
            content=ft.Text("Iniciar sesión"),
            on_click=lambda _: submit(),
            width=340,
        )
    )

    def validate_fields():
        """Validates required fields and the minimum password length."""
        username_field.error_text = None
        password_field.error_text = None
        valid = True

        username = (username_field.value or "").strip()
        password = password_field.value or ""

        if not username:
            username_field.error_text = "Ingresa tu nombre de usuario"
            valid = False
        elif len(username) < 3:
            username_field.error_text = "Debe tener al menos 3 caracteres"
            valid = False

        if not password:
            password_field.error_text = "Ingresa tu contraseña"
            valid = False
        elif len(password) < 6:
            password_field.error_text = "Debe tener al menos 6 caracteres"
            valid = False

        return valid

    def set_sending():
        error_banner.visible = False
        submit_button.disabled = True
        submit_button.content = ft.Row([
            ft.ProgressRing(width=18, height=18, stroke_width=2.5),
            ft.Text("Verificando credenciales..."),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        username_field.disabled = True
        password_field.disabled = True
        page.update()

    def reset_sending():
        submit_button.disabled = False
        submit_button.content = ft.Text("Iniciar sesión")
        username_field.disabled = False
        password_field.disabled = False

    def submit(e=None):
        if not validate_fields():
            page.update()
            return

        set_sending()

        username = (username_field.value or "").strip()
        password = password_field.value or ""
        success, message = authenticate(page, username, password)

        reset_sending()

        if success:
            dash_board(page)
            return

        error_label.value = message
        error_banner.visible = True
        page.update()

    content_column = ft.Column(
        [
            logo_image,
            ft.Text("Iniciar sesión", size=24, weight=ft.FontWeight.W_900),
            ft.Text(
                "Ingresa tus credenciales para continuar",
                size=13,
                color=ft.Colors.GREY_600
            ),
            ft.Divider(height=12, color=ft.Colors.TRANSPARENT),
            username_field,
            password_field,
            error_banner,
            submit_button,
        ],
        spacing=14,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    login_card = section.card(content_column, width=420, padding=32)

    controls_list = [login_card]
    if first_run:
        controls_list.insert(0, ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=section.ACCENT),
                ft.Text(
                    "Primer inicio - Usuario: admin. Contraseña: admin123",
                    size=12,
                    color=ft.Colors.GREY_700,
                ),
            ], spacing=8),
            width=420,
            bgcolor=ft.Colors.with_opacity(0.08, section.ACCENT),
            border_radius=10,
            padding=12,
            margin=ft.Margin.only(bottom=16),
        ))

    page.add(*controls_list)
    page.update()


if __name__ == "__main__":
    ft.run(login)
