from pathlib import Path

from pypdf import PdfReader


def extract_text(path: Path) -> str:
    """Extract text from all pages of a PDF."""
    reader = PdfReader(path)

    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text)

    return "\n".join(pages_text)

def extract_pages(path: Path) -> list[tuple[int, str]]:
    """Extract text from a PDF while preserving page numbers."""

    reader = PdfReader(path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages.append((page_number, text.strip()))

    return pages