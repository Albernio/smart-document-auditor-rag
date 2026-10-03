# ADR-0005: Sentence Transformers para embeddings

## Contexto

El sistema necesita convertir los chunks de texto en vectores numéricos para poder realizar búsquedas semánticas.

Necesito un modelo de embeddings que pueda ejecutarse localmente y que sea sencillo integrar en el MVP.

## Decisión

Utilizaré Sentence Transformers con el modelo:

`all-MiniLM-L6-v2`

EL modelo genera embeddings de 384 dimensiones.

## Alternativas

- Utilizar una API externa de embeddings.
- Utilizar otro modelo de embeddings local.
- Generar representaciones basadas en métodos tradicionales como TF-IDF.

## Motivo

`all-MiniLM-L6-v2` permite generar embeddings localmente y proporciona una interfaz sencilla para generar embeddings tanto individualmente como en lotes.

## Consecuencias

Los documentos pueden procesarse localmente y los embeddings pueden almacenarse directamente en PostgreSQL mediante pgvector.

La elección del modelo queda desacoplada del resto de la arquitectura, por lo que podrá sustituirse posteriormente si los experimentos de evaluación muestran que otro modelo proporciona mejores resultados.