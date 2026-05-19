from database.utils import fetchone, fetchall

# Agregar categoria
def agregar_categoria(conn, nombre : str) -> int:
    cursor = conn.cursor()
    
    try:
        cursor.execute('''INSERT INTO CATEGORIA
                       (nombre) VALUES
                       (?)
                       ''', (nombre, ))
        
        conn.commit()
        return cursor.lastrowid
        
    except Exception as E:
        raise Exception("Error al agregar una categoria.") from E

# Eliminar categoria
def eliminar_categoria(conn, categoria_id : int):
    cursor = conn.cursor()
    
    try:
        cursor.execute('''DELETE FROM CATEGORIA 
                       WHERE categoria_id = (?)
                       ''', (categoria_id, ))
        
        conn.commit()
        
    except Exception as E:
        raise Exception("Error al agregar una categoria.") from E

# Obtener una categoria 
def obtener_categoria(conn, categoria_id : int) -> dict:
    cursor = conn.cursor()

    try:
        cursor.execute('''
                       SELECT * FROM CATEGORIA 
                       WHERE categoria_id = (?)
                       ''', (categoria_id, ))
        
        return fetchone(cursor)

    except Exception as E:
        raise Exception ("Error al obtener la categoria.")from E

# Lista de categorias
def lista_categorias(conn) -> list[dict]:
    cursor = conn.cursor()

    try:
        cursor.execute('''
                        SELECT * FROM CATEGORIA
                       ''')
        
        return fetchall(cursor)

    except Exception as E:
        raise Exception("Error al obtener la lista de categorias") from E
    

