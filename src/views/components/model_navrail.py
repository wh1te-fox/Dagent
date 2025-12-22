import flet as ft 

class NavigationBar:

    def __init__(self, on_changes):
        self.on_changes = on_changes

    def build(self):
        return ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            expand=True,
            on_change=self.on_changes,
            destinations=[
                self.element_destination(
                    "Perfil",
                    ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                    ft.Icons.ACCOUNT_CIRCLE,
                ),
                self.element_destination(
                    "Agregar producto",
                    ft.Icons.ADD_CIRCLE_OUTLINE,
                    ft.Icons.ADD_CIRCLE_OUTLINED
                ),
                self.element_destination(
                    "Registrar producto",
                    ft.Icons.PERSON_ADD_ALT,
                    ft.Icons.PERSON_ADD_ALT_SHARP
                ),
                self.element_destination(
                    "Buscar",
                    ft.Icons.PERSON_SEARCH_OUTLINED,
                    ft.Icons.PERSON_SEARCH_ROUNDED
                ),
                self.element_destination(
                    "Configuración",
                    ft.Icons.SETTINGS_OUTLINED,
                    ft.Icons.SETTINGS
                ),
            ],
        )

    def element_destination(self, label, icons, icon_selected): # label = name icon
        self.element = ft.NavigationRailDestination(
                icon=icons,
                selected_icon=icon_selected,
                label=label
            )
        return self.element
    

