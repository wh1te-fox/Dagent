import flet as ft
import sqlite3

# Product Entry Page
def entry_product(page: ft.Page):
    from Testing.controlador.menu import dash_board

    # Limpiar solo el área de contenido si usas NavigationRail, o todo si no
    page.controls.clear()
    page.title = "Register Product"

    # Campos de entrada
    product_name = ft.TextField(label="Product Name", width=300, border_radius=10)
    product_price = ft.TextField(label="Price", width=300, border_radius=10)

    # Función para guardar
    def save_product(e):
        try:
            var = product_name.value.strip()
            num = float(product_price.value.strip())

            if not var or num <= 0:
                raise ValueError("Datos inválidos")

            conn = sqlite3.connect("information.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO sale (Producto, precio) VALUES (?, ?)", (var, num))
            conn.commit()
            conn.close()

            # Limpiar campos
            product_name.value = ""
            product_price.value = ""

            # Mostrar mensaje
            page.snack_bar = ft.SnackBar(ft.Text("Se guardó correctamente"), open=True)
            page.update()

        except Exception as e:
            print(f"Error al guardar: {e}")
            page.snack_bar = ft.SnackBar(ft.Text("Verifique las entradas"), open=True)
            page.update()

    # Botones
    save_button = ft.ElevatedButton(text="Save", on_click=save_product)
    exit_button = ft.ElevatedButton(text="Exit", on_click=lambda _: dash_board(page))

    # Agregar a la página
    page.add(
        ft.Column(
            controls=[product_name, product_price, save_button, exit_button],
            spacing=10
        )
    )
    page.update()
