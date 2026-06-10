from database.utils import fetchone, fetchall
from datetime import datetime
import sqlite3 # Type Hints

# Agregar gasto
def agregar_gasto(conn : sqlite3.Connection, telegram_usuario_id : int, categoria_id : int, comercio_id : int, monto : float,
                recibo_file_id : str, descripcion : str|None = None , fecha : str|None = None) -> int:
    cursor = conn.cursor()

    # Validaciones 
    if type(telegram_usuario_id) is not int:
        raise ValueError ("Coloque un telegram_usuario_id correcto.")
    
    if telegram_usuario_id <= 0:
        raise ValueError ("Coloque un telegram_usuario_id correcto.")

    if type(categoria_id) is not int:
        raise ValueError ("Coloque una categoria_id correcta.")
    
    if categoria_id <= 0:
        raise ValueError ("Coloque una categoria_id correcta.")

    if type(comercio_id) is not int:
        raise ValueError ("Coloque un comercio_id correcto.")
    
    if comercio_id <= 0:
        raise ValueError ("Coloque un comercio_id correcto")
    
    if not isinstance(monto, (float)):
        raise ValueError ("Coloque un monto correcto.")

    if monto < 0.0:
        raise ValueError ("Coloque un monto mayor a 0,0.")

    if not isinstance(recibo_file_id, str):
        raise ValueError ("Coloque el recibo_file_id correcto.")  

    if not isinstance(descripcion, str):
        raise ValueError ("Coloque una descripción correcta.") 

    if not fecha:
        fecha = datetime.now()

    else:
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M")

        except ValueError as V:
            raise ValueError ("Coloque una fecha correcta. Ej: YYYY-MM-DD HH:MM") from V
    
    if 2025 > int(datetime.strftime(fecha, "%Y")):
        raise ValueError ("Coloque un año correcto (2025+)")    

    fecha = fecha.strftime("%Y-%m-%d %H:%M")

    # SQL
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

    # Validaciones    
    if type(gasto_id) is not int:
        raise ValueError ("Coloque un gasto_id correcto.")
    
    if gasto_id <= 0:
        raise ValueError ("Coloque un gasto_id correcto.")
    
    # Validar registro
    obtener_gasto(conn, gasto_id) 

    # SQL
    try:
        cursor.execute('''DELETE FROM GASTO
                       WHERE gasto_id = (?)''', (gasto_id, ))
       
        conn.commit()

    except sqlite3.Error as E:
        raise Exception ("Error al eliminar un gasto.") from E
    
# Modificar gasto
def modificar_gasto(conn : sqlite3.Connection, gasto_id : int, telegram_usuario_id : int|None = None, categoria_id : int|None = None, 
                    comercio_id : int|None = None, fecha : str|None = None, monto : float|None = None, recibo_file_id : str|None = None, 
                    descripcion : str|None = None) -> int:
    cursor = conn.cursor()

    # Validar gasto_id
    if type(gasto_id) is not int:
        raise ValueError ("Coloque un gasto_id correcto.")

    if gasto_id <= 0:
        raise ValueError ("Coloque un gasto_id correcto.")
    
    # Validar registro actual
    gasto = obtener_gasto(conn, gasto_id) 

    # Completar datos faltantes
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

    if recibo_file_id is None:
        recibo_file_id = gasto["recibo_file_id"]

    if descripcion is None:
        descripcion = gasto["descripcion"]
    
    # Validar datos finales
    if type(telegram_usuario_id) is not int:
        raise ValueError ("Coloque un telegram_usuario_id correcto.")
    
    if telegram_usuario_id <= 0:
        raise ValueError ("Coloque un telegram_usuario_id correcto.")
    

    if type(categoria_id) is not int:
        raise ValueError ("Coloque una categoria_id correcta.")
    
    if categoria_id <= 0:
        raise ValueError ("Coloque una categoria_id correcta.")
    

    if type(comercio_id) is not int:
        raise ValueError ("Coloque un comercio_id correcto.")
    
    if comercio_id <= 0:
        raise ValueError ("Coloque un comercio_id correcto.")
    

    try:
        fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M")

    except ValueError as V:
        raise ValueError ("Coloque una fecha correcta. Ej: YYYY-MM-DD HH:MM") from V
    
    if 2025 > int(datetime.strftime(fecha, "%Y")):
        raise ValueError ("Coloque un año correcto (2025+)")    

    fecha = fecha.strftime("%Y-%m-%d %H:%M")


    if not isinstance(monto, float):
        raise ValueError ("Coloque un monto correcto.")
    
    if monto <= 0.0:
        raise ValueError ("Coloque un monto mayor a 0,0.")
    

    if not isinstance(descripcion, str):
        raise ValueError ("Coloque una descripción correcta.")
    

    if type(recibo_file_id) is not str:
        raise ValueError ("Coloque un recibo_file_id correcto.")
    
    # SQL
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

