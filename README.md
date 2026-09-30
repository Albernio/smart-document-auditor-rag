# Smart-document-auditor

Aplicación local basada en **Retrieval-Augmented Generation (RAG)** para analizar documentos PDF y responder preguntas utilizando su contenido.

El sistema extrae el texto de los documentos PDF, lo divide en fragmentos (*chunks*), genera embeddings vectoriales, los almacena en PostgreSQL con `pgvector`, recupera los fragmentos semánticamente relevantes y utiliza un LLM local mediante Ollama para generar respuestas fundamentadas con referencias al documento y a la página.

## Quick Start

Sigue estos pasos para ejecutar el proyecto localmente.

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd smart-document-auditor-rag
```

### 2. Crear el entorno virtual con Python 3.13

Asegúrate de tener Python 3.13 instalado.

```bash
python3.13 -m venv .venv
```

Activar el entorno virtual:

**Linux / macOS:**

```bash
source .venv/bin/activate
```

**Windows:**

```powershell
.venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -e ".[dev]"
```

### 4. Iniciar PostgreSQL + pgvector

Necesitas tener **Docker instalado y ejecutándose**.

```bash
docker compose up -d
```

Esto inicia PostgreSQL con la extensión `pgvector`.

### 5. Crear el esquema de la base de datos

Ejecuta:

```bash
python -c "from src.schema import create_tables; create_tables()"
```

Esto crea las tablas necesarias y habilita la extensión `vector`.

Este paso solo es necesario para inicializar el esquema de una base de datos nueva.

### 6. Ejecutar la aplicación

```bash
streamlit run app.py
```

Streamlit abrirá la aplicación en el navegador.

### Todos los comandos

Después de clonar el repositorio, la configuración básica es:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
docker compose up -d
python -c "from src.schema import create_tables; create_tables()"
streamlit run app.py
```

> **Requisitos:** Python 3.13 y Docker. Docker se utiliza para ejecutar PostgreSQL + pgvector.


## Arquitectura

```text
PDF
 ↓
Validación
 ↓
Hash SHA-256
 ↓
Extracción de texto
 ↓
Conservación de páginas
 ↓
Chunking
 ↓
Embeddings con Sentence Transformers
 ↓
PostgreSQL + pgvector
 ↓
Búsqueda por similitud semántica
 ↓
Chunks relevantes
 ↓
Construcción del contexto
 ↓
Ollama / qwen3:8b
 ↓
Respuesta + referencias
```

La aplicación Streamlit proporciona la interfaz de usuario para subir documentos y realizar preguntas.

```text
                    ┌──────────────────────┐
                    │      Streamlit       │
                    │       app.py         │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │    Pipeline RAG      │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       PostgreSQL          Embeddings         Ollama
        + pgvector        SentenceTransformers qwen3:8b
```

## Funcionalidades

* Validación de documentos PDF.
* Identificación de documentos mediante SHA-256.
* Extracción de texto de PDF.
* Conservación de metadatos de página.
* División del texto en chunks con solapamiento.
* Generación de embeddings mediante Sentence Transformers.
* Embeddings de 384 dimensiones utilizando `all-MiniLM-L6-v2`.
* PostgreSQL con `pgvector`.
* Búsqueda por similitud vectorial.
* Inferencia local mediante Ollama.
* Generación de respuestas basada en RAG.
* Referencias a documento, página y chunk.
* Interfaz de usuario con Streamlit.
* Tests unitarios y de integración.

## Estructura del proyecto

```text
smart-document-auditor-rag/
├── app.py
├── src/
│   ├── __init__.py
│   ├── hashing.py
│   ├── validation.py
│   ├── models.py
│   ├── ingestion.py
│   ├── pdf_extraction.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_similarity.py
│   ├── database.py
│   ├── schema.py
│   ├── semantic_search.py
│   ├── context_builder.py
│   ├── prompts.py
│   ├── answer_generator.py
│   ├── rag.py
│   ├── llm/
│   │   └── ollama_client.py
│   └── repositories/
│       ├── __init__.py
│       └── document_repository.py
├── tests/
├── docs/
│   └── adr/
├── pyproject.toml
├── docker-compose.yml
└── README.md
```

## Requisitos

* Python 3.13
* Docker y Docker Compose
* Ollama
* Modelo local de Ollama, actualmente `qwen3:8b`

## 1. Clonar el repositorio

```bash
git clone <repository-url>
cd smart-document-auditor-rag
```

## 2. Crear el entorno virtual

```bash
python3.13 -m venv .venv
```

Activarlo:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

## 3. Instalar el proyecto

