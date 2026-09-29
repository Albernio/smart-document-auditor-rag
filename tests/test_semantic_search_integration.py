from pathlib import Path

from reportlab.pdfgen import canvas

from src.database import get_connection
from src.embeddings import EmbeddingModel
from src.ingestion import ingest_document
from src.repositories.document_repository import DocumentRepository
from src.semantic_search import search_documents


def create_test_pdf(path: Path) -> None:
    """Create a PDF containing searchable contract text."""

    pdf = canvas.Canvas(str(path))

    pdf.drawString(
        100,
        750,
        "The provider must respond within thirty days.",
    )

    pdf.drawString(
        100,
        700,
        "The supplier must protect personal data.",
    )

    pdf.drawString(
        100,
        650,
        "The contract is valid for two years.",
    )

    pdf.save()


def test_semantic_search_returns_relevant_chunk(
    tmp_path: Path,
) -> None:
    pdf_path = tmp_path / "contract.pdf"

    create_test_pdf(pdf_path)

    embedding_model = EmbeddingModel()

    document_id = ingest_document(
        pdf_path,
        embedding_model,
    )

    assert document_id > 0

    with get_connection() as connection:
        repository = DocumentRepository(connection)

        results = search_documents(
            query="How many days does the provider have to respond?",
            embedding_model=embedding_model,
            repository=repository,
            limit=3,
        )

    assert len(results) > 0

    assert any(
        "thirty days" in result.chunk.text.lower()
        for result in results
    )