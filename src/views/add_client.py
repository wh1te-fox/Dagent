import flet as ft

def customer_page(page: ft.Page):
    # --- Importar clases asignadas ---
    from views.components.modelButton import Control_b
    from views.components.model_textfield import InputModel
    from views.components.model_alignment import Column
    from views.menu_interface import dash_board
    from services.database import guardar_cliente, cliente_existe
    
    
    '''
    # --- Importar servicio de clientes ---
    from services.customer_service import init_db, add_customer
    from views.menu_interface import dash_board
    from views.add_product_client import add_product

    # Inicializar la DB
    init_db()
    '''
    # --- Configuración de la página ---
    page.title = "Registrar Clientes"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.controls.clear()

    page.add(ft.Text("Registrar Clientes", size=30, weight=ft.FontWeight.W_900))

    # --- Entradas de cliente ---
    nombre_input = InputModel("Nombre").entry_style()
    apellido_input = InputModel("Apellido").entry_style()

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

    # --- Organizar todo en columnas ---
    ui_column = Column(
        nombre_input,
        apellido_input,
        guardar_btn,
        cancelar_btn,
    )

    page.add(ui_column.view_column(), txtMensaje)
    page.update()
