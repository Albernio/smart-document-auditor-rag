from src.database import get_connection
from src.models import Document


class DocumentRepository:
    """Persist documents and their vector data."""

    def save_document(self, document: Document) -> int:
        """Save a document and return its database identifier."""

        with get_connection() as connection:
            with connection.cursor() as cursor:
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

            connection.commit()

        return document_id