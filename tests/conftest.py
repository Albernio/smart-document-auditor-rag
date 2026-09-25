import pytest
import psycopg

from src.database import get_connection


@pytest.fixture
def database_connection() -> psycopg.Connection:
    with get_connection() as connection:
        yield connection
        connection.rollback()