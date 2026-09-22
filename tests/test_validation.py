from pathlib import Path

import pytest

from src.validation import validate_file


def test_missing_file_raises_file_not_found() -> None:
    path = Path("does_not_exist.pdf")

    with pytest.raises(FileNotFoundError):
        validate_file(path)

def test_non_pdf_file_raises_value_error(tmp_path: Path) -> None:
    path = tmp_path / "document.txt"
    path.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError):
        validate_file(path)

def test_empty_file_raises_value_error(tmp_path: Path) -> None:
    path = tmp_path / "document.pdf"
    path.touch()

    with pytest.raises(ValueError):
        validate_file(path)