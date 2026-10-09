import flet as ft

def customer_page(page: ft.Page):
    # --- Importar clases asignadas ---
    from views.components.modelButton import Control_b
    from views.components.model_textfield import InputModel
    from views.menu_interface import dash_board
    from services.database import guardar_cliente, cliente_existe
    
    # --- Configuración de la página ---
    page.title = "Registrar Clientes"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.controls.clear()

    # --- Entradas de cliente ---
    nombre_input = InputModel("Nombre").entry_style()
    nombre_input.width = 350
    nombre_input.border_radius = 10
    nombre_input.prefix_icon = ft.Icons.PERSON

    apellido_input = InputModel("Apellido").entry_style()
    apellido_input.width = 350
    apellido_input.border_radius = 10
    apellido_input.prefix_icon = ft.Icons.PERSON_OUTLINE

    # Mensaje general
    txtMensaje = ft.Text("", size=16)

    # --- Funciones para los botones ---
    def guardar_cliente_click(p):
        first_name = nombre_input.value.strip() if nombre_input.value else ""
        last_name = apellido_input.value.strip() if apellido_input.value else ""

        nombre_input.error_text = None
        apellido_input.error_text = None
        txtMensaje.value = ""

        valid = True
        if not first_name:
            nombre_input.error_text = "El nombre es obligatorio"
            valid = False
        if not last_name:
            apellido_input.error_text = "El apellido es obligatorio"
            valid = False

        if not valid:
            txtMensaje.value = "No se guardó el cliente"
            txtMensaje.color = "red"
            page.update()
            return

        if cliente_existe(first_name, last_name):
            txtMensaje.value = "El cliente ya existe en el sistema"
            txtMensaje.color = "red"
            page.update()
            return

        try:
            guardar_cliente(first_name, last_name)
            txtMensaje.value = "Cliente guardado correctamente"
            txtMensaje.color = "green"
            nombre_input.value = ""
            apellido_input.value = ""
            page.update()
        except Exception as error:
            nombre_input.error_text = str(error)
            txtMensaje.value = "No se guardó el cliente"
            txtMensaje.color = "red"
            page.update()

    def cancelar(p):
        dash_board(p)

    # --- Botones reutilizables ---
    guardar_btn = Control_b("Guardar", guardar_cliente_click, page).view()
    cancelar_btn = Control_b("Cancelar", cancelar, page).view()

    header_row = ft.Row([
        ft.Icon(ft.Icons.PERSON_ADD, size=32, color=ft.Colors.BLUE),
        ft.Text("Registrar Clientes", size=30, weight=ft.FontWeight.W_900, selectable=True)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    form_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                nombre_input,
                apellido_input,
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
