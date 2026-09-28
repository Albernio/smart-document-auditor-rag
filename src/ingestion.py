from pathlib import Path

from src.database import get_connection
from src.hashing import calculate_file_hash
from src.validation import validate_file
from src.pdf_extraction import extract_text
from src.models import Document
from src.embeddings import EmbeddingModel
from src.chunking import chunk_document
from src.repositories.document_repository import DocumentRepository


def ingest_file(path: Path) -> Document:
    """Validate a file, create a hash and create a Document object."""

    validate_file(path)

    file_hash = calculate_file_hash(path)

    text = extract_text(path)

    return Document(
        path=path,
        filename=path.name,
        file_hash=file_hash,
        size=path.stat().st_size,
        text=text,
    )

def ingest_document(
    path: Path,
    embedding_model: EmbeddingModel,
) -> int:
    """Ingest a document and persist its chunks and embeddings."""

    document = ingest_file(path)

    chunks = chunk_document(document)

    records = embedding_model.create_vector_records(chunks)

    with get_connection() as connection:
        repository = DocumentRepository(connection)

        document_id = repository.save_document(document)
        repository.save_vector_records(document_id, records)

        connection.commit()

    return document_id