import flet as ft


class ControlButton:
    """Reusable button component that encapsulates click actions and page reference."""

    def __init__(self, button_text, action_parameter, page):
        self.button_text = button_text
        self.action_parameter = action_parameter
        self.page = page

    def view(self):
        self.button = ft.Button(
            content=ft.Text(self.button_text),
            on_click=lambda e: self.action_parameter(self.page)
        )
        return self.button


# Backward compatibility alias
Control_b = ControlButton


class ButtonIcon:
    """Reusable icon button component with tooltip and click action."""

    def __init__(self, icon_name, icon_color, callback_function, hover_text: str):
        self.icon_name = icon_name
        self.icon_color = icon_color
        self.callback_function = callback_function
        self.hover_text = hover_text

    def model_icon(self):
        self.button = ft.IconButton(
            icon=self.icon_name,
            icon_color=self.icon_color,
            on_click=lambda _: self.callback_function(),
            tooltip=self.hover_text
        )
        return self.button
