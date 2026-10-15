# Archivos modificados

- models.py: se añadió el enum TaskPriority con los valores low, medium y high. El campo priority de Task tiene medium como valor predeterminado.
- main.py: se añadió el campo priority a los modelos de creación y actualización. El endpoint GET /tasks permite filtrar por prioridad, manteniendo el filtro por estado.
- test_main.py: se añadió una prueba para comprobar el valor predeterminado, el filtro por prioridad y la combinación de los filtros status y priority.

# Coherencia entre archivos

Los cambios son coherentes: main.py importa y utiliza TaskPriority, definido en models.py, y las pruebas usan los mismos valores del enum. El filtro combinado devuelve únicamente las tareas que cumplen ambas condiciones.

# Revisión

Antes de aceptar los cambios, revisé el diff. Pedí una versión más clara porque la propuesta inicial parecía mostrar fragmentos duplicados. En la versión revisada comprobé que se modificaba la función list_tasks existente, sin duplicarla, y que los cambios estaban separados por archivo.

También pedí que se añadiera una prueba para comprobar los filtros de estado y prioridad juntos.

# Resultado de las pruebas

Después de aplicar los cambios, ejecuté el comando python -m pytest -v.

Resultado: 12 tests passed.

# Contexto automático y menciones explícitas

Cursor puede utilizar el contexto del proyecto para proponer cambios en varios archivos. Para comparar ese contexto automático con una mención explícita, se puede pedir la misma explicación o cambio incluyendo @models.py.

La mención explícita ayuda a indicar qué archivo debe consultar. En este caso, es importante comprobar que el enum definido en models.py coincide con su uso en main.py y en las pruebas.

# @models.py

Pedí a Cursor que revisara @models.py y explicara cómo se utiliza TaskPriority en main.py, sin modificar archivos.

Cursor identificó correctamente los valores low, medium y high, el valor predeterminado medium y el uso del enum en el filtro de GET /tasks. También explicó que se pueden combinar los filtros de status y priority y que un valor no válido produce un error 422.

**Comparación:** el contexto automático permitió proponer cambios en varios archivos. La mención explícita @models.py orientó la consulta hacia el modelo y permitió comprobar cómo se relaciona con main.py. En ambos casos, fue necesario revisar las propuestas y comprobar el resultado con las pruebas.