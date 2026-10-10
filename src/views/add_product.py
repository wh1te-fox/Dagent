"""Product registration view module."""
import flet as ft


def main(page: ft.Page):
    """Renders the product registration interface."""
    from views.components.modelButton import Control_b
    from views.components.model_textfield import InputModel
    from services.database import guardar_producto as db_guardar_producto

    page.title = "Registrar Producto"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.controls.clear()

    code_input = InputModel("Código").entry_style()
    code_input.width = 350
    code_input.border_radius = 10
    code_input.prefix_icon = ft.Icons.BARCODE_READER

    name_input = InputModel("Nombre").entry_style()
    name_input.width = 350
    name_input.border_radius = 10
    name_input.prefix_icon = ft.Icons.LABEL

    category_input = InputModel("Categoría").entry_style()
    category_input.width = 350
    category_input.border_radius = 10
    category_input.prefix_icon = ft.Icons.CATEGORY

    price_input = InputModel("Precio").entry_style()
    price_input.width = 350
    price_input.border_radius = 10
    price_input.prefix_icon = ft.Icons.ATTACH_MONEY

    stock_input = InputModel("Stock").entry_style()
    stock_input.width = 350
    stock_input.border_radius = 10
    stock_input.prefix_icon = ft.Icons.INVENTORY

    message_text = ft.Text(
        "",
        size=16
    )

    def clear_input(e):
        code_input.value = ""
        name_input.value = ""
        category_input.value = ""
        price_input.value = ""
        stock_input.value = ""

        code_input.error_text = None
        name_input.error_text = None
        category_input.error_text = None
        price_input.error_text = None
        stock_input.error_text = None

        page.update()

    def guardar_producto(p):
        code = code_input.value.strip() if code_input.value else ""
        name = name_input.value.strip() if name_input.value else ""
        category = category_input.value.strip() if category_input.value else ""
        price = price_input.value.strip() if price_input.value else ""
        stock = stock_input.value.strip() if stock_input.value else ""

        code_input.error_text = None
        name_input.error_text = None
        category_input.error_text = None
        price_input.error_text = None
        stock_input.error_text = None

        message_text.value = ""
        message_text.color = None

        if code == "":
            code_input.error_text = "El código es obligatorio"
            message_text.value = "No se guardó el producto"
            message_text.color = "red"
            page.update()
            return

        if name == "":
            name_input.error_text = "El nombre es obligatorio"
            message_text.value = "No se guardó el producto"
            message_text.color = "red"
            page.update()
            return

        if category == "":
            category_input.error_text = "La categoría es obligatoria"
            message_text.value = "No se guardó el producto"
            message_text.color = "red"
            page.update()
            return

        try:
            price_val = float(price)
            if price_val <= 0:
                price_input.error_text = "El precio debe ser mayor que cero"
                message_text.value = "No se guardó el producto"
                message_text.color = "red"
                page.update()
                return
        except ValueError:
            price_input.error_text = "Ingrese un precio válido"
            message_text.value = "No se guardó el producto"
            message_text.color = "red"
            page.update()
            return

        try:
            stock_val = int(stock)
            if stock_val < 0:
                stock_input.error_text = "La existencia no puede ser negativa"
                message_text.value = "No se guardó el producto"
                message_text.color = "red"
                page.update()
                return
        except ValueError:
            stock_input.error_text = "Ingrese una existencia válida"
            message_text.value = "No se guardó el producto"
            message_text.color = "red"
            page.update()
            return

        try:
            db_guardar_producto(
                code,
                name,
                category,
                price_val,
                stock_val
            )

            message_text.value = "Producto guardado correctamente"
            message_text.color = "green"

            code_input.value = ""
            name_input.value = ""
            category_input.value = ""
            price_input.value = ""
            stock_input.value = ""

            page.update()

        except ValueError as error:
            code_input.error_text = str(error)
            message_text.value = "No se guardó el producto"
            message_text.color = "red"
            page.update()

    def cancel_click(p):
        from views.menu_interface import dash_board
        dash_board(p)

    save_btn = Control_b(
        "Guardar",
        guardar_producto,
        page
    ).view()

    cancel_btn = Control_b(
        "Cancelar",
        cancel_click,
        page
    ).view()

    header_row = ft.Row([
        ft.Icon(ft.Icons.INVENTORY_2, size=32, color=ft.Colors.BLUE),
        ft.Text("Registrar Producto", size=30, weight=ft.FontWeight.W_900, selectable=True)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    form_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                code_input,
                name_input,
                category_input,
                price_input,
                stock_input,
                ft.Divider(),
                message_text
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=25,
            width=450
        )
    )

    buttons_row = ft.Row(
        controls=[save_btn, cancel_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        header_row,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        form_card,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        buttons_row
    )

    page.update()

