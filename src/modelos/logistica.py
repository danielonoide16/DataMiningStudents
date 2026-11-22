"""regresion logistica (aprendizaje supervisado, clasificacion)

objetivo   saber que factores se relacionan con reprobar, sin conocer ninguna calificacion del alumno
por que    da la probabilidad de reprobar y sus coeficientes dicen que variables suben o bajan el riesgo
"""
import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.modelos.evaluacion import (GRUPOS_EQUIDAD, guardar_matriz_confusion, metricas_clasificacion,
                                    revision_equidad)
from src.utils import (CARPETA_FIGURAS, CARPETA_METRICAS, CARPETA_MODELOS, DATOS_TEST, DATOS_TRAIN,
                       OBJETIVO, cargar_params, guardar_json, variables_riesgo)


def main():
    params = cargar_params()["logistica"]
    train, test = pd.read_csv(DATOS_TRAIN), pd.read_csv(DATOS_TEST)
    columnas = variables_riesgo(train)
    X_train, y_train = train[columnas], train[OBJETIVO]
    X_test, y_test = test[columnas], test[OBJETIVO]

    # se escala porque la regularizacion castiga parejo a todos los coeficientes
    # class_weight balanced porque solo ~13% reprueba y queremos detectar a esos alumnos
    modelo = Pipeline([
        ("escalador", StandardScaler()),
        ("logistica", LogisticRegression(C=params["C"], class_weight=params["class_weight"], max_iter=5000)),
    ])
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    metricas = metricas_clasificacion(y_test, y_pred)
    metricas["log_loss_train"] = round(float(log_loss(y_train, modelo.predict_proba(X_train))), 4)
    metricas["log_loss_test"] = round(float(log_loss(y_test, modelo.predict_proba(X_test))), 4)
    metricas["equidad"] = revision_equidad(X_test, y_test.to_numpy(), y_pred, GRUPOS_EQUIDAD)

    # coeficientes. positivo = sube la probabilidad de reprobar
    coef = pd.Series(modelo.named_steps["logistica"].coef_[0], index=columnas)
    top = coef.reindex(coef.abs().sort_values(ascending=False).index).head(12)
    metricas["coeficientes_principales"] = top.round(3).to_dict()

    fig, ax = plt.subplots(figsize=(7, 5))
    top[::-1].plot(kind="barh", ax=ax, color=["tab:red" if v > 0 else "tab:blue" for v in top[::-1]])
    ax.axvline(0, color="black", lw=0.8)
    ax.set_title("Variables con más peso para predecir reprobación")
    ax.set_xlabel("coeficiente (datos escalados)")
    fig.tight_layout()
    fig.savefig(CARPETA_FIGURAS / "logistica_coeficientes.png", dpi=120)
    plt.close(fig)

    guardar_matriz_confusion(y_test, y_pred, "Regresión logística", "logistica_matriz_confusion.png")
    CARPETA_MODELOS.mkdir(exist_ok=True)
    joblib.dump({"modelo": modelo, "columnas": columnas}, CARPETA_MODELOS / "logistica.joblib")
    guardar_json(metricas, CARPETA_METRICAS / "logistica.json")
    print(metricas)


if __name__ == "__main__":
    main()
