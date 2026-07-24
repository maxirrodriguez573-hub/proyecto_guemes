import sqlite3 # Type Hints
from database.categoria import *
from database.utils import *
import pytest

class TestAgregarCategoria():

    def obtener_total_categorias(self, conn : sqlite3.Connection) -> int:
        cursor = conn.cursor()

        cursor.execute("""SELECT COUNT(*) AS total FROM CATEGORIA""")

        total_categorias = fetchone(cursor)

        return total_categorias["total"]

    def eliminar_categoria_de_prueba(self, conn : sqlite3.Connection, categoria_id : int):
        cursor = conn.cursor()

        cursor.execute("""DELETE FROM CATEGORIA WHERE categoria_id == (?)""", (categoria_id, ))
        conn.commit()

    def test_deberia_insertar_una_nueva_categoria(self, conn : sqlite3.Connection):
        
        categorias_viejas = self.obtener_total_categorias(conn)

        categoria_id = agregar_categoria(conn, "categoria_test")

        categorias_nuevas = self.obtener_total_categorias(conn) 

        try:
            assert categorias_nuevas == categorias_viejas + 1
        finally:
            self.eliminar_categoria_de_prueba(conn, categoria_id)

            

