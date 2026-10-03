# ADR-0002: Utilizar SHA-256 para identificar el contenido de los documentos

## Contexto

La aplicación necesita identificar de forma fiable los documentos que procesa durante el proceso de ingestión. El nombre del archivo no es suficiente para identificar su contenido, ya que dos archivos diferentes pueden tener el mismo nombre y un mismo documento puede cambiar de nombre sin que su contenido haya cambiado.

Además, el sistema debe poder detectar si un documento ya ha sido procesado para evitar la indexación duplicada del mismo contenido.

Para ello necesito una representación determinista del contenido binario del archivo que pueda almacenarse junto con los metadatos del documento y utilizarse posteriormente para comprobar su identidad.

## Decisión

Utilizaré SHA-256 para calcular una huella digital del contenido binario de cada documento.

El hash se calculará directamente sobre los bytes del archivo mediante lectura incremental en bloques, evitando cargar el archivo completo en memoria.

La implementación utilizará el algoritmo SHA-256 proporcionado por la biblioteca estándar de Python mediante `hashlib.sha256`.

El resultado se almacenará como una cadena hexadecimal en el atributo `file_hash` del objeto `Document`.

En PostgreSQL, el campo `file_hash` tendrá una restricción `UNIQUE` para impedir que el mismo contenido binario sea registrado más de una vez.

## Consecuencias

### Positivas

- Permite identificar el contenido independientemente del nombre del archivo.
- Facilita la detección de documentos duplicados.
- Permite utilizar una restricción `UNIQUE` en PostgreSQL.
- SHA-256 está disponible en la biblioteca estándar de Python, por lo que no es necesario añadir una dependencia externa.
- La lectura incremental permite calcular el hash de archivos grandes sin cargar todo el contenido en memoria.
- El hash puede utilizarse para mantener la trazabilidad entre el documento original, sus chunks y sus embeddings.

### Negativas

- El cálculo del hash requiere leer el archivo completo.
- Un cambio de un solo byte produce un hash diferente, por lo que una modificación mínima del archivo se considera un contenido diferente.
- SHA-256 identifica el contenido binario del archivo, no su contenido semántico. Dos archivos PDF que representan visualmente la misma información pueden producir hashes diferentes debido a diferencias en metadatos, estructura interna u otros elementos del archivo.

## Alcance

Esta decisión se refiere a la identificación del contenido binario de los archivos durante el proceso de ingestión.

SHA-256 no se utilizará como identificador de similitud semántica. 