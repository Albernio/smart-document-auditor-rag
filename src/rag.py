from src.answer_generator import AnswerGenerator
from src.context_builder import build_context
from src.embeddings import EmbeddingModel
from src.models import Answer
from src.repositories.document_repository import DocumentRepository
from src.semantic_search import search_documents


def ask_question(
    question: str,
    embedding_model: EmbeddingModel,
    repository: DocumentRepository,
    answer_generator: AnswerGenerator,
    limit: int = 5,
) -> Answer:
    """Answer a question using retrieved document context."""

    results = search_documents(
        query=question,
        embedding_model=embedding_model,
        repository=repository,
        limit=limit,
    )

    context = build_context(results)

    return answer_generator.generate(
        question=question,
        context=context,
        references=results,
    )