from src.database import get_connection
from src.schema import create_tables


def test_tables_exist() -> None:
    create_tables()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name IN ('documents', 'document_chunks')
                ORDER BY table_name;
                """
            )

            tables = [row[0] for row in cursor.fetchall()]

    assert tables == ["document_chunks", "documents"]

def test_pgvector_extension_exists() -> None:
    create_tables()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT extname
                FROM pg_extension
                WHERE extname = 'vector';
                """
            )

            extension = cursor.fetchone()

    assert extension == ("vector",)


def test_embedding_column_has_correct_dimension() -> None:
    create_tables()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT udt_name
                FROM information_schema.columns
                WHERE table_name = 'document_chunks'
                AND column_name = 'embedding';
                """
            )

            result = cursor.fetchone()

    assert result == ("vector",)