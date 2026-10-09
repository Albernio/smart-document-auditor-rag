from pathlib import Path

import pytesseract
from PIL import Image



def extract_text_from_image(path: Path) -> str:
    """Extract text from an image using Tesseract OCR"""

    with Image.open(path) as image:
        text = pytesseract.image_to_string(image)

    return text.strip()