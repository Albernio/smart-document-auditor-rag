from pathlib import Path

from src.models import Document, Chunk, VectorRecord, Embedding
from src.repositories.document_repository import DocumentRepository


def test_save_document(database_connection) -> None:
    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="abc123",
        size=1024,
        text="Contract content",
    )

    
    repository = DocumentRepository(database_connection)

    document_id = repository.save_document(document)

    assert document_id > 0

    with database_connection.cursor() as cursor:
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

def test_save_vector_records(database_connection) -> None:

    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="def456",
        size=2048,
        text="Contract content",
    )

    records = [
                VectorRecord(
                    chunk=Chunk(
                        text="The provider must respond within thirty days.",
                        index=0,
                        document_hash="def456",
                    ),
                    embedding=Embedding(
                        vector=[1.0] + [0.0] * 383,
                        dimension=384,
                    ),
                ),
                VectorRecord(
                    chunk=Chunk(
                        text="The supplier must protect personal data.",
                        index=1,
                        document_hash="def456",
                    ),
                    embedding=Embedding(
                        vector=[0.0, 1.0] + [0.0] * 382,
                        dimension=384,
                    ),
                ),
            ]

    
    repository = DocumentRepository(database_connection)

    document_id = repository.save_document(document)

    repository.save_vector_records(
        document_id=document_id,
        records=records,
    )

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT chunk_index, text, vector_dims(embedding)
            FROM document_chunks
            WHERE document_id = %s
            ORDER BY chunk_index;
            """,
            (document_id,),
        )

        rows = cursor.fetchall()

    assert rows == [
            (
                0,
                "The provider must respond within thirty days.",
                384,
            ),
            (
                1,
                "The supplier must protect personal data.",
                384,
            ),
        ]