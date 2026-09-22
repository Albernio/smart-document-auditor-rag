from pathlib import Path

from reportlab.pdfgen import canvas

from src.pdf_extraction import extract_text


def create_test_pdf(path: Path, pages: list[str]) -> None:
    pdf = canvas.Canvas(str(path))

    for page_text in pages:
        pdf.drawString(100, 750, page_text)
        pdf.showPage()

    pdf.save()


def test_extract_text_from_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "document.pdf"
    create_test_pdf(
        pdf_path,
        [
            "First page",
            "Second page",
        ],
    )

    text = extract_text(pdf_path)

    assert "First page" in text
    assert "Second page" in text

def test_extract_text_ignores_empty_pages(tmp_path: Path) -> None:
    pdf_path = tmp_path / "document.pdf"
    create_test_pdf(
        pdf_path,
        [
            "First page",
            "",
            "Third page",
        ],
    )

    text = extract_text(pdf_path)

    assert "First page" in text
    assert "Third page" in text