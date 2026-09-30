from src.answer_generator import LLMAnswerGenerator
from tests.fakes import FakeLLMClient, MockAnswerGenerator
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


def test_llm_answer_generator_returns_answer() -> None:
    client = FakeLLMClient()
    generator = LLMAnswerGenerator(client)

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

    assert answer.text == "The provider has thirty days to respond."
    assert answer.references == references

def test_llm_answer_generator_sends_rag_prompt_to_client() -> None:
    client = FakeLLMClient()
    generator = LLMAnswerGenerator(client)

    generator.generate(
        question="How many days does the provider have to respond?",
        context="The provider must respond within thirty days.",
        references=[],
    )

    assert (
        "How many days does the provider have to respond?"
        in client.last_prompt
    )

    assert (
        "The provider must respond within thirty days."
        in client.last_prompt
    )

    assert (
        "Do not invent facts, dates, obligations, or references."
        in client.last_prompt
    )