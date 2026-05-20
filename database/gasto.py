from database.utils import fetchone, fetchall
from datetime import datetime

# Agregar gasto
def agregar_gasto(conn, telegram_usuario_id : int, categoria_id : int, comercio_id : int, monto : float, recibo_file_id : str, descripcion : str|None = None , fecha : str|None = None) -> int:
    if not fecha:
        fecha : str = datetime.now().strftime("%Y-%m-%d %H:%M",)

    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO GASTO 
                       (telegram_usuario_id, categoria_id, comercio_id, fecha, monto, descripcion, recibo_file_id)
                       VALUES ((?), (?), (?), (?), (?), (?), (?))
                       ''', (telegram_usuario_id, categoria_id, comercio_id, fecha, monto, descripcion, recibo_file_id))
        
        conn.commit()
        return cursor.lastrowid

    except Exception as E:
        raise Exception ("Error al agregar el gasto.") from E
    
# Eliminar gasto
def eliminar_gasto(conn, gasto_id : int):
    cursor = conn.cursor()

    try:
        cursor.execute('''DELETE FROM GASTO
                       WHERE gasto_id = (?)''', (gasto_id, ))
        
        conn.commit()

    except Exception as E:
        raise Exception ("Error al eliminar un gasto.") from E

# Obtener un gasto 
def obtener_gasto(conn, gasto_id : int) -> dict:
    cursor = conn.cursor()

    try:
        cursor.execute('''SELECT * FROM GASTO 
                       WHERE gasto_id = (?)
                       ''', (gasto_id, ))
        
        return fetchone(cursor)

    except Exception as E:
        raise Exception ("Error al obtener un gasto") from E
    
# Obtener lista de gastos
def lista_gastos(conn) -> list[dict]:
    cursor = conn.cursor()

    try:
        cursor.execute('''SELECT * FROM GASTO''')

        return fetchall(cursor)

    except Exception as E:
        raise Exception ("Error al obtener los gastos.") from E