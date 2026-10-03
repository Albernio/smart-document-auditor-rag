# ADR-0010 — Docker Compose para PostgreSQL y pgvector

## Contexto

El proyecto necesita PostgreSQL con la extensión pgvector para almacenar documentos, chunks y embeddings y realizar búsquedas vectoriales.

Necesito una forma reproducible de ejecutar esta infraestructura durante el desarrollo local.

## Motivo

Docker Compose permite definir la infraestructura del proyecto como código y facilita que el entorno pueda reproducirse en otra máquina.

Además, evita depender de una instalación específica de PostgreSQL y pgvector en el sistema operativo.

## Consecuencias

El entorno de desarrollo requiere Docker.

Los datos de PostgreSQL se mantienen mediante un volumen Docker, por lo que sobreviven al reinicio del contenedor.

La configuración está preparada para evolucionar posteriormente hacia otros entornos de despliegue sin acoplar la aplicación a una instalación local específica de PostgreSQL.