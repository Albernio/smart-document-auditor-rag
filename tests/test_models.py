from pathlib import Path

from src.models import Document, Chunk

def test_create_document() -> None:
    path = Path("contract.pdf")

    document = Document(
        path=path,
        filename = "contract.pdf",
        file_hash = "abc123",
        size = 1024,
        text="Contract content",
    )

    assert document.path == path
    assert document.filename == "contract.pdf"
    assert document.file_hash == "abc123"
    assert document.size == 1024
    assert document.text == "Contract content"

def test_document_text_defaults_to_empty() -> None:
    document = Document(
        path=Path("contract.pdf"),
        filename="contract.pdf",
        file_hash="abc123",
        size=1024,
    )

    assert document.text == ""

def test_chunk_creation() -> None:
    chunk = Chunk(
        text="Contract obligations",
        index=0,
        document_hash="abc123",
    )

    assert chunk.text == "Contract obligations"
    assert chunk.index == 0
    assert chunk.document_hash == "abc123"