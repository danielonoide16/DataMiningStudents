"""etapa final de dvc. junta lo que necesita la app en un solo archivo.

app/modelo_app.joblib se guarda en git (cache: false en dvc.yaml) para que streamlit cloud
lo pueda leer sin tener acceso al remoto de dvc.
"""
import joblib
import pandas as pd

from src.utils import CARPETA_MODELOS, DATOS_TRAIN, RAIZ


def main():
    log = joblib.load(CARPETA_MODELOS / "logistica.joblib")
    km = joblib.load(CARPETA_MODELOS / "kmeans.joblib")
    train = pd.read_csv(DATOS_TRAIN)

    # valores tipicos para las variables que el usuario no mueve en la app
    valores_tipicos = train[log["columnas"]].median().to_dict()

    paquete = {
        "logistica": log["modelo"],
        "columnas_logistica": log["columnas"],
        "kmeans": km["modelo"],
        "columnas_kmeans": km["columnas"],
        "perfiles": km["perfiles"],
        "valores_tipicos": valores_tipicos,
    }
    salida = RAIZ / "app" / "modelo_app.joblib"
    salida.parent.mkdir(exist_ok=True)
    joblib.dump(paquete, salida)
    print("guardado", salida)


if __name__ == "__main__":
    main()
