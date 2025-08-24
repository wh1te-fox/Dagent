import flet as ft
import sqlite3

class Boton:
    def crear(self, texto, accion):
        return ft.ElevatedButton(text=texto, on_click=accion)

class Consulta:
    def __init__(self, nombre_db):
        self.nombre_db = nombre_db

    def ejecutar(self, consulta):
        try:
            with sqlite3.connect(self.nombre_db) as conn:
                cur = conn.cursor()
                cur.execute(consulta)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")

class Ventana:
    def configurar(self, page: ft.Page, titulo: str):
        page.title = titulo
        page.controls.clear()
