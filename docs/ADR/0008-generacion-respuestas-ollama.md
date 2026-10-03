# ADR-0008 — Ollama para generación local de respuestas

## Contexto

El sistema RAG necesita un modelo de lenguaje que genere respuestas utilizando el contexto recuperado de los documentos.

Para el MVP quiero ejecutar la generación localmente y evitar depender de una API externa.

## Decisión

Utilizaré **Ollama** como runtime local para ejecutar el modelo de lenguaje **Qwen3:8b**.

La aplicación se comunicará con Ollama mediante su cliente de Python.

## Alternativas

- Utilizar una API externa de un proveedor de LLM.
- Ejecutar directamente el modelo mediante otra librería de inferencia.
- Utilizar otro runtime local de modelos.

## Consecuencias

La generación de respuestas depende de que Ollama esté disponible localmente y de los recursos de hardware necesarios para ejecutar el modelo.

La elección de modelo queda desacoplada mediante la clase `OllamaClient`, por lo que podrá sustituirse posteriormente si las pruebas de evaluación justifican otro modelo o infraestructura de inferencia.