from database.utils import fetchone, fetchall

# Agregar comercio
def agregar_comercio(conn, nombre : str, direccion : str|None = None, horario : str|None = None) -> int:
    cursor = conn.cursor()

    try:
        cursor.execute('''  
                    INSERT INTO COMERCIO (nombre, direccion, horario) 
                    VALUES ((?), (?), (?))
                       ''', (nombre, direccion, horario))
        conn.commit()
        return cursor.lastrowid
    
    except Exception as E:
        raise Exception ("Error al agregar un comercio") from E
    
# Eliminar comercio 
def eliminar_comercio(conn, comercio_id : int):
    cursor = conn.cursor()

    try:
        cursor.execute('''DELETE FROM COMERCIO
                       WHERE comercio_id = (?)
                       ''', (comercio_id, ))
        
        conn.commit()

    except Exception as E:
        raise Exception("Error al eliminar el comercio") from E

# Obtener un comercio
def obtener_comercio(conn, comercio_id : int) -> dict:
    cursor = conn.cursor()

    try:
        cursor.execute('''
                       SELECT * FROM COMERCIO 
                       WHERE comercio_id = (?)
                       ''', (comercio_id, ))
        
        return fetchone(cursor)

    except Exception as E:
        raise Exception ("Error al obtener la categoria.")from E

# Lista de categorias
def lista_comercio(conn) -> list[dict]:
    cursor = conn.cursor()

    try:
        cursor.execute('''
                        SELECT * FROM COMERCIO
                       ''')
        
        return fetchall(cursor)

    except Exception as E:
        raise Exception("Error al obtener la lista de categorias") from E
 