# Suma gasto total
def calcular_gasto_total(conn : sqlite3.Connection) -> float:
    cursor = conn.cursor()
    
    # SQL
    try: 
        cursor.execute('''SELECT COALESCE(SUM(monto), 0.0) FROM GASTO
                       ''')

        monto = cursor.fetchone()

    except sqlite3.Error as E:
        raise Exception ("Error al sumar gastos.") from E
    
    return monto[0]

# Suma gasto por mes 
def calcular_gasto_mes(conn : sqlite3.Connection, mes : int, año : int|None = None) -> float:
    cursor = conn.cursor()
    
    # Validaciones 
    if not 0 < mes < 13: # Rango de meses inválidos
        raise ValueError ("Coloque un número de mes correcto. Ej: (1-12)")

    if not año: # Año actual por defecto
        año_actual : str = datetime.now().strftime("%Y")
        año = año_actual
    
    if not 2025 <= año <= 2027: # Rango de años inválidos 
        raise ValueError("Año fuera del rango.")

    try:
        periodo = datetime.strptime(f"{año}-{mes:02}", "%Y-%m") 

    except ValueError as V:
        raise Exception ("Coloque un año correcto. Ej: AAAA") from V

    # SQL
    try:
        cursor.execute('''
                       SELECT ROUND(COALESCE(SUM(monto), 0), 2) FROM GASTO
                       WHERE strftime("%Y-%m", fecha) = (?)
                       ''', (periodo.strftime("%Y-%m"), ))

        gasto_mes = cursor.fetchone()

    except sqlite3.Error as E:
        raise Exception ("Error al intentar calcular el gasto por mes.") from E 
    
    return gasto_mes[0]

# Suma gasto por comercio
def calcular_gasto_comercio(conn : sqlite3.Connection, comercio_id : int) -> float:
    cursor = conn.cursor()

    # Validaciones
    if not isinstance(comercio_id, int):
        raise ValueError ("Coloque un comercio_id correcto.")
    
    if comercio_id <= 0:
        raise ValueError ("Coloque un comercio_id correcto.")

    # SQL
    try:
        cursor.execute('''
                       SELECT ROUND(COALESCE(SUM(monto), 0), 2) FROM GASTO WHERE comercio_id = (?)
                       ''', (comercio_id, ))

        gasto_comercio = cursor.fetchone()

    except sqlite3.Error as E:
        raise Exception ("Error al intentar calcular gasto por comercio.") from E
    
    return gasto_comercio[0]

# Suma gasto por categoria 
def calcular_gasto_categoria(conn : sqlite3.Connection, categoria_id : int) -> float:
    cursor = conn.cursor()

    # Validaciones
    if not isinstance(categoria_id, int):
        raise ValueError ("Coloque una categoria_id correcta.")
    
    if categoria_id <= 0:
        raise ValueError("Coloque una categoria_id correcta.")
    
    # SQL
    try:
        cursor.execute('''
                       SELECT ROUND(COALESCE(SUM(monto), 0), 2) FROM GASTO WHERE categoria_id = (?)
                       ''', (categoria_id, ))
        
        gasto_categoria = cursor.fetchone()

    except sqlite3.Error as E:
        raise Exception ("Error al intentar calcular gasto por categoria.") from E
    
    return gasto_categoria[0]

