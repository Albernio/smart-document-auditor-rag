# ADR-0004: Character Based Chunking

## Contexto

Los documentos pueden ser demasiado grandes para procesarlos como una única unidad.
Necesitamos dividir el texto antes de generar los embeddings.

## Decisión

Inicialmente, utilizaré chunking basado en caracteres con:

- `chunk_size`: 1000
- `overlap`: 200

Cada chunk conservará además su índice y, cuando esté disponible, el número de página del documento.

## Alternativas

- Chunking por frases.
- Chunking por tokens.
- Chunking semántico.

## Motivo

El chunking basado en caracteres es sencillo, determinista y suficiente para el MVP.

## Consecuencias

La implementación es simple y reproducible. Sin embargo, un chunk puede dividir una idea o una frase entre 2 fragmentos, lo que puede afectar a la calidad del retrieval.

Esta limitación podrá evaluarse posteriormente mediante experimentos con otras estrategias de chunking.