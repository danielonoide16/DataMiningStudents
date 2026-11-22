"""etapa 1 de dvc. limpia los datos crudos y deja un reporte de todo lo que se cambio.

entrada  data/raw/estudiantes_portugues.csv
salidas  data/interim/estudiantes_limpio.csv, reports/metrics/limpieza.json
"""
import numpy as np
import pandas as pd

from src.utils import DATOS_CRUDOS, DATOS_LIMPIOS, CARPETA_METRICAS, cargar_params, guardar_json


def main():
    params = cargar_params()["limpiar"]
    df = pd.read_csv(DATOS_CRUDOS)
    reporte = {"filas_originales": int(len(df))}

    # 1. texto uniforme (sin espacios extra y en minusculas) para que "Yes" y "yes" sean lo mismo
    columnas_texto = df.select_dtypes(exclude="number").columns
    for c in columnas_texto:
        df[c] = df[c].astype(str).str.strip().str.lower()

    # 2. renglones duplicados
    reporte["duplicados_quitados"] = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # 3. valores fuera de rango se vuelven faltantes, porque no son confiables
    fuera_de_rango = {}
    for columna, (minimo, maximo) in params["rangos"].items():
        malos = ~df[columna].between(minimo, maximo)
        fuera_de_rango[columna] = int(malos.sum())
        df.loc[malos, columna] = np.nan
    reporte["fuera_de_rango"] = fuera_de_rango

    # 4. valores faltantes. numericos con la mediana, texto con la moda
    reporte["faltantes_antes"] = {c: int(n) for c, n in df.isna().sum().items() if n > 0}
    for c in df.columns:
        if df[c].isna().any():
            if c in columnas_texto:
                df[c] = df[c].fillna(df[c].mode()[0])
            else:
                df[c] = df[c].fillna(df[c].median())
    reporte["faltantes_despues"] = int(df.isna().sum().sum())

    # 5. calificacion final en 0. en este dataset significa que el alumno no presento el examen,
    #    no que saco 0, asi que se quitan para no mezclar desercion con bajo rendimiento
    if params["quitar_g3_cero"]:
        ceros = df["G3"] == 0
        reporte["g3_cero_quitados"] = int(ceros.sum())
        df = df[~ceros]

    # 6. outliers con el metodo iqr. no se borran, se recortan al limite (winsorizacion)
    #    para no perder alumnos pero evitar que unos pocos valores extremos dominen
    outliers = {}
    for c in params["columnas_outliers"]:
        q1, q3 = df[c].quantile([0.25, 0.75])
        limite = q3 + params["factor_iqr"] * (q3 - q1)
        n = int((df[c] > limite).sum())
        outliers[c] = {"limite_superior": float(limite), "valores_recortados": n,
                       "maximo_original": float(df[c].max())}
        df[c] = df[c].clip(upper=limite)
    reporte["outliers"] = outliers

    reporte["filas_finales"] = int(len(df))
    DATOS_LIMPIOS.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATOS_LIMPIOS, index=False)
    guardar_json(reporte, CARPETA_METRICAS / "limpieza.json")
    print(reporte)


if __name__ == "__main__":
    main()
