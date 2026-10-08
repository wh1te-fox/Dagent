import flet as ft
import sqlite3
from flet import SnackBar

# lista de clientes
def search(page: ft.Page):

    from views.menu_interface import dash_board
    from views.components.model_textfield import InputModel
    from views.components.modelButton import Control_b, ButtonIcon
    from views.components.model_alignment import Column
    from services.database import buscar_clientes, actualizar_cliente

    page.update()
    page.controls.clear()

    page.add (ft.Text("Buscar Clientes", 
        size=30, weight=ft.FontWeight.W_900, 
        selectable=True))

    parameter_name = InputModel('nombre')
    execute_entry = parameter_name.entry_style()

    last_name = InputModel('apellido')
    execute_entry1 = last_name.entry_style()

    txtMensaje = ft.Text("", size=16)
    edit_switch = ft.Switch(label="Modo Edición", value=False, on_change=lambda _: realizar_busqueda())
    results_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=300)

    def realizar_busqueda(e=None):
        nombre = execute_entry.value.strip() if execute_entry.value else ""
        apellido = execute_entry1.value.strip() if execute_entry1.value else ""

        execute_entry.error_text = None
        execute_entry1.error_text = None
        txtMensaje.value = ""
        results_column.controls.clear()

        if not nombre and not apellido:
            txtMensaje.value = "Ingrese al menos un criterio de búsqueda (nombre o apellido)"
            txtMensaje.color = "red"
            page.update()
            return

        clientes = buscar_clientes(nombre, apellido)

        if not clientes:
            txtMensaje.value = "No se encontraron clientes"
            txtMensaje.color = "orange"
        else:
            txtMensaje.value = f"Se encontraron {len(clientes)} cliente(s)"
            txtMensaje.color = "green"
            for cli in clientes:
                if not edit_switch.value:
                    results_column.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text(f"Nombre: {cli[1]} {cli[2]}", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"ID: {cli[0]}", size=12, color=ft.Colors.GREY_700)
                                ]),
                                padding=10
                            )
                        )
                    )
                else:
                    client_id = cli[0]
                    tf_nombre = ft.TextField(value=cli[1], label="Nombre", width=180)
                    tf_apellido = ft.TextField(value=cli[2], label="Apellido", width=180)

                    def make_update_handler(cid, tn, ta):
                        def update_click(e):
                            n = tn.value.strip() if tn.value else ""
                            a = ta.value.strip() if ta.value else ""
                            if n and a:
                                actualizar_cliente(cid, n, a)
                                txtMensaje.value = f"Cliente ID {cid} actualizado correctamente"
                                txtMensaje.color = "green"
                                page.update()
                            else:
                                txtMensaje.value = "Nombre y apellido son obligatorios para actualizar"
                                txtMensaje.color = "red"
                                page.update()
                        return update_click

                    btn_actualizar = ft.Button("Actualizar", on_click=make_update_handler(client_id, tf_nombre, tf_apellido), icon=ft.Icons.SAVE)

                    results_column.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text(f"ID: {client_id}", size=12, color=ft.Colors.GREY_700),
                                    ft.Row([tf_nombre, tf_apellido, btn_actualizar], alignment=ft.MainAxisAlignment.START, spacing=15)
                                ]),
                                padding=15
                            )
                        )
                    )

        page.update()

    def exit_window(e):
        dash_board(page)

    btnCerrar = ft.Button(
        "Cerrar",
        on_click=exit_window
    )

    search_button = ButtonIcon(ft.Icons.SEARCH_OUTLINED, ft.Colors.GREEN_300, realizar_busqueda, "Buscar")
    add_search = search_button.model_icon()

    element_column = Column(execute_entry, execute_entry1)
    execute_column = element_column.view_column()

    page.add(
        ft.Row(
            controls=[
                execute_column,
                add_search,
                btnCerrar
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        edit_switch,
        txtMensaje,
        results_column
    )
    page.update()

print("search_client")