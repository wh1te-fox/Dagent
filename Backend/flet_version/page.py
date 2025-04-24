import flet as ft
import sqlite3

# Start Database (SQLite)
def create_table():
    conn = sqlite3.connect('information.db')
    cur = conn.cursor()

    # N:N Relationship between sale and product
    cur.execute('''
    CREATE TABLE IF NOT EXISTS sale (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        total REAL NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS sale_product (
        sale_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (sale_id) REFERENCES sale(id),
        FOREIGN KEY (product_id) REFERENCES product(id),
        PRIMARY KEY (sale_id, product_id)
    )
    ''')

    # 1:N Relationship between customer and shopping
    cur.execute('''
    CREATE TABLE IF NOT EXISTS customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        name TEXT NOT NULL,
        nickname TEXT NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS shopping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        total REAL NOT NULL,
        customer_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customer(id)
    )
    ''')

    conn.commit()
    conn.close()

# Welcome Page
def welcome(page: ft.Page):
    page.controls.clear()
    page.title = "Welcome"

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(ft.Text(
        "Welcome to Dagent\n"
        "Digital solution for businesses\n"
        "Register your income easily and quickly\n",
        text_align=ft.TextAlign.CENTER
    ))
    page.add(
        ft.ElevatedButton(
            text="Start",
            on_click=lambda _: main(page)
        )
    )
    page.update()

# Main Page
def main(page: ft.Page):
    page.title = "Dagent"
    page.controls.clear()

    btn_data = ft.ElevatedButton(text="Add Product", on_click=lambda _: entry_product(page))
    btn_client = ft.ElevatedButton(text="New Client", on_click=lambda _: client(page))
    btn_exit = ft.ElevatedButton(text="Exit", on_click=lambda _: welcome(page))
    btn_consult = ft.ElevatedButton(text="Consult", on_click=lambda _: consult_sale(page))

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=72,
        min_extended_width=180,
        group_alignment=0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
            ),
        ],
        on_change=lambda e: setting(page)
    )

    page.add(
        ft.Row(
            [
                ft.Container(rail, width=72),
                ft.VerticalDivider(width=1),
                ft.Column(
                    [
                        ft.Text("Main content goes here"),
                        ft.Row([btn_data, btn_client, btn_consult, btn_exit], spacing=10),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                    spacing=20,
                ),
            ],
            expand=True,
        )
    )

    
    page.update()

# Settings Page
def setting(page: ft.Page):
    page.controls.clear()
    page.title = "Settings"

    btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))
    page.add(btn)
    
    page.update()

# Product Entry Page
def entry_product(page: ft.Page):
    page.controls.clear()
    page.title = "Register Product"

    product_name = ft.TextField(label="Product Name", width=300)
    product_price = ft.TextField(label="Price", width=300)

    save_button = ft.ElevatedButton(text="Save", on_click=lambda _: save_product(product_name, product_price))
    exit_button = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))

    page.add(product_name, product_price, save_button, exit_button)
    page.update()

# Save Product to DB
def save_product(name_field, price_field):
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO product (description, price) VALUES (?, ?)
    ''', (name_field.value, float(price_field.value)))
    conn.commit()
    conn.close()
    print("Product saved successfully!")

# Client Entry Page
def client(page: ft.Page):
    page.controls.clear()
    page.title = "New Client"

    name_field = ft.TextField(label="First Name", width=200)
    nickname_field = ft.TextField(label="Nickname", width=200)

    save_btn = ft.ElevatedButton(text="Save", on_click=lambda _: save_client(name_field, nickname_field))
    exit_btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))

    page.add(name_field, nickname_field, save_btn, exit_btn)
    page.update()

# Save Client to DB
def save_client(name_field, nickname_field):
    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO customer (name, nickname) VALUES (?, ?)
    ''', (name_field.value, nickname_field.value))
    conn.commit()
    conn.close()
    print("Client saved successfully!")

# Placeholder for consultation page
def consult_sale(page: ft.Page):
    page.controls.clear()
    exit_btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))
    page.add(exit_btn)
    page.update()

# Initialize Database
create_table()

# Run the Flet application
ft.app(target=main)
