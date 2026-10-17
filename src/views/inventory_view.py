"""Inventory management and stock view module."""
import flet as ft


def inventory_page(page: ft.Page):
    """Renders the inventory interface with product search and stock management."""
    from services.database import actualizar_producto_stock, buscar_productos, obtener_productos
    from views.components.text_field import InputModel
    from views.menu_interface import dash_board

    page.update()
    page.controls.clear()
    page.title = "Gestión de Inventario"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    header_row = ft.Row([
        ft.Icon(ft.Icons.INVENTORY, size=32, color=ft.Colors.BLUE),
        ft.Text("Gestión de Inventario", size=30, weight=ft.FontWeight.W_900, selectable=True)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    search_input = InputModel('Buscar por código, nombre o categoría')
    search_field = search_input.entry_style()
    search_field.width = 350

    message_text = ft.Text("", size=16)
    results_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=350, width=650, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def perform_search(e=None):
        termino = search_field.value.strip() if search_field.value else ""
        message_text.value = ""
        results_column.controls.clear()

        productos = buscar_productos(termino) if termino else obtener_productos()

        if not productos:
            message_text.value = "No se encontraron productos"
            message_text.color = "orange"
        else:
            message_text.value = f"Se encontraron {len(productos)} producto(s)"
            message_text.color = "green"
            for prod in productos:
                prod_id, codigo, nombre, categoria, precio, existencia = prod

                card_container = ft.Container(padding=15, width=600)

                def make_card_handlers(pid, cod, nom, cat, pre, ext, container):
                    def build_view_mode():
                        def on_edit_click(e):
                            build_edit_mode()

                        container.content = ft.Column([
                            ft.Row([
                                ft.Row([
                                    ft.Icon(ft.Icons.INVENTORY_2, color=ft.Colors.BLUE_400),
                                    ft.Text(f"{nom} ({cod})", weight=ft.FontWeight.BOLD, size=16)
                                ], spacing=10),
                                ft.IconButton(icon=ft.Icons.EDIT, tooltip="Actualizar Stock", on_click=on_edit_click)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([
                                ft.Text(f"Categoría: {cat}", size=13, color=ft.Colors.GREY_700),
                                ft.Text(f"Precio: ${pre:.2f}", size=13, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Stock: {ext}", size=13, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ], spacing=8)
                        page.update()

                    def build_edit_mode():
                        tf_stock = ft.TextField(value=str(ext), label="Nueva Existencia / Stock", width=200)

                        def save_click(e):
                            try:
                                nuevo_stock = int(tf_stock.value.strip())
                                if nuevo_stock < 0:
                                    message_text.value = "El stock no puede ser negativo"
                                    message_text.color = "red"
                                    page.update()
                                    return
                                actualizar_producto_stock(pid, nuevo_stock)
                                message_text.value = f"Stock actualizado correctamente para {nom}"
                                message_text.color = "green"
                                perform_search()
                            except ValueError:
                                message_text.value = "Ingrese un número válido para el stock"
                                message_text.color = "red"
                                page.update()

                        def cancel_click(e):
                            build_view_mode()

                        btn_guardar = ft.Button("Guardar", on_click=save_click, icon=ft.Icons.SAVE)
                        btn_cancelar = ft.Button("Cancelar", on_click=cancel_click, icon=ft.Icons.CANCEL)

                        container.content = ft.Column([
                            ft.Text(f"Producto: {nom} - Código: {cod}", size=13, color=ft.Colors.GREY_700),
                            ft.Row([tf_stock], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([btn_guardar, btn_cancelar], alignment=ft.MainAxisAlignment.END, spacing=10)
                        ], spacing=8)
                        page.update()

                    build_view_mode()

                make_card_handlers(prod_id, codigo, nombre, categoria, precio, existencia, card_container)
                results_column.controls.append(ft.Card(content=card_container))

        page.update()

    search_field.on_change = perform_search
    perform_search()

    def exit_window(e):
        dash_board(page)

    btn_close = ft.Button(
        "Cerrar",
        on_click=exit_window,
        icon=ft.Icons.ARROW_BACK,
        height=45
    )

    def go_add_product(e):
        from views.add_product import main as add_prod_view
        add_prod_view(page)

    btn_add = ft.Button(
        "Registrar Nuevo Producto",
        on_click=go_add_product,
        icon=ft.Icons.ADD_CIRCLE,
        height=45
    )

    search_inputs_row = ft.Row(
        controls=[search_field, btn_add, btn_close],
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
