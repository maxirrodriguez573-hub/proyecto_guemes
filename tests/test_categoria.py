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

class TestObtenerCategorias:
    def test_deberia_retornar_lista_vacia_si_no_hay_categorias(self, conn: sqlite3.Connection):
        categorias = obtener_categorias(conn)

        assert categorias == []

    def test_deberia_retornar_una_unica_categoria(self, conn: sqlite3.Connection, crear_categoria):
        categoria_id = crear_categoria("categoria_test")

        categorias = obtener_categorias(conn)

        assert len(categorias) == 1
        assert categorias[0]["categoria_id"] == categoria_id
        assert categorias[0]["nombre"] == "categoria_test"


    def test_deberia_retornar_todas_las_categorias(self, conn: sqlite3.Connection, crear_categoria):
        crear_categoria("categoria_1")
        crear_categoria("categoria_2")
        crear_categoria("categoria_3")

        categorias = obtener_categorias(conn)

        assert len(categorias) == 3

    def test_deberia_retornar_el_contenido_de_todas_las_categorias(self, conn: sqlite3.Connection, crear_categoria):
        crear_categoria("categoria_1")
        crear_categoria("categoria_2")
        crear_categoria("categoria_3")

        nombres = [categoria["nombre"] for categoria in obtener_categorias(conn)]

        assert nombres == ["categoria_1", "categoria_2", "categoria_3"]

    def test_deberia_retornar_una_lista_de_diccionarios(self, conn: sqlite3.Connection, crear_categoria):
        crear_categoria()

        categorias = obtener_categorias(conn)

        assert isinstance(categorias, list)
        assert isinstance(categorias[0], dict)

