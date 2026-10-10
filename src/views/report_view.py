"""Reports view module for viewing sales and product inventories."""
import flet as ft
from services.database import obtener_productos, obtener_ventas
from views.menu_interface import dash_board


def list_report(page: ft.Page):
    """Renders the reports and queries interface."""
    page.controls.clear()
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.title = "Sistema de Consultas"

    def exit_window(e):
        dash_board(page)

    sales = obtener_ventas()
    products = obtener_productos()

    content_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def show_products(e=None):
        content_container.controls.clear()
        product_rows = []

        for product in products:
            product_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(product[1])),
                        ft.DataCell(ft.Text(product[2])),
                        ft.DataCell(ft.Text(product[3])),
                        ft.DataCell(ft.Text(f"{product[4]:.2f}")),
                        ft.DataCell(ft.Text(str(product[5]))),
                    ]
                )
            )

        table_products = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Codigo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Categoria", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Existencia", weight=ft.FontWeight.BOLD)),
            ],
            rows=product_rows
        )

        content_container.controls.append(
            ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, color=ft.Colors.BLUE_400),
                    ft.Text(
                        "Lista de Productos",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE
                    )
                ], spacing=10),
                ft.Divider(),
                table_products
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def show_sales(e=None):
        content_container.controls.clear()
        sales_rows = []

        for sale in sales:
            sales_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(sale[0])),
                        ft.DataCell(ft.Text(sale[1])),
                        ft.DataCell(ft.Text(str(sale[2]))),
                        ft.DataCell(ft.Text(f"{sale[3]:.2f}")),
                        ft.DataCell(ft.Text(f"{sale[4]:.2f}")),
                        ft.DataCell(ft.Text(f"{sale[5]:.2f}%")),
                        ft.DataCell(ft.Text(f"{sale[6]:.2f}")),
                    ]
                )
            )

        table_sales = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Codigo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Subtotal", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Descuento", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD)),
            ],
            rows=sales_rows
        )

        content_container.controls.append(
            ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.RECEIPT_LONG, color=ft.Colors.BLUE_400),
                    ft.Text(
                        "Lista de Ventas",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE
                    )
                ], spacing=10),
                ft.Divider(),
                table_sales
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    show_products()

    btn_products = ft.Button("Ver Lista de Productos", on_click=show_products, icon=ft.Icons.INVENTORY, height=45)
    btn_sales = ft.Button("Ver Lista de Ventas", on_click=show_sales, icon=ft.Icons.RECEIPT_LONG, height=45)
    btn_close = ft.Button("Cerrar", on_click=exit_window, icon=ft.Icons.ARROW_BACK, height=45)

    buttons_row = ft.Row([btn_products, btn_sales, btn_close], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    header_row = ft.Row([
        ft.Icon(ft.Icons.ASSESSMENT, size=32, color=ft.Colors.BLUE),
        ft.Text("Sistema de Consultas", size=30, weight=ft.FontWeight.W_900, selectable=True)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    report_card = ft.Card(
        content=ft.Container(
            content=content_container,
            padding=20,
            height=450,
            width=900
        )
    )

    page.add(
        header_row,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        buttons_row,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        report_card
    )
    page.update()

