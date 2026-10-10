import flet as ft


class Column:
    """Component to align elements in a centered row."""

    def __init__(self, *elements):
        self.elements = elements
    
    def view_column(self):
        self.column = ft.Row(
            controls=[
                ft.Column([e]) for e in self.elements
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50,
        )
        return self.column


# Backward compatibility alias
CustomColumn = Column
