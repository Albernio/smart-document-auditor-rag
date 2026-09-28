from pathlib import Path
import pytest

from src.models import Document, Chunk, VectorRecord, Embedding, SearchResult
from src.repositories.document_repository import DocumentRepository

# save_vector tests
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

# search_similar tests
def test_search_similar_returns_most_similar_chunks(database_connection) -> None:
    repository = DocumentRepository(database_connection)

    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="search-test-document",
        size=1024,
    )

    document_id = repository.save_document(document)

    records = [
        VectorRecord(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=0,
                document_hash=document.file_hash,
            ),
            embedding=Embedding(
                vector=[1.0] + [0.0]*383,
                dimension=384,
            ),
        ),
        VectorRecord(
            chunk=Chunk(
                text="The supplier must protect personal data.",
                index=1,
                document_hash=document.file_hash,
            ),
            embedding=Embedding(
                vector=[0.0, 1.0] + [0.0]*382,
                dimension=384,
            ),
        ),
        VectorRecord(
            chunk=Chunk(
                text="The contract is valid for two years.",
                index=2,
                document_hash=document.file_hash,
            ),
            embedding=Embedding(
                vector=[0.0, 0.0, 1.0] + [0.0]*381,
                dimension=384,
            ),
        ),
    ]

    repository.save_vector_records(
        document_id=document_id,
        records=records,
    )

    results = repository.search_similar(
        query_embedding=[1.0] + [0.0]*383,
        limit=3,
    )

    assert len(results) == 3

    assert results[0].chunk.text == (
        "The provider must respond within thirty days."
    )

def test_search_similar_returns_search_results(database_connection) -> None:
    repository = DocumentRepository(database_connection)

    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="search-result-test",
        size=1024,
    )

    document_id = repository.save_document(document)

    record = VectorRecord(
        chunk=Chunk(
            text="The provider must respond within thirty days.",
            index=0,
            document_hash=document.file_hash,
        ),
        embedding=Embedding(
            vector=[1.0] + [0.0]*383,
            dimension=384,
        ),
    )

    repository.save_vector_records(
        document_id=document_id,
        records=[record],
    )

    results = repository.search_similar(
        query_embedding=[1.0] + [0.0]*383,
        limit=1,
    )

    assert len(results) == 1
    assert isinstance(results[0], SearchResult)
    assert isinstance(results[0].chunk, Chunk)
    assert isinstance(results[0].distance, float)

def test_search_similar_preserves_document_hash(database_connection) -> None:
    repository = DocumentRepository(database_connection)

    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="hash-to-preserve",
        size=1024,
    )

    document_id = repository.save_document(document)

    record = VectorRecord(
        chunk=Chunk(
            text="The provider must respond within thirty days.",
            index=0,
            document_hash=document.file_hash,
        ),
        embedding=Embedding(
            vector=[1.0] + [0.0]*383,
            dimension=384,
        ),
    )

    repository.save_vector_records(
        document_id=document_id,
        records=[record],
    )

    results = repository.search_similar(
        query_embedding=[1.0] + [0.0]*383,
        limit=1,
    )

    assert results[0].chunk.document_hash == "hash-to-preserve"

def test_search_similar_respects_limit(database_connection) -> None:
    repository = DocumentRepository(database_connection)

    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="limit-test-document",
        size=1024,
    )

    document_id = repository.save_document(document)

    records = []

    for index in range(3):
        vector = [0.0] * 384
        vector[index] = 1.0

        records.append(
            VectorRecord(
                chunk=Chunk(
                    text=f"Chunk {index}",
                    index=index,
                    document_hash=document.file_hash,
                ),
                embedding=Embedding(
                    vector=vector,
                    dimension=384,
                ),
            )
        )

    repository.save_vector_records(
        document_id=document_id,
        records=records,
    )

    results = repository.search_similar(
        query_embedding=[1.0] + [0.0]*383,
        limit=2,
    )

    assert len(results) == 2

def test_search_similar_rejects_invalid_limit(database_connection) -> None:
    repository = DocumentRepository(database_connection)

    with pytest.raises(
        ValueError,
        match="Limit must be greater than 0.",
    ):
        repository.search_similar(
            query_embedding=[0.0]*384,
            limit=0,
        )

def test_search_similar_orders_by_distance(database_connection) -> None:
    repository = DocumentRepository(database_connection)

    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="distance-order-test",
        size=1024,
    )

    document_id = repository.save_document(document)

    records = [
        VectorRecord(
            chunk=Chunk(
                text="Exact match",
                index=0,
                document_hash=document.file_hash,
            ),
            embedding=Embedding(
                vector=[1.0] + [0.0]*383,
                dimension=384,
            ),
        ),
        VectorRecord(
            chunk=Chunk(
                text="Different direction",
                index=1,
                document_hash=document.file_hash,
            ),
            embedding=Embedding(
                vector=[0.0, 1.0] + [0.0]*382,
                dimension=384,
            ),
        ),
    ]

    repository.save_vector_records(
        document_id=document_id,
        records=records,
    )

    results = repository.search_similar(
        query_embedding=[1.0] + [0.0]*383,
        limit=2,
    )

    assert results[0].distance <= results[1].distance
    assert results[0].chunk.index == 0