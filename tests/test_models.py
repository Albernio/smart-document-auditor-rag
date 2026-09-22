from pathlib import Path

from src.models import Document

def test_create_document() -> None:
    path = Path("contract.pdf")

    document = Document(
        path=path,
        filename = "contract.pdf",
        file_hash = "abc123",
        size = 1024
    )

    assert document.path == path
    assert document.filename == "contract.pdf"
    assert document.file_hash == "abc123"
    assert document.size == 1024