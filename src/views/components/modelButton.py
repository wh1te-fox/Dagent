# si creo un botonn lo que cambia seria el texto, ahora otra cosa que cambauria seria la funcion que hace el boton, 
# cunstruir una clase.
# lo que necesirtamos es encapsular codigo
import flet as ft 


# crea atributos para que el boton se areutilizable, y solo pasar los paramtros para usarlo
class Control_b:
    def __init__(self, text_b, parameter_b, page): 
        self.text_b = text_b
        #self.parametroB = parameter_b # error
        self.parameter_b = parameter_b
        self.page = page
        

    def view1(self, views): # mala practica, no necesita paramtros 
        self.views = ft.ElevatedButton()
        pass

    def view(self):
        self.boton = ft.ElevatedButton(text=self.text_b, on_click=lambda e: self.parameter_b(self.page)) # usamos self para poder usar los paramtros 
        return self.boton # retornar el boton y que me permita hacer in .add

class ButtonIcon:
    def __init__(self, name_icon, color_icon, funcion, hover_text: str):
        self.name_icon = name_icon
        self.color_icon = color_icon
        self.funcion = funcion
        self.hover_text = hover_text

    def model_icon(self):
        self.button = ft.IconButton(
                        icon = self.name_icon,
                        icon_color = self.color_icon,
                        on_click = lambda _: self.funcion(),
                        tooltip = self.hover_text
                        )

        return self.button