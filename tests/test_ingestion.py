from pathlib import Path
import pytest

from src.ingestion import ingest_file


def test_ingest_file_creates_document(tmp_path: Path) -> None:
    file_path = tmp_path / "contract.pdf"
    file_path.write_bytes(b"fake pdf content")

    document = ingest_file(file_path)

    assert document.path == file_path
    assert document.filename == "contract.pdf"
    assert document.file_hash
    assert document.size == len(b"fake pdf content")

def test_ingest_rejects_non_pdf(tmp_path: Path) -> None:
    file_path = tmp_path / "contract.txt"
    file_path.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="File is not a PDF"):
        ingest_file(file_path)

def test_ingest_file_rejects_empty_file(tmp_path: Path) -> None:
    file_path = tmp_path / "contract.pdf"
    file_path.touch()

    with pytest.raises(ValueError, match="File is empty"):
        ingest_file(file_path)

def test_ingest_file_rejects_missing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError, match="File Not Found"):
            ingest_file(file_path)