from pathlib import Path

from src.database import get_connection
from src.models import Document
from src.repositories.document_repository import DocumentRepository


def test_save_document() -> None:
    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="abc123",
        size=1024,
        text="Contract content",
    )

    repository = DocumentRepository()

    document_id = repository.save_document(document)

    assert document_id > 0

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT filename, file_hash, size
                FROM documents
                WHERE id = %s;
                """,
                (document_id,),
            )

            row = cursor.fetchone()

    assert row == (
        "contract.pdf",
        "abc123",
        1024,
    )