# Obtener un registro en un diccionario
def fetchone(cursor) -> dict:
    return dict(cursor.fetchone())