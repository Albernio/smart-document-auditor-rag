# ADR-0001: Estructura modular del proyecto

## Contexto

El proyecto necesita separar las distintas responsabilidades del sistema RAG: ingestión, extracción de texto, chunking, embeddings, persistencia, búsqueda y generación de respuestas.

Quiero evitar concentrar toda la lógica en un único módulo y facilitar la escalabilidad del sistema.

## Decisión

Utilizaré una arquitectura modular con los componentes organizados directamente bajo `src/`.

Cada módulo tendrá una responsabilidad concreta y podrá evolucionar de forma independiente.

## Consecuencias

La arquitectura queda preparada para evolucionar hacia componentes más independientes.

A cambio, será necesario mantener claras las responsabilidades de cada módulo y evitar que la lógica de negocio se duplique entre componentes.