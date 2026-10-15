# Caso 1: Sugerencia correcta — Actualización parcial con PATCH

Utilicé GitHub Copilot para desarrollar y revisar el endpoint PATCH /tasks/{task_id} del servicio tasks-service.

El endpoint permite modificar parcialmente una tarea existente. Por ejemplo, se puede actualizar su descripción sin cambiar el título ni el estado. La implementación utiliza model_dump(exclude_unset=True) para obtener únicamente los campos enviados en la petición y aplica esos cambios a la tarea original.

Comprobé este comportamiento con la prueba test_patch_updates_only_provided_fields, que verifica que la descripción se actualiza y que el título y el estado se mantienen.

## Resultado
La actualización parcial funciona correctamente y conserva los campos que no se han enviado.

# Caso 2: Problema detectado y corrección — Campos desconocidos en PATCH

Pedí a GitHub Copilot que revisara el endpoint PATCH frente a los requisitos del ejercicio, buscando un caso concreto que pudiera fallar. Le indiqué expresamente que no modificara el código todavía.

Copilot detectó que el modelo TaskPatch podía ignorar los campos desconocidos del JSON. Por ejemplo, al enviar {"titel": "Nuevo título"}, la API respondía 200 OK, aunque el título original permanecía sin cambios.

Copilot propuso configurar TaskPatch con ConfigDict(extra="forbid") y añadir una prueba automatizada.

Apliqué esta configuración y añadí la prueba test_patch_rejects_unknown_fields, que comprueba que la API devuelve 422 Unprocessable Entity ante un campo desconocido y que el título original no cambia.

## Resultado
Tras la corrección, ejecuté python -m pytest -v y las nueve pruebas pasaron correctamente.

