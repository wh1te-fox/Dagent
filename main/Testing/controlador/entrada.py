import flet as ft
import sqlite3


# Product Entry Page
def entry_product(page: ft.Page):
    from Testing.controlador.menu import dash_board

    page.controls.clear()
    page.title = "Register Product"

    product_name = ft.TextField(label="Product Name", width=300, border_radius=10)
    product_price = ft.TextField(label="Price", width=300, border_radius=10)

    save_button = ft.ElevatedButton(text="Save", on_click=lambda _: save_product())
    exit_button = ft.ElevatedButton(text="Exit", on_click=lambda _: dash_board(page))

    page.add(product_name, product_price, save_button, exit_button)
    page.update()

    def save_product():
        var = product_name.value
        num = float(product_price.value)

        conn = sqlite3.connect("information.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO sale (Producto, precio) VALUES (?,?)",
        (product_name.value, int(product_price.value)))
        conn.commit()
        conn.close()

        print("good")
        page.add(ft.Text("se guardo correctamente"))
        page.update()

        
        try:
            if var and num > 0:

                conn = sqlite3.connect("information.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO sale (product, valor) VALUES (?,?)",
                (var, float(num)))
                conn.commit()
                conn.close()
                print("good")
                page.add(ft.Text("se guardo correctamente"))
                page.update()

        except:
            print("confirme la entradas")
            page.add (ft.Text("Verifique si las entradas son corectas"))
            page.update()

