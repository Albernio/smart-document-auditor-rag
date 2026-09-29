from pathlib import Path
import pytest
from reportlab.pdfgen import canvas

from src.ingestion import ingest_file, ingest_document
from src.hashing import calculate_file_hash
from src.embeddings import EmbeddingModel

def create_test_pdf(path: Path, text: str) -> None:
    pdf = canvas.Canvas(str(path))
    pdf.drawString(100, 750, text)
    pdf.save()

def create_empty_pdf(path: Path) -> None:
        pdf = canvas.Canvas(str(path))
        pdf.save()

def test_ingest_file_creates_document(tmp_path: Path) -> None:
    file_path = tmp_path / "contract.pdf"
    create_test_pdf(file_path, "Contract content")

    document = ingest_file(file_path)

    assert document.path == file_path
    assert document.filename == "contract.pdf"
    assert document.file_hash
    assert document.size > 0
    assert "Contract content" in document.text

def test_ingest_rejects_non_pdf(tmp_path: Path) -> None:
    file_path = tmp_path / "contract.txt"
    file_path.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="File is not a PDF"):
        ingest_file(file_path)

def test_ingest_file_rejects_empty_file(tmp_path: Path) -> None:
    file_path = tmp_path / "contract.pdf"
    file_path.touch()

    with pytest.raises(ValueError, match="File is empty"):
        ingest_file(file_path)

def test_ingest_file_rejects_missing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError, match="File Not Found"):
        ingest_file(file_path)

def test_ingest_file_accepts_pdf_without_text(tmp_path: Path) -> None:
    file_path = tmp_path / "scanned.pdf"
    create_empty_pdf(file_path)

    document = ingest_file(file_path)

    assert document.path == file_path
    assert document.filename == "scanned.pdf"
    assert document.file_hash
    assert document.size > 0
    assert document.text == ""


def test_ingest_document_persists_document(tmp_path: Path) -> None:
    pdf_path = tmp_path / "contract.pdf"

    create_test_pdf(pdf_path, "The provider must respond within thirty days.")

    embedding_model = EmbeddingModel()

    document_id = ingest_document(
        pdf_path,
        embedding_model,
    )

    assert document_id > 0

def test_ingest_document_persists_chunks(
    tmp_path: Path,
    database_connection,
) -> None:
    pdf_path = tmp_path / "contract.pdf"

    create_test_pdf(pdf_path, "The provider must respond within thirty days.")

    embedding_model = EmbeddingModel()

    document_id = ingest_document(
        pdf_path,
        embedding_model,
    )

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM document_chunks
            WHERE document_id = %s;
            """,
            (document_id,),
        )

        result = cursor.fetchone()

    assert result[0] > 0

def test_ingest_document_persists_document_metadata(
    tmp_path: Path,
    database_connection,
) -> None:
    pdf_path = tmp_path / "contract.pdf"

    create_test_pdf(
        pdf_path,
        "The provider must respond within thirty days.",
    )

    expected_hash = calculate_file_hash(pdf_path)
    expected_size = pdf_path.stat().st_size

    embedding_model = EmbeddingModel()

    document_id = ingest_document(
        pdf_path,
        embedding_model,
    )

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT filename, file_hash, size
            FROM documents
            WHERE id = %s;
            """,
            (document_id,),
        )

        result = cursor.fetchone()

    assert result == (
        "contract.pdf",
        expected_hash,
        expected_size,
    )

def test_ingest_document_persists_chunk_indexes(
    tmp_path: Path,
    database_connection,
) -> None:
    pdf_path = tmp_path / "contract.pdf"

    create_test_pdf(
        pdf_path,
        "The provider must respond within thirty days.",
    )

    embedding_model = EmbeddingModel()

    document_id = ingest_document(
        pdf_path,
        embedding_model,
    )

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT chunk_index
            FROM document_chunks
            WHERE document_id = %s
            ORDER BY chunk_index;
            """,
            (document_id,),
        )

        indexes = [row[0] for row in cursor.fetchall()]

    assert indexes == list(range(len(indexes)))

def test_ingest_document_rejects_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        ingest_document(
            Path("does_not_exist.pdf"),
            EmbeddingModel(),
        )

def test_ingest_document_persists_384_dimension_embeddings(
    tmp_path: Path,
    database_connection,
) -> None:
    pdf_path = tmp_path / "contract.pdf"

    create_test_pdf(
        pdf_path,
        "The provider must respond within thirty days.",
    )

    embedding_model = EmbeddingModel()

    document_id = ingest_document(
        pdf_path,
        embedding_model,
    )

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT vector_dims(embedding)
            FROM document_chunks
            WHERE document_id = %s
            LIMIT 1;
            """,
            (document_id,),
        )

        result = cursor.fetchone()

    assert result == (384,)

def test_ingest_document_rejects_non_pdf(
    tmp_path: Path,
) -> None:
    path = tmp_path / "document.txt"
    path.write_text("hello", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="File is not a PDF",
    ):
        ingest_document(
            path,
            EmbeddingModel(),
        )