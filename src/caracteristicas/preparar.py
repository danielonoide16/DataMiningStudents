"""etapa 2 de dvc. crea la variable objetivo, codifica las columnas de texto y separa train/test.

entrada  data/interim/estudiantes_limpio.csv
salidas  data/processed/train.csv, data/processed/test.csv

la normalizacion (StandardScaler) no se hace aqui, sino dentro de cada modelo con un Pipeline.
asi el escalador solo aprende de los datos de entrenamiento y no hay fuga de informacion.
"""
import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils import DATOS_LIMPIOS, DATOS_TRAIN, DATOS_TEST, OBJETIVO, cargar_params


def main():
    todos = cargar_params()
    params = todos["preparar"]
    df = pd.read_csv(DATOS_LIMPIOS)

    # variable objetivo. 1 si la calificacion final no alcanza la aprobatoria
    df[OBJETIVO] = (df["G3"] < params["calificacion_aprobatoria"]).astype(int)

    # columnas yes/no a 1/0
    binarias = [c for c in df.columns if set(df[c].dropna().unique()) <= {"yes", "no"}]
    for c in binarias:
        df[c] = (df[c] == "yes").astype(int)

    # el resto de columnas de texto no tienen orden, asi que van con one hot
    # drop_first evita tener una columna que se puede deducir de las demas
    nominales = df.select_dtypes(exclude="number").columns.tolist()
    df = pd.get_dummies(df, columns=nominales, drop_first=True, dtype=int)

    # stratify mantiene la misma proporcion de reprobados en train y en test
    train, test = train_test_split(df, test_size=params["tamano_prueba"],
                                   random_state=todos["general"]["semilla"], stratify=df[OBJETIVO])

    DATOS_TRAIN.parent.mkdir(parents=True, exist_ok=True)
    train.to_csv(DATOS_TRAIN, index=False)
    test.to_csv(DATOS_TEST, index=False)
    print(f"train {train.shape} | test {test.shape} | reprobados en train {train[OBJETIVO].mean():.1%}")


if __name__ == "__main__":
    main()
