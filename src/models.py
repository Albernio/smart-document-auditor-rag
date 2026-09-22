from dataclasses import dataclass
from pathlib import Path

@dataclass
class Document:
    path: Path
    filename: str
    file_hash: str
    size: int