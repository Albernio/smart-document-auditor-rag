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