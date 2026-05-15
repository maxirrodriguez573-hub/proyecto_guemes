import sqlite3 # Importamos sql

def conexion():
    '''
    Conexión a la base de datos "proyect", donde este tiene el atributo row_factory para que a la hora de obtener los registros, pueda
    formatearlos a diccionarios.
    Este activa las FK cada vez que se conecta a la base de datos.
    '''
    conn = sqlite3.connect("C:/Users/maxir/Documents/Proyecto Guemes/proyect/data/proyecto.db")

    conn.row_factory = sqlite3.Row # Para obtener registros en diccionarios

    conn.execute('''PRAGMA foreign_keys = ON''')

    return conn



