import pytest

from src.chunking import chunk_text


def test_empty_text_returns_no_chunks() -> None:
    chunks = chunk_text("")

    assert chunks == []


def test_short_text_returns_one_chunk() -> None:
    text = "Hello world"

    chunks = chunk_text(text, chunk_size=100, overlap=20)

    assert chunks == [text]


def test_long_text_is_split_into_multiple_chunks() -> None:
    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=200,
    )

    assert len(chunks) == 3

def test_chunks_have_expected_overlap() -> None:
    text = "0123456789" * 300

    chunks = chunk_text(
        text,
        chunk_size=100,
        overlap=20,
    )

    assert chunks[0][-20:] == chunks[1][:20]
    assert chunks[1][-20:] == chunks[2][:20]

def test_chunk_size_must_be_positive() -> None:
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("hello", chunk_size=0)


def test_overlap_cannot_be_negative() -> None:
    with pytest.raises(ValueError, match="overlap cannot be negative"):
        chunk_text("hello", chunk_size=100, overlap=-1)


def test_overlap_must_be_smaller_than_chunk_size() -> None:
    with pytest.raises(ValueError, match="overlap must be smaller"):
        chunk_text("hello", chunk_size=100, overlap=100)