import flet as ft

def actualizar(page: ft.Page):

    from Testing.controlador.menu import main
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