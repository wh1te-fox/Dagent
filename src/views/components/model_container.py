import flet as ft


# encapsular contendore
# usar contenesores
# iterar contenedores
# retornar uno por cada cliente

    page.add(
   
                    ft.Container(
                        bgcolor=ft.Colors.SURFACE_TINT,
                        padding=20,
                        width=300,
                        content=ft.Button("Page theme button"),
                    ),
                    # Inherited theme with primary color overridden
                    ft.Container(
                        theme=ft.Theme(
                            color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)
                        ),
                        bgcolor=ft.Colors.SURFACE_TINT,
                        padding=20,
                        width=300,
                        content=ft.Button("Inherited theme button"),
                    ),
                    # Unique always DARK theme
                    ft.Container(
                        theme=ft.Theme(color_scheme_seed=ft.Colors.INDIGO),
                        theme_mode=ft.ThemeMode.DARK,
                        bgcolor=ft.Colors.SURFACE_TINT,
                        padding=20,
                        width=300,
                        content=ft.Button("Unique theme button"),
                    ),
                
            
        ),