from pathlib import Path
import pytest

from src.chunking import chunk_text, chunk_document
from src.models import Document


def test_empty_text_returns_no_chunks() -> None:
    chunks = chunk_text("", document_hash="abc123")

    assert chunks == []


def test_short_text_returns_one_chunk() -> None:
    text = "Hello world"

    chunks = chunk_text(
        text,
        document_hash="abc123",
        chunk_size=100,
        overlap=20
    )

    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].index == 0
    assert chunks[0].document_hash == "abc123"


def test_long_text_is_split_into_multiple_chunks() -> None:
    text = "A" * 2500

    chunks = chunk_text(
        text,
        document_hash="abc123",
        chunk_size=1000,
        overlap=200,
    )

    assert len(chunks) == 3

def test_chunks_have_expected_overlap() -> None:
    text = "0123456789" * 300

    chunks = chunk_text(
        text,
        document_hash="abc123",
        chunk_size=100,
        overlap=20,
    )

    assert chunks[0].text[-20:] == chunks[1].text[:20]
    assert chunks[1].text[-20:] == chunks[2].text[:20]

def test_chunk_size_must_be_positive() -> None:
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("hello", document_hash="abc123", chunk_size=0)


def test_overlap_cannot_be_negative() -> None:
    with pytest.raises(ValueError, match="overlap cannot be negative"):
        chunk_text("hello", document_hash="abc123",  chunk_size=100, overlap=-1)


def test_overlap_must_be_smaller_than_chunk_size() -> None:
    with pytest.raises(ValueError, match="overlap must be smaller"):
        chunk_text("hello", document_hash="abc123",  chunk_size=100, overlap=100)

def test_chunk_document_uses_document_data() -> None:
    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="abc123",
        size=5000,
        text="A" * 2500,
    )

    chunks = chunk_document(
        document,
        chunk_size=1000,
        overlap=200,
    )

    assert len(chunks) == 3
    assert all(chunk.document_hash == "abc123" for chunk in chunks)

def test_chunks_have_sequential_indexes() -> None:
    text = "A" * 2500

    chunks = chunk_text(
        text,
        document_hash="abc123",
        chunk_size=1000,
        overlap=200,
    )

    assert [chunk.index for chunk in chunks] == [0, 1, 2]