# Calcular promedio de gastos
def calcular_promedio_gastos(conn : sqlite3.Connection) -> float:
    cursor = conn.cursor()

    # SQL
    try:
        cursor.execute('''
                    SELECT COALESCE(ROUND(AVG(monto), 2), 0.0) AS promedio FROM GASTO
                       ''')
        
        promedio = fetchone(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al calcular el promedio.") from E
    
    return promedio["promedio"]

# Calcular gasto minimo 
def calcular_gasto_minimo(conn : sqlite3.Connection) -> float:
    cursor = conn.cursor()

    # SQL
    try:
        cursor.execute('''SELECT COALESCE(ROUND(MIN(monto), 2), 0.0) AS monto from GASTO''')

        monto = fetchone(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al calcular el gasto mínimo.") from E
    
    return monto["monto"]

# Calcular gasto maximo 
def calcular_gasto_maximo(conn : sqlite3.Connection) -> float:
    cursor = conn.cursor()

    # SQL
    try:
        cursor.execute('''SELECT COALESCE(ROUND(MAX(monto), 2), 0.0) AS monto from GASTO''')

        monto = fetchone(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al calcular el gasto máximo.") from E
    
    return monto["monto"]

# Obtener un gasto 
def obtener_gasto(conn : sqlite3.Connection, gasto_id : int) -> dict:
    cursor = conn.cursor()

    # SQL
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

    # SQL
    try:
        cursor.execute('''SELECT * FROM GASTO''')

    except Exception as E:
        raise Exception ("Error al obtener los gastos.") from E
    
    return fetchall(cursor)

# Suma total de gastos de las categorias
def obtener_totales_por_categoria(conn : sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()

    # SQL
    try:
        cursor.execute('''
                       SELECT C.nombre, 
                       ROUND(SUM(monto), 2) AS total 
                       FROM GASTO G 
                       JOIN CATEGORIA C 
                       ON G.categoria_id = C.categoria_id 
                       GROUP BY C.categoria_id
                       ''')
        
        gastos = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al sumar los gastos por categoria.") from E
    
    return gastos

# Obtener gastos entre fechas
def obtener_gastos_entre_fechas(conn : sqlite3.Connection, fecha_inicio : str, fecha_final : str) -> list[dict]:
    cursor = conn.cursor()

    # Validaciones
    try:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")

    except ValueError as V:
        raise Exception ("Coloque una fecha correcta.") from V

    if not 2025 <= int(fecha_inicio.strftime("%Y")): # Años invalidos fecha_inicio
        raise ValueError ("Coloque un año correcto. Ej: YYYY.")
    
    if not 2025 <= int(fecha_final.strftime("%Y")) <= 2027: # Años invalidos fecha_final
        raise ValueError ("Coloque un año correcto. Ej: YYYY")
    
    if fecha_inicio > fecha_final: # Diferencia entre fechas 
        raise ValueError ("Las fechas deben ser ascendentes.")

    # SQL
    try:
        cursor.execute('''
                    SELECT * FROM GASTO WHERE DATE(fecha) BETWEEN (?) AND (?) ORDER BY fecha
                       ''', (fecha_inicio.strftime("%Y-%m-%d"), fecha_final.strftime("%Y-%m-%d")))
        
        gastos = fetchall(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al obtener gastos entre fechas.") from E
    
    return gastos

# Obtener últimos gastos 
def obtener_ultimos_gastos(conn : sqlite3.Connection, limit : int = 3) -> list[dict]:
    cursor = conn.cursor()

    # Validaciones
    if type(limit) is not int:
        raise ValueError ("Coloque un número.")
    
    if 2 > limit:
        raise ValueError ("Limit debe ser mayor a 2.")

    # SQL
    try:
        cursor.execute('''SELECT * FROM GASTO ORDER BY gasto_id DESC LIMIT (?)
                       ''', (limit, ))

    except sqlite3.Error as E:
        raise Exception ("Error al obtener los ultimos gastos.") from E
    
    return fetchall(cursor)

# Buscar gastos por texto
def buscar_gastos_por_texto(conn : sqlite3.Connection, texto : str ="") -> list[dict]:
    cursor = conn.cursor()

    # Validaciones
    if not isinstance(texto, str):
        raise ValueError ("Coloque un texto correcto.")
    
    if not texto.strip():
        raise ValueError ("Coloque un texto.")

    # SQL
    try:
        cursor.execute('''
                       SELECT * FROM GASTO WHERE descripcion LIKE (?)
                       ''', (f"%{texto}%", ))
        
        gastos = fetchall(cursor)
    
    except sqlite3.Error as E:
        raise Exception ("Error al buscar gasto por texto.") from E
    
    return gastos

