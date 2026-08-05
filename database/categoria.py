from database.utils import fetchone, fetchall
import sqlite3 # Type Hints

# Agregar categoria
def agregar_categoria(conn : sqlite3.Connection , nombre : str) -> int:
    cursor = conn.cursor()
    
    # Validaciones
    if not isinstance(nombre, str):
        raise ValueError ("Coloque un nombre correcto.")
    
    if not nombre.strip():
        raise ValueError("Colocar un nombre correcto.")
    
    # SQL
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
def eliminar_categoria(conn : sqlite3.Connection, categoria_id : int) -> None:
    cursor = conn.cursor()
    
    # Validaciones
    if type(categoria_id) is not int:
        raise ValueError ("Coloque una categoria_id correcta.")
    
    if categoria_id <= 0:
        raise ValueError ("Coloque una categoria_id correcta.")
    
    # Validar registro actual
    obtener_categoria(conn, categoria_id)

    # SQL
    try:
        cursor.execute('''DELETE FROM CATEGORIA 
                       WHERE categoria_id = (?)
                       ''', (categoria_id, ))

        conn.commit()
        
    except sqlite3.Error as E:
        raise Exception("Error al eliminar una categoria.") from E
    
# Modificar categoria
def modificar_categoria(conn : sqlite3.Connection, categoria_id : int, nombre : str) -> dict:
    cursor = conn.cursor()
 
    # Validaciones
    if not isinstance(categoria_id, int):
        raise ValueError ("Coloque una categoria_id correcta.")

    if categoria_id <= 0:
        raise ValueError ("Coloque una categoria_id correcta.")

    # Validar registro actual 
    categoria = obtener_categoria(conn, categoria_id) 

    if not isinstance(nombre, str):
        raise ValueError ("Colocar un nuevo nombre.")
    
    if not nombre.strip():
        raise ValueError ("Colocar un nuevo nombre.")

    # SQL
    try:
        cursor.execute('''UPDATE CATEGORIA 
                       SET nombre = (?)
                       WHERE categoria_id = (?)
                       ''', (nombre, categoria_id))

        conn.commit()

    except sqlite3.Error as E:
        raise Exception("Error al modificar una categoria.") from E
    
    return categoria 
 
# Obtener una categoria 
def obtener_categoria(conn : sqlite3.Connection, categoria_id : int) -> dict:
    cursor = conn.cursor()

    # Validaciones
    if type(categoria_id) is not int:
        raise ValueError ("Coloque una categoria_id correcta.")
    
    if categoria_id <= 0:
        raise ValueError ("Coloque una categoria_id correcta.")

    # SQL
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

    # SQL
    try:
        cursor.execute('''
                        SELECT * FROM CATEGORIA
                       ''')
        
        categorias : list[dict] = fetchall(cursor)
       
    except sqlite3.Error as E:
        raise Exception("Error al obtener la lista de categorias") from E
    
    return categorias
   
# Obtener categorias más usadas
def obtener_categorias_mas_usadas(conn : sqlite3.Connection, limit : int = -1) -> list[dict]:
    cursor = conn.cursor()

    # Validaciones
    if type(limit) is not int:
        raise ValueError ("Coloque un número.")
    
    if limit != -1 and limit <= 0: 
        raise ValueError ("limit debe ser mayor a 0 o -1.")  

    # SQL     
    try:
        cursor.execute('''SELECT COUNT(G.gasto_id) AS cantidad_gastos, C.nombre 
                            FROM CATEGORIA C 
                            LEFT JOIN GASTO G 
                            ON G.categoria_id = C.categoria_id 
                            GROUP BY C.categoria_id 
                            ORDER BY cantidad_gastos DESC, C.nombre ASC 
                            LIMIT (?)''', (limit,))
        
        categorias = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al obtener las categorias.") from E
    
    return categorias

# Obtener categorias con mayores gastos
def obtener_categorias_con_mayores_gastos(conn : sqlite3.Connection, limit : int = -1) -> list[dict]:
    cursor = conn.cursor()

    # Validaciones
    if type(limit) is not int:
        raise ValueError ("Coloque un número.")

    if limit != -1 and limit <= 0:
        raise ValueError ("limit debe ser mayor a 0 o -1.")
    
    # SQL
    try:
        cursor.execute('''
                        SELECT COALESCE(ROUND(SUM(G.monto), 2), 0.0) AS total,
                        C.nombre
                        FROM CATEGORIA C
                        LEFT JOIN GASTO G
                        ON G.categoria_id = C.categoria_id
                        GROUP BY C.categoria_id
                        ORDER BY total DESC, C.nombre ASC
                        LIMIT (?)
                        ''', (limit, ))
        
        categoria = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al obtener las categoria con mayor gasto.") from E
    
    return categoria

# Obtener los gastos de una categoria
def obtener_gastos_de_categoria(conn : sqlite3.Connection, categoria_id : int) -> list[dict]:
    cursor = conn.cursor()
    
    # Validaciones
    if type(categoria_id) is not int:
        raise ValueError ("Coloque una categoria_id correcta.") 
    
    if categoria_id < 1:
        raise ValueError ("Coloque una categoria_id correcta.")
    
    # SQL
    try:
        cursor.execute('''SELECT * FROM GASTO WHERE categoria_id = (?)
                       ''', (categoria_id, ))
        
        gastos = fetchall(cursor)
        
    except sqlite3.Error as E:
        raise Exception ("Error al obtener los gastos de una categoria.") from E
    
    return gastos