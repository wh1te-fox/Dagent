import flet as ft 

# Ventana normal
def main(page: ft.Page):
    page.title = "Dagent - Bienvenido"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.controls.clear()

    from views.components.modelButton import Control_b
    from views.menu_interface import dash_board

    logo_image = ft.Image(
        src="assets/logo.png",
        width=120,
        height=120,
        fit=ft.ImageFit.CONTAIN
    )

    welcome_text = ft.Text(
        "Te damos la bienvenida",
        size=28,
        weight=ft.FontWeight.W_900,
        text_align=ft.TextAlign.CENTER
    )

    subtitle_text = ft.Text(
        "Sistema de Gestión de Ventas, Productos y Clientes",
        size=14,
        color=ft.Colors.GREY_700,
        text_align=ft.TextAlign.CENTER
    )

    use_class = Control_b("Ingresar al Sistema", dash_board, page)
    enter_button = use_class.view()

    welcome_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                logo_image,
                welcome_text,
                subtitle_text,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                enter_button
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=35,
            width=420
        )
    )

    page.add(welcome_card)
    page.update()
    
if __name__ == "__main__": # solo ejecutara si estas en page.py
    ft.run(main)
    