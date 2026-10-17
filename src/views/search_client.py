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
                client_id = cli[0]
                initial_nombre = cli[1]
                initial_apellido = cli[2]

                card_container = ft.Container(padding=15, width=550)

                def make_card_handlers(cid, nom, ape, container):
                    def build_view_mode():
                        def on_edit_click(e):
                            build_edit_mode()

                        container.content = ft.Column([
                            ft.Row([
                                ft.Row([
                                    ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400),
                                    ft.Text(f"{nom} {ape}", weight=ft.FontWeight.BOLD, size=16)
                                ], spacing=10),
                                ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=on_edit_click)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"ID del Cliente: {cid}", size=12, color=ft.Colors.GREY_700)
                        ], spacing=5)
                        page.update()

                    def build_edit_mode():
                        tf_nombre = ft.TextField(value=nom, label="Nombre", width=170)
                        tf_apellido = ft.TextField(value=ape, label="Apellido", width=170)

                        def save_click(e):
                            n = tf_nombre.value.strip() if tf_nombre.value else ""
                            a = tf_apellido.value.strip() if tf_apellido.value else ""
                            if n and a:
                                actualizar_cliente(cid, n, a)
                                message_text.value = f"Cliente ID {cid} actualizado correctamente"
                                message_text.color = "green"
                                perform_search()
                            else:
                                message_text.value = "Nombre y apellido son obligatorios para actualizar"
                                message_text.color = "red"
                                page.update()

                        def cancel_click(e):
                            build_view_mode()

                        btn_guardar = ft.Button("Guardar", on_click=save_click, icon=ft.Icons.SAVE)
                        btn_cancelar = ft.Button("Cancelar", on_click=cancel_click, icon=ft.Icons.CANCEL)

                        container.content = ft.Column([
                            ft.Text(f"ID: {cid}", size=12, color=ft.Colors.GREY_700),
                            ft.Row([tf_nombre, tf_apellido], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                            ft.Row([btn_guardar, btn_cancelar], alignment=ft.MainAxisAlignment.END, spacing=10)
                        ], spacing=8)
                        page.update()

                    build_view_mode()

                make_card_handlers(client_id, initial_nombre, initial_apellido, card_container)
                results_column.controls.append(ft.Card(content=card_container))

        page.update()

    first_name_field.on_change = perform_search
    last_name_field.on_change = perform_search

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
        message_text,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        results_column
    )
    page.update()
