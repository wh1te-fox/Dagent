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
    page.title = "Buscar Clientes"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    header_row = ft.Row([
        ft.Icon(ft.Icons.PERSON_SEARCH, size=32, color=ft.Colors.BLUE),
        ft.Text("Buscar Clientes", size=30, weight=ft.FontWeight.W_900, selectable=True)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    parameter_name = InputModel('Nombre')
    execute_entry = parameter_name.entry_style()
    execute_entry.width = 200

    last_name = InputModel('Apellido')
    execute_entry1 = last_name.entry_style()
    execute_entry1.width = 200

    txtMensaje = ft.Text("", size=16)
    edit_switch = ft.Switch(label="Modo Edición", value=False, on_change=lambda _: realizar_busqueda())
    results_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=320, width=600, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

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
                                    ft.Row([
                                        ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400),
                                        ft.Text(f"{cli[1]} {cli[2]}", weight=ft.FontWeight.BOLD, size=16)
                                    ], spacing=10),
                                    ft.Text(f"ID del Cliente: {cli[0]}", size=12, color=ft.Colors.GREY_700)
                                ], spacing=5),
                                padding=15
                            ),
                            width=500
                        )
                    )
                else:
                    client_id = cli[0]
                    tf_nombre = ft.TextField(value=cli[1], label="Nombre", width=170)
                    tf_apellido = ft.TextField(value=cli[2], label="Apellido", width=170)

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
                                    ft.Row([tf_nombre, tf_apellido, btn_actualizar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10)
                                ], spacing=8),
                                padding=15
                            ),
                            width=550
                        )
                    )

        page.update()

    def exit_window(e):
        dash_board(page)

    btnCerrar = ft.Button(
        "Cerrar",
        on_click=exit_window,
        icon=ft.Icons.ARROW_BACK,
        height=45
    )

    search_button = ButtonIcon(ft.Icons.SEARCH_OUTLINED, ft.Colors.GREEN_300, realizar_busqueda, "Buscar")
    add_search = search_button.model_icon()

    search_inputs_row = ft.Row(
        controls=[execute_entry, execute_entry1, add_search, btnCerrar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    page.add(
        header_row,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        search_inputs_row,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        edit_switch,
        txtMensaje,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        results_column
    )
    page.update()

print("search_client")