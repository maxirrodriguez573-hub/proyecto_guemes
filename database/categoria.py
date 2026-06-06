from database.utils import fetchone, fetchall
import sqlite3 # Type Hints

# Agregar categoria
def agregar_categoria(conn : sqlite3.Connection , nombre : str) -> int:
    cursor = conn.cursor()
    
    try:
        cursor.execute('''INSERT INTO CATEGORIA
                       (nombre) VALUES
                       (?)
                       ''', (nombre, ))
        
        conn.commit()
        
    except sqlite3.Error as E:
        raise Exception("Error al agregar una categoria.") from E
    
    return cursor.lastrowid

# Eliminar categoria
def eliminar_categoria(conn : sqlite3.Connection, categoria_id : int):
    cursor = conn.cursor()
    
    categoria = obtener_categoria(conn, categoria_id) # Validar registro

    try:
        cursor.execute('''DELETE FROM CATEGORIA 
                       WHERE categoria_id = (?)
                       ''', (categoria_id, ))

        conn.commit()
        
    except sqlite3.Error as E:
        raise Exception("Error al eliminar una categoria.") from E

# Obtener una categoria 
def obtener_categoria(conn : sqlite3.Connection, categoria_id : int) -> dict:
    cursor = conn.cursor()

    try:
        cursor.execute('''
                       SELECT * FROM CATEGORIA 
                       WHERE categoria_id = (?)
                       ''', (categoria_id, ))
        
        categoria : dict|None = fetchone(cursor)
    
    except sqlite3.Error as E:
        raise Exception ("Error al obtener la categoria.")from E
    
    if not categoria:
        raise ValueError("Error: No existe la categoria.")
    
    return categoria

# Lista de categorias
def obtener_categorias(conn : sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()

    try:
        cursor.execute('''
                        SELECT * FROM CATEGORIA
                       ''')
        
        categorias : list[dict] = fetchall(cursor)
       
    except sqlite3.Error as E:
        raise Exception("Error al obtener la lista de categorias") from E
    
    return categorias
    
# Modificar categoria
def modificar_categoria(conn : sqlite3.Connection, categoria_id : int, nombre : str) -> dict:
    cursor = conn.cursor()

    categoria : dict = obtener_categoria(conn, categoria_id) # Validar si la categoria existe

    # Validaciones
    if not isinstance(categoria_id, int) and categoria_id <= 0:
        raise ValueError ("Colocar categoria_id correcto.")

    if not nombre.strip():
        raise ValueError ("Colocar un nuevo nombre.")

    try:
        cursor.execute('''UPDATE CATEGORIA 
                       SET nombre = (?)
                       WHERE categoria_id = (?)
                       ''', (nombre, categoria_id))

        conn.commit()

    except sqlite3.Error as E:
        raise Exception("Error al modificar una categoria.") from E
    
    return categoria 
    
# Obtener categorias más usadas
def obtener_categorias_mas_usadas(conn : sqlite3.Connection, limit : int = -1) -> list[dict]:
    cursor = conn.cursor()

    # Validaciones
    if type(limit) is not int:
        raise ValueError ("Coloque un número.")
    
    if limit != -1 and limit <= 0: 
        raise ValueError ("Coloque un número mayor a 0.")       
    try:
        cursor.execute('''SELECT COUNT(G.gasto_id) AS cantidad_gastos, C.nombre 
                        FROM GASTO G 
                        JOIN CATEGORIA C 
                        ON G.categoria_id = C.categoria_id 
                        GROUP BY C.categoria_id 
                        ORDER BY cantidad_gastos DESC LIMIT (?)''', (limit,))
        
        categorias = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al obtener las categorias.") from E
    
    return categorias


