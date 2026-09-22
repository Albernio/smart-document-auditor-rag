# Smart Document Auditor

Intelligent document auditing system based on **Retrieval-Augmented Generation (RAG)**.

The project aims to build a local, modular and reproducible application capable of processing multiple PDF documents, indexing their content in a vector database, answering natural-language questions and returning answers with references to the original documents.

The project is being developed as a **Data Engineering + AI Engineering portfolio project**, with a strong focus on architecture, data pipelines, retrieval quality, evaluation and software engineering practices.

---

## Project Status

**Current status:** Initial development

The project is being built incrementally, starting with the document ingestion pipeline and progressively incorporating semantic search, RAG, local LLM inference, API, frontend and evaluation.

---

## Problem

Organizations often work with large collections of:

- Procedures
- Internal policies
- Contracts
- Regulations
- Manuals
- Technical documentation
- Compliance documents

Finding specific information across these documents can be slow and error-prone.

Examples of questions the system should eventually answer:

- What clauses refer to data protection?
- What is the maximum time allowed to respond to complaints?
- Summarize the supplier's obligations.
- Which document contains the confidentiality requirements?
- What are the termination conditions?

The system should provide not only an answer, but also the evidence used to produce it.

---

## Objective

Build a document intelligence platform with the following capabilities:

1. Upload multiple PDF documents.
2. Extract and structure their content.
3. Split documents into meaningful chunks.
4. Generate vector embeddings.
5. Index chunks and metadata in a vector-enabled database.
6. Retrieve relevant information for a natural-language query.
7. Generate an answer using a local LLM.
8. Return traceable references to the original document.
9. Evaluate retrieval and answer quality.
10. Provide a reproducible local development environment.

---

## High-Level Architecture

```text
                         USER
                           |
                           v
                  +----------------+
                  |   Streamlit    |
                  |    Frontend    |
                  +-------+--------+
                          |
                          | HTTP
                          v
                  +----------------+
                  |    FastAPI     |
                  |      API       |
                  +-------+--------+
                          |
             +------------+------------+
             |                         |
             v                         v
      INGESTION PIPELINE          QUERY PIPELINE
             |                         |
             v                         v
         PyMuPDF                  Query Embedding
             |                         |
             v                         v
         Cleaning                Vector Retrieval
             |                         |
             v                         v
         Chunking                    Top-K
             |                         |
             v                         v
       Embeddings               Optional Reranking
             |                         |
             +------------+------------+
                          |
                          v
              +-----------------------+
              | PostgreSQL + pgvector |
              |                       |
              | Documents             |
              | Chunks                |
              | Embeddings            |
              | Metadata              |
              +-----------+-----------+
                          |
                          v
                    +-----------+
                    |  Ollama   |
                    |    LLM    |
                    +-----+-----+
                          |
                          v
                  Answer + Citations
                          |
                          v
                        USER
```

---

## Data Flow

### Document ingestion

```text
PDF
 |
 v
Validation
 |
 v
File storage
 |
 v
PDF parsing
 |
 v
Text extraction
 |
 v
Cleaning
 |
 v
Chunking
 |
 v
Metadata enrichment
 |
 v
Embeddings
 |
 v
PostgreSQL + pgvector
```

### Query processing

```text
Natural-language question
 |
 v
Query embedding
 |
 v
Vector search
 |
 v
Relevant chunks
 |
 v
Optional reranking
 |
 v
Context construction
 |
 v
LLM generation
 |
 v
Answer + document references
```

---

## Technology Stack

### Core

- **Python 3.13**
- **FastAPI**
- **Streamlit**
- **PostgreSQL**
- **pgvector**
- **PyMuPDF**
- **Sentence Transformers**
- **Ollama**
- **Qwen3** as the initial local LLM

### Development

- **Git / GitHub**
- **pytest**
- **Ruff**
- **mypy**
- **Docker**
- **Docker Compose**
- **SQLAlchemy**
- **Alembic**
- **Pydantic / pydantic-settings**

---

## Project Principles

The project follows several engineering principles.

### Modular architecture

Document ingestion, retrieval, generation and data access are isolated into independent modules.

### Reproducibility

The complete development environment should be reproducible locally using documented dependencies and Docker.

### Idempotent ingestion

The system should detect previously processed documents using file hashes and avoid unnecessary duplicate processing.

### Traceability

Every generated answer should be linked to the original evidence through document and page metadata.

### Retrieval before generation

Retrieval quality is treated as an independent problem from LLM generation.

### Evaluation

The system should be evaluated using a predefined dataset rather than only through manual inspection.

### Local-first

The initial architecture uses local/open-source components wherever practical, including local LLM inference through Ollama.

---

## Initial Data Model

