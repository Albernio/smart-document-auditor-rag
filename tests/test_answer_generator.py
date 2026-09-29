from src.answer_generator import MockAnswerGenerator
from src.models import Chunk, SearchResult


def test_mock_answer_generator_returns_answer() -> None:
    generator = MockAnswerGenerator()

    references = [
        SearchResult(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=0,
                document_hash="abc123",
            ),
            distance=0.1,
        )
    ]

    answer = generator.generate(
        question="How many days does the provider have to respond?",
        context="The provider must respond within thirty days.",
        references=references,
    )

    assert answer.text
    assert answer.references == references