import sqlite3 # Type Hints
from database.categoria import *
from database.utils import *
import pytest

def obtener_total_categorias(conn : sqlite3.Connection) -> int:
        cursor = conn.cursor()

        cursor.execute("""SELECT COUNT(*) AS total FROM CATEGORIA""")

        total_categorias = fetchone(cursor)

        return total_categorias["total"]

def obtener_categoria_por_id(conn : sqlite3.Connection):
        def obtener(categoria_id : int) -> dict:
            cursor = conn.cursor()

            cursor.execute('''SELECT * FROM CATEGORIA WHERE categoria_id == (?)''', (categoria_id, ))

            return fetchone(cursor)

        return obtener

def eliminar_categoria_por_id(conn : sqlite3.Connection, categoria_id : int):
        cursor = conn.cursor()

        cursor.execute("""DELETE FROM CATEGORIA WHERE categoria_id == (?)""", (categoria_id, ))
        conn.commit()


class TestAgregarCategoria():

    def test_deberia_insertar_una_nueva_categoria(conn : sqlite3.Connection):
        
        categorias_viejas = obtener_total_categorias(conn)

        categoria_id = agregar_categoria(conn, "categoria_test")

        categorias_nuevas = obtener_total_categorias(conn) 

        try:
            assert categorias_nuevas == categorias_viejas + 1
        finally:
            eliminar_categoria_por_id(conn, categoria_id)

         