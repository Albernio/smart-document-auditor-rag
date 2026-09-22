from pathlib import Path

from src.hashing import calculate_file_hash


def test_same_file_produces_same_hash(tmp_path: Path) -> None:
    file_path = tmp_path / "document.txt"
    file_path.write_text("hello world", encoding="utf-8")

    hash_1 = calculate_file_hash(file_path)
    hash_2 = calculate_file_hash(file_path)

    assert hash_1 == hash_2