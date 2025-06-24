    def validacion(name_field, nickname_field):

        conn = sqlite3.connect("information.db")
        cur = conn.cursor()

        consult_n = cur.execute("SELECT name FROM customer WHERE name = ?", (name_field.value)
                                ).fetchone()
        
        consult_nk = cur.execute("SELECT lastname FROM customer WRERE lastname = ?", (nickname_field.value)
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

        cur.execute("INSERT INTO customer (name, lastname) VALUES (?, ?)", 
                    (name_field.value, nickname_field.value))
        cur.execute("INSERT INTO inputs (product, valor) VALUES (?,?)", 
                    (product.value, num.value))
        
        conn.commit()
        conn.close()
        print("Client saved successfully!")
            
    save_btn = ft.ElevatedButton(text="Save", on_click= lambda _: save_client(name_field, nickname_field, product, num))
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
