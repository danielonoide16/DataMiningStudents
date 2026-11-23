# Riesgo académico en estudiantes de secundaria



Proyecto integrador de Minería de Datos. Analizamos datos de 649 estudiantes de secundaria en Portugal para entender qué factores se relacionan con reprobar, qué perfiles de estudiantes existen según sus hábitos y qué tanto se puede predecir la calificación final. Usamos cuatro algoritmos (regresión logística, árbol de decisión, K-means y regresión lineal) y todo el proceso está versionado con git y DVC para que los datos y los resultados tengan trazabilidad.

**App en vivo** https://dataminingstudents.streamlit.app/

## Equipo

- Daniel Jiménez Sánchez
- Axel Roman Vázquez Pelayo

## Documentación

La justificación de cada algoritmo y los primeros resultados están en [`docs/modelos.md`](docs/modelos.md). El análisis ético está en [`docs/etica.md`](docs/etica.md) y la descripción de cada variable en [`docs/diccionario_datos.md`](docs/diccionario_datos.md).

## Datos

Usamos el dataset Student Performance de la UCI (Cortez y Silva, 2008), archivo de la materia de portugués. El archivo original está en `data/raw/` y lo controla DVC, no git. En git solo se guarda `data/raw/estudiantes_portugues.csv.dvc`, que tiene el hash del archivo, así sabemos exactamente qué versión de los datos produjo cada resultado.

## Estructura del proyecto

```
├── data
│   ├── raw/            datos originales, nunca se modifican (DVC)
│   ├── interim/        datos limpios (DVC)
│   └── processed/      datos codificados y separados en train/test (DVC)
├── docs/               análisis ético, justificación de los modelos y diccionario de datos
├── models/             modelos entrenados (DVC)
├── notebooks
│   ├── 01_exploracion.ipynb   análisis exploratorio y justificación de la limpieza
│   └── 02_resultados.ipynb    resultados e interpretación de los 4 modelos
├── reports
│   ├── figures/        gráficas que genera el pipeline
│   └── metrics/        métricas en json (las compara `dvc metrics show`)
├── src
│   ├── datos/limpiar.py              etapa 1, limpieza
│   ├── caracteristicas/preparar.py   etapa 2, codificación y train/test
│   ├── modelos/logistica.py          regresión logística
│   ├── modelos/arbol.py              árbol de decisión
│   ├── modelos/kmeans.py             k-means (no supervisado)
│   ├── modelos/lineal.py             regresión lineal
│   └── modelos/exportar.py           arma el modelo que usa la app
├── app/app.py          despliegue con Streamlit
├── dvc.yaml            etapas del pipeline
├── params.yaml         todos los parámetros en un solo lugar
└── requirements.txt
```

## Pipeline

```
data/raw → limpiar → preparar → logistica ┐
                              → arbol     │
                              → kmeans    ├→ exportar → app
                              → lineal    ┘
```

La limpieza revisa duplicados, valores fuera de rango y faltantes, quita a los 15 alumnos con calificación final de 0 (no presentaron el examen) y recorta los outliers de faltas con el método IQR. Todo lo que cambia queda registrado en `reports/metrics/limpieza.json`. La normalización con `StandardScaler` va dentro de cada modelo con un `Pipeline` para que solo aprenda de los datos de entrenamiento. Las justificaciones completas están en el notebook de exploración y en los comentarios de cada script.

## Configuración inicial (solo la hace una persona, una vez)

```bash
# 1. ambiente
python -m venv .venv
source .venv/bin/activate          # en windows .venv\Scripts\activate
pip install -r requirements.txt

# 2. subir a github
git init
git add .
git commit -m "base del proyecto"
git branch -M main
git remote add origin https://github.com/<usuario>/<repo>.git
git push -u origin main

# 3. conectar el remoto de dvc en dagshub
#    en dagshub.com: Create → New Repository → Connect a repository → GitHub → elegir el repo
#    el token sale en dagshub.com/user/settings/tokens
dvc remote add -d origin https://dagshub.com/<usuario>/<repo>.dvc
dvc remote modify origin --local auth basic
dvc remote modify origin --local user <usuario-dagshub>
dvc remote modify origin --local password <token-dagshub>

# 4. correr el pipeline (vuelve a generar data/interim, data/processed y models)
#    y subir los datos y modelos al remoto
dvc repro
dvc push
git add .dvc/config
git commit -m "remoto de dvc en dagshub"
git push
```

El usuario y el token van con `--local`, así se guardan en `.dvc/config.local`, que no se sube a git.

## Para el otro integrante

```bash
git clone https://github.com/<usuario>/<repo>.git
cd <repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# credenciales propias de dagshub (cada quien las suyas)
dvc remote modify origin --local auth basic
dvc remote modify origin --local user <su-usuario-dagshub>
dvc remote modify origin --local password <su-token-dagshub>

dvc pull                           # baja los datos y modelos
```

En DagsHub hay que agregar al otro integrante como colaborador del repo (Settings → Collaborators).

## Trabajo del día a día

```bash
git pull && dvc pull               # traer lo último del equipo

# cambiar un script o un valor de params.yaml, y luego
dvc repro                          # corre solo las etapas que cambiaron
dvc metrics diff                   # compara las métricas contra el último commit
dvc dag                            # muestra el grafo del pipeline

git add .
git commit -m "describir el cambio"
dvc push                           # sube datos y modelos nuevos
git push                           # sube código, dvc.lock y métricas
```

El orden importa. Siempre `dvc push` antes o junto con `git push`, si no el otro integrante va a tener un `dvc.lock` que apunta a archivos que no existen en el remoto.

## Despliegue

La app está en `app/app.py` y se corre local con `streamlit run app/app.py`. Para publicarla, en [share.streamlit.io](https://share.streamlit.io) se elige el repo, la rama `main` y el archivo `app/app.py`. Streamlit Cloud instala `requirements.txt` y lee `app/modelo_app.joblib`, que es el único modelo que se guarda en git (en `dvc.yaml` tiene `cache: false`) para que la app no necesite acceso al remoto de DVC. Cada vez que cambie el modelo hay que correr `dvc repro`, hacer commit de ese archivo y la app se actualiza sola.
