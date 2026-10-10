import flet as ft


class InputModel:
    """Reusable text field component."""

    def __init__(self, input_text: str):
        self.input_text = input_text
        
    def entry_style(self):
        self.entry = ft.TextField(label=self.input_text, width=150, border_radius=10)
        return self.entry
