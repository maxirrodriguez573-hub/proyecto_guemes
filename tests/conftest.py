from database.connection import conexion
import pytest

@pytest.fixture
def conn():
    conn = conexion()

    yield conn

    conn.close()