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
    
    except sqlite3.Error as E:
        raise Exception ("Error al agregar un comercio") from E
    
    return cursor.lastrowid
    
# Eliminar comercio 
def eliminar_comercio(conn : sqlite3.Connection, comercio_id : int):
    cursor = conn.cursor()
    
    comercio = obtener_comercio(conn, comercio_id) # Validar registro 

    try:
        cursor.execute('''DELETE FROM COMERCIO
                       WHERE comercio_id = (?)
                       ''', (comercio_id, ))
        
        conn.commit()

    except sqlite3.Error as E:
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

    except sqlite3.Error as E:
        raise Exception ("Error al obtener la comercio.")from E

    if not comercio:
            raise ValueError("Error: No existe el comercio.")
    
    return comercio

# Lista de comercios
def obtener_comercios(conn : sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()

    try:
        cursor.execute('''
                        SELECT * FROM COMERCIO
                       ''')
        
        comercios : list[dict] = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception("Error al obtener la lista de comercios") from E
    
    return comercios

# Modificar comercio
def modificar_comercio(conn : sqlite3.Connection, comercio_id : int, nombre : str|None = None, direccion : str|None = None, horario : str|None = None) -> dict:
    cursor = conn.cursor()

    comercio : dict = obtener_comercio(conn, comercio_id) # Validar registro
    
    # Validaciones
    if nombre is None and direccion is None and horario is None: # Parámetros obligatorios
        raise ValueError ("No existen cambios.")
    
    if nombre is None:
        nombre = comercio["nombre"]

    if not nombre.strip():
        raise ValueError("Colocar un nombre correcto.")

    if direccion is None:
        direccion = comercio["direccion"]

    if horario is None:
        horario = comercio["horario"]

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

# Obtener comercios más usados
def obtener_comercios_mas_usados(conn : sqlite3.Connection, limit : int = -1) -> list[dict]:
    cursor = conn.cursor()

    # Validaciones
    if type(limit) is not int:
        raise ValueError ("Coloque un número.")
    
    if limit != -1 and limit <= 0: 
        raise ValueError ("Coloque un número mayor a 0.")       
    
    try:
        cursor.execute('''SELECT COUNT(G.gasto_id) AS cantidad_gastos, C.nombre 
                        FROM GASTO G 
                        JOIN COMERCIO C 
                        ON G.comercio_id = C.comercio_id 
                        GROUP BY C.comercio_id 
                        ORDER BY cantidad_gastos DESC LIMIT (?)''', (limit,))
        
        comercios = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al obtener los comercios.") from E
    
    return comercios
