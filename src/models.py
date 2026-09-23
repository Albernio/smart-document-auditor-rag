from dataclasses import dataclass
from pathlib import Path

@dataclass
class Document:
    path: Path
    filename: str
    file_hash: str
    size: int
    text: str = ""

@dataclass
class Chunk:
    text: str
    index: int
    document_hash: str

@dataclass
class Embedding:
    vector: list[float]
    dimension: int