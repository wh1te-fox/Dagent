"""Reports view module for viewing sales and product inventories."""
import flet as ft
from services.database import obtener_productos, obtener_ventas
from views.menu_interface import dash_board


def _ancho_disponible(page, margen=120):
    """Returns the usable content width according to the current window size."""
    layout = getattr(page, "_app_layout", None)
    sidebar = 78 if (layout is not None and not getattr(layout, "expanded", True)) else 245

    ancho_ventana = page.width if isinstance(page.width, (int, float)) and page.width > 0 else 1200
    ancho = int(ancho_ventana) - sidebar - margen

    return max(420, min(ancho, 900))


def list_report(page: ft.Page):
    """Renders the reports and queries interface."""
    from views.components import section

    section.setup(page, "Reportes")

    def exit_window(e):
        dash_board(page)

    vista_actual = "productos"

    content_container = ft.Column([], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)

    def show_products(e=None):
        nonlocal vista_actual
        vista_actual = "productos"

        content_container.controls.clear()

        products = obtener_productos()
        ancho_tabla = _ancho_disponible(page)

        product_rows = []
        for product in products:
            product_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(product[1])),
                        ft.DataCell(ft.Text(product[2])),
                        ft.DataCell(ft.Text(product[3])),
                        ft.DataCell(ft.Text(f"{product[4]:.2f}", weight=ft.FontWeight.BOLD, selectable=True)),
                        ft.DataCell(
                            ft.Text(
                                str(product[5]),
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_700 if product[5] > 0 else ft.Colors.RED_700,
                            )
                        ),
                    ]
                )
            )

        resumen_row = ft.Row(
            [
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
            ],
            spacing=15,
            run_spacing=15,
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        table_products = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Categoría", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Existencia", weight=ft.FontWeight.BOLD)),
            ],
            rows=product_rows,
        )

        content_container.controls.append(
            ft.Column([
                resumen_row,
                section.spacer(4),
                ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, color=section.ACCENT),
                    ft.Text(
                        "Lista de Productos",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=section.ACCENT
                    )
                ], spacing=10),
                ft.Divider(),
                section.card(
                    section.table_wrapper(table_products, width=ancho_tabla),
                    width=ancho_tabla + 16,
                    padding=8,
                ) if product_rows else
                section.empty_state("No hay productos registrados", ft.Icons.INVENTORY_2_OUTLINED)
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def show_sales(e=None):
        nonlocal vista_actual
        vista_actual = "ventas"

        content_container.controls.clear()
        ancho_tabla = _ancho_disponible(page)

        filter_dropdown = ft.Dropdown(
            label="Filtrar por",
            value="todas",
            options=[
                ft.dropdown.Option("todas", "Todas"),
                ft.dropdown.Option("fecha", "Fecha específica"),
                ft.dropdown.Option("personalizada", "Rango personalizado"),
                ft.dropdown.Option("semana", "Esta semana"),
                ft.dropdown.Option("mes", "Este mes"),
            ],
            width=210,
            border_radius=10,
        )

        date_input = ft.TextField(
            label="Fecha",
            hint_text="AAAA-MM-DD",
            width=150,
            border_radius=10,
            visible=False,
        )

        date_input_hasta = ft.TextField(
            label="Hasta",
            hint_text="AAAA-MM-DD",
            width=150,
            border_radius=10,
            visible=False,
        )

        def on_filter_change(e):
            val = filter_dropdown.value
            date_input.visible = val in ("fecha", "personalizada")
            date_input_hasta.visible = val == "personalizada"
            date_input.label = "Desde" if val == "personalizada" else "Fecha"
            page.update()

        filter_dropdown.on_select = on_filter_change

        summary_row = ft.Row(spacing=15, run_spacing=15, wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        tabla_holder = ft.Column([], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        def load_sales_table(e=None):
            filtro = filter_dropdown.value
            valor = date_input.value.strip() if date_input.value else None
            valor_hasta = date_input_hasta.value.strip() if date_input_hasta.value else None

            if filtro in ("fecha", "personalizada") and not valor:
                tabla_holder.controls.clear()
                tabla_holder.controls.append(
                    section.empty_state(
                        "Ingrese una fecha (AAAA-MM-DD) para filtrar",
                        ft.Icons.CALENDAR_MONTH_OUTLINED,
                    )
                )
                page.update()
                return

            ventas_filtradas = obtener_ventas(filtro, valor, valor_hasta)

            total_vendido = sum(sale[6] for sale in ventas_filtradas)
            unidades = sum(sale[2] for sale in ventas_filtradas)
            total_descuento = sum(sale[4] for sale in ventas_filtradas)

            summary_row.controls = [
                section.stat_card("Ventas en el filtro", str(len(ventas_filtradas)), ft.Icons.RECEIPT_LONG_OUTLINED, section.ACCENT),
                section.stat_card("Total vendido", f"${total_vendido:.2f}", ft.Icons.PAYMENTS_OUTLINED, ft.Colors.GREEN_400),
                section.stat_card("Unidades", str(unidades), ft.Icons.STACKED_LINE_CHART, ft.Colors.AMBER_400),
                section.stat_card("Descuentos aplicados", f"${total_descuento:.2f}", ft.Icons.PERCENT, ft.Colors.PURPLE_400),
            ]

            sales_rows = []
            for sale in ventas_filtradas:
                sales_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(sale[7]))),
                            ft.DataCell(ft.Text(str(sale[0]))),
                            ft.DataCell(ft.Text(str(sale[1]))),
                            ft.DataCell(ft.Text(str(sale[2]))),
                            ft.DataCell(ft.Text(f"{sale[3]:.2f}")),
                            ft.DataCell(ft.Text(f"{sale[5]:.2f}%")),
                            ft.DataCell(ft.Text(f"{sale[6]:.2f}", weight=ft.FontWeight.BOLD, selectable=True)),
                        ]
                    )
                )

            tabla_holder.controls.clear()
            if sales_rows:
                tabla_holder.controls.append(
                    section.card(
                        section.table_wrapper(
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Código", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Cant.", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Subtotal", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Desc.", weight=ft.FontWeight.BOLD)),
                                    ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD)),
                                ],
                                rows=sales_rows,
                            ),
                            width=ancho_tabla,
                        ),
                        width=ancho_tabla + 16,
                        padding=8,
                    )
                )
            else:
                tabla_holder.controls.append(
                    section.empty_state("No hay ventas para el filtro seleccionado", ft.Icons.RECEIPT_LONG_OUTLINED)
                )

            page.update()

        filter_dropdown.on_select = on_filter_change

        def on_date_picked(e):
            fecha = e.control.value
            fecha_str = fecha.strftime("%Y-%m-%d") if hasattr(fecha, "strftime") else str(fecha)[:10]
            filter_dropdown.value = "fecha"
            date_input.value = fecha_str
            on_filter_change(None)
            load_sales_table()

        date_picker = ft.DatePicker(
            on_change=on_date_picked,
            help_text="Seleccione la fecha de las ventas",
        )

        def open_date_picker(e):
            page.show_dialog(date_picker)

        date_button = section.secondary_button(
            ft.Button(
                "Elegir fecha",
                icon=ft.Icons.CALENDAR_MONTH_OUTLINED,
                on_click=open_date_picker,
            )
        )

        btn_buscar = section.primary_button(
            ft.Button("Filtrar", on_click=load_sales_table, icon=ft.Icons.FILTER_LIST)
        )

        filters_row = ft.Row(
            [filter_dropdown, date_input, date_input_hasta, date_button, btn_buscar],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
            wrap=True,
            run_spacing=10,
        )

        filter_dropdown.value = "todas"
        load_sales_table()

        content_container.controls.append(
            ft.Column([
                summary_row,
                section.spacer(4),
                ft.Row([
                    ft.Icon(ft.Icons.RECEIPT_LONG, color=section.ACCENT),
                    ft.Text(
                        "Lista de Ventas",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=section.ACCENT
                    )
                ], spacing=10),
                ft.Divider(),
                filters_row,
                section.spacer(10),
                tabla_holder,
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def on_resize(e):
        layout = getattr(page, "_app_layout", None)
        if layout is None or layout.active_key != "reports":
            return
        if vista_actual == "productos":
            show_products()
        else:
            show_sales()

    page.on_resize = on_resize

    show_products()

    btn_products = ft.Button("Ver Lista de Productos", on_click=show_products, icon=ft.Icons.INVENTORY, height=45)
    btn_sales = section.secondary_button(ft.Button("Ver Lista de Ventas", on_click=show_sales, icon=ft.Icons.RECEIPT_LONG, height=45))
    section.primary_button(btn_products)
    btn_close = section.secondary_button(ft.Button("Cerrar", on_click=exit_window, icon=ft.Icons.ARROW_BACK, height=45))

    buttons_row = ft.Row(
        [btn_products, btn_sales, btn_close],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        wrap=True,
        run_spacing=10,
    )

    header_row = section.header(
        ft.Icons.ASSESSMENT,
        "Reportes",
        "Consultas de productos y ventas registradas"
    )

    report_card = section.card(content_container, width=_ancho_disponible(page), padding=20)

    page.add(
        header_row,
        section.spacer(16),
        buttons_row,
        section.spacer(16),
        report_card
    )
    page.update()
