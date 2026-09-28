# ADR-0002: Utilizar pypdf para la extracción inicial de texto de documentos PDF

## Estado

Aceptada

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

En esta primera versión del proyecto necesitamos una solución sencilla, gratuita, mantenida y compatible con Python que permita extraer texto de PDFs que contienen una capa de texto.

No todos los archivos PDF contienen texto extraíble. Algunos pueden estar formados únicamente por imágenes escaneadas o utilizar estructuras que dificulten la extracción. Por este motivo, la extracción mediante OCR se considera una capacidad diferente que se incorporará posteriormente si el proyecto lo requiere.

## Decisión

Utilizaremos `pypdf` como biblioteca inicial para la extracción de texto de documentos PDF.

La extracción se realizará página por página mediante `PdfReader` y `page.extract_text()`.

El resultado de la extracción será un único `str` que contendrá el texto combinado de las páginas del documento.

Si una página no contiene texto extraíble, se omitirá su contenido.

Si ninguna página contiene texto extraíble, la función devolverá una cadena vacía (`""`).

La implementación inicial será deliberadamente sencilla y no incorporará OCR ni lógica específica para diferentes tipos de documentos PDF.

La dependencia `pypdf` se declarará en `pyproject.toml`.

## Alternativas consideradas

### pypdf

Se selecciona porque proporciona una API sencilla para leer documentos PDF y extraer su capa de texto, es una biblioteca Python adecuada para este caso de uso y permite mantener la primera versión del pipeline sencilla.

### PyMuPDF

PyMuPDF proporciona capacidades avanzadas para trabajar con documentos PDF y puede ofrecer un mayor control sobre la extracción y el procesamiento del contenido.

No se selecciona inicialmente porque las necesidades actuales del proyecto son más simples y `pypdf` permite implementar la primera versión de la extracción sin introducir capacidades adicionales que todavía no necesitamos.

Podrá evaluarse posteriormente si las necesidades de extracción requieren mayor control o rendimiento.

### pdfplumber

`pdfplumber` proporciona herramientas adicionales para analizar el contenido y el diseño de documentos PDF.

No se selecciona inicialmente porque el objetivo actual es obtener texto para alimentar el pipeline RAG, no realizar análisis detallado del layout del documento.

Podrá considerarse posteriormente si necesitamos preservar información estructural como tablas, posiciones o elementos de diseño.

### OCR

El OCR permite extraer texto de documentos escaneados que no contienen una capa de texto.

No se incorpora en esta etapa porque introduce una problemática diferente: reconocimiento óptico de caracteres, procesamiento de imágenes, mayor coste computacional y una nueva fuente potencial de errores.

El OCR se considera una capacidad futura independiente de la extracción de texto estándar de un PDF.

## Consecuencias

### Positivas

- Permite implementar rápidamente la primera etapa de extracción de texto.
- Mantiene el pipeline de ingestión sencillo.
- No requiere servicios externos.
- Permite trabajar localmente con los documentos.
- Se integra directamente con el procesamiento posterior de chunks y embeddings.
- Facilita la creación de tests deterministas sobre documentos PDF.
- Permite detectar posteriormente documentos que no contienen texto extraíble.

### Negativas

- No todos los PDFs permiten extraer texto correctamente.
- Los documentos escaneados pueden producir una cadena vacía porque no contienen una capa de texto.
- La calidad de la extracción puede variar dependiendo de cómo se haya generado el PDF.
- La estructura visual del documento no se conserva necesariamente en el texto extraído.
- Tablas, columnas, encabezados, pies de página y otros elementos complejos pueden no quedar representados de forma óptima.
- Para documentos que requieren OCR será necesario incorporar una solución adicional.

## Alcance

Esta decisión se limita a la extracción inicial de texto de archivos PDF que contienen una capa de texto accesible.

No establece que `pypdf` vaya a ser necesariamente la solución definitiva para todos los tipos de documentos PDF.

El objetivo de esta decisión es proporcionar una primera implementación estable y sencilla sobre la que construir las siguientes etapas del pipeline RAG.

## Comportamiento ante PDFs sin texto extraíble

Un PDF válido que no contenga texto extraíble no se considerará automáticamente un archivo inválido.

La función de extracción devolverá `""`.

La decisión sobre cómo tratar posteriormente estos documentos pertenece a la capa de ingestión y validación del pipeline.

En una evolución futura, el sistema podrá detectar esta situación y derivar el documento a un proceso de OCR.

## Estado futuro

Si el proyecto necesita procesar documentos escaneados, tablas complejas, layouts avanzados o PDFs con problemas de extracción, se evaluará la incorporación de capacidades adicionales.

Entre las posibles evoluciones se encuentran:

- incorporación de OCR;
- evaluación de PyMuPDF u otras bibliotecas de extracción;
- extracción específica de tablas;
- preservación de estructura y layout;
- detección automática del tipo de documento;
- pipeline híbrido que seleccione diferentes estrategias de extracción según las características del PDF.