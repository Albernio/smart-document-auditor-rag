from pathlib import Path

from reportlab.pdfgen import canvas

from src.database import get_connection
from src.embeddings import EmbeddingModel
from src.ingestion import ingest_document
from src.llm.ollama_client import OllamaClient
from src.rag import ask_question
from src.repositories.document_repository import DocumentRepository
from src.answer_generator import LLMAnswerGenerator


def create_test_pdf(path: Path) -> None:
    """Create a PDF containing a simple contract."""

    pdf = canvas.Canvas(str(path))

    pdf.drawString(
        100,
        750,
        "The provider must respond to complaints within thirty days.",
    )

    pdf.drawString(
        100,
        700,
        "The supplier must protect all personal data.",
    )

    pdf.drawString(
        100,
        650,
        "The contract is valid for two years.",
    )

    pdf.save()


def test_rag_answers_question_using_real_documents_and_ollama(
    tmp_path: Path,
) -> None:
    pdf_path = tmp_path / "contract.pdf"

    create_test_pdf(pdf_path)

    embedding_model = EmbeddingModel()

    ingest_document(
        pdf_path,
        embedding_model,
    )

    llm_client = OllamaClient(
        model_name="qwen3:8b",
    )

    answer_generator = LLMAnswerGenerator(llm_client)

    with get_connection() as connection:
        repository = DocumentRepository(connection)

        answer = ask_question(
            question="How many days does the provider have to respond to complaints?",
            embedding_model=embedding_model,
            repository=repository,
            answer_generator=answer_generator,
            limit=3,
        )

    assert isinstance(answer.text, str)
    assert answer.text.strip()

    assert len(answer.references) > 0

    assert any(
        "thirty days" in reference.chunk.text.lower()
        for reference in answer.references
    )