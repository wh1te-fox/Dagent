import flet as ft


def input_sale(page: ft.Page):
    from services.database import obtener_producto_por_codigo, guardar_venta
    
    page.controls.clear()
    page.title = "Vender Producto"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    producto_actual = None

    def buscar_producto(e):
        nonlocal producto_actual

        codigo = inpCodigo.value.strip()

        if codigo == "":
            producto_actual = None
            txtMensaje.value = ""
            inpPrecio.value = ""
            txtPrecio.value = "Precio"
            inpCantidad.options = []
            page.update()
            return

        producto_actual = obtener_producto_por_codigo(codigo)

        if producto_actual is None:
            inpCodigo.error_text = "Producto no encontrado"
            txtMensaje.value = "Producto no encontrado"
            txtMensaje.color = "red"

            inpPrecio.value = ""
            txtPrecio.value = "Precio"
            inpCantidad.options = []

        else:
            inpCodigo.error_text = None
            txtMensaje.value = ""
            
            inpPrecio.value = str(producto_actual[4])
            txtPrecio.value = f"Precio: {producto_actual[4]}"

            inpCantidad.options = [
                ft.dropdown.Option(str(i))
                for i in range(1, producto_actual[5] + 1)
            ]

            if producto_actual[5] <= 0:
                inpCantidad.options = []
                txtMensaje.value = "Producto sin existencia"
                txtMensaje.color = "red"

        page.update()

    def calcular_total(e):
        try:
            cantidad = int(inpCantidad.value)
            precio = float(inpPrecio.value)

            if cantidad <= 0:
                txtSubTotal.value = "Sub Total"
                page.update()
                return

            subtotal = cantidad * precio

            descuento = float(inpDescuento.value or 0)

            if descuento < 0 or descuento > 100:
                txtSubTotal.value = "Descuento debe estar entre 0 y 100"
                page.update()
                return

            descuento_monto = subtotal * descuento / 100

            total = subtotal - descuento_monto

            txtSubTotal.value = (
                f"Sub Total: {subtotal:.2f} | "
                f"Descuento: {descuento_monto:.2f} | "
                f"Total: {total:.2f}"
            )

        except (ValueError, TypeError):
            txtSubTotal.value = "Sub Total"

        page.update()

    def save_input(e):

        if producto_actual is None:
            txtMensaje.value = "Producto no encontrado"
            txtMensaje.color = "red"
            page.update()
            return

        if producto_actual[5] <= 0:
            txtMensaje.value = "El producto no tiene existencia"
            txtMensaje.color = "red"
            page.update()
            return

        if inpCantidad.value is None or inpCantidad.value == "":
            inpCantidad.error_text = "Seleccione una cantidad"
            page.update()
            return

        try:
            cantidad = int(inpCantidad.value)

            if cantidad <= 0:
                inpCantidad.error_text = "La cantidad debe ser mayor que cero"
                page.update()
                return

        except ValueError:
            inpCantidad.error_text = "Ingrese una cantidad valida"
            page.update()
            return

        if cantidad > producto_actual[5]:
            inpCantidad.error_text = (
                f"Existencia disponible: {producto_actual[5]}"
            )
            page.update()
            return

        try:
            precio = float(inpPrecio.value)

            if precio <= 0:
                inpPrecio.error_text = "El precio debe ser mayor que cero"
                page.update()
                return

        except ValueError:
            inpPrecio.error_text = "El precio no es valido"
            page.update()
            return

        try:
            descuento = float(inpDescuento.value or 0)

            if descuento < 0 or descuento > 100:
                inpDescuento.error_text = (
                    "El descuento debe estar entre 0 y 100"
                )
                page.update()
                return

        except ValueError:
            inpDescuento.error_text = "Ingrese un descuento valido"
            page.update()
            return

        subtotal = cantidad * precio

        descuento_monto = subtotal * descuento / 100

        total = subtotal - descuento_monto

        try:
            guardar_venta(
                producto_actual[0],
                producto_actual[1],
                producto_actual[2],
                cantidad,
                precio,
                subtotal,
                descuento,
                total
            )

            txtMensaje.value = "Venta guardada correctamente"
            txtMensaje.color = "green"

            clear_input(None)

        except ValueError as error:
            txtMensaje.value = str(error)
            txtMensaje.color = "red"
            page.update()

    def clear_input(e):
        nonlocal producto_actual

        producto_actual = None

        inpCodigo.value = ""
        inpCantidad.value = ""
        inpPrecio.value = ""
        inpDescuento.value = ""

        inpCodigo.error_text = None
        inpCantidad.error_text = None
        inpPrecio.error_text = None
        inpDescuento.error_text = None

        inpCantidad.options = []

        txtPrecio.value = "Precio"
        txtSubTotal.value = "Sub Total"
        txtMensaje.value = ""

        page.update()

    def exit_window(e):
        from views.menu_interface import dash_board
        dash_board(page)

    inpCodigo = ft.TextField(
        label="Código de Producto",
        on_change=buscar_producto,
        width=350,
        border_radius=10,
        prefix_icon=ft.Icons.BARCODE_READER
    )

    inpCantidad = ft.Dropdown(
        label="Cantidad",
        on_select=calcular_total,
        width=350,
        border_radius=10
    )

    inpPrecio = ft.TextField(
        label="Precio Unitario",
        read_only=True,
        width=350,
        border_radius=10,
        prefix_icon=ft.Icons.ATTACH_MONEY
    )

    txtPrecio = ft.Text("Precio", size=14, weight=ft.FontWeight.W_500)
    txtSubTotal = ft.Text("Sub Total", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
    txtMensaje = ft.Text("", size=14)

    inpDescuento = ft.TextField(
        label="Descuento (%)",
        on_change=calcular_total,
        width=350,
        border_radius=10,
        prefix_icon=ft.Icons.PERCENT
    )

    btnGuardar = ft.Button(
        "Guardar Venta",
        on_click=save_input,
        icon=ft.Icons.SAVE,
        width=150,
        height=45
    )

    btnLimpiar = ft.Button(
        "Limpiar",
        on_click=clear_input,
        icon=ft.Icons.CLEAR_ALL,
        width=120,
        height=45
    )

    btnCerrar = ft.Button(
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
                inpCodigo,
                inpPrecio,
                inpCantidad,
                inpDescuento,
                ft.Divider(),
                txtSubTotal,
                txtMensaje
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=25,
            width=450
        )
    )

    buttons_row = ft.Row(
        controls=[btnGuardar, btnLimpiar, btnCerrar],
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
