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

Para revisarlo, comparamos el desempeño del modelo entre hombres y mujeres y entre zona urbana y rural (ver `reports/metrics/logistica.json`). La regresión logística da más falsas alarmas a los alumnos de zona rural (cerca de 33%) que a los de zona urbana (cerca de 14%), o sea que marca como "en riesgo" a más alumnos rurales que en realidad aprueban. Hay que tomarlo con cuidado porque en la prueba solo hay 32 alumnos rurales, pero es justo el tipo de problema que puede hacer que un grupo cargue con más etiquetas injustas.

Pensamos en quitar las variables sensibles como sexo o zona, pero eso no elimina el sesgo, porque otras variables como el tiempo de traslado o la escuela funcionan casi igual. Preferimos dejarlas para poder medir el sesgo y reportarlo.

## Decisiones que tomamos por razones éticas

Los modelos de riesgo (regresión logística y árbol de decisión) no usan ninguna calificación, porque la idea es detectar riesgo antes de que el alumno ya vaya reprobando. Usamos `class_weight="balanced"` porque nos importa más no dejar sin apoyo a un alumno que sí necesita ayuda, aunque eso genere algunas falsas alarmas. Quitamos a los alumnos con calificación final de 0 porque no presentaron el examen, y mezclar deserción con bajo rendimiento haría que el modelo culpe de la deserción a cosas que tal vez no tienen que ver.

## Límites de los datos

Los datos son de dos escuelas de Portugal de hace casi 20 años. El sistema educativo, la cultura y el contexto son muy distintos a los de México hoy, así que las conclusiones no se pueden aplicar directo a nuestras escuelas. Con 634 alumnos tampoco se puede generalizar mucho. Todo lo que encontremos son relaciones, no causas. Por ejemplo, que salir mucho con amigos se relacione con reprobar no significa que salir cause que repruebes.

## Análisis con los principios de la bioética

Para ordenar todo lo anterior usamos el principialismo, un marco muy usado en bioética que se basa en cuatro principios, que son autonomía, beneficencia, no maleficencia y justicia. Aunque nació para la medicina, encaja bien con nuestro proyecto, porque también se trata de tomar decisiones sobre personas, en este caso menores de edad, a partir de datos sensibles.

### Autonomía

La autonomía es el derecho de cada persona a decidir sobre sí misma con información suficiente. En nuestro caso los alumnos no decidieron que sus datos se usaran para predecir si reprueban. Respondieron un cuestionario para una investigación de 2008 y no sabemos qué tanto se les explicó. Los datos vienen anonimizados y son públicos, pero eso no es lo mismo que haber dado permiso para este uso.

Por eso en el proyecto no mostramos resultados de ningún alumno real, y en la app solo se prueban casos inventados. Si esto se usara en una escuela de verdad, habría que pedir consentimiento a los alumnos y a sus padres, explicarles qué datos se usan y para qué, y darles la opción de no participar.

La autonomía también tiene que ver con poder entender y cuestionar una decisión. Por eso elegimos modelos que se pueden explicar. La regresión logística dice qué variables suben o bajan el riesgo y el árbol da reglas que cualquier maestro entiende, como "ya reprobó antes y no quiere ir a la universidad". Si a un alumno se le ofrece apoyo, debería poder saber por qué y decidir si lo acepta. El modelo nunca debería tomar la decisión solo, siempre tiene que haber una persona que revise.

### Beneficencia

La beneficencia es actuar para hacer el bien. El objetivo del proyecto va por ahí, porque busca detectar a tiempo a los alumnos que podrían reprobar para darles apoyo, como tutorías u orientación, antes de que sea tarde.

Varias decisiones del proyecto salen de este principio. Los modelos de riesgo no usan ninguna calificación, para que la alerta llegue desde el inicio del año y no cuando el alumno ya va mal. Usamos `class_weight="balanced"` y nos fijamos sobre todo en el recall, porque para nosotros es peor dejar sin apoyo a un alumno que lo necesita. Con eso la regresión logística detecta a 10 de los 17 alumnos que reprueban en los datos de prueba.