class TestObtenerCategoriasMasUsadas:
    def test_deberia_retornar_todas_las_categorias_ordenadas_por_cantidad_de_gastos(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_a = crear_categoria("A")
        categoria_b = crear_categoria("B")
        categoria_c = crear_categoria("C")

        comercio_id = crear_comercio()

        crear_gasto(categoria_a, comercio_id)
        crear_gasto(categoria_a, comercio_id)
        crear_gasto(categoria_a, comercio_id)

        crear_gasto(categoria_b, comercio_id)

        categorias = obtener_categorias_mas_usadas(conn)

        assert categorias == [
            {"cantidad_gastos": 3, "nombre": "A"},
            {"cantidad_gastos": 1, "nombre": "B"},
            {"cantidad_gastos": 0, "nombre": "C"},
        ]

    def test_deberia_retornar_todas_las_categorias_sin_limit(self, conn, crear_categoria):
        crear_categoria("A")
        crear_categoria("B")

        categorias = obtener_categorias_mas_usadas(conn)

        assert len(categorias) == 2

    def test_deberia_retornar_todas_las_categorias_con_limit_menos_uno(self, conn, crear_categoria):
        crear_categoria("A")
        crear_categoria("B")

        categorias = obtener_categorias_mas_usadas(conn, -1)

        assert len(categorias) == 2

    def test_deberia_respetar_el_parametro_limit(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_a = crear_categoria("A")
        categoria_b = crear_categoria("B")
        categoria_c = crear_categoria("C")

        comercio_id = crear_comercio()

        crear_gasto(categoria_a, comercio_id)
        crear_gasto(categoria_a, comercio_id)

        crear_gasto(categoria_b, comercio_id)

        categorias = obtener_categorias_mas_usadas(conn, 2)

        assert len(categorias) == 2

    def test_deberia_retornar_correctamente_los_datos(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_id = crear_categoria("Ferretería")
        comercio_id = crear_comercio()

        crear_gasto(categoria_id, comercio_id)
        crear_gasto(categoria_id, comercio_id)

        categoria = obtener_categorias_mas_usadas(conn)[0]

        assert categoria["nombre"] == "Ferretería"
        assert categoria["cantidad_gastos"] == 2

    @pytest.mark.parametrize("limit",
        [[], {}, None, 10.5, "", True, False],
    )
    def test_deberia_rechazar_tipos_invalidos_para_limit(self, conn, limit):
        with pytest.raises(ValueError):
            obtener_categorias_mas_usadas(conn, limit)

    @pytest.mark.parametrize("limit",
        [0, -2, -100],
    )
    def test_deberia_rechazar_limit_fuera_del_rango(self, conn, limit):
        with pytest.raises(ValueError):
            obtener_categorias_mas_usadas(conn, limit)

    def test_deberia_lanzar_error_si_no_existen_categorias(self, conn):
            assert obtener_categorias_mas_usadas(conn) == []

    def test_deberia_incluir_categorias_sin_gastos(self, conn, crear_categoria):
        crear_categoria("A")
        crear_categoria("B")

        categorias = obtener_categorias_mas_usadas(conn)

        assert categorias == [
            {"cantidad_gastos": 0, "nombre": "A"},
            {"cantidad_gastos": 0, "nombre": "B"},
        ]

    def test_deberia_retornar_una_categoria_con_limit_uno(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_a = crear_categoria("A")
        categoria_b = crear_categoria("B")

        comercio_id = crear_comercio()

        crear_gasto(categoria_a, comercio_id)

        categorias = obtener_categorias_mas_usadas(conn, 1)

        assert len(categorias) == 1
        assert categorias[0]["nombre"] == "A"

class TestObtenerCategoriasConMayoresGastos:
    def test_deberia_retornar_categorias_ordenadas_por_total_de_gastos(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_a = crear_categoria("A")
        categoria_b = crear_categoria("B")
        categoria_c = crear_categoria("C")

        comercio_id = crear_comercio()

        crear_gasto(categoria_a, comercio_id, monto=300)
        crear_gasto(categoria_a, comercio_id, monto=200)

        crear_gasto(categoria_b, comercio_id, monto=100)

        categorias = obtener_categorias_con_mayores_gastos(conn)

        assert categorias == [
            {"total": 500.0, "nombre": "A"},
            {"total": 100.0, "nombre": "B"},
            {"total": 0.0, "nombre": "C"},
        ] 

    def test_deberia_calcular_correctamente_el_total_de_gastos(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_id = crear_categoria("Ferretería")
        comercio_id = crear_comercio()

        crear_gasto(categoria_id, comercio_id, monto=100)
        crear_gasto(categoria_id, comercio_id, monto=250.50)

        categorias = obtener_categorias_con_mayores_gastos(conn)

        assert categorias[0]["total"] == 350.50

    def test_deberia_ordenar_por_nombre_si_los_totales_son_iguales(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_b = crear_categoria("B")
        categoria_a = crear_categoria("A")

        comercio_id = crear_comercio()

        crear_gasto(categoria_b, comercio_id, monto=100)
        crear_gasto(categoria_a, comercio_id, monto=100)

        categorias = obtener_categorias_con_mayores_gastos(conn)

        assert categorias == [
            {"total": 100.0, "nombre": "A"},
            {"total": 100.0, "nombre": "B"},
        ]

    def test_deberia_incluir_categorias_sin_gastos(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_con_gasto = crear_categoria("A")
        categoria_sin_gasto = crear_categoria("B")

        comercio_id = crear_comercio()

        crear_gasto(categoria_con_gasto, comercio_id, monto=100)

        categorias = obtener_categorias_con_mayores_gastos(conn)

        assert categorias == [
            {"total": 100.0, "nombre": "A"},
            {"total": 0.0, "nombre": "B"},
        ]

    def test_deberia_retornar_cero_si_los_gastos_tienen_monto_cero(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_id = crear_categoria("A")
        comercio_id = crear_comercio()

        crear_gasto(categoria_id, comercio_id, monto=0)
        crear_gasto(categoria_id, comercio_id, monto=0)

        categorias = obtener_categorias_con_mayores_gastos(conn)

        assert categorias[0] == {
            "total": 0.0,
            "nombre": "A",
        }

    def test_deberia_retornar_todas_las_categorias_con_limit_menos_uno(self, conn, crear_categoria): 
        crear_categoria("A")
        crear_categoria("B")
        crear_categoria("C")

        categorias = obtener_categorias_con_mayores_gastos(conn, -1)

        assert len(categorias) == 3

    def test_deberia_retornar_una_categoria_con_limit_uno(self, conn, crear_categoria): 
        crear_categoria("A")
        crear_categoria("B")
        crear_categoria("C")

        categorias = obtener_categorias_con_mayores_gastos(conn, 1)

        assert len(categorias) == 1

    def test_deberia_retornar_la_cantidad_de_categorias_especificada_por_limit(self, conn, crear_categoria):
        crear_categoria("A")
        crear_categoria("B")
        crear_categoria("C")

        categorias = obtener_categorias_con_mayores_gastos(conn, 2)

        assert len(categorias) == 2

    def test_deberia_retornar_las_categorias_disponibles_si_limit_es_mayor(self, conn, crear_categoria):
        crear_categoria("A")
        crear_categoria("B")

        categorias = obtener_categorias_con_mayores_gastos(conn, 10)

        assert len(categorias) == 2

    @pytest.mark.parametrize("limit",
        [[], {}, None, 10.5, "", False, True],
    )
    def test_deberia_rechazar_tipos_invalidos_para_limit(self, conn, limit):
        with pytest.raises(ValueError):
            obtener_categorias_con_mayores_gastos(conn, limit)

    @pytest.mark.parametrize("limit",
        [0, -2, -10, -100],
    )
    def test_deberia_rechazar_limit_fuera_del_rango(self, conn, limit):
        with pytest.raises(ValueError):
            obtener_categorias_con_mayores_gastos(conn, limit)

    def test_deberia_retornar_lista_vacia_si_no_existen_categorias(self, conn):
        categorias = obtener_categorias_con_mayores_gastos(conn)

        assert categorias == []

    def test_deberia_redondear_el_total_a_dos_decimales(self, conn, crear_categoria, crear_comercio, crear_gasto):
        categoria_id = crear_categoria("A")
        comercio_id = crear_comercio()

        crear_gasto(categoria_id, comercio_id, monto=100.123)
        crear_gasto(categoria_id, comercio_id, monto=50.456)

        categorias = obtener_categorias_con_mayores_gastos(conn)

        assert categorias[0]["total"] == 150.58


