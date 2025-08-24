import flet as ft
import sqlite3

class Boton:

    def modelo_boton (self, texto, parametro):
        return ft.ElevatedButton(text=texto, on_click= lambda _: parametro())
        # con return muestra el boton

    
class Consulta:

    def modelo_informacion (self, nombre_db, consulta):
        conn = sqlite3.connect (nombre_db)
        cur = conn.cursor()
        cur.execute(consulta)
        # resultado = cur.fetchall() # devuelve las filas
        conn.commit()
        conn.close()
        # return resultado

class Ventana:

    def modelo_ventana (self, page: ft.Page):
        page.controls.clear()
        page.update()

    def contenido (self, page, titulo):    
        page.title = titulo
        page.update()

    def configurar_ventana(self, page, titulo):
        page.title = titulo
        page.controls.clear()
        page.update()

        
    