### Documents

```text
documents
-------------------------
id
filename
file_hash
file_path
upload_date
page_count
status
metadata
```

### Chunks

```text
chunks
-------------------------
id
document_id
chunk_index
page_start
page_end
section
content
token_count
embedding
created_at
```

Future versions may introduce query history, retrieval results, answers, document versions and audit results.

---

## Development Roadmap

### Phase 1 — Python foundation

- Project structure
- Virtual environment
- Type hints
- Dataclasses
- File management
- Validation
- Hashing
- Logging
- Unit testing
- Code quality

### Phase 2 — PDF ingestion

- PDF parsing
- Text extraction
- Page-level representation
- Cleaning
- Document metadata

### Phase 3 — Chunking

- Chunking strategy
- Overlap
- Structural metadata
- Chunk quality analysis

### Phase 4 — Database

- PostgreSQL
- SQL
- SQLAlchemy
- Alembic
- pgvector
- Database schema

### Phase 5 — Embeddings

- Embedding models
- Query/document embeddings
- Similarity metrics
- Vector storage

### Phase 6 — Retrieval

- Vector search
- Top-K retrieval
- Retrieval evaluation

### Phase 7 — RAG

- Context construction
- Prompt design
- Grounded generation
- No-answer behaviour

### Phase 8 — Local LLM

- Ollama
- Local model inference
- Model comparison
- Context window
- Performance considerations

### Phase 9 — Citations

- Source metadata
- Page references
- Evidence tracking
- Citation generation

### Phase 10 — API and UI

- FastAPI
- REST endpoints
- Streamlit interface
- Document management
- Question answering

### Phase 11 — Testing and Evaluation

- Unit tests
- Integration tests
- Retrieval benchmarks
- Recall@K
- MRR
- Answer correctness
- Faithfulness
- Latency

### Phase 12 — Advanced Retrieval

- Full-text search
- BM25
- Hybrid search
- Result fusion
- Reranking

### Phase 13 — Scalability

Potential future additions:

- MinIO / object storage
- Redis
- Celery
- Kafka
- Asynchronous processing
- Worker architecture

### Phase 14 — Observability and Production

Potential future additions:

- Structured logging
- Prometheus
- Grafana
- OpenTelemetry
- Authentication
- RBAC
- CI/CD
- Cloud deployment

### Phase 15 — Advanced AI capabilities

Potential future additions:

- Multi-document reasoning
- Automated document auditing
- Rule-based compliance checks
- Knowledge graphs / GraphRAG
- Human-in-the-loop workflows
- Document versioning

---

## Initial Project Structure

```text
smart-document-auditor/
|
├── src/
│   ├── api/
│   ├── core/
│   ├── ingestion/
│   ├── embeddings/
│   ├── retrieval/
│   ├── generation/
│   ├── citations/
│   ├── db/
│   └── schemas/
|
├── tests/
|
├── frontend/
|
├── scripts/
|
├── data/
│   ├── raw/
│   └── processed/
|
├── pyproject.toml
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Example Future Workflow

The final user experience should look approximately like:

```text
1. Upload documents

   contract.pdf
   complaints_manual.pdf
   privacy_policy.pdf

2. Documents are indexed

   contract.pdf              ✓
   complaints_manual.pdf     ✓
   privacy_policy.pdf        ✓

3. Ask a question

   "What is the maximum period for responding to complaints?"

4. System retrieves relevant evidence

   contract.pdf
   page 17
   section 7.2

5. Local LLM generates the answer

   "The maximum response period is 15 days."

6. System returns the evidence

   Source:
   contract.pdf
   Page 17
   Section 7.2
```

---

## Goals of the Portfolio Project

This project is intended to demonstrate practical skills in:

### Data Engineering

- Data pipelines
- ETL
- Document processing
- Data modelling
- SQL
- PostgreSQL
- Vector databases
- Data quality
- Idempotency

### AI Engineering

- Embeddings
- Semantic search
- Retrieval-Augmented Generation
- LLM inference
- Prompt engineering
- Reranking
- RAG evaluation

### Software Engineering

- Modular architecture
- REST APIs
- Testing
- Type checking
- Logging
- Configuration management
- Version control

### Infrastructure

- Docker
- Reproducible environments
- Local AI inference
- CI/CD
- Observability
- Scalable processing

---

## Current Focus

The project is currently focused on the foundations:

```text
Python
  ↓
Project structure
  ↓
File management
  ↓
Validation
  ↓
Hashing
  ↓
Document model
  ↓
Tests
```

The next milestone is to implement real PDF ingestion using **PyMuPDF**.

---

## License

License to be defined.

---

## Author

**Alberto**

Data Engineering / AI Engineering Portfolio Project
