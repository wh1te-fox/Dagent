import flet as ft 

from Testing.controlador.menu import main
from Testing.other.SQlite.SQlite.Iniciador import inicializar_base_datos

inicializar_base_datos() # repara toda la base de datos

ft.app(target=main)