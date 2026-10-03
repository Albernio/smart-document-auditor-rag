# ADR-0007 — VectorRecord para representar chunks y embeddings

## Contexto

Durante la ingestión, cada chunk de un documento necesita asociarse con su embedding antes de ser persistido en la base de datos.

## Decisión

Utilizaré una clase creada llamada `VectorRecord` para agrupar un `Chunk` con su correspondiente `Embedding`.

La estructura será:

```text
@dataclass
class VectorRecord:
    chunk: Chunk
    embedding: Embedding
```

## Motivo

`VectorRecord` proporciona una representación explícita de la unidad que será persistida: **un fragmento de documento junto con su representación vectorial**.

Además, mantiene separadas las responsabilidades de `Chunk` y `Embedding` y facilita el intercambio de datos entre la generación de embeddings y el repositorio.

## Consecuencias

LA capa de embeddings puede generar `VectorRecord` y el repositorio puede recibirlos directamente para su persistencia.

La estructura añade un modelo intermedio, pero mejora la claridad y mantiene desacoplados el contenido textual y su representación vectorial.