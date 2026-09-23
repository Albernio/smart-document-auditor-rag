import psycopg


def get_connection() -> psycopg.Connection:
    """Create a connection to PostgreSQL."""

    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="document_auditor",
        user="auditor",
        password="auditor",
    )