from database.utils import fetchone, fetchall
import sqlite3 # Type Hints

# Agregar comercio
def agregar_comercio(conn : sqlite3.Connection, nombre : str, direccion : str|None = None, horario : str|None = None) -> int:
    cursor = conn.cursor()

    try:
        cursor.execute('''  
                    INSERT INTO COMERCIO (nombre, direccion, horario) 
                    VALUES (?, ?, ?)
                       ''', (nombre, direccion, horario))
        conn.commit()
        return cursor.lastrowid
    
    except Exception as E:
        raise Exception ("Error al agregar un comercio") from E
    
# Eliminar comercio 
def eliminar_comercio(conn : sqlite3.Connection, comercio_id : int):
    cursor = conn.cursor()

    try:
        cursor.execute('''DELETE FROM COMERCIO
                       WHERE comercio_id = (?)
                       ''', (comercio_id, ))
        
        if cursor.rowcount == 0:
            raise ValueError ("Comercio no encontrado.")
        
        conn.commit()

    except Exception as E:
        raise Exception("Error al eliminar el comercio") from E

# Obtener un comercio
def obtener_comercio(conn : sqlite3.Connection, comercio_id : int) -> dict:
    cursor : sqlite3.Cursor = conn.cursor()

    try:
        cursor.execute('''
                       SELECT * FROM COMERCIO 
                       WHERE comercio_id = (?)
                       ''', (comercio_id, ))
        
        comercio : dict|None = fetchone(cursor)

    except Exception as E:
        raise Exception ("Error al obtener la comercio.")from E

    if not comercio:
            raise ValueError("No existe el comercio")
    
    return comercio

# Lista de comercios
def obtener_comercios(conn : sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()

    try:
        cursor.execute('''
                        SELECT * FROM COMERCIO
                       ''')
        
        registros : list[dict] = fetchall(cursor)

        # Validación: Error al obtener una lista vacía
        if not registros:
            raise Exception ("Error al obtener el comercio.")
        
        return registros

    except Exception as E:
        raise Exception("Error al obtener la lista de comercios") from E

# Modificar comercio
def modificar_comercio(conn : sqlite3.Connection, comercio_id : int, nombre : str|None = None, direccion : str|None = None, horario : str|None = None) -> int:
    cursor = conn.cursor()

    # Validación: Parámetros obligatorios 
    if nombre is None and direccion is None and horario is None:
        raise ValueError ("No existen cambios.")

    try:
        # Registro
        comercio : dict = obtener_comercio(conn, comercio_id)

        # Validaciones
        if nombre is None:
            nombre = comercio["nombre"]
        
        if direccion is None:
            direccion = comercio["direccion"]

        if horario is None:
            horario = comercio["horario"]
            
        cursor.execute('''
                       UPDATE COMERCIO 
                       SET nombre = (?), direccion = (?), horario = (?) 
                       WHERE comercio_id = (?)
                       ''', (nombre, direccion, horario, comercio_id))
        
        conn.commit()
        return cursor.rowcount

    except sqlite3.Error as E:
        raise Exception ("Error al modificar el comercio.") from E