"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import glob
import os

import pandas as pd

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    def load_data(input_directory):

        for f in glob.glob(os.path.join(input_directory, "*.csv")):
            return pd.read_csv(f, sep=";", index_col=0)

    def process_data(df):
        """Procesa los datos"""

        df = df.drop_duplicates()
        df = df.dropna()

        # Convertir fechas
        df["year"] = df["fecha_de_beneficio"].map(
            lambda x: (
                int(x.split("/")[0])
                if len(x.split("/")[0]) > 2
                else int(x.split("/")[-1])
            )
        )
        df["month"] = df["fecha_de_beneficio"].map(lambda x: int(x.split("/")[1]))
        df["day"] = df["fecha_de_beneficio"].map(
            lambda x: (
                int(x.split("/")[-1])
                if len(x.split("/")[0]) > 2
                else int(x.split("/")[0])
            )
        )
        df["fecha_de_beneficio"] = pd.to_datetime(df[["year", "month", "day"]])

        df = df.drop(columns=["year", "month", "day"])

        # Manipulacion strings
        columns = df.columns.tolist()
        columns.remove("barrio")

        df["barrio"] = df["barrio"].map(
            lambda x: x.lower().replace("_", "-").replace("-", " ")
        )

        df[columns] = df[columns].map(
            lambda x: (
                x.lower()
                .replace("-", " ")
                .replace("_", " ")
                .replace("$", "")
                .replace(".00", "")
                .replace(",", "")
                .strip()
                if isinstance(x, str)
                else x
            )
        )

        # Eliminar registros duplicados nuevamente
        df = df.drop_duplicates()

        return df

    def save_file(df, output_directory, file_name):
        """Guarda el archivo en la carpeta de salida"""
        if os.path.exists(output_directory):
            os.remove(os.path.join(output_directory, file_name))
            os.rmdir(output_directory)
        os.makedirs(output_directory, exist_ok=True)

        df.to_csv(os.path.join(output_directory, file_name), sep=";", index=False)

    df = load_data("files/input")
    df = process_data(df)
    save_file(df, "files/output", "solicitudes_de_credito.csv")

    return "Se ha limpiado el archivo correctamente"


if __name__ == "__main__":
    print(pregunta_01())