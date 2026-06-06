from database.utils import fetchone, fetchall
from datetime import datetime
import sqlite3 # Type Hints

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

# Suma gasto total
def calcular_gasto_total(conn : sqlite3.Connection) -> float:
    cursor = conn.cursor()
    
    try: 
        cursor.execute('''SELECT COALESCE(SUM(monto), 0.0) FROM GASTO
                       ''')

        monto = cursor.fetchone()

    except sqlite3.Error as E:
        raise Exception ("Error al sumar montos.") from E
    
    return monto[0]

# Suma gasto por mes 
def calcular_gasto_mes(conn : sqlite3.Connection, mes : int, año : int|None = None) -> float:
    cursor = conn.cursor()
    
    # Validaciones 
    if not año: # Año actual por defecto
        año_actual : str = datetime.now().strftime("%Y")
        año = año_actual
    
    if not 2025 <= año <= 2027: # Rango de años inválidos 
        raise ValueError("Año fuera del rango.")

    if not 0 < mes < 13: # Rango de meses inválidos
        raise ValueError ("Coloque un número de mes correcto. Ej: (1-12)")

    try:
        periodo = datetime.strptime(f"{año}-{mes:02}", "%Y-%m") 

    except ValueError as V:
        raise Exception ("Coloque un año correcto. Ej: AAAA") from V

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

    try:
        cursor.execute('''SELECT COALESCE(ROUND(MIN(monto), 2), 0.0) AS monto from GASTO''')

        monto = fetchone(cursor)

    except sqlite3.Error as E:
        raise Exception ("Error al calcular el gasto mínimo.") from E
    
    return monto

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

# Suma total de gastos de las categorias
def obtener_totales_por_categoria(conn : sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()

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

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")

    except ValueError as V:
        raise Exception ("Coloque una fecha correcta.") from V

    # Validaciones
    if not 2025 <= int(fecha_inicio.strftime("%Y")): # Años invalidos fecha_inicio
        raise ValueError ("Coloque un año correcto. Ej: YYYY.")
    
    if not 2025 <= int(fecha_final.strftime("%Y")) <= 2027: # Años invalidos fecha_final
        raise ValueError ("Coloque un año correcto. Ej: YYYY")
    
    if fecha_inicio > fecha_final: # Diferencia entre fechas 
        raise ValueError ("Las fechas deben ser ascendentes.")

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
    
    if 0 > limit:
        raise ValueError ("Limit no puede ser negativo.")

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

    try:
        cursor.execute('''
                       SELECT * FROM GASTO WHERE descripcion LIKE (?)
                       ''', (f"%{texto}%", ))
        
        gastos = fetchall(cursor)
    
    except sqlite3.Error as E:
        raise Exception ("Error al buscar gasto por texto.") from E
    
    return gastos

