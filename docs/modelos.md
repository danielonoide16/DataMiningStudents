# Algoritmos usados y por qué

El objetivo del proyecto es entender qué se relaciona con que un estudiante de secundaria repruebe y qué tanto se puede anticipar. Para eso usamos cuatro algoritmos, tres supervisados y uno no supervisado, cada uno con un objetivo distinto.

| Algoritmo | Tipo | Objetivo | Script |
|---|---|---|---|
| Regresión logística | Supervisado, clasificación | Saber qué factores se relacionan con reprobar, sin conocer ninguna calificación | `src/modelos/logistica.py` |
| Árbol de decisión | Supervisado, clasificación | Encontrar reglas sencillas que una escuela podría usar para detectar alumnos en riesgo | `src/modelos/arbol.py` |
| K-means | No supervisado, clustering | Encontrar perfiles de estudiantes según sus hábitos y ver en cuál se reprueba más | `src/modelos/kmeans.py` |
| Regresión lineal | Supervisado, regresión | Ver qué tanto se puede predecir la calificación final y cuánto ayuda conocer la del primer periodo | `src/modelos/lineal.py` |

## Justificación

**Regresión logística.** La variable que queremos predecir es si el alumno reprueba o no, así que es un problema de clasificación binaria. La logística da una probabilidad y sus coeficientes dicen qué variables suben o bajan el riesgo, que es justo lo que queremos entender. Escalamos los datos porque la regularización castiga parejo a todos los coeficientes, y usamos `class_weight="balanced"` porque solo 13% de los alumnos reprueba.

**Árbol de decisión.** Resuelve el mismo problema que la logística pero de otra forma. En vez de coeficientes da reglas del tipo "si ya reprobó una materia y no quiere ir a la universidad, hay riesgo", que cualquier maestro puede entender sin saber de modelos. Lo dejamos con profundidad 3 para que las reglas sigan siendo legibles y no se sobreajuste. Compararlo con la logística nos dice si un modelo simple de reglas pierde mucho contra uno de probabilidades.

**K-means.** Aquí no hay una etiqueta de "perfil", queremos que los grupos salgan solos de los datos, por eso es no supervisado. Solo usamos seis hábitos (estudio, tiempo libre, salidas, alcohol entre semana y fin de semana, faltas). Ya con los grupos formados vemos qué tanto se reprueba en cada uno, pero esa columna no se usa para agrupar. Para elegir K usamos el codo y la silueta.

**Regresión lineal.** La calificación final es un número de 0 a 20, así que es un problema de regresión. Entrenamos dos versiones, una solo con el contexto del alumno y otra que además conoce la calificación del primer periodo, para medir cuánto aporta esa información.

## Primeros resultados

Estos son los números que salen con los parámetros actuales de `params.yaml`. La interpretación completa va en `notebooks/02_resultados.ipynb`.

La regresión logística detecta 59% de los alumnos que reprueban (recall) con 78% de exactitud. Las variables con más peso hacia reprobar son estudiar en la escuela MS, haber reprobado antes y tener muchas faltas. Querer ir a la universidad y hacer actividades extraescolares van en sentido contrario.

El árbol de profundidad 3 llega a 83% de exactitud y 53% de recall. Su primera regla es si el alumno ya reprobó alguna materia, y después si quiere estudiar la universidad.

Con K-means y K = 4 salen cuatro perfiles. El de alumnos que salen mucho y toman más alcohol reprueba 22%, mientras que el de alumnos que estudian más de 5 horas a la semana reprueba solo 5%. La silueta es baja (0.17). La más alta sale con K = 2, pero elegimos K = 4 porque con dos grupos solo se separan los alumnos que salen y toman más del resto, y con cuatro ya aparece un grupo de alumnos estudiosos. La justificación completa está en el notebook de resultados.

En la regresión lineal, sin calificaciones se explica 32% de la variación de la calificación final (R² de 0.32, error promedio de 1.9 puntos). Al agregar la calificación del primer periodo sube a 75% (R² de 0.75, error de 1.1 puntos).
