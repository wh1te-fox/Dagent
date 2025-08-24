  #conn = sqlite3.connect("information.db")
    conn = sqlite3.connect("testing.db")
    cur = conn.cursor()
    cur.execute("SELECT name, lastname, date FROM customer")
    products = cur.fetchall()
    conn.close()

    product_list = [
        ft.Text(f"{prod[0]} - {prod[1]} : {prod[2]}") for prod in products
    ]

    for cliente_id, nombre in products:
        
        def abonar_click (id = cliente_id):
            page.snack_bar = ft.SnackBar(ft.Text(f"abonoar a {nombre} (id = {id})"))
            page.snack_bar.open = True
            page.update()
    #exit_btn = ft.ElevatedButton(text="Exit", on_click=lambda _: main(page))

        fila = ft.Row ([
            ft.Text(nombre),
            ft.ElevatedButton ("abonar", on_click= lambda id = cliente_id: abonar_click(id))
        ])
        page.controls.append(fila)