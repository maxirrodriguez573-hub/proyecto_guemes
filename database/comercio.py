from database.utils import fetchone, fetchall
from datetime import datetime
import sqlite3 # Type Hints

# Agregar comercio
def agregar_comercio(conn : sqlite3.Connection, nombre : str, direccion : str|None = None, horario : str|None = None) -> int:
    cursor = conn.cursor()
    
    # Validaciones
    if not isinstance(nombre, str):
        raise ValueError ("Coloque un nombre correcto.")
    
    if not nombre.strip():
        raise ValueError("Colocar un nombre correcto.")
    
    if type(direccion) is not None:
        if not isinstance(direccion, str):
            raise ValueError ("Coloque una dirección correcta.")
        
    if type(horario) is not None:
        if not isinstance(horario, str):
            raise ValueError ("Coloque un horario correcto.")

    # SQL
    try:
        cursor.execute('''  
                    INSERT INTO COMERCIO (nombre, direccion, horario) 
                    VALUES (?, ?, ?)
                       ''', (nombre, direccion, horario))
        conn.commit()
    
    except sqlite3.Error as E:
        raise Exception ("Error al agregar un comercio") from E
    
    return cursor.lastrowid
    
# Eliminar comercio 
def eliminar_comercio(conn : sqlite3.Connection, comercio_id : int):
    cursor = conn.cursor()
    
    # Validaciones
    if type(comercio_id) is not int:
        raise ValueError ("Coloque un comercio_id correcto.")
    
    if comercio_id <= 0:
        raise ValueError ("Coloque un comercio_id correcto.")
    
    # Validar registro 
    obtener_comercio(conn, comercio_id) 

    # SQL
    try:
        cursor.execute('''DELETE FROM COMERCIO
                       WHERE comercio_id = (?)
                       ''', (comercio_id, ))
        
        conn.commit()

    except sqlite3.Error as E:
        raise Exception("Error al eliminar el comercio") from E

# Modificar comercio
def modificar_comercio(conn : sqlite3.Connection, comercio_id : int, nombre : str|None = None, direccion : str|None = None, horario : str|None = None) -> dict:
    cursor = conn.cursor()

    # Validar comercio_id
    if type(comercio_id) is not int:
        raise ValueError ("Coloque un comercio_id correcto.")
    
    if comercio_id <= 0:
        raise ValueError ("Coloque un comercio_id correcto.")
    
    # Parámetros obligatorios
    if nombre is None and direccion is None and horario is None: 
        raise ValueError ("No existen cambios.")

    # Validar registro
    comercio = obtener_comercio(conn, comercio_id) 

    # Completar datos faltantes
    
    if nombre is None:
        nombre = comercio["nombre"]

    if direccion is None:
        direccion = comercio["direccion"]

    if horario is None:
        horario = comercio["horario"]

    # Validar datos
    if not isinstance(nombre, str):
        raise ValueError ("Coloque un nombre correcto.")
    
    if not nombre.strip():
        raise ValueError("Colocar un nombre correcto.")


    if not isinstance(direccion, str):
        raise ValueError ("Coloque una dirección correcta.")
    if type(horario) is not None:
        if not isinstance(horario, str):
            raise ValueError ("Coloque un horario correcto.")
    
    # SQL
    try:
        cursor.execute('''
                       UPDATE COMERCIO 
                       SET nombre = (?), direccion = (?), horario = (?) 
                       WHERE comercio_id = (?)
                       ''', (nombre, direccion, horario, comercio_id))
        
        conn.commit()

    except sqlite3.Error as E:
        raise Exception ("Error al modificar el comercio.") from E
    
    return comercio

# Obtener un comercio
def obtener_comercio(conn : sqlite3.Connection, comercio_id : int) -> dict:
    cursor : sqlite3.Cursor = conn.cursor()

    # SQL
    try:
        cursor.execute('''
                       SELECT * FROM COMERCIO 
                       WHERE comercio_id = (?)
                       ''', (comercio_id, ))
        
        comercio : dict|None = fetchone(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al obtener la comercio.")from E

    if not comercio:
            raise ValueError("Error: No existe el comercio.")
    
    return comercio

# Lista de comercios
def obtener_comercios(conn : sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()

    # SQL
    try:
        cursor.execute('''
                        SELECT * FROM COMERCIO
                       ''')
        
        comercios : list[dict] = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception("Error al obtener la lista de comercios") from E
    
    return comercios

# Obtener comercios más usados
def obtener_comercios_mas_usados(conn : sqlite3.Connection, limit : int = -1) -> list[dict]:
    cursor = conn.cursor()

    # Validaciones
    if type(limit) is not int:
        raise ValueError ("Coloque un número.")
    
    if limit != -1 and limit <= 0: 
        raise ValueError ("limit debe ser mayor a 0 o -1.")       
    
    # SQL
    try:
        cursor.execute('''SELECT COUNT(G.gasto_id) AS cantidad_gastos, C.nombre 
                        FROM GASTO G 
                        JOIN COMERCIO C 
                        ON G.comercio_id = C.comercio_id 
                        GROUP BY C.comercio_id 
                        ORDER BY cantidad_gastos DESC LIMIT (?)''', (limit, ))
        
        comercios = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al obtener los comercios.") from E
    
    return comercios

# Obtener comercios con mayores gastos
def obtener_comercios_con_mayores_gastos(conn : sqlite3.Connection, limit : int = -1) -> list[dict]:
    cursor = conn.cursor()

    # Validaciones
    if type(limit) is not int:
        raise ValueError ("Coloque un número.")

    if limit != -1 and limit <= 0:
        raise ValueError ("limit debe ser mayor a 0 o -1.")
    
    # SQL
    try:
        cursor.execute('''
                        SELECT ROUND(SUM(monto), 2) AS total, C.nombre 
                        FROM GASTO G 
                        JOIN COMERCIO C 
                        ON G.comercio_id = C.comercio_id 
                        GROUP BY C.comercio_id 
                        ORDER BY total DESC
                        LIMIT (?)
                        ''', (limit, ))
        
        comercios = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al obtener los comercios con mayor gasto.") from E
    
    return comercios

# Obtener los gastos de un comercio
def obtener_gastos_de_comercio(conn : sqlite3.Connection, comercio_id : int) -> list[dict]:
    cursor = conn.cursor()
    
    # Validaciones
    if type(comercio_id) is not int:
        raise ValueError ("Coloque un comercio_id correcto.") 
    
    if comercio_id <= 0:
        raise ValueError ("Coloque un comercio_id correcto.")
    
    # SQL
    try:
        cursor.execute('''SELECT * FROM GASTO WHERE comercio_id = (?)
                       ''', (comercio_id, ))
        
        gastos = fetchall(cursor)
        
    except sqlite3.Error as E:
        raise Exception ("Error al obtener los gastos de un comercio.") from E
    
    return gastos

