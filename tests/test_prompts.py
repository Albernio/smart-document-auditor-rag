from src.prompts import build_rag_prompt


def test_build_rag_prompt_includes_question() -> None:
    prompt = build_rag_prompt(
        question="How many days does the provider have to respond?",
        context="The provider must respond within thirty days.",
    )

    assert "How many days does the provider have to respond?" in prompt


def test_build_rag_prompt_includes_context() -> None:
    prompt = build_rag_prompt(
        question="How many days does the provider have to respond?",
        context="The provider must respond within thirty days.",
    )

    assert "The provider must respond within thirty days." in prompt


def test_build_rag_prompt_contains_grounding_rules() -> None:
    prompt = build_rag_prompt(
        question="What is the response deadline?",
        context="The provider must respond within thirty days.",
    )

    assert "Do not use information that is not present in the context." in prompt
    assert "Do not invent facts, dates, obligations, or references." in prompt