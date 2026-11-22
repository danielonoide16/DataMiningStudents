"""arbol de decision (aprendizaje supervisado, clasificacion)

objetivo   encontrar reglas sencillas que una escuela podria usar para detectar alumnos en riesgo
por que    sus decisiones se leen como reglas "si pasa esto y esto, hay riesgo", que cualquier
           maestro puede entender. no necesita datos escalados porque solo compara cada variable
           contra un umbral. sirve para comparar contra la regresion logistica.
"""
import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

from src.modelos.evaluacion import (GRUPOS_EQUIDAD, guardar_matriz_confusion, metricas_clasificacion,
                                    revision_equidad)
from src.utils import (CARPETA_FIGURAS, CARPETA_METRICAS, CARPETA_MODELOS, DATOS_TEST, DATOS_TRAIN,
                       OBJETIVO, cargar_params, guardar_json, variables_riesgo)


def main():
    todos = cargar_params()
    params = todos["arbol"]
    train, test = pd.read_csv(DATOS_TRAIN), pd.read_csv(DATOS_TEST)
    columnas = variables_riesgo(train)

    # max_depth chico para que las reglas sigan siendo legibles y no se sobreajuste
    modelo = DecisionTreeClassifier(max_depth=params["max_depth"], min_samples_leaf=params["min_samples_leaf"],
                                    class_weight=params["class_weight"], random_state=todos["general"]["semilla"])
    modelo.fit(train[columnas], train[OBJETIVO])

    y_pred = modelo.predict(test[columnas])
    metricas = metricas_clasificacion(test[OBJETIVO], y_pred)
    metricas["exactitud_train"] = round(float(modelo.score(train[columnas], train[OBJETIVO])), 4)
    metricas["equidad"] = revision_equidad(test[columnas], test[OBJETIVO].to_numpy(), y_pred, GRUPOS_EQUIDAD)
    importancia = pd.Series(modelo.feature_importances_, index=columnas).sort_values(ascending=False)
    metricas["importancia_variables"] = importancia[importancia > 0].round(3).to_dict()

    reglas = export_text(modelo, feature_names=columnas)
    (CARPETA_METRICAS / "arbol_reglas.txt").write_text(reglas, encoding="utf-8")

    fig, ax = plt.subplots(figsize=(16, 7))
    plot_tree(modelo, feature_names=columnas, class_names=["aprueba", "reprueba"],
              filled=True, rounded=True, fontsize=8, ax=ax)
    ax.set_title("Árbol de decisión para detectar riesgo de reprobación")
    fig.tight_layout()
    fig.savefig(CARPETA_FIGURAS / "arbol.png", dpi=120)
    plt.close(fig)

    guardar_matriz_confusion(test[OBJETIVO], y_pred, "Árbol de decisión", "arbol_matriz_confusion.png")
    CARPETA_MODELOS.mkdir(exist_ok=True)
    joblib.dump({"modelo": modelo, "columnas": columnas}, CARPETA_MODELOS / "arbol.joblib")
    guardar_json(metricas, CARPETA_METRICAS / "arbol.json")
    print(metricas)
    print(reglas)


if __name__ == "__main__":
    main()
