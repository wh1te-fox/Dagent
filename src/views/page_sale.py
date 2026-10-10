"""Sales transaction view module."""
import flet as ft


def input_sale(page: ft.Page):
    """Renders the sales processing interface."""
    from services.database import guardar_venta, obtener_producto_por_codigo
    
    page.controls.clear()
    page.title = "Vender Producto"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    current_product = None

    def search_product(e):
        nonlocal current_product

        code = code_input.value.strip()

        if code == "":
            current_product = None
            message_text.value = ""
            price_field.value = ""
            price_text.value = "Precio"
            quantity_dropdown.options = []
            page.update()
            return

        current_product = obtener_producto_por_codigo(code)

        if current_product is None:
            code_input.error_text = "Producto no encontrado"
            message_text.value = "Producto no encontrado"
            message_text.color = "red"

            price_field.value = ""
            price_text.value = "Precio"
            quantity_dropdown.options = []

        else:
            code_input.error_text = None
            message_text.value = ""
            
            price_field.value = str(current_product[4])
            price_text.value = f"Precio: {current_product[4]}"

            quantity_dropdown.options = [
                ft.dropdown.Option(str(i))
                for i in range(1, current_product[5] + 1)
            ]

            if current_product[5] <= 0:
                quantity_dropdown.options = []
                message_text.value = "Producto sin existencia"
                message_text.color = "red"

        page.update()

    def calculate_total(e):
        try:
            quantity = int(quantity_dropdown.value)
            price = float(price_field.value)

            if quantity <= 0:
                subtotal_text.value = "Sub Total"
                page.update()
                return

            subtotal = quantity * price

            discount = float(discount_field.value or 0)

            if discount < 0 or discount > 100:
                subtotal_text.value = "Descuento debe estar entre 0 y 100"
                page.update()
                return

            discount_amount = subtotal * discount / 100

            total = subtotal - discount_amount

            subtotal_text.value = (
                f"Sub Total: {subtotal:.2f} | "
                f"Descuento: {discount_amount:.2f} | "
                f"Total: {total:.2f}"
            )

        except (ValueError, TypeError):
            subtotal_text.value = "Sub Total"

        page.update()

    def save_sale(e):
        if current_product is None:
            message_text.value = "Producto no encontrado"
            message_text.color = "red"
            page.update()
            return

        if current_product[5] <= 0:
            message_text.value = "El producto no tiene existencia"
            message_text.color = "red"
            page.update()
            return

        if quantity_dropdown.value is None or quantity_dropdown.value == "":
            quantity_dropdown.error_text = "Seleccione una cantidad"
            page.update()
            return

        try:
            quantity = int(quantity_dropdown.value)

            if quantity <= 0:
                quantity_dropdown.error_text = "La cantidad debe ser mayor que cero"
                page.update()
                return

        except ValueError:
            quantity_dropdown.error_text = "Ingrese una cantidad valida"
            page.update()
            return

        if quantity > current_product[5]:
            quantity_dropdown.error_text = (
                f"Existencia disponible: {current_product[5]}"
            )
            page.update()
            return

        try:
            price = float(price_field.value)

            if price <= 0:
                price_field.error_text = "El precio debe ser mayor que cero"
                page.update()
                return

        except ValueError:
            price_field.error_text = "El precio no es valido"
            page.update()
            return

        try:
            discount = float(discount_field.value or 0)

            if discount < 0 or discount > 100:
                discount_field.error_text = (
                    "El descuento debe estar entre 0 y 100"
                )
                page.update()
                return

        except ValueError:
            discount_field.error_text = "Ingrese un descuento valido"
            page.update()
            return

        subtotal = quantity * price

        discount_amount = subtotal * discount / 100

        total = subtotal - discount_amount

        try:
            guardar_venta(
                current_product[0],
                current_product[1],
                current_product[2],
                quantity,
                price,
                subtotal,
                discount,
                total
            )

            message_text.value = "Venta guardada correctamente"
            message_text.color = "green"

            clear_form(None)

        except ValueError as error:
            message_text.value = str(error)
            message_text.color = "red"
            page.update()

    def clear_form(e):
        nonlocal current_product

        current_product = None

        code_input.value = ""
        quantity_dropdown.value = ""
        price_field.value = ""
        discount_field.value = ""

        code_input.error_text = None
        quantity_dropdown.error_text = None
        price_field.error_text = None
        discount_field.error_text = None

        quantity_dropdown.options = []

        price_text.value = "Precio"
        subtotal_text.value = "Sub Total"
        message_text.value = ""

        page.update()

    def exit_window(e):
        from views.menu_interface import dash_board
        dash_board(page)

    code_input = ft.TextField(
        label="Código de Producto",
        on_change=search_product,
        width=350,
        border_radius=10,
        prefix_icon=ft.Icons.BARCODE_READER
    )

    quantity_dropdown = ft.Dropdown(
        label="Cantidad",
        on_select=calculate_total,
        width=350,
        border_radius=10
    )

    price_field = ft.TextField(
        label="Precio Unitario",
        read_only=True,
        width=350,
        border_radius=10,
        prefix_icon=ft.Icons.ATTACH_MONEY
    )

    price_text = ft.Text("Precio", size=14, weight=ft.FontWeight.W_500)
    subtotal_text = ft.Text("Sub Total", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
    message_text = ft.Text("", size=14)

    discount_field = ft.TextField(
        label="Descuento (%)",
        on_change=calculate_total,
        width=350,
        border_radius=10,
        prefix_icon=ft.Icons.PERCENT
    )

    save_button = ft.Button(
        "Guardar Venta",
        on_click=save_sale,
        icon=ft.Icons.SAVE,
        width=150,
        height=45
    )

    clear_button = ft.Button(
        "Limpiar",
        on_click=clear_form,
        icon=ft.Icons.CLEAR_ALL,
        width=120,
        height=45
    )

    close_button = ft.Button(
        "Cerrar",
        on_click=exit_window,
        icon=ft.Icons.ARROW_BACK,
        width=120,
        height=45
    )

    header_row = ft.Row([
        ft.Icon(ft.Icons.POINT_OF_SALE, size=32, color=ft.Colors.BLUE),
        ft.Text("Vender Producto", size=30, weight=ft.FontWeight.W_900, selectable=True)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    form_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                code_input,
                price_field,
                quantity_dropdown,
                discount_field,
                ft.Divider(),
                subtotal_text,
                message_text
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=25,
            width=450
        )
    )

    buttons_row = ft.Row(
        controls=[save_button, clear_button, close_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    page.add(
        header_row,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        form_card,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        buttons_row
    )
    page.update()

