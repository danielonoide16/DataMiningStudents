"""funciones que comparten todas las etapas del pipeline"""
import json
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]

DATOS_CRUDOS = RAIZ / "data" / "raw" / "estudiantes_portugues.csv"
DATOS_LIMPIOS = RAIZ / "data" / "interim" / "estudiantes_limpio.csv"
DATOS_TRAIN = RAIZ / "data" / "processed" / "train.csv"
DATOS_TEST = RAIZ / "data" / "processed" / "test.csv"
CARPETA_MODELOS = RAIZ / "models"
CARPETA_METRICAS = RAIZ / "reports" / "metrics"
CARPETA_FIGURAS = RAIZ / "reports" / "figures"

# columnas que nunca se usan como variables de entrada para predecir riesgo
CALIFICACIONES = ["G1", "G2", "G3"]
OBJETIVO = "reprobado"


def cargar_params():
    with open(RAIZ / "params.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def guardar_json(datos, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def variables_riesgo(df):
    """variables para predecir riesgo sin conocer ninguna calificacion"""
    return [c for c in df.columns if c not in CALIFICACIONES + [OBJETIVO]]
