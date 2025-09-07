import flet as ft

def dash_board(page: ft.Page): # ventana principal
    page.controls.clear()
    page.title = "Dagent"
    page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment= - 0.9,
        expand= True,
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

    page.add(rail)

    def cambiar_vista(e, page):

        #from Code.controlador.entrada import entry_product
        from Code.controlador.entrada import entry_product
        from Code.modelo.setting import sett
        from Code.modelo.busqueda import search
        from Code.other.cliente import client

        index = e.control.selected_index
        if index == 0:  # pagina principal
            dash_board(page)  
 
        elif index == 1:  # funciones pendientes
            entry_product(page)

        elif index == 2:
            client(page)

        elif index == 3: # funciones pendientes
            search(page)

        elif index == 4: # funcional
            sett(page)     

