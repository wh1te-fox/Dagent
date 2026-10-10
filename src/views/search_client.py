"""Client search and management view module."""
import flet as ft
import sqlite3
from flet import SnackBar


def search(page: ft.Page):
    """Renders the client search and editing interface."""
    from services.database import actualizar_cliente, buscar_clientes
    from views.components.alignment import Column
    from views.components.button import ButtonIcon, Control_b
    from views.components.text_field import InputModel
    from views.menu_interface import dash_board

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

    first_name_input = InputModel('Nombre')
    first_name_field = first_name_input.entry_style()
    first_name_field.width = 200

    last_name_input = InputModel('Apellido')
    last_name_field = last_name_input.entry_style()
    last_name_field.width = 200

    message_text = ft.Text("", size=16)
    edit_switch = ft.Switch(label="Modo Edición", value=False, on_change=lambda _: perform_search())
    results_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=320, width=600, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def perform_search(e=None):
        first_name = first_name_field.value.strip() if first_name_field.value else ""
        last_name = last_name_field.value.strip() if last_name_field.value else ""

        first_name_field.error_text = None
        last_name_field.error_text = None
        message_text.value = ""
        results_column.controls.clear()

        if not first_name and not last_name:
            message_text.value = "Ingrese al menos un criterio de búsqueda (nombre o apellido)"
            message_text.color = "red"
            page.update()
            return

        clients = buscar_clientes(first_name, last_name)

        if not clients:
            message_text.value = "No se encontraron clientes"
            message_text.color = "orange"
        else:
            message_text.value = f"Se encontraron {len(clients)} cliente(s)"
            message_text.color = "green"
            for cli in clients:
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
                                message_text.value = f"Cliente ID {cid} actualizado correctamente"
                                message_text.color = "green"
                                page.update()
                            else:
                                message_text.value = "Nombre y apellido son obligatorios para actualizar"
                                message_text.color = "red"
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

    btn_close = ft.Button(
        "Cerrar",
        on_click=exit_window,
        icon=ft.Icons.ARROW_BACK,
        height=45
    )

    search_button = ButtonIcon(ft.Icons.SEARCH_OUTLINED, ft.Colors.GREEN_300, perform_search, "Buscar")
    add_search = search_button.model_icon()

    search_inputs_row = ft.Row(
        controls=[first_name_field, last_name_field, add_search, btn_close],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    page.add(
        header_row,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        search_inputs_row,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        edit_switch,
        message_text,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        results_column
    )
    page.update()