Instalar el proyecto junto con sus dependencias de desarrollo:

```bash
pip install -e ".[dev]"
```

Esto instala las dependencias de la aplicación, entre ellas:

* `pypdf`
* `sentence-transformers`
* `psycopg`
* `ollama`
* `streamlit`
* `pytest`
* `reportlab`

## 4. Iniciar PostgreSQL + pgvector

El proyecto utiliza la imagen de PostgreSQL con `pgvector`:

```bash
docker compose up -d
```

Comprobar el contenedor:

```bash
docker compose ps
```

La aplicación utiliza actualmente estos parámetros de conexión:

```text
Host:     localhost
Port:     5432
Database: document_auditor
User:     auditor
Password: auditor
```

## 5. Crear el esquema de base de datos

El esquema está definido en:

```text
src/schema.py
```

El esquema contiene dos tablas principales.

### `documents`

Almacena metadatos del documento:

* nombre del archivo
* hash SHA-256
* tamaño
* fecha de creación

### `document_chunks`

Almacena:

* ID del documento
* índice del chunk
* número de página
* texto extraído
* embedding vectorial
* fecha de creación

La columna de embeddings está configurada para vectores de **384 dimensiones**.

## 6. Instalar y ejecutar Ollama

Instala Ollama siguiendo las instrucciones oficiales.

Comprobar la instalación:

```bash
ollama --version
```

Descargar el modelo utilizado por la aplicación:

```bash
ollama pull qwen3:8b
```

Comprobar los modelos disponibles:

```bash
ollama list
```

La aplicación se conecta actualmente a:

```text
http://localhost:11434
```

La integración con Ollama se encuentra en:

```text
src/llm/ollama_client.py
```

La aplicación utiliza una abstracción (`LLMClient`) para desacoplar el proveedor de LLM del resto de la arquitectura RAG.

Esto permite sustituir Ollama por otro proveedor en el futuro sin modificar la lógica principal del pipeline.

## 7. Ejecutar los tests

Ejecutar toda la suite:

```bash
pytest -v
```

El proyecto contiene tests unitarios y de integración.

Los tests de integración requieren que esté disponible la infraestructura correspondiente:

* PostgreSQL + pgvector
* Ollama
* `qwen3:8b`

## 8. Ejecutar la aplicación Streamlit

Desde la raíz del proyecto:

```bash
streamlit run app.py
```

Streamlit abrirá la aplicación en el navegador.

Actualmente la interfaz permite:

1. Subir un PDF.
2. Procesar el documento.
3. Realizar una pregunta en lenguaje natural.
4. Ejecutar una búsqueda semántica.
5. Generar una respuesta mediante Ollama.
6. Mostrar referencias de documento, página y chunk.

## 9. Ejecutar el pipeline RAG completo

Una vez ejecutándose Streamlit:

### Paso 1 — Subir un PDF

Utiliza el control **Upload a PDF document**.

### Paso 2 — Procesar el documento

Pulsa:

```text
Ingest document
```

La aplicación ejecutará:

```text
PDF
 ↓
Validación
 ↓
SHA-256
 ↓
Extracción de texto
 ↓
Chunking
 ↓
Embeddings
 ↓
PostgreSQL + pgvector
```

### Paso 3 — Realizar una pregunta

Introduce una pregunta relacionada con los documentos.

Por ejemplo:

```text
How many days does the provider have to respond to a complaint?
```

La aplicación ejecutará:

```text
Pregunta
 ↓
Embedding de la pregunta
 ↓
Búsqueda por similitud vectorial
 ↓
Chunks relevantes
 ↓
Construcción del contexto
 ↓
Ollama
 ↓
Respuesta
```

### Paso 4 — Consultar las referencias

La respuesta incluye referencias que identifican:

```text
Documento
Página
Chunk
```

Esto permite mantener trazabilidad entre la respuesta generada y el contenido recuperado del documento.

## Ejemplo

Si un documento contiene:

```text
The service provider must respond to any formal customer complaint
within thirty days from the date on which the complaint is received.
```

y realizamos la pregunta:

```text
How many days does the provider have to respond?
```

el sistema debería recuperar el chunk correspondiente y generar una respuesta basada en el contexto del documento.

## Flujo de datos

### Ingestión de documentos

```text
PDF subido
     │
     ▼
ingest_document()
     │
     ├── validate_file()
     ├── calculate_file_hash()
     ├── extract_pages()
     ├── chunk_document()
     ├── create_vector_records()
     └── save_vector_records()
                │
                ▼
        PostgreSQL + pgvector
```

### Respuesta a preguntas

