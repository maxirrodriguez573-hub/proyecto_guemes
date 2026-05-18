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
    
