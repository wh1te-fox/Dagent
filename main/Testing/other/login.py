import flet as ft

def main(page: ft.Page):
    page.title = "Inicio de Sesión"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 300

    # Credenciales de ejemplo (puedes reemplazarlas con una base de datos, etc.)
    USUARIO_CORRECTO = "admin"
    CONTRASENA_CORRECTA = "12345"

    txt_username = ft.TextField(
        label="Nombre de usuario",
        width=250,
        border_radius=10
    )
    txt_password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=250,
        border_radius=10
    )
    txt_message = ft.Text(
        value="",
        color=ft.colors.RED_500,
        size=14
    )

    def on_login_click(e):
        username = txt_username.value
        password = txt_password.value

        if username == USUARIO_CORRECTO and password == CONTRASENA_CORRECTA:
            txt_message.value = "¡Inicio de sesión exitoso!"
            txt_message.color = ft.colors.GREEN_500
            # Aquí podrías redirigir a otra página o cargar el contenido principal de la app
        else:
            txt_message.value = "Nombre de usuario o contraseña incorrectos."
            txt_message.color = ft.colors.RED_500
        page.update()

    btn_login = ft.ElevatedButton(
        text="Iniciar Sesión",
        on_click=on_login_click,
        width=250,
        height=40
    )

    page.add(
        ft.Column(
            [
                ft.Text("Bienvenido", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                txt_username,
                txt_password,
                btn_login,
                txt_message,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15
        )
    )

if __name__ == "__main__":
    ft.app(target=main)