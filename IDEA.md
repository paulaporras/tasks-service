# tasks-service

Microservicio REST para gestionar tareas de un equipo.

Recurso: Task
- id: UUID (autogenerado)
- title: string (obligatorio, 1-200 chars)
- description: string (opcional)
- status: enum [todo, in_progress, done] (por defecto "todo")
- assignee: string (opcional, email)
- created_at: timestamp ISO-8601 (autogenerado)

Endpoints:
- POST /tasks -> crea una tarea
- GET /tasks -> lista tareas (filtro opcional ?status=)
- GET /tasks/{id} -> obtiene una tarea
- PATCH /tasks/{id} -> actualiza campos parciales
- DELETE /tasks/{id} -> elimina una tarea

Persistencia: en memoria (diccionario) para esta primera versión.
Validación con Pydantic. Errores 404 si la tarea no existe.

# PROMPTS: CONTEXTO

Estoy desarrollando un microservicio REST llamado tasks-service para gestionar las tareas de un equipo de trabajo. Utilizaré Python, FastAPI y Pydantic, y guardaré los datos en un diccionario en memoria, sin utilizar una base de datos. El servicio permitirá crear, consultar, actualizar y eliminar tareas. Quiero que el código sea sencillo, esté bien organizado y valide correctamente los datos. También necesito comprobar su funcionamiento mediante pruebas automatizadas.

## PROMPT 1: Generar el modelo de datos
Crea el modelo de datos de un microservicio REST llamado tasks-service utilizando Python, FastAPI y Pydantic. Cada tarea debe tener un identificador UUID autogenerado, un título obligatorio de entre 1 y 200 caracteres, una descripción opcional, un estado (todo, in_progress o done) con valor por defecto todo, un email opcional para la persona asignada y una fecha de creación automática en formato ISO-8601. Añade las validaciones necesarias y muestra un ejemplo de los datos en formato JSON.

## PROMPT 2: Generar los endpoints REST
Implementa los endpoints REST de tasks-service con Python y FastAPI. La API debe permitir crear, listar, consultar, actualizar parcialmente y eliminar tareas. Guarda los datos en un diccionario en memoria y permite filtrar las tareas por estado mediante el parámetro ?status=. Utiliza Pydantic para validar los datos, devuelve los códigos HTTP adecuados y un error 404 cuando una tarea no exista. Incluye un ejemplo de petición y respuesta.

## PROMPT 3: Generar los tests
Crea pruebas automatizadas para tasks-service utilizando pytest y TestClient de FastAPI. Comprueba que se pueden crear, listar, consultar, actualizar y eliminar tareas correctamente. Incluye pruebas para validar el título, comprobar el filtro por estado y verificar que los identificadores y las fechas se generan automáticamente. Comprueba también que las tareas inexistentes devuelven un error 404 y que los datos incorrectos son rechazados. Explica brevemente cómo ejecutar las pruebas.

# Fases del Vibe Coding

- IDEA: el desarrollador define qué necesita y qué objetivos debe cumplir el proyecto.
- PROMPT: el desarrollador explica a la IA los requisitos y las tecnologías que debe utilizar.
- GENERACIÓN: la IA propone código que el desarrollador debe comprobar y adaptar al proyecto.
- REVISIÓN: el desarrollador debe comprobar el código, ejecutar los tests, detectar errores y verificar que se cumplen los requisitos.
Esta fase nunca debe delegarse, el desarrolador es quien tiene la responsabilidad sobre la calidad del resultado