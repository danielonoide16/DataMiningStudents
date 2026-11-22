"""funciones de evaluacion que comparten los modelos de clasificacion"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score, precision_score,
                             recall_score, ConfusionMatrixDisplay)

from src.utils import CARPETA_FIGURAS


def metricas_clasificacion(y_real, y_pred):
    # el recall es la metrica mas importante aqui: de los alumnos que si reprueban, cuantos detectamos
    return {
        "exactitud": round(float(accuracy_score(y_real, y_pred)), 4),
        "precision": round(float(precision_score(y_real, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_real, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_real, y_pred, zero_division=0)), 4),
    }


def guardar_matriz_confusion(y_real, y_pred, titulo, nombre_archivo):
    fig, ax = plt.subplots(figsize=(4.5, 4))
    ConfusionMatrixDisplay(confusion_matrix(y_real, y_pred),
                           display_labels=["aprueba", "reprueba"]).plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(titulo)
    fig.tight_layout()
    fig.savefig(CARPETA_FIGURAS / nombre_archivo, dpi=120)
    plt.close(fig)


def revision_equidad(X_test, y_real, y_pred, columnas):
    """compara el recall y las falsas alarmas entre grupos (por ejemplo hombres y mujeres).
    si un grupo tiene muchas mas falsas alarmas, el modelo lo estaria etiquetando de mas."""
    resultado = {}
    for columna, nombres in columnas.items():
        if columna not in X_test.columns:
            continue
        for valor, nombre in nombres.items():
            mascara = (X_test[columna] == valor).to_numpy()
            yr, yp = y_real[mascara], y_pred[mascara]
            aprobados = yr == 0
            resultado[nombre] = {
                "alumnos": int(mascara.sum()),
                "recall": round(float(recall_score(yr, yp, zero_division=0)), 4),
                "falsas_alarmas": round(float((yp[aprobados] == 1).mean()) if aprobados.any() else 0.0, 4),
            }
    return resultado


GRUPOS_EQUIDAD = {
    "sex_m": {0: "mujeres", 1: "hombres"},
    "address_u": {0: "zona_rural", 1: "zona_urbana"},
}
