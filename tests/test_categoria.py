import sqlite3 # Type Hints
from database.categoria import *
from database.utils import *
import pytest

def obtener_total_categorias(conn : sqlite3.Connection) -> int:
        cursor = conn.cursor()

        cursor.execute("""SELECT COUNT(*) AS total FROM CATEGORIA""")

        total_categorias = fetchone(cursor)

        return total_categorias["total"]

def obtener_categoria_por_id(conn : sqlite3.Connection, categoria_id : int) -> dict:
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM CATEGORIA WHERE categoria_id == (?)''', (categoria_id, ))

        return fetchone(cursor)


def eliminar_categoria_por_id(conn : sqlite3.Connection, categoria_id : int):
        cursor = conn.cursor()

        cursor.execute("""DELETE FROM CATEGORIA WHERE categoria_id == (?)""", (categoria_id, ))
        conn.commit()

@pytest.fixture
def crear_categoria(conn : sqlite3.Connection) -> callable:
    categorias_id = []

    def agregar(nombre : str = "categoria_test") -> int:
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO CATEGORIA (nombre)
                        VALUES (?)''', (nombre, ))
        conn.commit()

        categorias_id.append(cursor.lastrowid)

        return cursor.lastrowid
    
    yield agregar

    for categoria_id in categorias_id:
        eliminar_categoria_por_id(conn, categoria_id)



class TestAgregarCategoria():

    def test_deberia_insertar_una_nueva_categoria(self, conn : sqlite3.Connection):
        
        categorias_viejas = obtener_total_categorias(conn)

        categoria_id = agregar_categoria(conn, "categoria_test")

        categorias_nuevas = obtener_total_categorias(conn) 

        try:
            assert categorias_nuevas == categorias_viejas + 1
        finally:
            eliminar_categoria_por_id(conn, categoria_id)

    def test_deberia_insertar_los_datos_correctamente(self, conn : sqlite3.Connection):
        categoria_id = agregar_categoria(conn, "categoria_test")

        categoria = obtener_categoria_por_id(conn, categoria_id)

        try: 
            assert categoria["nombre"] == "categoria_test"
        finally:
             eliminar_categoria_por_id(conn, categoria_id)



    @pytest.mark.parametrize("nombres_invalidos",[[], {}, 0, 1, 10.5, False, True, None])
    def test_deberia_rechazar_tipos_de_datos_invalidos(self, conn : sqlite3.Connection, nombres_invalidos : object):
        categorias_viejas = obtener_total_categorias(conn)

        with pytest.raises(ValueError):
            agregar_categoria(conn, nombres_invalidos)

        categorias_nuevas = obtener_total_categorias(conn)

        assert categorias_nuevas == categorias_viejas

    @pytest.mark.parametrize("nombres_vacios", ["", " ", "   ", "\t", "\n", "\t \n"])
    def test_deberia_rechazar_nombres_vacios(self, conn : sqlite3.Connection , nombres_vacios : str):
        categorias_viejas = obtener_total_categorias(conn)

        with pytest.raises(ValueError):
            agregar_categoria(conn, nombres_vacios)

        categorias_nuevas = obtener_total_categorias(conn)

        assert categorias_nuevas == categorias_viejas

    def test_deberia_lanzar_error_si_la_categoria_ya_existe(self, conn : sqlite3.Connection, crear_categoria):

        crear_categoria("categoria_existente")

        with pytest.raises(Exception):
            agregar_categoria(conn, "categoria_existente")








        
