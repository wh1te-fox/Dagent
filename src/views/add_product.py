import flet as ft


def main(page: ft.Page):
    # --- Configuración de la página ---
    from views.components.modelButton import Control_b
    from views.components.model_textfield import InputModel
    from services.database import guardar_producto as db_guardar_producto

    page.title = "Registrar Producto"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.controls.clear()

    # CAMPOS
    codigo_input = InputModel("Código").entry_style()
    codigo_input.width = 350
    codigo_input.border_radius = 10
    codigo_input.prefix_icon = ft.Icons.BARCODE_READER

    nombre_input = InputModel("Nombre").entry_style()
    nombre_input.width = 350
    nombre_input.border_radius = 10
    nombre_input.prefix_icon = ft.Icons.LABEL

    categoria_input = InputModel("Categoría").entry_style()
    categoria_input.width = 350
    categoria_input.border_radius = 10
    categoria_input.prefix_icon = ft.Icons.CATEGORY

    precio_input = InputModel("Precio").entry_style()
    precio_input.width = 350
    precio_input.border_radius = 10
    precio_input.prefix_icon = ft.Icons.ATTACH_MONEY

    stock_input = InputModel("Stock").entry_style()
    stock_input.width = 350
    stock_input.border_radius = 10
    stock_input.prefix_icon = ft.Icons.INVENTORY

    # Mensaje general
    txtMensaje = ft.Text(
        "",
        size=16
    )

    # LIMPIAR CAMPOS
    def clear_input(e):
        codigo_input.value = ""
        nombre_input.value = ""
        categoria_input.value = ""
        precio_input.value = ""
        stock_input.value = ""

        codigo_input.error_text = None
        nombre_input.error_text = None
        categoria_input.error_text = None
        precio_input.error_text = None
        stock_input.error_text = None

        page.update()

    # GUARDAR PRODUCTO
    def guardar_producto(p):
        codigo = codigo_input.value.strip() if codigo_input.value else ""
        nombre = nombre_input.value.strip() if nombre_input.value else ""
        categoria = categoria_input.value.strip() if categoria_input.value else ""
        precio = precio_input.value.strip() if precio_input.value else ""
        existencia = stock_input.value.strip() if stock_input.value else ""

        # Limpiar errores anteriores
        codigo_input.error_text = None
        nombre_input.error_text = None
        categoria_input.error_text = None
        precio_input.error_text = None
        stock_input.error_text = None

        # Limpiar mensaje general
        txtMensaje.value = ""
        txtMensaje.color = None

        # VALIDAR CÓDIGO
        if codigo == "":
            codigo_input.error_text = "El código es obligatorio"
            txtMensaje.value = "No se guardó el producto"
            txtMensaje.color = "red"
            page.update()
            return

        # VALIDAR NOMBRE
        if nombre == "":
            nombre_input.error_text = "El nombre es obligatorio"
            txtMensaje.value = "No se guardó el producto"
            txtMensaje.color = "red"
            page.update()
            return

        # VALIDAR CATEGORÍA
        if categoria == "":
            categoria_input.error_text = "La categoría es obligatoria"
            txtMensaje.value = "No se guardó el producto"
            txtMensaje.color = "red"
            page.update()
            return

        # VALIDAR PRECIO
        try:
            precio_val = float(precio)
            if precio_val <= 0:
                precio_input.error_text = "El precio debe ser mayor que cero"
                txtMensaje.value = "No se guardó el producto"
                txtMensaje.color = "red"
                page.update()
                return
        except ValueError:
            precio_input.error_text = "Ingrese un precio válido"
            txtMensaje.value = "No se guardó el producto"
            txtMensaje.color = "red"
            page.update()
            return

        # VALIDAR EXISTENCIA
        try:
            existencia_val = int(existencia)
            if existencia_val < 0:
                stock_input.error_text = "La existencia no puede ser negativa"
                txtMensaje.value = "No se guardó el producto"
                txtMensaje.color = "red"
                page.update()
                return
        except ValueError:
            stock_input.error_text = "Ingrese una existencia válida"
            txtMensaje.value = "No se guardó el producto"
            txtMensaje.color = "red"
            page.update()
            return

        # GUARDAR
        try:
            db_guardar_producto(
                codigo,
                nombre,
                categoria,
                precio_val,
                existencia_val
            )

            # Mensaje de confirmación
            txtMensaje.value = "Producto guardado correctamente"
            txtMensaje.color = "green"

            # Limpiar campos
            codigo_input.value = ""
            nombre_input.value = ""
            categoria_input.value = ""
            precio_input.value = ""
            stock_input.value = ""

            page.update()

        except ValueError as error:
            codigo_input.error_text = str(error)
            txtMensaje.value = "No se guardó el producto"
            txtMensaje.color = "red"
            page.update()

    # CANCELAR
    def cancelar(p):
        from views.menu_interface import dash_board
        dash_board(p)

    # BOTONES
    guardar_btn = Control_b(
        "Guardar",
        guardar_producto,
        page
    ).view()

    cancelar_btn = Control_b(
        "Cancelar",
        cancelar,
        page
    ).view()

    header_row = ft.Row([
        ft.Icon(ft.Icons.INVENTORY_2, size=32, color=ft.Colors.BLUE),
        ft.Text("Registrar Producto", size=30, weight=ft.FontWeight.W_900, selectable=True)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    form_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                codigo_input,
                nombre_input,
                categoria_input,
                precio_input,
                stock_input,
                ft.Divider(),
                txtMensaje
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=25,
            width=450
        )
    )

    buttons_row = ft.Row(
        controls=[guardar_btn, cancelar_btn],
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
