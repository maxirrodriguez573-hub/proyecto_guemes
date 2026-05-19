# Obtener un registro en un diccionario
def fetchone(cursor) -> dict:
    return dict(cursor.fetchone())

# Obtener lista de registros en una lista de diccionarios
def fetchall(cursor) -> list[dict]:
    rows = cursor.fetchall()
    return [dict(row) for row in rows if row]