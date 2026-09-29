from abc import ABC, abstractmethod

from src.models import Answer, SearchResult


class AnswerGenerator(ABC):
    """Generate an answer from retrieved document context."""

    @abstractmethod
    def generate(
        self,
        question: str,
        context: str,
        references: list[SearchResult],
    ) -> Answer:
        """Generate an answer using the provided context."""
        raise NotImplementedError

class MockAnswerGenerator(AnswerGenerator):
    """Generate deterministic answers for testing."""

    def generate(
        self,
        question: str,
        context: str,
        references: list[SearchResult],
    ) -> Answer:
        return Answer(
            text=f"Question: {question}\nContext: {context}",
            references=references,
        )