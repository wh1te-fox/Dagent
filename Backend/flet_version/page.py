import flet as ft 
import sqlite3

# from Backend.tkinter_version.registro import consulta_c

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
def welcome(page: ft.Page): # conversion dolares. 
    page.controls.clear()
    page.title = "Welcome"

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    container = ft.Container(
        ft.Column([
            ft.Text(
        "Welcome to Dagent\n"
        "Digital solution for businesses\n"
        "Register your income easily and quickly\n",
        text_align=ft.TextAlign.CENTER, color= "black", size= 18),
        
        ft.ElevatedButton( text="Start",
            on_click=lambda _: main(page)
        )

        ], horizontal_alignment="center"),

        width= 400, height=200, bgcolor= "blue",
        border_radius=18, padding=20,
    )
    
    page.add(container)
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
        group_alignment= - 0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                selected_icon=ft.Icons.ACCOUNT_CIRCLE,
                label="Perfil"
            ),
            
            ft.NavigationRailDestination(
                icon=ft.Icons.ADD_CIRCLE_OUTLINE, # sin entrar
                selected_icon=ft.Icons.ADD_CIRCLE_OUTLINED, # entrando
                label="add product"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PERSON_ADD_ALT,
                selected_icon=ft.Icons.PERSON_ADD_ALT_SHARP,
                label="registrar cliente"
            ),

            ft.NavigationRailDestination(
                icon=ft.Icons.PERSON_SEARCH_OUTLINED,
                selected_icon=ft.Icons.PERSON_SEARCH_ROUNDED,
            ),

            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
            ),
            ft.NavigationBarDestination(
                icon= ft.Icons.ARROW_BACK_IOS_OUTLINED,
                label= "exit"
            ),
        ],
        on_change=lambda e: cambiar_vista(e, page)
    )

    

    page.add(
        ft.Row(
            [
                ft.Container(rail, width=72),
                ft.VerticalDivider(width=1),
                ft.Column(
                    [
                        ft.Text("estadisticas de la tienda"),
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

def cambiar_vista(e, page):
    index = e.control.selected_index
    if index == 0:
        main(page)
        # lógica para mostrar Inicio
    elif index == 1:
        entry_product(page)
        # lógica para mostrar Buscar
    elif index == 2:
        client(page)
    elif index == 3:
        print("bucar clente")
        search(page)
    elif index == 4:
        setting(page)
    elif index == 5:
        welcome(page)

# Settings Page
def setting(page: ft.Page):
    page.controls.clear()
    page.title = "Settings"


    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()
    # def app():


    page.theme_mode = ft.ThemeMode.LIGHT

    theme_swith = ft.Switch(
        label="Cambia al modo oscuro", 
        label_position=ft.LabelPosition.LEFT, 
        on_change=theme_changed
        )
    '''c2 = ft.Switch(
        label= "sistema de credito\n" \
        "puedes activar o descativar para tener un sistem de creditos"
        label_position= ft.LabelPosition=LEFT,
        on_change=
    )'''


    
    btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))
    page.add(theme_swith, btn)
    page.update()
def actualizar(page: ft.Page):
    page.controls.clear()
    
    page.title = "actualizar cliente"

    product = ft.TextField (label= "product", width= 100)
    num = ft.TextField (label="precio", width= 100)
    but = ft.Button (text="save", width= 100)
    ex = ft.Button (text= "exit", on_click= lambda _: main(page))

                # data
            
    page.add(product, num, but, ex)
    page.add( ft.Text ("contelido aqui"))

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

    def save_product(product_name, product_price):
        var = product_name.value
        num = product_price.value

        try:
            if var and float(num) > 0:

                conn = sqlite3.connect("information.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO inputs (product, valor) VALUES (?,?)",
                (product_name.value, float(product_price.value)))
                conn.commit()
                conn.close()
                print("good")
                page.add(ft.Text("se guardo correctamente"))
                page.update()

        except:
            print("confirme la entradas")
            page.add (ft.Text("error"))
            page.update()

def client(page: ft.Page):
    page.controls.clear()
    page.title = "New Client"

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    name_field = ft.TextField(label="First Name", width=200)
    nickname_field = ft.TextField(label="Nickname", width=200)
    product = ft.TextField (label= "product", width= 100)
    num = ft.TextField (label="precio", width= 100)

    def validacion(name_field, nickname_field):

        conn = sqlite3.connect("information.db")
        cur = conn.cursor()

        consult_n = cur.execute("SELECT name FROM customer WHERE = ?", (name_field.value)
                                ).fetchone()
        
        consult_nk = cur.execute("SELECT name FROM customer WRERE = ?", (nickname_field.value)
                                 ).fetchall
 
        n = name_field.value
        nk = nickname_field.value

        
        conn.close()

        if n == consult_n and nk == consult_nk:
            
            page.add(
                ft.Text("El cliente ya existe. ¿Desea actualizarlo?"),
                ft.ElevatedButton(text="Actualizar", on_click=lambda _: actualizar(page))
            )


        else:
            save_client()
            print("finalizado")



        # Save Client to DB
    def save_client(name_field, nickname_field, product, num):
        conn = sqlite3.connect("information.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO customer (name, nickname) VALUES (?, ?)", 
                    (name_field.value, nickname_field.value))
        cur.execute("INSERT INTO inputs (product, valor) VALUES (?,?)", 
                    (product.value, num.value))
        
        conn.commit()
        conn.close()
        print("Client saved successfully!")
            
    save_btn = ft.ElevatedButton(text="Save", on_click= lambda _: validacion(name_field, nickname_field))
    exit_btn = ft.ElevatedButton(text="Exit", on_click= lambda _: main(page))
    
    row = ft.Row(
        controls=[
            ft.Column([
                name_field, nickname_field, save_btn
            ]),
            ft.Column([
                product, num, exit_btn
            ])
        ],
        spacing= 50,
        alignment=ft.MainAxisAlignment.CENTER
    )
    page.add(row)
    page.update()




# Placeholder for consultation page
def consult_sale(page: ft.Page):
    page.controls.clear()

    conn = sqlite3.connect("information.db")
    cur = conn.cursor()

    lis = cur.execute('''
    SELECT description, price FROM product''').fetchall()

    #page.add(*lis)
    conn.close()

    exit_btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))
    page.add(exit_btn)

    page.update()



# lista de clientes
def search(page: ft.Page):
    page.controls.clear()
    page.update()

    entry_name = ft.TextField(label="name client", width = 150)
    entry_nick = ft.TextField(label="nickname client", width = 150)

    conn = sqlite3.connect("information.db")
    cur = conn.cursor()
    cur.execute("SELECT name, nickname, date FROM customer")
    products = cur.fetchall()
    conn.close()

    product_list = [
        ft.Text(f"{prod[0]} - {prod[1]} : {prod[2]}") for prod in products
    ]

    exit_btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))

    search_e = ft.Row(
        controls=[
            ft.Column(
                [
                    ft.IconButton(
                        icon=ft.Icons.SEARCH_OUTLINED,
                        icon_color = ft.Colors.GREEN_300,
                        on_click= lambda _:search_c (entry_name, entry_nick),
                        tooltip="search"
                    )
                ]
            )
        ],
    )
    search_setting = ft.Row(
        controls=[
            ft.Column([entry_name]),
            ft.Column([entry_nick]),
            ft.Column([search_e])

            ],
            spacing= 50,
            alignment=ft.MainAxisAlignment.CENTER
        )
    
    page.add (ft.Text("Clientes", size=30, weight=ft.FontWeight.W_900, selectable=True), search_setting)

    page.add(*product_list, exit_btn)
    
    
    page.update()

    def search_c(entry_name, entry_nick):

        conn = sqlite3.connect("information.db")
        cur = conn.cursor()

        cont = cur.execute('''
        SELECT name, nickname FROM customer WHERE name=? AND nickname=?''',
        (entry_name.value, entry_nick.value)).fetchall()

        conn.close()

        if cont:
            """controls = ft.Row(
                controls=[
                    ft.Column([
                        page.add( ft.Text(cont))]),

                    ft.Column([
                        page.add(ft.Button(text="editar", on_click= lambda _: test()))]
                    )
                ],
                alignment= ft.MainAxisAlignment.CENTER
            ) """


            b = ft.Button(text="editar", on_click= lambda _: actualizar(entry_name, entry_nick))
            a = ft.Text(cont)

            controls = ft.Row(
                controls=[
                    ft.Column([a]),
                    ft.Column([b])
                ], alignment= ft.MainAxisAlignment.CENTER, spacing= 100
            )
            page.add(controls)


        
        else:
            print("intenta de nuevo")
                

# Initialize Database
create_table()

# Run the Flet application
ft.app(target=main)