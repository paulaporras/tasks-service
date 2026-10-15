# Arquitectura del servicio

- **models.py:** define los modelos de datos Task y los enums TaskStatus y TaskPriority. Valida los datos y genera el identificador y la fecha de creación.
- **main.py:** contiene los esquemas de entrada, los endpoints FastAPI y la lógica para crear, consultar, actualizar y eliminar tareas. También mantiene las tareas en un diccionario global.
- **test_main.py:** contiene pruebas automatizadas para comprobar los endpoints, los filtros y la validación de datos.

La API utiliza FastAPI para recibir peticiones y Pydantic para validar los datos. Las tareas se almacenan en memoria.

# Riesgos para producción

1. **Persistencia:** los datos se pierden al reiniciar el proceso porque se almacenan en un diccionario en memoria.
2. **Seguridad:** no hay autenticación ni autorización, por lo que cualquier cliente con acceso a la API podría consultar o modificar tareas.
3. **Escalabilidad:** no hay paginación y cada consulta de listado recorre las tareas almacenadas.
4. **Concurrencia:** varias peticiones simultáneas podrían provocar actualizaciones perdidas o errores al modificar el diccionario.
5. **Validación:** Claude identificó un posible error 500 al enviar priority con valor null en PATCH. Debe comprobarse mediante una prueba.
6. **Tests:** faltan pruebas para algunos errores, como PATCH con priority null y determinados casos 404.
7. **Mantenibilidad:** los esquemas y la lógica están concentrados en main.py y algunas validaciones están duplicadas.

# Mejoras recomendadas

- Corregir y probar el caso priority null en PATCH.
- Incorporar una base de datos persistente.
- Implementar autenticación y autorización.
- Añadir paginación y orden estable al listado.
- Ampliar las pruebas automatizadas.
- Separar rutas, esquemas, servicios y acceso a datos cuando crezca el proyecto.
- Fijar las versiones de las dependencias.

# Conclusión

Claude realizó un análisis de arquitectura a partir de models.py, main.py y test_main.py. Distinguió problemas visibles en el código de riesgos que dependen del despliegue y propuso mejoras ordenadas por prioridad.

El posible error de priority null es una hipótesis de debugging que debe reproducirse antes de considerarse confirmada. El análisis ayuda a detectar riesgos, pero las conclusiones deben contrastarse con el código y las pruebas.

# Debugging asistido con Claude

## Error introducido

Para reproducir un error, sustituí temporalmente tasks.get(task_id) por tasks[task_id] en la función get_or_404 de main.py.

Al ejecutar python -m pytest -v, obtuve 2 tests fallidos y 10 correctos. El traceback mostraba un KeyError al intentar acceder a un UUID que no existía en el diccionario tasks.

## Análisis de la causa raíz

Claude identificó que el acceso mediante tasks[task_id] lanza KeyError cuando la clave no existe. Por eso, la ejecución no llega al if task is None y FastAPI termina devolviendo un error 500 en lugar del 404 esperado.

## Corrección aplicada

Restauré tasks.get(task_id). Este método devuelve None cuando no encuentra la clave, lo que permite ejecutar la condición que lanza HTTPException con estado 404 y detalle Task not found.

## Verificación

Después de aplicar la corrección, ejecuté python -m pytest -v de nuevo.

Resultado: 12 tests passed.

## Conclusión

Claude identificó correctamente la causa raíz y propuso una corrección mínima. La solución se verificó mediante las pruebas automatizadas, que volvieron a pasar tras restaurar el comportamiento esperado.