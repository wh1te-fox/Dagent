"""Inventory management and stock view module."""
import flet as ft
from views.components import section
from views.menu_interface import dash_board
from services.database import actualizar_producto_stock, buscar_productos, obtener_productos


def inventory_page(page: ft.Page):
    """Renders the inventory interface with product search and stock management."""
    section.setup(page, "Gestión de Inventario")

    search_field = section.input("Buscar por código, nombre o categoría", icon=ft.Icons.SEARCH)

    summary_row = ft.Row(spacing=15, run_spacing=15, wrap=True, alignment=ft.MainAxisAlignment.CENTER)
    message_text = ft.Text("", size=14)
    results_column = ft.Column(
        [],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def cargar_resumen():
        products = obtener_productos()
        summary_row.controls = [
            section.stat_card("Productos", str(len(products)), ft.Icons.INVENTORY_2_OUTLINED, section.ACCENT),
            section.stat_card(
                "Valor del inventario",
                f"${sum(p[4] * p[5] for p in products):.2f}",
                ft.Icons.REQUEST_QUOTE_OUTLINED,
                ft.Colors.GREEN_400,
            ),
            section.stat_card(
                "Bajo stock",
                str(sum(1 for p in products if p[5] <= 5)),
                ft.Icons.WARNING_AMBER_OUTLINED,
                ft.Colors.ORANGE_400,
            ),
        ]

    def update_stock(pid, nuevo_stock, nombre):
        actualizar_producto_stock(pid, nuevo_stock)
        message_text.value = f"Stock actualizado correctamente para {nombre}"
        message_text.color = "green"
        perform_search()

    def perform_search(e=None):
        termino = search_field.value.strip() if search_field.value else ""
        message_text.value = ""
        results_column.controls.clear()

        productos = buscar_productos(termino) if termino else obtener_productos()

        if not productos:
            message_text.value = "No se encontraron productos"
            message_text.color = "red"
            results_column.controls.append(
                section.empty_state("No hay productos que coincidan", ft.Icons.INVENTORY_2_OUTLINED)
            )
        else:
            message_text.value = f"Se encontraron {len(productos)} producto(s)"
            message_text.color = "green"

            for prod in productos:
                prod_id, codigo, nombre, categoria, precio, existencia = prod
                card_container = section.result_card(ft.Column(spacing=8))

                def make_stock_card(pid, cod, nom, cat, pre, ext, container):
                    stock_input = section.input("Nueva Existencia / Stock", width=200)

                    def update_stock_action(e):
                        try:
                            nuevo_stock = int(stock_input.value.strip())
                            if nuevo_stock < 0:
                                stock_input.error_text = "El stock no puede ser negativo"
                                page.update()
                                return
                            message_text.value = f"Stock actualizado correctamente para {nom}"
                            message_text.color = "green"
                            actualizar_producto_stock(pid, nuevo_stock)
                            perform_search()
                        except ValueError:
                            stock_input.error_text = "Ingrese un número válido para el stock"
                            page.update()

                    def build_view_mode():
                        container.content = ft.Column([
                            ft.Row([
                                ft.Row([
                                    ft.Icon(ft.Icons.INVENTORY_2, color=section.ACCENT),
                                    ft.Text(f"{nom} ({cod})", weight=ft.FontWeight.BOLD, size=16),
                                ], spacing=10),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Actualizar Stock",
                                    on_click=build_edit_mode,
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([
                                ft.Text(f"Categoría: {cat}", size=13, color=ft.Colors.GREY_700),
                                ft.Text(f"Precio: ${pre:.2f}", size=13, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Stock: {ext}", size=13, color=section.ACCENT, weight=ft.FontWeight.BOLD),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ], spacing=8)

                    def build_edit_mode(e=None):
                        stock_input.error_text = None
                        container.content = ft.Column([
                            ft.Text(f"Producto: {nom} - Código: {cod}", size=13, color=ft.Colors.GREY_700),
                            ft.Row([stock_input], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([
                                section.primary_button(ft.Button("Guardar", on_click=update_stock_action, icon=ft.Icons.SAVE)),
                                section.secondary_button(ft.Button("Cancelar", on_click=lambda e: build_view_mode(), icon=ft.Icons.CANCEL)),
                            ], alignment=ft.MainAxisAlignment.END, spacing=10),
                        ], spacing=8)
                        page.update()

                    build_view_mode()

                make_stock_card(prod_id, codigo, nombre, categoria, precio, existencia, card_container)
                results_column.controls.append(ft.Row([card_container], alignment=ft.MainAxisAlignment.CENTER))

        cargar_resumen()
        page.update()

    search_field.on_change = perform_search
    perform_search()

    def go_productos(e):
        layout = getattr(page, "_app_layout", None)
        if layout is not None:
            layout.open_section("products")
        else:
            from views.add_product import main as add_prod_view
            add_prod_view(page)

    btn_add = section.secondary_button(ft.Button("Registrar Nuevo Producto", on_click=go_productos, icon=ft.Icons.ADD_CIRCLE, height=45))
    btn_close = section.secondary_button(ft.Button("Cerrar", on_click=lambda e: dash_board(page), icon=ft.Icons.ARROW_BACK, height=45))

    page.add(
        section.header(
            ft.Icons.STORAGE,
            "Gestión de Inventario",
            "Busca productos y actualiza su existencia",
        ),
        section.spacer(16),
        summary_row,
        section.spacer(16),
        section.buttons_row([search_field, btn_add, btn_close]),
        section.spacer(10),
        message_text,
        section.spacer(10),
        results_column,
    )
    page.update()
