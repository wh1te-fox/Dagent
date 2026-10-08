import flet as ft


def main(page: ft.Page):
    # --- Configuración de la página ---
    from views.components.modelButton import Control_b
    from views.components.model_textfield import InputModel
    from views.components.model_alignment import Column
    from services.database import guardar_producto as db_guardar_producto

    page.title = "Registrar Producto"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()

    page.add(
        ft.Text(
            "Registrar Producto",
            size=30,
            weight=ft.FontWeight.W_900
        )
    )

    # CAMPOS
    
    codigo_input = InputModel("Código").entry_style()
    nombre_input = InputModel("Nombre").entry_style()
    categoria_input = InputModel("Categoría").entry_style()
    precio_input = InputModel("Precio").entry_style()
    stock_input = InputModel("Stock").entry_style()

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

        codigo = codigo_input.value.strip()
        nombre = nombre_input.value.strip()
        categoria = categoria_input.value.strip()
        precio = precio_input.value.strip()
        existencia = stock_input.value.strip()

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
            precio = float(precio)

            if precio <= 0:
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
            existencia = int(existencia)

            if existencia < 0:
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
                precio,
                existencia
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

    # ORGANIZAR INTERFAZ

    ui_column = Column(
        codigo_input,
        nombre_input,
    )

    row_two = Column(
        categoria_input,
        precio_input,
    )

    row_three = Column(
        guardar_btn,
        cancelar_btn
    )
    row_fouth = Column(
        stock_input
    )
    row_five = Column(
        txtMensaje,
    )

# Nota para nueva funcion para el modelo, pasaler un numero para generar una cierta cantidad de filas
    page.add(ui_column.view_column(),
        row_two.view_column(),
        row_fouth.view_column(),
        row_three.view_column(),
        row_five.view_column())

    page.update()


# ft.app(target=main)
