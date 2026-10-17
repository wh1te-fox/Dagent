"""Credit registration view module."""
import flet as ft


def credit_page(page: ft.Page):
    """Renders the credit registration interface."""
    from views.components.button import Control_b
    from views.components import section
    from views.components.text_field import InputModel
    from views.menu_interface import dash_board
    from services.database import obtener_clientes, guardar_credito

    section.setup(page, "Registrar Crédito")

    clientes = obtener_clientes()

    client_options = [ft.dropdown.Option(key="", text="-- Sin asignar (Opcional) --")]
    for cli in clientes:
        client_options.append(ft.dropdown.Option(key=str(cli[0]), text=f"{cli[1]} {cli[2]}"))

    client_dropdown = ft.Dropdown(
        label="Cliente",
        options=client_options,
        width=350,
        border_radius=10,
        leading_icon=ft.Icons.PERSON
    )

    amount_input = InputModel("Monto").entry_style()
    amount_input.width = 350
    amount_input.border_radius = 10
    amount_input.prefix_icon = ft.Icons.ATTACH_MONEY

    desc_input = InputModel("Descripción / Concepto").entry_style()
    desc_input.width = 350
    desc_input.border_radius = 10
    desc_input.prefix_icon = ft.Icons.DESCRIPTION

    message_text = ft.Text("", size=16)

    def guardar_credito_click(p):
        client_val = client_dropdown.value
        cliente_id = int(client_val) if client_val and client_val != "" else None
        monto_str = amount_input.value.strip() if amount_input.value else ""
        descripcion = desc_input.value.strip() if desc_input.value else ""

        amount_input.error_text = None
        message_text.value = ""

        try:
            monto_val = float(monto_str)
            if monto_val <= 0:
                amount_input.error_text = "El monto debe ser mayor que cero"
                message_text.value = "No se guardó el crédito"
                message_text.color = "red"
                page.update()
                return
        except ValueError:
            amount_input.error_text = "Ingrese un monto válido"
            message_text.value = "No se guardó el crédito"
            message_text.color = "red"
            page.update()
            return

        try:
            guardar_credito(cliente_id, monto_val, descripcion)
            message_text.value = "Crédito guardado correctamente"
            message_text.color = "green"
            client_dropdown.value = ""
            amount_input.value = ""
            desc_input.value = ""
            page.update()
        except Exception as error:
            message_text.value = f"Error al guardar: {str(error)}"
            message_text.color = "red"
            page.update()

    def cancel_click(p):
        dash_board(p)

    save_button = section.primary_button(Control_b("Guardar", guardar_credito_click, page, icon=ft.Icons.SAVE).view())
    cancel_button = section.secondary_button(Control_b("Cancelar", cancel_click, page, icon=ft.Icons.CANCEL).view())

    header_row = section.header(
        ft.Icons.CREDIT_CARD,
        "Registrar Crédito",
        "Da de alta créditos y cuentas por cobrar",
    )

    form_card = section.card(
        ft.Column([
            client_dropdown,
            amount_input,
            desc_input,
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
