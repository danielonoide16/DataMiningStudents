"""despliegue en vivo con streamlit.

para correrla local:   streamlit run app/app.py
"""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

RUTA_MODELO = Path(__file__).parent / "modelo_app.joblib"

st.set_page_config(page_title="Riesgo académico", page_icon="🥸", layout="centered")


@st.cache_resource
def cargar():
    return joblib.load(RUTA_MODELO)


paquete = cargar()

st.title("Riesgo de reprobación y perfil de hábitos")
st.caption("Proyecto integrador de Minería de Datos. Datos de estudiantes de secundaria en Portugal (UCI, 2008).")

st.warning(
    "Esta herramienta es un ejercicio académico. No es un diagnóstico ni debe usarse para tomar "
    "decisiones sobre alumnos reales. El modelo se entrenó con 634 estudiantes de dos escuelas "
    "portuguesas y comete errores, sobre todo con alumnos distintos a los de esos datos."
)

st.subheader("Datos del alumno")
col1, col2 = st.columns(2)
with col1:
    studytime = st.select_slider("Horas de estudio a la semana", options=[1, 2, 3, 4],
                                 format_func=lambda v: {1: "menos de 2", 2: "2 a 5", 3: "5 a 10", 4: "más de 10"}[v],
                                 value=2)
    failures = st.slider("Materias reprobadas antes", 0, 3, 0)
    absences = st.slider("Faltas en el año", 0, 15, 2)
    higher = st.radio("¿Quiere estudiar la universidad?", ["sí", "no"], horizontal=True)
with col2:
    goout = st.slider("Qué tanto sale con amigos (1 a 5)", 1, 5, 3)
    freetime = st.slider("Tiempo libre después de clases (1 a 5)", 1, 5, 3)
    dalc = st.slider("Consumo de alcohol entre semana (1 a 5)", 1, 5, 1)
    walc = st.slider("Consumo de alcohol en fin de semana (1 a 5)", 1, 5, 2)

# las variables que no se preguntan toman el valor tipico de los datos de entrenamiento
alumno = dict(paquete["valores_tipicos"])
alumno.update({"studytime": studytime, "failures": failures, "absences": absences,
               "higher": 1 if higher == "sí" else 0, "goout": goout, "freetime": freetime,
               "Dalc": dalc, "Walc": walc})

X_log = pd.DataFrame([alumno])[paquete["columnas_logistica"]]
X_km = pd.DataFrame([alumno])[paquete["columnas_kmeans"]]

prob = paquete["logistica"].predict_proba(X_log)[0, 1]
perfil = int(paquete["kmeans"].predict(X_km)[0])
tabla_perfiles = paquete["perfiles"]


def nombrar_perfiles(tabla):
    """le pone nombre a cada perfil segun sus promedios y no segun su numero,
    porque el numero que le toca a cada grupo puede cambiar si se vuelve a entrenar k-means"""
    restantes = list(tabla.index)
    nombres = {}
    estudiosos = tabla.loc[restantes, "studytime"].idxmax()
    nombres[estudiosos] = ("Estudiosos", "estudian más de 5 horas a la semana y salen poco")
    restantes.remove(estudiosos)
    fiesteros = tabla.loc[restantes, "Walc"].idxmax()
    nombres[fiesteros] = ("Fiesteros", "salen mucho, toman más y son los que más faltan")
    restantes.remove(fiesteros)
    sociables = tabla.loc[restantes, "goout"].idxmax()
    nombres[sociables] = ("Sociables tranquilos", "salen seguido, pero casi no toman y faltan poco")
    restantes.remove(sociables)
    for p in restantes:
        nombres[p] = ("Ocupados", "tienen poco tiempo libre, casi no salen y faltan un poco más")
    return nombres


nombres_perfiles = nombrar_perfiles(tabla_perfiles)
nombre, descripcion = nombres_perfiles[perfil]

st.subheader("Resultado")
c1, c2 = st.columns(2)
c1.metric("Probabilidad estimada de reprobar", f"{prob:.0%}")
c2.metric("Perfil de hábitos", nombre,
          help="Grupo encontrado con K-means según hábitos de estudio, vida social y faltas")

if prob >= 0.5:
    st.error("El modelo lo marcaría como alumno en riesgo. En la vida real esto solo debería servir "
             "para ofrecer apoyo, nunca para castigar o etiquetar.")
else:
    st.success("El modelo no lo marcaría como alumno en riesgo.")

st.markdown(f"Los alumnos del perfil **{nombre}** {descripcion}. En los datos hay "
            f"**{tabla_perfiles.loc[perfil, 'alumnos']:.0f} alumnos** con este perfil y de ellos reprobó el "
            f"**{tabla_perfiles.loc[perfil, 'porcentaje_reprobados']:.1f}%**.")

with st.expander("Ver promedio de cada perfil"):
    st.dataframe(tabla_perfiles.rename(index={p: n for p, (n, _) in nombres_perfiles.items()}))

with st.expander("¿Cómo funciona?"):
    st.markdown(
        "La probabilidad viene de una regresión logística entrenada sin usar ninguna calificación, "
        "solo datos del contexto del alumno. El perfil viene de K-means usando seis hábitos. "
        "Las variables que no aparecen arriba (familia, escuela, etc.) se llenan con el valor típico "
        "de los datos. Todo el código y los datos están versionados con git y DVC en el repositorio."
    )
