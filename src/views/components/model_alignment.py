import flet as ft

class Column:

    def __init__(self, element_one, element_two):
        self.element_one = element_one 
        self.element_two = element_two
    
    def view_column(self):
        self.column = ft.Row (
            controls=[
                ft.Column ([self.element_one]),
                ft.Column ([self.element_two])
            ], alignment=ft.MainAxisAlignment.CENTER, spacing= 50,
        )
        
        return self.column