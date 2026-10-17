"""Sales history view with filters and summary of registered sales."""
import flet as ft
from services.database import obtener_ventas
from views.components import section


def show(page):
    """Renders the sales history interface with filters and totals."""
    section.setup(page, "Ventas e historial")

    filter_dropdown = ft.Dropdown(
        label="Filtrar por",
        value="todas",
        options=[
            ft.dropdown.Option("todas", "Todas"),
            ft.dropdown.Option("fecha", "Día específico"),
            ft.dropdown.Option("semana", "Última semana"),
            ft.dropdown.Option("mes", "Este mes"),
            ft.dropdown.Option("personalizada", "Rango personalizado"),
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
    list_container = ft.Column([], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def load_history(e=None):
        filtro = filter_dropdown.value
        valor = date_input.value.strip() if date_input.value else None
        valor_hasta = date_input_hasta.value.strip() if date_input_hasta.value else None
        ventas = obtener_ventas(filtro, valor, valor_hasta)

        total = sum(sale[6] for sale in ventas)
        unidades = sum(sale[2] for sale in ventas)

        summary_row.controls = [
            section.stat_card("Ventas", str(len(ventas)), ft.Icons.RECEIPT_LONG_OUTLINED, section.ACCENT),
            section.stat_card("Total vendido", f"${total:.2f}", ft.Icons.PAYMENTS_OUTLINED, ft.Colors.GREEN_400),
            section.stat_card("Unidades", str(unidades), ft.Icons.STACKED_LINE_CHART, ft.Colors.AMBER_400),
        ]

        list_container.controls.clear()

        if not ventas:
            list_container.controls.append(
                section.empty_state(
                    "No hay ventas registradas para el filtro seleccionado",
                    ft.Icons.RECEIPT_LONG_OUTLINED,
                )
            )
        else:
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(sale[7]))),
                        ft.DataCell(ft.Text(str(sale[0]))),
                        ft.DataCell(ft.Text(str(sale[1]))),
                        ft.DataCell(ft.Text(str(sale[2]))),
                        ft.DataCell(ft.Text(f"{sale[3]:.2f}")),
                        ft.DataCell(ft.Text(f"{sale[5]:.2f}%")),
                        ft.DataCell(ft.Text(f"{sale[6]:.2f}", weight=ft.FontWeight.BOLD)),
                    ]
                )
                for sale in ventas
            ]
            list_container.controls.append(
                section.card(
                    section.table_wrapper(
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Código", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Desc.", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD)),
                            ],
                            rows=rows,
                        )
                    ),
                    width=section.CONTENT_WIDTH,
                    padding=16,
                )
            )
        page.update()

    filter_button = section.primary_button(
        ft.Button("Filtrar", on_click=load_history, icon=ft.Icons.FILTER_LIST)
    )

    filters_row = ft.Row(
        [filter_dropdown, date_input, date_input_hasta, filter_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        wrap=True,
        run_spacing=10,
    )

    page.add(
        section.header(ft.Icons.RECEIPT_LONG_OUTLINED, "Ventas e historial", "Registro completo de ventas con filtros"),
        section.spacer(16),
        summary_row,
        section.spacer(16),
        filters_row,
        section.spacer(16),
        list_container,
    )

    load_history()
    page.update()
