from src.models import Document, Chunk
from src.pdf_extraction import extract_pages

def chunk_text(
    text: str,
    document_hash: str,
    chunk_size: int = 1000,
    overlap: int = 200,
    page_number: int | None = None,
) -> list[Chunk]:
    """Split text into overlapping chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    if not text:
        return []

    step = chunk_size - overlap

    chunks = []

    for start in range(0, len(text), step):
        chnk_text = text[start:start + chunk_size]
        chunks.append(
            Chunk(
                text=chnk_text,
                index=len(chunks),
                document_hash=document_hash,
                page_number=page_number,
            )
        )

        if start + chunk_size >= len(text):
            break

    return chunks

def chunk_document(
    document: Document,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[Chunk]:
    """Split a document into overlapping chunks."""

    if document.pages is None:
        return chunk_text(
            text=document.text,
            document_hash=document.file_hash,
            chunk_size=chunk_size,
            overlap=overlap,
        )

    chunks = []

    for page_number, page_text in document.pages:
        page_chunks = chunk_text(
            text=page_text,
            document_hash=document.file_hash,
            chunk_size=chunk_size,
            overlap=overlap,
            page_number=page_number,
        )

        for chunk in page_chunks:
            chunk.index = len(chunks)
            chunks.append(chunk)

    return chunks