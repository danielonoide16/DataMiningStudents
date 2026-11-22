# Diccionario de datos

**Fuente.** Student Performance, UCI Machine Learning Repository (dataset 320). Cortez, P. y Silva, A. (2008). *Using Data Mining to Predict Secondary School Student Performance*. Se usa el archivo de la materia de portugués (`student-por.csv`), con 649 alumnos de dos escuelas públicas de Portugal en el ciclo 2005 a 2006. Los datos se juntaron con reportes escolares y cuestionarios.

Página oficial https://archive.ics.uci.edu/dataset/320/student+performance

El archivo de `data/raw/` se descargó de una copia en GitHub (https://github.com/X1nzhe/Student-Performance-Data) porque el sitio de la UCI pide descargar un zip. Se revisó que tuviera 649 filas, 33 columnas y un promedio de calificación final de 11.906, igual que el original.

| Columna | Qué significa | Valores |
|---|---|---|
| school | escuela | GP (Gabriel Pereira) o MS (Mousinho da Silveira) |
| sex | sexo | F o M |
| age | edad | 15 a 22 |
| address | zona donde vive | U urbana, R rural |
| famsize | tamaño de la familia | LE3 (3 o menos), GT3 (más de 3) |
| Pstatus | situación de los padres | T viven juntos, A separados |
| Medu | escolaridad de la madre | 0 ninguna, 1 primaria, 2 secundaria baja, 3 secundaria, 4 universidad |
| Fedu | escolaridad del padre | igual que Medu |
| Mjob | trabajo de la madre | teacher, health, services, at_home, other |
| Fjob | trabajo del padre | igual que Mjob |
| reason | razón para elegir la escuela | home (cerca de casa), reputation, course, other |
| guardian | tutor | mother, father, other |
| traveltime | tiempo de traslado a la escuela | 1 menos de 15 min, 2 de 15 a 30, 3 de 30 min a 1 h, 4 más de 1 h |
| studytime | horas de estudio a la semana | 1 menos de 2 h, 2 de 2 a 5, 3 de 5 a 10, 4 más de 10 |
| failures | materias reprobadas antes | 0 a 3 (4 significa 3 o más) |
| schoolsup | apoyo educativo extra de la escuela | yes, no |
| famsup | apoyo educativo de la familia | yes, no |
| paid | clases particulares pagadas de la materia | yes, no |
| activities | actividades extraescolares | yes, no |
| nursery | fue al kínder | yes, no |
| higher | quiere estudiar la universidad | yes, no |
| internet | internet en casa | yes, no |
| romantic | tiene pareja | yes, no |
| famrel | calidad de la relación familiar | 1 muy mala a 5 excelente |
| freetime | tiempo libre después de clases | 1 muy poco a 5 mucho |
| goout | qué tanto sale con amigos | 1 muy poco a 5 mucho |
| Dalc | consumo de alcohol entre semana | 1 muy bajo a 5 muy alto |
| Walc | consumo de alcohol en fin de semana | 1 muy bajo a 5 muy alto |
| health | estado de salud | 1 muy malo a 5 muy bueno |
| absences | faltas | 0 a 93 |
| G1 | calificación del primer periodo | 0 a 20 |
| G2 | calificación del segundo periodo | 0 a 20 |
| G3 | calificación final | 0 a 20, se aprueba con 10 |

**Variables que crea el pipeline.** `reprobado` vale 1 si G3 es menor a 10. Las columnas yes/no se convierten a 1/0 y las de texto sin orden se convierten con one hot (por ejemplo `school_ms`, `sex_m`, `address_u`).