```text
Pregunta del usuario
     │
     ▼
search_documents()
     │
     ├── EmbeddingModel.encode()
     │
     ▼
search_similar()
     │
     ▼
SearchResult[]
     │
     ▼
build_context()
     │
     ▼
LLMAnswerGenerator
     │
     ▼
Ollama / qwen3:8b
     │
     ▼
Answer
 + referencias
```

## Reiniciar la base de datos

Durante el desarrollo se puede vaciar la base de datos con:

```sql
TRUNCATE TABLE documents RESTART IDENTITY CASCADE;
```

Esto elimina los documentos y sus chunks asociados y reinicia los contadores de identidad.

Comprobar:

```sql
SELECT COUNT(*) FROM documents;
SELECT COUNT(*) FROM document_chunks;
```

Ambas consultas deberían devolver:

```text
0
```

## Configuración

Actualmente la aplicación utiliza valores predeterminados para desarrollo local.

### PostgreSQL

```text
host=localhost
port=5432
database=document_auditor
user=auditor
password=auditor
```

### Ollama

```text
host=http://localhost:11434
model=qwen3:8b
```

### Embeddings

```text
model=all-MiniLM-L6-v2
dimensions=384
```

Estos valores están actualmente definidos en el código y son adecuados para el entorno local de desarrollo.

Para un despliegue de producción, la configuración debería externalizarse mediante variables de entorno o una capa específica de configuración.

## Estrategia de testing

El proyecto utiliza varias capas de testing.

### Tests unitarios

Se prueban componentes individuales como:

* hashing
* validación
* extracción de PDF
* chunking
* embeddings
* similitud vectorial
* construcción del contexto
* construcción de prompts

### Tests del repositorio

Verifican la persistencia en PostgreSQL y el comportamiento de las búsquedas vectoriales.

### Tests de integración

Verifican la interacción entre:

```text
Aplicación
 ↓
PostgreSQL
 ↓
pgvector
```

y:

```text
Aplicación
 ↓
Ollama
```

### Test end-to-end del RAG

El test de integración del RAG verifica el flujo completo:

```text
Documento
 ↓
Ingestión
 ↓
Almacenamiento vectorial
 ↓
Búsqueda semántica
 ↓
Contexto
 ↓
LLM
 ↓
Respuesta
```

## Decisiones de diseño

Las decisiones arquitectónicas importantes están documentadas mediante ADRs en:

```text
docs/adr/
```

Las decisiones actuales incluyen:

* estructura del proyecto
* identificación de documentos mediante SHA-256
* extracción de texto de PDF
* chunking basado en caracteres
* embeddings mediante Sentence Transformers
* PostgreSQL + pgvector
* diseño de `VectorRecord`

## Arquitectura local

La implementación actual está diseñada para ejecutarse localmente:

```text
PDF ───────────────┐
                   │
PostgreSQL ────────┤── Máquina local
                   │
Embeddings ────────┤
                   │
Ollama / qwen3:8b ─┘
```

Durante la ejecución normal, los documentos y la inferencia del LLM permanecen en el entorno local.

Además, este enfoque evita costes por petición asociados a APIs externas de LLM.

## Limitaciones actuales

Este proyecto es un MVP. Entre sus limitaciones actuales:

* No existe autenticación ni autorización.
* No existe configuración para despliegue en producción.
* El PDF original subido no se conserva de forma persistente.
* Las credenciales de PostgreSQL son actualmente valores de desarrollo.
* La configuración todavía no está externalizada.
* La interfaz Streamlit es todavía mínima.
* No existe una interfaz avanzada de gestión de documentos.
* El chunking es actualmente basado en caracteres y no en la estructura semántica del documento.
* Los PDFs escaneados o basados únicamente en imágenes no tienen OCR.
* La recuperación utiliza actualmente similitud vectorial sin una capa híbrida de búsqueda por palabras clave.
* No existe todavía una etapa de reranking.
* No existe todavía una capa específica de evaluación de calidad del RAG.

## Próximas mejoras

Posibles siguientes pasos:

* Mejorar la interfaz de Streamlit.
* Aplicar caching a los modelos de embeddings y clientes LLM.
* Añadir gestión de documentos.
* Mejorar las referencias de las fuentes.
* Añadir OCR para documentos escaneados.
* Añadir búsqueda híbrida.
* Añadir reranking.
* Externalizar la configuración.
* Añadir logging y observabilidad.
* Preparar un despliegue de producción.
* Crear datasets de evaluación y métricas específicas para evaluar la calidad del RAG.

## Licencia

Este proyecto está desarrollado como proyecto de portfolio y código abierto.
