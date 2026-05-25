from database.utils import fetchone, fetchall
from datetime import datetime
import sqlite3

# Agregar gasto
def agregar_gasto(conn : sqlite3.Connection, telegram_usuario_id : int, categoria_id : int, comercio_id : int, monto : float, recibo_file_id : str, descripcion : str|None = None , fecha : str|None = None) -> int:
    cursor = conn.cursor()

    # Validaciones 
    if not fecha:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        cursor.execute('''INSERT INTO GASTO 
                       (telegram_usuario_id, categoria_id, comercio_id, fecha, monto, descripcion, recibo_file_id)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       ''', (telegram_usuario_id, categoria_id, comercio_id, fecha, monto, descripcion, recibo_file_id))
        
        conn.commit()
        
    except sqlite3.Error as E:
        raise Exception ("Error al agregar el gasto.") from E
    
    return cursor.lastrowid
    
# Eliminar gasto
def eliminar_gasto(conn : sqlite3.Connection, gasto_id : int):
    cursor = conn.cursor()

    gasto = obtener_gasto(conn, gasto_id) # Validar registro

    try:
        cursor.execute('''DELETE FROM GASTO
                       WHERE gasto_id = (?)''', (gasto_id, ))
       
        conn.commit()

    except sqlite3.Error as E:
        raise Exception ("Error al eliminar un gasto.") from E

# Obtener un gasto 
def obtener_gasto(conn : sqlite3.Connection, gasto_id : int) -> dict:
    cursor = conn.cursor()

    try:
        cursor.execute('''SELECT * FROM GASTO 
                       WHERE gasto_id = (?)
                       ''', (gasto_id, ))
        
        gasto = fetchone(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al obtener un gasto") from E
    
    if not gasto:
        raise ValueError ("Error: No existe el gasto.")

    return gasto
    
# Obtener lista de gastos
def obtener_gastos(conn) -> list[dict]:
    cursor = conn.cursor()

    try:
        cursor.execute('''SELECT * FROM GASTO''')

    except Exception as E:
        raise Exception ("Error al obtener los gastos.") from E
    
    return fetchall(cursor)
    
# Modificar gasto
def modificar_gasto(conn : sqlite3.Connection, gasto_id : int, telegram_usuario_id : int|None = None, categoria_id : int|None = None, 
                    comercio_id : int|None = None, fecha : str|None = None, monto : float|None = None, recibo_file_id : int|None = None, 
                    descripcion : str|None = None) -> int:
    cursor = conn.cursor()

    gasto = obtener_gasto(conn, gasto_id) # Validar registro

    # Validaciones 
    if telegram_usuario_id is None:
        telegram_usuario_id = gasto["telegram_usuario_id"]

    if categoria_id is None:
        categoria_id = gasto["categoria_id"]
    
    if comercio_id is None:
        comercio_id = gasto["comercio_id"]

    if fecha is None:
        fecha = gasto["fecha"]

    if monto is None:
        monto = gasto["monto"]

    if descripcion is None:
        descripcion = gasto["descripcion"]
        
    if recibo_file_id is None:
        recibo_file_id = gasto["recibo_file_id"]

    try:
        cursor.execute('''UPDATE GASTO 
                       SET telegram_usuario_id = (?), categoria_id = (?), comercio_id = (?), fecha = (?),
                       monto = (?), descripcion = (?), recibo_file_id = (?) 
                       WHERE gasto_id = (?)
                       ''', (telegram_usuario_id, categoria_id, comercio_id, fecha, monto, descripcion, recibo_file_id, gasto_id))
        
        conn.commit()

    except sqlite3.Error as E:
        raise Exception ("Error al modificar el gasto.") from E
    
    return cursor.rowcount
    
