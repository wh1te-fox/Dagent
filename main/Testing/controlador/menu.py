import flet as ft


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

def main(page: ft.Page):

    page.controls.clear()
    page.title = "Dagent"
    page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
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
                label="register"
            ),

            ft.NavigationRailDestination(
                icon=ft.Icons.PERSON_SEARCH_OUTLINED,
                selected_icon=ft.Icons.PERSON_SEARCH_ROUNDED,
                label= "search"
            ),

            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label= "setting"
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
                
                ft.Container(rail, width=100),
                ft.VerticalDivider(width=1),
                ft.Column(
                    [
                        ft.Text("estadisticas de la tienda"),

                                ft.Image(

                                    src = f"main/Testing/other/freepik__an-elegant-logo-for-revenue-management-with-a-focu__86848.png",

                        #src=f"/icons/icon-512.png",
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN),
                        # ft.Row([], spacing=10),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                    spacing=20,
                ),
            ],
            expand=True,
        )
    )



def cambiar_vista(e, page):


    from Testing.modelo.setting import sett
    from Testing.controlador.entrada import entry_product
    from Testing.modelo.busqueda import search
    from Testing.vista.cliente import client
    
    
    index = e.control.selected_index
    if index == 0:
        main(page)
        # lógica para mostrar Inicio
    elif index == 1:
        entry_product(page)
        # lógica para mostrar Buscar
    elif index == 2:
        client(page)

    elif index == 3: # funciones pendientes
        print("bucar clente")
        search(page)

    elif index == 4: # funcional
        sett(page)       

    elif index == 5: # funcional
        welcome(page)

# ft.app(target=main)