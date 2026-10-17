"""Sales transaction view module."""
import flet as ft


def input_sale(page: ft.Page):
    """Renders the sales processing interface."""
    from services.database import obtener_clientes, obtener_producto_por_codigo, guardar_venta, guardar_venta_con_credito
    from views.components import section

    section.setup(page, "Punto de venta")

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

        modo_pago = payment_dropdown.value
        abono = 0.0
        cliente_id = None

        if modo_pago in ("credito", "mixto"):
            cliente_val = client_dropdown.value
            if not cliente_val:
                client_dropdown.error_text = "Seleccione un cliente para el crédito"
                page.update()
                return

            cliente_id = int(cliente_val)

            if modo_pago == "mixto":
                try:
                    abono = float(abono_field.value.strip()) if abono_field.value else 0.0
                except ValueError:
                    abono_field.error_text = "Ingrese un abono válido"
                    page.update()
                    return

                if abono < 0:
                    abono_field.error_text = "El abono no puede ser negativo"
                    page.update()
                    return

                if abono >= total:
                    abono_field.error_text = (
                        f"El abono cubre el total (${total:.2f}); use el modo Contado"
                    )
                    page.update()
                    return

        descripcion_credito = None
        if modo_pago == "credito":
            descripcion_credito = f"Venta a crédito - {current_product[2]} x{quantity}"
        elif modo_pago == "mixto":
            descripcion_credito = f"Venta mixta (abono ${abono:.2f}) - {current_product[2]} x{quantity}"

        try:
            if modo_pago == "contado":
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
            else:
                guardar_venta_con_credito(
                    current_product[0],
                    current_product[1],
                    current_product[2],
                    quantity,
                    price,
                    subtotal,
                    discount,
                    total,
                    abono,
                    cliente_id,
                    descripcion_credito
                )

            if modo_pago == "credito":
                message_text.value = f"Venta guardada a crédito por ${total:.2f}"
            elif modo_pago == "mixto":
                message_text.value = (
                    f"Venta guardada: abono ${abono:.2f} en efectivo "
                    f"y ${total - abono:.2f} a crédito"
                )
            else:
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
        client_dropdown.value = ""
        abono_field.value = ""

        code_input.error_text = None
        quantity_dropdown.error_text = None
        price_field.error_text = None
        discount_field.error_text = None
        client_dropdown.error_text = None
        abono_field.error_text = None

        quantity_dropdown.options = []

        payment_dropdown.value = "contado"
        payment_mode_changed(None)

        price_text.value = "Precio"
        subtotal_text.value = "Sub Total"
        message_text.value = ""

        page.update()

    def payment_mode_changed(e):
        modo = payment_dropdown.value

        if modo == "contado":
            client_dropdown.visible = False
            abono_field.visible = False
        elif modo == "credito":
            client_dropdown.visible = True
            abono_field.visible = False
        else:
            client_dropdown.visible = True
            abono_field.visible = True
            abono_field.label = "Abono en efectivo"
            abono_field.hint_text = None

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

    client_options = [ft.dropdown.Option(key="", text="-- Seleccione cliente --")]
    for cli in obtener_clientes():
        client_options.append(ft.dropdown.Option(key=str(cli[0]), text=f"{cli[1]} {cli[2]}"))

    client_dropdown = ft.Dropdown(
        label="Cliente (crédito)",
        options=client_options,
        width=350,
        border_radius=10,
        visible=False,
        leading_icon=ft.Icons.PERSON
    )

    payment_dropdown = ft.Dropdown(
        label="Forma de pago",
        options=[
            ft.dropdown.Option(key="contado", text="Contado"),
            ft.dropdown.Option(key="credito", text="Crédito"),
            ft.dropdown.Option(key="mixto", text="Mixto (efectivo + crédito)"),
        ],
        value="contado",
        on_select=payment_mode_changed,
        width=350,
        border_radius=10,
        leading_icon=ft.Icons.PAYMENTS
    )

    abono_field = ft.TextField(
        label="Abono en efectivo",
        hint_text="Monto pagado al instante",
        width=350,
        border_radius=10,
        visible=False,
        prefix_icon=ft.Icons.MONEY
    )

    save_button = section.primary_button(
        ft.Button(
            "Guardar Venta",
            on_click=save_sale,
            icon=ft.Icons.SAVE,
            width=150,
        )
    )

    clear_button = section.secondary_button(
        ft.Button(
            "Limpiar",
            on_click=clear_form,
            icon=ft.Icons.CLEAR_ALL,
            width=120,
        )
    )

    close_button = section.secondary_button(
        ft.Button(
            "Cerrar",
            on_click=exit_window,
            icon=ft.Icons.ARROW_BACK,
            width=120,
        )
    )

    header_row = section.header(
        ft.Icons.POINT_OF_SALE,
        "Punto de venta",
        "Registra una venta mediante el código de producto"
    )

    form_card = section.card(
        ft.Column([
            code_input,
            price_field,
            quantity_dropdown,
            discount_field,
            payment_dropdown,
            client_dropdown,
            abono_field,
            ft.Divider(),
            subtotal_text,
            message_text
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=section.FORM_WIDTH
    )

    buttons_row = ft.Row(
        controls=[save_button, clear_button, close_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    page.add(
        header_row,
        section.spacer(20),
        form_card,
        section.spacer(16),
        buttons_row
    )
    page.update()

