import flet as ft
from services.database import obtener_ventas, obtener_productos
from views.menu_interface import dash_board


def list_report(page: ft.Page):
    page.controls.clear()
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.title = "Sistema de Consultas"

    def exit_window(e):
        dash_board(page)

    ventas = obtener_ventas()
    productos = obtener_productos()

    content_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def mostrar_productos(e=None):
        content_container.controls.clear()
        filas_productos = []

        for producto in productos:
            filas_productos.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(producto[1])),
                        ft.DataCell(ft.Text(producto[2])),
                        ft.DataCell(ft.Text(producto[3])),
                        ft.DataCell(ft.Text(f"{producto[4]:.2f}")),
                        ft.DataCell(ft.Text(str(producto[5]))),
                    ]
                )
            )

        tabla_productos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Codigo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Categoria", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Existencia", weight=ft.FontWeight.BOLD)),
            ],
            rows=filas_productos
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
                tabla_productos
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def mostrar_ventas(e=None):
        content_container.controls.clear()
        filas = []

        for venta in ventas:
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(venta[0])),
                        ft.DataCell(ft.Text(venta[1])),
                        ft.DataCell(ft.Text(str(venta[2]))),
                        ft.DataCell(ft.Text(f"{venta[3]:.2f}")),
                        ft.DataCell(ft.Text(f"{venta[4]:.2f}")),
                        ft.DataCell(ft.Text(f"{venta[5]:.2f}%")),
                        ft.DataCell(ft.Text(f"{venta[6]:.2f}")),
                    ]
                )
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Codigo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Subtotal", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Descuento", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD)),
            ],
            rows=filas
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
                tabla
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    # Mostrar productos por defecto
    mostrar_productos()

    btn_productos = ft.Button("Ver Lista de Productos", on_click=mostrar_productos, icon=ft.Icons.INVENTORY, height=45)
    btn_ventas = ft.Button("Ver Lista de Ventas", on_click=mostrar_ventas, icon=ft.Icons.RECEIPT_LONG, height=45)
    btnCerrar = ft.Button("Cerrar", on_click=exit_window, icon=ft.Icons.ARROW_BACK, height=45)

    buttons_row = ft.Row([btn_productos, btn_ventas, btnCerrar], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

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
