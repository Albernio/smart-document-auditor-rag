from src.context_builder import build_context
from src.models import Chunk, SearchResult


def test_build_context_returns_empty_string_for_no_results() -> None:
    result = build_context([])

    assert result == ""

def test_build_context_includes_chunk_text() -> None:
    results = [
        SearchResult(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=0,
                page_number=2,
                document_hash="abc123",
            ),
            distance=0.1,
        )
    ]

    result = build_context(results)

    assert "The provider must respond within thirty days." in result

def test_build_context_includes_document_and_chunk_reference() -> None:
    results = [
        SearchResult(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=2,
                page_number=2,
                document_hash="abc123",
            ),
            distance=0.1,
        )
    ]

    result = build_context(results)

    assert "abc123" in result
    assert "Chunk: 2" in result