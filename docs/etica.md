# Análisis ético

## El problema que queremos resolver

Queremos entender qué factores se relacionan con que un estudiante de secundaria repruebe, y ver si se podría detectar a tiempo a los alumnos en riesgo para darles apoyo. La idea suena bien, pero un modelo así trabaja con datos de menores de edad y puede afectar cómo una escuela trata a sus alumnos, así que vale la pena pensar en los riesgos antes de empezar.

## ¿A quién afecta?

A los propios estudiantes, que son los que serían etiquetados por el modelo. También a los maestros y orientadores que usarían los resultados, a las familias, y a la escuela como institución. Los estudiantes son los que tienen más que perder y los que menos voz tienen en cómo se usa el modelo.

## Privacidad y datos sensibles

Los datos son públicos y vienen anonimizados, no tienen nombres ni matrículas. Aun así incluyen información muy personal de menores de edad, como su consumo de alcohol, si tienen pareja, la relación con su familia, su salud y el trabajo de sus padres. En el artículo original los datos se juntaron con cuestionarios para una investigación, pero no sabemos qué tanto se les explicó a los alumnos sobre cómo se usarían.

Por eso decidimos no publicar resultados a nivel de alumno individual, y en la app solo se prueban casos inventados por el usuario. Si este proyecto se aplicara en una escuela real, habría que pedir consentimiento a los alumnos y a sus padres, y cuidar quién puede ver los datos.

## Riesgo de etiquetar a los alumnos

El riesgo más grande es que el modelo se use para etiquetar. Si a un alumno se le marca como "en riesgo", un maestro podría tratarlo distinto o esperar menos de él, y eso puede terminar empeorando sus calificaciones (la profecía autocumplida). También se podría usar mal, por ejemplo para no admitir a ciertos alumnos o para decidir a quién expulsar.

Por eso en todo el proyecto planteamos el modelo solo como una herramienta para ofrecer apoyo, nunca para castigar ni para tomar decisiones automáticas. La app lo dice de forma visible.

## Sesgos

Los modelos aprenden de los datos tal como son, incluyendo las desigualdades. En nuestros resultados la escuela MS aparece como una de las variables con más peso para predecir reprobación, y vivir en zona rural también influye. Eso no quiere decir que esos alumnos sean menos capaces, probablemente refleja diferencias de recursos, traslados más largos o condiciones de cada escuela.

Para revisarlo, comparamos el desempeño del modelo entre hombres y mujeres y entre zona urbana y rural (ver `reports/metrics/logistica.json`). La regresión logística da más falsas alarmas a los alumnos de zona rural (cerca de 33%) que a los de zona urbana (cerca de 15%), o sea que marca como "en riesgo" a más alumnos rurales que en realidad aprueban. Hay que tomarlo con cuidado porque en la prueba solo hay 32 alumnos rurales, pero es justo el tipo de problema que puede hacer que un grupo cargue con más etiquetas injustas.

Pensamos en quitar las variables sensibles como sexo o zona, pero eso no elimina el sesgo, porque otras variables como el tiempo de traslado o la escuela funcionan casi igual. Preferimos dejarlas para poder medir el sesgo y reportarlo.

## Decisiones que tomamos por razones éticas

Los modelos de riesgo (regresión logística y árbol de decisión) no usan ninguna calificación, porque la idea es detectar riesgo antes de que el alumno ya vaya reprobando. Usamos `class_weight="balanced"` porque nos importa más no dejar sin apoyo a un alumno que sí necesita ayuda, aunque eso genere algunas falsas alarmas. Quitamos a los alumnos con calificación final de 0 porque no presentaron el examen, y mezclar deserción con bajo rendimiento haría que el modelo culpe de la deserción a cosas que tal vez no tienen que ver.

## Límites de los datos

Los datos son de dos escuelas de Portugal de hace casi 20 años. El sistema educativo, la cultura y el contexto son muy distintos a los de México hoy, así que las conclusiones no se pueden aplicar directo a nuestras escuelas. Con 634 alumnos tampoco se puede generalizar mucho. Todo lo que encontremos son relaciones, no causas. Por ejemplo, que salir mucho con amigos se relacione con reprobar no significa que salir cause que repruebes.
