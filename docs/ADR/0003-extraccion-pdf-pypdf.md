# ADR-0003: Utilizar pypdf para la extracción inicial de texto de documentos PDF

## Contexto

La aplicación necesita extraer el contenido textual de los documentos PDF durante el proceso de ingestión para poder procesarlo posteriormente mediante chunking, embeddings y búsqueda vectorial.

La extracción de texto es una etapa fundamental del pipeline:

PDF
↓
Validación
↓
Hashing
↓
Extracción de texto
↓
Chunking
↓
Embeddings
↓
PostgreSQL + pgvector

En esta primera versión del proyecto necesito una solución sencilla, gratuita, mantenida y compatible con Python que permita extraer texto de PDFs que contienen una capa de texto.

No todos los archivos PDF contienen texto extraíble. Algunos pueden estar formados únicamente por imágenes escaneadas o utilizar estructuras que dificulten la extracción. Por este motivo, la extracción mediante OCR se considera una capacidad diferente que se incorporará posteriormente.

## Decisión

Utilizaré `pypdf` como biblioteca inicial para la extracción de texto de documentos PDF.

La implementación inicial será deliberadamente sencilla y no incorporará OCR ni lógica específica para diferentes tipos de documentos PDF.

## Alcance

Esta decisión se limita a la extracción inicial de texto de archivos PDF que contienen una capa de texto accesible.

No establece que `pypdf` vaya a ser necesariamente la solución definitiva para todos los tipos de documentos PDF.