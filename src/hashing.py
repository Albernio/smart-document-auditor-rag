from hashlib import sha256
from pathlib import Path


def calculate_file_hash(path : Path) -> str:
    """Calculate the SHA-256 hash of a file."""
    hash_sha256 = sha256()

    with path.open("rb") as file:
        while chunk := file.read(8192):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()