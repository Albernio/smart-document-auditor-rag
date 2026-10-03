# ADR-0006 — PostgreSQL + pgvector para almacenamiento vectorial

## Contexto

El sistema necesita almacenar los documentos, sus chunks y los embeddings generados para poder realizar búsquedas semánticas.

También necesito conservar metadatos asociados a cada chunk, como el documento de origen, el índice y el número de página.

## Decisión

Utilizaré **PostgreSQL** como base de datos y la extensión **pgvector** para almacenar embeddings y realizar búsquedas por similitud vectorial.

Los embeddings utilizados actualmente tienen una dimensión de 384.

## Alternativas

- Utilizar PostgreSQL sin soporte vectorial y una base de datos vectorial especializada.
- Utilizar otra sistema gestor de bases de datos y una base de datos vectorial especializada.

## Motivo

PostgreSQL permite mantener en un mismo sistema:

- Metadatos
- Chunks de texto
- Embeddings
- Relaciones entre documentos y chunks
- Búsquedas vectoriales mediante pgvector

## Consecuencias

La aplicación dispone de un único sistema de persistencia para los datos documentales y vectoriales.

Si las necesidades de escala cambian, la estrategia de almacenamiento podrá revisarse posteriormente.