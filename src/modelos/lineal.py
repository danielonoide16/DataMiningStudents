"""regresion lineal (aprendizaje supervisado, regresion)

objetivo   ver que tanto se puede predecir la calificacion final y cuanto ayuda conocer la del
           primer periodo
por que    la calificacion final es un numero continuo de 0 a 20, y la regresion lineal permite
           comparar facil dos modelos, uno sin calificaciones y otro "temprano" que agrega G1
"""
import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.utils import (CARPETA_FIGURAS, CARPETA_METRICAS, CARPETA_MODELOS, DATOS_TEST, DATOS_TRAIN,
                       cargar_params, guardar_json, variables_riesgo)


def entrenar(train, test, columnas):
    modelo = Pipeline([("escalador", StandardScaler()), ("lineal", LinearRegression())])
    modelo.fit(train[columnas], train["G3"])
    pred = modelo.predict(test[columnas])
    metricas = {
        "r2": round(float(r2_score(test["G3"], pred)), 4),
        "mae": round(float(mean_absolute_error(test["G3"], pred)), 4),
        "rmse": round(float(root_mean_squared_error(test["G3"], pred)), 4),
    }
    return modelo, pred, metricas


def main():
    params = cargar_params()["lineal"]
    train, test = pd.read_csv(DATOS_TRAIN), pd.read_csv(DATOS_TEST)

    base = variables_riesgo(train)
    temprano = base + params["columnas_extra_temprano"]

    modelo_base, pred_base, met_base = entrenar(train, test, base)
    modelo_temp, pred_temp, met_temp = entrenar(train, test, temprano)
    metricas = {"sin_calificaciones": met_base, "con_primer_periodo": met_temp}

    fig, ejes = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    for ax, pred, nombre, m in [(ejes[0], pred_base, "Sin calificaciones", met_base),
                                (ejes[1], pred_temp, "Con calificación del 1er periodo", met_temp)]:
        ax.scatter(test["G3"], pred, alpha=0.6, s=20)
        ax.plot([0, 20], [0, 20], "k--", lw=0.8)
        ax.set_title(f"{nombre}\nR² = {m['r2']}  |  MAE = {m['mae']}")
        ax.set_xlabel("calificación final real")
    ejes[0].set_ylabel("calificación final predicha")
    fig.suptitle("Regresión lineal de la calificación final")
    fig.tight_layout()
    fig.savefig(CARPETA_FIGURAS / "lineal_real_vs_predicho.png", dpi=120)
    plt.close(fig)

    CARPETA_MODELOS.mkdir(exist_ok=True)
    joblib.dump({"sin_calificaciones": modelo_base, "con_primer_periodo": modelo_temp,
                 "columnas_base": base, "columnas_temprano": temprano},
                CARPETA_MODELOS / "lineal.joblib")
    guardar_json(metricas, CARPETA_METRICAS / "lineal.json")
    print(metricas)


if __name__ == "__main__":
    main()
