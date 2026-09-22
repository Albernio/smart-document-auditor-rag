from pathlib import Path

from src.hashing import calculate_file_hash
from src.validation import validate_file
from src.models import Document


def ingest_file(path: Path) -> Document:
    """Validate a file, create a hash and create a Document object."""

    validate_file(path)

    file_hash = calculate_file_hash(path)

    return Document(
        path=path,
        filename=path.name,
        file_hash=file_hash,
        size=path.stat().st_size
    )