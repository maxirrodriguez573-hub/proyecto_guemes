import sqlite3

# Obtener un registro en un diccionario
def fetchone(cursor : sqlite3.Cursor) -> dict:
    row : sqlite3.Row|None = cursor.fetchone()

    if row is None: # Sí no se obtiene el registro, retornar None
        return None
    
    return dict(row)

# Obtener lista de registros en una lista de diccionarios
def fetchall(cursor : sqlite3.Cursor) -> list[dict]:
    rows : list[sqlite3.Row] = cursor.fetchall()

    return [dict(row) for row in rows]