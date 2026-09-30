from dataclasses import dataclass
from pathlib import Path

@dataclass
class Document:
    path: Path
    filename: str
    file_hash: str
    size: int
    text: str = ""
    pages: list[tuple[int, str]] | None = None

@dataclass
class Chunk:
    text: str
    index: int
    document_hash: str
    page_number: int | None = None

@dataclass
class Embedding:
    vector: list[float]
    dimension: int

@dataclass
class VectorRecord:
    chunk: Chunk
    embedding: Embedding

@dataclass
class SearchResult:
    chunk: Chunk
    distance: float

@dataclass
class Answer:
    text: str
    references: list[SearchResult]