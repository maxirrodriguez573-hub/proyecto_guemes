from database.connection import conexion
import pytest
import sqlite3

@pytest.fixture
def conn():
    conn = conexion()

    yield conn

    conn.close()

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
    
    cursor = conn.cursor()
    for categoria_id in categorias_id:
        cursor.execute("""DELETE FROM CATEGORIA WHERE categoria_id == (?)""", (categoria_id, ))
        conn.commit()

@pytest.fixture
def crear_comercio(conn : sqlite3.Connection) -> callable:
    comercios_id = []

    def agregar(nombre : str = "comercio_test") -> int:
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO COMERCIO (nombre)
                        VALUES (?)''', (nombre, ))
        conn.commit()

        comercios_id.append(cursor.lastrowid)

        return cursor.lastrowid
    
    yield agregar

    cursor = conn.cursor()
    for comercio_id in comercios_id:
        cursor.execute("""DELETE FROM COMERCIO WHERE comercio_id == (?)""", (comercio_id, ))
        conn.commit()

@pytest.fixture
def crear_gasto(conn : sqlite3.Connection) -> callable:
    gastos_id = []

    def agregar(categoria_id : int, comercio_id : int, telegram_usuario_id : int = 1, fecha : str = "2026-01-01 12:00", 
                monto : float = 100.0, descripcion : str = "", recibo_file_id : str = "") -> int:
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO GASTO 
                       (telegram_usuario_id, categoria_id, comercio_id, fecha, monto, descripcion, recibo_file_id)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       ''', (telegram_usuario_id, categoria_id, comercio_id, fecha, monto, descripcion, recibo_file_id))
        conn.commit()

        gastos_id.append(cursor.lastrowid)

        return cursor.lastrowid

    yield agregar

    cursor = conn.cursor()
    for gasto_id in gastos_id:
        cursor.execute("""DELETE FROM GASTO WHERE gasto_id == (?)""", (gasto_id, ))
        conn.commit()
