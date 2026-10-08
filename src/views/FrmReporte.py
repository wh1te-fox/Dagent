import flet as ft
from services.database import obtener_ventas, obtener_productos
from views.menu_interface import dash_board


def list_report(page: ft.Page):
    page.controls.clear()
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    def exit_window(e):
        dash_board(page)

    ventas = obtener_ventas()
    productos = obtener_productos()

    content_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

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
                ft.DataColumn(ft.Text("Codigo")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Existencia")),
            ],
            rows=filas_productos
        )

        content_container.controls.append(
            ft.Column([
                ft.Text(
                    "Lista de Productos",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE
                ),
                tabla_productos
            ], spacing=10)
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
                ft.DataColumn(ft.Text("Codigo")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Subtotal")),
                ft.DataColumn(ft.Text("Descuento")),
                ft.DataColumn(ft.Text("Total")),
            ],
            rows=filas
        )

        content_container.controls.append(
            ft.Column([
                ft.Text(
                    "Lista de Ventas",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE
                ),
                tabla
            ], spacing=10)
        )
        page.update()

    # Mostrar productos por defecto
    mostrar_productos()

    btn_productos = ft.Button("Ver Lista de Productos", on_click=mostrar_productos, icon=ft.Icons.INVENTORY)
    btn_ventas = ft.Button("Ver Lista de Ventas", on_click=mostrar_ventas, icon=ft.Icons.RECEIPT_LONG)
    btnCerrar = ft.Button("Cerrar", on_click=exit_window)

    buttons_row = ft.Row([btn_productos, btn_ventas, btnCerrar], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    page.add(
        ft.Text(
            "Sistema de Consultas",
            size=30,
            weight=ft.FontWeight.W_900,
        ),
        ft.Divider(height=20),
        buttons_row,
        ft.Divider(height=20),
        content_container
    )
    page.update()
