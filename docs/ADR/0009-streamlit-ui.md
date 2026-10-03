# ADR-0009 — Streamlit como interfaz de usuario

## Contexto

El sistema necesita una interfaz que permita al usuario cargar documentos PDF y realizar preguntas sobre su contenido.

Para el MVP necesito una interfaz funcional sin introducir complejidad innecesaria en la arquitectura.

## Decisión

Utilizaré **Streamlit** como interfaz de usuario.

La aplicación tendrá un punto de entrada en `app.py` y utilizará los componentes en `/src` para realizar la ingestión y las consultas RAG.

## Alternativas

- Desarrollar una API con FastAPI y una interfaz frontend independiente.
- Utilizar Flask u otro framework web.
- Crear únicamente una interfaz de línea de comandos.

## Motivo

Streamlit permite construir rápidamente una interfaz para interactuar con el sistema RAG utilizando Python.

Además, permite mantener el frontend sencillo durante la fase de MVP y reutilizar directamente la lógica existente del backend.

## Consecuencias

El MVP dispone de una interfaz web funcional.

Si el proyecto requiere posteriormente autenticación, múltiples usuarios, una API independiente o una interfaz más compleja, podrá sustituirse Streamlit por una arquitectura web más completa.