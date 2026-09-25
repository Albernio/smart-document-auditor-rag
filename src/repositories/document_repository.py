import psycopg

from src.models import Document, VectorRecord


class DocumentRepository:
    """Persist documents and their vector data."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self.connection = connection

    def save_document(self, document: Document) -> int:
        """Save a document and return its database identifier."""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (
                    filename,
                    file_hash,
                    size
                )
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (
                    document.filename,
                    document.file_hash,
                    document.size,
                ),
            )

            document_id = cursor.fetchone()[0]

        return document_id

    def save_vector_records(
        self,
        document_id: int,
        records: list[VectorRecord],
    ) -> None:
        """Save chunk and embedding records for a document."""

        if not records:
            return

        with self.connection.cursor() as cursor:
            for record in records:
                cursor.execute(
                    """
                    INSERT INTO document_chunks (
                        document_id,
                        chunk_index,
                        text,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s::vector);
                    """,
                    (
                        document_id,
                        record.chunk.index,
                        record.chunk.text,
                        str(record.embedding.vector),
                    ),
                )