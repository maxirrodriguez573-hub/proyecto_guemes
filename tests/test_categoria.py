import sqlite3 # Type Hints
from database.categoria import *
from database.utils import *
import pytest

def obtener_total_categorias(conn : sqlite3.Connection) -> int:
        cursor = conn.cursor()

        cursor.execute("""SELECT COUNT(*) AS total FROM CATEGORIA""")

        total_categorias = fetchone(cursor)

        return total_categorias["total"]

def obtener_categoria_por_id(conn : sqlite3.Connection, categoria_id : int) -> dict|None:
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



class TestAgregarCategoria:

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

class TestEliminarCategoria:

    def test_deberia_eliminar_una_categoria_existente(self, conn: sqlite3.Connection, crear_categoria):
        categoria_id = crear_categoria()

        categorias_viejas = obtener_total_categorias(conn)

        eliminar_categoria(conn, categoria_id)

        categorias_nuevas = obtener_total_categorias(conn)

        assert categorias_nuevas == categorias_viejas - 1

    def test_deberia_eliminar_solo_la_categoria_indicada(self, conn: sqlite3.Connection, crear_categoria):
        categoria_1 = crear_categoria("categoria_1")
        categoria_2 = crear_categoria("categoria_2")

        eliminar_categoria(conn, categoria_1)

        assert obtener_categoria_por_id(conn, categoria_1) is None

        categoria = obtener_categoria_por_id(conn, categoria_2)

        assert categoria["nombre"] == "categoria_2"

    @pytest.mark.parametrize("categoria_id_invalida",
        [
            [],
            {},
            "",
            10.5,
            None,
            False,
            True,
        ],)
    def test_deberia_rechazar_tipos_de_datos_invalidos(self, conn: sqlite3.Connection, categoria_id_invalida: object,):
        categorias_viejas = obtener_total_categorias(conn)

        with pytest.raises(ValueError):
            eliminar_categoria(conn, categoria_id_invalida)

        categorias_nuevas = obtener_total_categorias(conn)

        assert categorias_nuevas == categorias_viejas

    @pytest.mark.parametrize("categoria_id_invalida",
        [
            0,
            -1,
            -10,
        ],)
    def test_deberia_rechazar_ids_fuera_del_limite(self, conn: sqlite3.Connection, categoria_id_invalida: int,):
        categorias_viejas = obtener_total_categorias(conn)

        with pytest.raises(ValueError):
            eliminar_categoria(conn, categoria_id_invalida)

        categorias_nuevas = obtener_total_categorias(conn)

        assert categorias_nuevas == categorias_viejas

class TestModificarCategoria:
    def test_deberia_modificar_correctamente_el_nombre(self, conn: sqlite3.Connection, crear_categoria):

        categoria_id = crear_categoria("categoria_vieja")

        modificar_categoria(conn, categoria_id, "categoria_nueva")

        categoria = obtener_categoria_por_id(conn, categoria_id)

        assert categoria["nombre"] == "categoria_nueva"

    def test_deberia_retornar_la_categoria_anterior(self, conn: sqlite3.Connection, crear_categoria):
        categoria_id = crear_categoria("categoria_vieja")

        categoria = modificar_categoria(conn, categoria_id, "categoria_nueva")

        assert categoria["categoria_id"] == categoria_id
        assert categoria["nombre"] == "categoria_vieja"

    def test_deberia_modificar_solo_la_categoria_indicada(self, conn: sqlite3.Connection, crear_categoria):
        categoria_1 = crear_categoria("categoria_1")
        categoria_2 = crear_categoria("categoria_2")

        modificar_categoria(conn, categoria_1, "categoria_modificada")

        categoria = obtener_categoria_por_id(conn, categoria_2)

        assert categoria["nombre"] == "categoria_2"

    @pytest.mark.parametrize("categoria_id",
        [
            [],
            {},
            "",
            10.5,
            None,
            False,
            True,
        ],
    )
    def test_deberia_rechazar_tipos_invalidos_para_categoria_id(self, conn: sqlite3.Connection, categoria_id):
        with pytest.raises(ValueError):
            modificar_categoria(conn, categoria_id, "categoria_nueva")

    @pytest.mark.parametrize("categoria_id",
    [
        0,
        -1,
        -50,
    ],
)
    def test_deberia_rechazar_categoria_id_fuera_del_limite(self, conn: sqlite3.Connection, categoria_id):
        with pytest.raises(ValueError):
            modificar_categoria(conn, categoria_id, "categoria_nueva")

    @pytest.mark.parametrize("nombre", 
    [
        [],
        {},
        (),
        set(),
        10,
        10.5,
        None,
        False,
        True,
    ],
)
    def test_deberia_rechazar_tipos_invalidos_para_nombre(self, conn: sqlite3.Connection, crear_categoria, nombre):
        categoria_id = crear_categoria()


        with pytest.raises(ValueError):
            modificar_categoria(conn, categoria_id, nombre)    
        categoria = obtener_categoria_por_id(conn, categoria_id)
        assert categoria["nombre"] == "categoria_test"

    @pytest.mark.parametrize("nombre",
        [
            "",
            " ",
            "     ",
            "\t",
            "\n",
        ],
    )
    def test_deberia_rechazar_nombres_vacios(self, conn: sqlite3.Connection, crear_categoria, nombre):
        categoria_id = crear_categoria()

        with pytest.raises(ValueError):
            modificar_categoria(conn, categoria_id, nombre,)

    def test_deberia_lanzar_error_si_el_nombre_ya_existe(self, conn: sqlite3.Connection, crear_categoria):
        categoria_1 = crear_categoria("categoria_1")
        categoria_2 = crear_categoria("categoria_2")

        with pytest.raises(Exception):
            modificar_categoria(conn, categoria_2, "categoria_1")

        categoria_1 = obtener_categoria_por_id(conn, categoria_1)
        assert categoria_1["nombre"] == "categoria_1"

    def test_deberia_lanzar_error_si_la_categoria_no_existe(self, conn: sqlite3.Connection):
        with pytest.raises(ValueError):
            modificar_categoria(conn, 9999, "categoria_nueva")

class TestObtenerCategoria:
    def test_deberia_retornar_la_categoria_correcta(self, conn: sqlite3.Connection, crear_categoria):
        categoria_id = crear_categoria("categoria_test")

        categoria = obtener_categoria(conn, categoria_id)

        assert categoria["categoria_id"] == categoria_id
        assert categoria["nombre"] == "categoria_test"

    def test_deberia_retornar_un_diccionario(self, conn: sqlite3.Connection, crear_categoria):
        categoria_id = crear_categoria()

        categoria = obtener_categoria(conn, categoria_id)

        assert isinstance(categoria, dict)

    @pytest.mark.parametrize("categoria_id",
        [
            [],
            {},
            "",
            10.5,
            None,
            False,
            True,
        ],
    )
    def test_deberia_rechazar_tipos_invalidos_para_categoria_id(self, conn: sqlite3.Connection, categoria_id):
        with pytest.raises(ValueError):
            obtener_categoria(conn, categoria_id)
    
    @pytest.mark.parametrize("categoria_id",
        [
            0,
            -1,
            -100,
        ],
    )
    def test_deberia_rechazar_categoria_id_fuera_del_limite(self, conn: sqlite3.Connection, categoria_id):
        with pytest.raises(ValueError):
            obtener_categoria(conn, categoria_id)

    def test_deberia_lanzar_error_si_la_categoria_no_existe(self, conn: sqlite3.Connection):
        with pytest.raises(ValueError):
            obtener_categoria(conn, 999999)







