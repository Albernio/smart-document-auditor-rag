# ADR-0011 — Tesseract OCR para escanear texto en imágenes

## Contexto

El sistema debe procesar PDFs que pueden contener:

- Texto digital extraíble mediante **pypdf**.
- Páginas escaneadas sin capa de texto.
- Documentos mixtos con texto digital e imágenes con texto.

El sistema debe poder convertir el contenido visual en texto para que posteriormente pueda participar en el pipeline RAG.

## Decisión

Usaré **Tesseract OCR** como motor de reconocimiento óptico de caracteres.

## Motivos

- Ejecución local
- Integración sencilla con Python
- Tecnología madura con soporte multilingüe
- Reproducibilidad. Al ejecutarse localmente, no dependemos de APIs externas cuyo comportamiento podría cambiar.
- Coste cero.

## Alternativas

- Tesseract (Elegida)
- Google Cloud Vision
- AWS Textract
- Azure Document Intelligence