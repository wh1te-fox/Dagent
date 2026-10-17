"""Client search and management view module."""
import flet as ft
import sqlite3
from flet import SnackBar


def search(page: ft.Page):
    """Renders the client search and editing interface."""
    from services.database import actualizar_cliente, buscar_clientes
    from views.components import section
    from views.components.alignment import Column
    from views.components.button import ButtonIcon, Control_b
    from views.components.text_field import InputModel
    from views.menu_interface import dash_board

    section.setup(page, "Clientes")

    header_row = section.header(
        ft.Icons.PERSON_SEARCH,
        "Buscar Clientes",
        "Localiza clientes y actualiza sus datos"
    )

    first_name_input = InputModel('Nombre')
    first_name_field = first_name_input.entry_style()
    first_name_field.width = 280

    last_name_input = InputModel('Apellido')
    last_name_field = last_name_input.entry_style()
    last_name_field.width = 280

    message_text = ft.Text("", size=14, color=ft.Colors.GREY_600)
    results_column = ft.Column(width=section.RESULTS_WIDTH, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def perform_search(e=None):
        first_name = first_name_field.value.strip() if first_name_field.value else ""
        last_name = last_name_field.value.strip() if last_name_field.value else ""

        first_name_field.error_text = None
        last_name_field.error_text = None
        message_text.value = ""
        results_column.controls.clear()

        if not first_name and not last_name:
            clients = buscar_clientes("", "")
            message_text.value = f"Mostrando todos los clientes ({len(clients)})"
            message_text.color = None
        else:
            clients = buscar_clientes(first_name, last_name)

        first_name_field.error_text = None
        last_name_field.error_text = None

        if not clients:
            results_column.controls.append(
                section.empty_state("No se encontraron clientes", ft.Icons.PERSON_SEARCH_OUTLINED)
            )
        else:
            message_text.value = f"Se encontraron {len(clients)} cliente(s)"
            message_text.color = "green"
            for cli in clients:
                client_id = cli[0]
                initial_nombre = cli[1]
                initial_apellido = cli[2]

                card_container = section.result_card(ft.Column(spacing=5))

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

                        btn_guardar = section.primary_button(ft.Button("Guardar", on_click=save_click, icon=ft.Icons.SAVE))
                        btn_cancelar = section.secondary_button(ft.Button("Cancelar", on_click=cancel_click, icon=ft.Icons.CANCEL))

                        container.content = ft.Column([
                            ft.Text(f"ID: {cid}", size=12, color=ft.Colors.GREY_700),
                            ft.Row([tf_nombre, tf_apellido], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                            ft.Row([btn_guardar, btn_cancelar], alignment=ft.MainAxisAlignment.END, spacing=10),
                        ], spacing=8)
                        page.update()

                    build_view_mode()

                make_card_handlers(client_id, initial_nombre, initial_apellido, card_container)
                results_column.controls.append(card_container)

        page.update()

    first_name_field.on_change = perform_search
    last_name_field.on_change = perform_search

    def exit_window(e):
        dash_board(page)

    btn_close = section.secondary_button(
        ft.Button(
            "Cerrar",
            on_click=exit_window,
            icon=ft.Icons.ARROW_BACK,
            height=45
        )
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
        section.spacer(16),
        search_inputs_row,
        section.spacer(10),
        message_text,
        section.spacer(10),
        results_column
    )

    perform_search()
    page.update()