Pero el beneficio solo existe si la alerta se convierte en ayuda real. Un modelo que marca alumnos y no hace nada más no beneficia a nadie. Además hay que ser honestos con lo que el modelo puede hacer. Se le pasan 7 de cada 17 alumnos que reprueban, y la regresión lineal muestra que la calificación del primer periodo dice más que todo el contexto junto. El modelo sirve como una primera señal, no como reemplazo de lo que ya saben los maestros.

### No maleficencia

La no maleficencia es no hacer daño, y en este proyecto es el principio con más riesgos. El daño más grande es la etiqueta. Si a un alumno se le marca como "en riesgo", un maestro podría esperar menos de él o tratarlo distinto, y eso puede empeorar sus calificaciones. A eso se le llama profecía autocumplida.

Las falsas alarmas hacen que este riesgo sea real. De los 110 alumnos de prueba que aprobaron, la regresión logística marca a 20 como en riesgo, o sea al 18%. Esos alumnos cargarían con una etiqueta sin necesitarla. El árbol de decisión da menos falsas alarmas, 13 de 110, pero detecta a un alumno menos de los que reprueban. Ahí hay una tensión entre beneficencia y no maleficencia, porque detectar a más alumnos que necesitan ayuda también significa marcar a más que no la necesitan.

También está el daño por privacidad. Los datos incluyen el consumo de alcohol, si tienen pareja, su salud y cómo se llevan con su familia. Si esa información se filtrara o se usara para otra cosa, por ejemplo para decidir admisiones o expulsiones, podría lastimar a los alumnos. Por eso planteamos el modelo solo para ofrecer apoyo, y la app lo recuerda cuando marca a alguien en riesgo.

Otra decisión que tomamos para no hacer daño fue quitar a los 15 alumnos con 0 en la calificación final. Eran alumnos que no presentaron el examen, y si los dejábamos, el modelo iba a culpar de esa deserción a cosas que tal vez no tienen que ver. Por último, aplicar el modelo tal cual en una escuela de México también podría hacer daño, porque los datos son de Portugal y de hace casi 20 años, y el modelo se equivocaría más con alumnos tan distintos.

### Justicia

La justicia es tratar a todos de forma equitativa y repartir de forma justa los beneficios y las cargas. Aquí encontramos el problema más claro del proyecto. La regresión logística da falsas alarmas al 33% de los alumnos de zona rural que aprueban, contra el 14% de los de zona urbana. El árbol tiene el mismo problema, con 25% contra 8%. Entre hombres y mujeres la diferencia es más chica, 20% contra 17%. O sea que los alumnos rurales cargarían con más etiquetas injustas.

Algo parecido pasa con la escuela. En la escuela MS reprueba el 26% de los alumnos y en GP el 7%, y por eso estudiar en MS es una de las variables que más sube el riesgo en el modelo. Eso no quiere decir que los alumnos de MS sean menos capaces. Lo más probable es que refleje diferencias de recursos, de traslados o de condiciones entre las dos escuelas, y el modelo solo está repitiendo esa desigualdad.

Pensamos en quitar las variables de zona y escuela, pero eso no arregla el problema, porque otras variables como el tiempo de traslado dicen casi lo mismo. Preferimos dejarlas para poder medir el sesgo y reportarlo, que esconderlo. Si el modelo se usara de verdad, habría que revisar estos números con más alumnos, porque en la prueba solo hay 32 de zona rural, y pensar en ajustes como revisar con más cuidado las alertas de los grupos con más falsas alarmas.

La justicia también se puede ver del otro lado. Si los alumnos rurales y los de MS de verdad reprueban más, también son los que más necesitan apoyo, y un reparto justo de recursos tendría que llegarles a ellos. La clave está en cómo se usa la alerta. Si sirve para dar más apoyo a quien tiene menos, ayuda a la justicia, y si sirve para etiquetar, la empeora.

### Lo que sacamos de este análisis

Los cuatro principios llevan a la misma idea. Un modelo así solo es ético si se usa para ofrecer apoyo y no para castigar, si los alumnos y sus familias saben cómo se usan sus datos, si una persona revisa cada alerta y si se vigila que no trate peor a ningún grupo. El modelo en sí no es bueno ni malo, lo que lo hace ético o no es la forma en que una escuela lo use.
