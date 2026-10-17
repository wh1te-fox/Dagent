"""Client registration view module."""
import flet as ft


def customer_page(page: ft.Page):
    """Renders the client registration interface."""
    from views.components.button import Control_b
    from views.components import section
    from views.components.text_field import InputModel
    from views.menu_interface import dash_board
    from services.database import cliente_existe, guardar_cliente

    section.setup(page, "Registrar Clientes")

    name_input = InputModel("Nombre").entry_style()
    name_input.width = 350
    name_input.border_radius = 10
    name_input.prefix_icon = ft.Icons.PERSON

    last_name_input = InputModel("Apellido").entry_style()
    last_name_input.width = 350
    last_name_input.border_radius = 10
    last_name_input.prefix_icon = ft.Icons.PERSON_OUTLINE

    def validate_client(e):
        first_name = name_input.value.strip() if name_input.value else ""
        last_name = last_name_input.value.strip() if last_name_input.value else ""
        if not first_name and not last_name:
            message_text.value = ""
            page.update()
            return

        if first_name and last_name and cliente_existe(first_name, last_name):
            message_text.value = "El cliente ya existe en el sistema"
            message_text.color = "red"
        elif first_name or last_name:
            message_text.value = "Cliente disponible para registrar"
            message_text.color = "green"
        page.update()

    name_input.on_change = validate_client
    last_name_input.on_change = validate_client

    message_text = ft.Text("", size=16)

    def save_client_click(p):
        first_name = name_input.value.strip() if name_input.value else ""
        last_name = last_name_input.value.strip() if last_name_input.value else ""

        name_input.error_text = None
        last_name_input.error_text = None
        message_text.value = ""

        valid = True
        if not first_name:
            name_input.error_text = "El nombre es obligatorio"
            valid = False
        if not last_name:
            last_name_input.error_text = "El apellido es obligatorio"
            valid = False

        if not valid:
            message_text.value = "No se guardó el cliente"
            message_text.color = "red"
            page.update()
            return

        if cliente_existe(first_name, last_name):
            message_text.value = "El cliente ya existe en el sistema"
            message_text.color = "red"
            page.update()
            return

        try:
            guardar_cliente(first_name, last_name)
            message_text.value = "Cliente guardado correctamente"
            message_text.color = "green"
            name_input.value = ""
            last_name_input.value = ""
            page.update()
        except Exception as error:
            name_input.error_text = str(error)
            message_text.value = "No se guardó el cliente"
            message_text.color = "red"
            page.update()

    def cancel_click(p):
        dash_board(p)

    save_button = section.primary_button(
        Control_b("Guardar", save_client_click, page, icon=ft.Icons.SAVE).view()
    )
    cancel_button = section.secondary_button(
        Control_b("Cancelar", cancel_click, page, icon=ft.Icons.CANCEL).view()
    )

    header_row = section.header(ft.Icons.PERSON_ADD, "Registrar Clientes", "Da de alta clientes en el sistema")

    form_card = section.card(
        ft.Column([
            name_input,
            last_name_input,
            ft.Divider(),
            message_text
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=section.FORM_WIDTH
    )

    buttons_row = ft.Row(
        controls=[save_button, cancel_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        header_row,
        section.spacer(20),
        form_card,
        section.spacer(16),
        buttons_row
    )
    page.update()

