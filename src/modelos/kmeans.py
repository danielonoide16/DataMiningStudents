"""k-means (aprendizaje NO supervisado, clustering) + pca solo para graficar

objetivo   encontrar perfiles de estudiantes segun sus habitos y ver en cual se reprueba mas
por que    no hay una etiqueta de "perfil", queremos que los grupos salgan de los datos. despues
           comparamos que tanto se reprueba en cada grupo, pero esa columna no se usa para agrupar.
"""
import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.utils import (CARPETA_FIGURAS, CARPETA_METRICAS, CARPETA_MODELOS, DATOS_TEST, DATOS_TRAIN,
                       OBJETIVO, cargar_params, guardar_json)


def main():
    todos = cargar_params()
    params = todos["kmeans"]
    semilla = todos["general"]["semilla"]

    # en no supervisado no hay que separar train y test, se usan todos los alumnos
    df = pd.concat([pd.read_csv(DATOS_TRAIN), pd.read_csv(DATOS_TEST)], ignore_index=True)
    X = df[params["columnas"]]

    # k-means usa distancias, por eso es indispensable escalar
    X_esc = StandardScaler().fit_transform(X)

    # codo y silueta para elegir k
    valores_k = list(range(params["k_min"], params["k_max"] + 1))
    inercias, siluetas = [], []
    for k in valores_k:
        km = KMeans(n_clusters=k, random_state=semilla, n_init=10).fit(X_esc)
        inercias.append(float(km.inertia_))
        siluetas.append(float(silhouette_score(X_esc, km.labels_)))

    fig, ejes = plt.subplots(1, 2, figsize=(11, 4))
    ejes[0].plot(valores_k, inercias, marker="o")
    ejes[0].set(title="Método del codo", xlabel="K", ylabel="Inercia (WCSS)")
    ejes[1].plot(valores_k, siluetas, marker="o", color="tab:orange")
    ejes[1].axvline(params["k"], color="gray", ls="--", lw=0.8)
    ejes[1].set(title="Coeficiente de silueta", xlabel="K", ylabel="Silueta promedio")
    fig.suptitle("Elección de K")
    fig.tight_layout()
    fig.savefig(CARPETA_FIGURAS / "kmeans_elegir_k.png", dpi=120)
    plt.close(fig)

    # modelo final con el k elegido en params.yaml
    modelo = Pipeline([("escalador", StandardScaler()),
                       ("kmeans", KMeans(n_clusters=params["k"], random_state=semilla, n_init=10))])
    df["perfil"] = modelo.fit_predict(X)

    perfiles = df.groupby("perfil")[params["columnas"]].mean().round(2)
    perfiles["alumnos"] = df["perfil"].value_counts().sort_index()
    perfiles["porcentaje_reprobados"] = (df.groupby("perfil")[OBJETIVO].mean() * 100).round(1)
    perfiles.to_csv(CARPETA_METRICAS / "kmeans_perfiles.csv")

    # pca solo para poder ver los grupos en 2d
    X_2d = PCA(n_components=2, random_state=semilla).fit_transform(X_esc)
    fig, ax = plt.subplots(figsize=(7, 5.5))
    for p in sorted(df["perfil"].unique()):
        m = (df["perfil"] == p).to_numpy()
        ax.scatter(X_2d[m, 0], X_2d[m, 1], s=18, alpha=0.7, label=f"perfil {p}")
    ax.set(title="Perfiles de estudiantes (vista con PCA)", xlabel="Componente 1", ylabel="Componente 2")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CARPETA_FIGURAS / "kmeans_perfiles_pca.png", dpi=120)
    plt.close(fig)

    metricas = {
        "k_elegido": params["k"],
        "silueta_k_elegido": round(siluetas[valores_k.index(params["k"])], 4),
        "silueta_por_k": dict(zip(map(str, valores_k), [round(s, 4) for s in siluetas])),
        "inercia_por_k": dict(zip(map(str, valores_k), [round(i, 1) for i in inercias])),
    }
    CARPETA_MODELOS.mkdir(exist_ok=True)
    joblib.dump({"modelo": modelo, "columnas": params["columnas"], "perfiles": perfiles},
                CARPETA_MODELOS / "kmeans.joblib")
    guardar_json(metricas, CARPETA_METRICAS / "kmeans.json")
    print(metricas)
    print(perfiles)


if __name__ == "__main__":
    main()
