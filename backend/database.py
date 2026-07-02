import sqlite3
import pandas as pd
from pathlib import Path


class database:
    def __init__(self, DB_PATH, SCHEMA_PATH):
        self.DB_PATH = DB_PATH
        self.SCHEMA_PATH = SCHEMA_PATH

        self.conn = sqlite3.connect(self.DB_PATH)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row

        schema = self.SCHEMA_PATH.read_text(encoding="utf-8")
        self.conn.executescript(schema)
        self.conn.commit()
        print(f"Base de données prête : {self.DB_PATH}")

    def load_from_csv(self, csv_path: str, table_name: str, **kwargs) -> None:
        print(f"loading {table_name}")
        csv_data = pd.read_csv(csv_path, **kwargs)
        
        csv_data.columns = (csv_data.columns
                .str.replace(":", "_", regex=False)
                .str.replace(" ", "_", regex=False)
                .str.replace("-", "_", regex=False)
                .str.replace("(", "", regex=False)
                .str.replace(")", "", regex=False)
                )

        cursor = self.conn.cursor()

        columns = ', '.join(csv_data.columns)
        placeholders = ', '.join(
            ['?'] * len(csv_data.columns))  # Use ? for SQLite

        # Convert DataFrame to list of tuples
        values = [tuple(row) for _, row in csv_data.iterrows()]

        # Execute all inserts at once
        cursor.executemany(f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
        """, values)

        self.conn.commit()
        cursor.close()


if __name__ == "__main__":
    db = database(
        DB_PATH=f"{Path(__file__).parent}/database.db",
        SCHEMA_PATH=Path(__file__).parent / "database_schema.sql"
    )

    db.load_from_csv(r"Naiades_filter/stations.csv",
                     table_name="Stations", sep=";", on_bad_lines="skip", dtype=str)
    db.load_from_csv(r"Naiades_filter/cep_94.csv",
                     table_name="CEP", sep=";", on_bad_lines="skip", dtype=str)
    db.load_from_csv(r"Naiades_filter/fauneflore_94.csv",
                     table_name="FauneFlore", sep=";", on_bad_lines="skip", dtype=str)
    db.load_from_csv(r"Naiades_filter/operation_94.csv",
                     table_name="Operations", sep=";", on_bad_lines="skip", dtype=str)
    db.load_from_csv(r"Naiades_filter/resultat_94.csv",
                     table_name="Resultats", sep=";", on_bad_lines="skip", dtype=str)
    db.load_from_csv(r"filtre_donnees_animaux/ammonium.CSV",
                     table_name="Ammonium", sep=",", on_bad_lines="skip", dtype=str)
    db.load_from_csv(r"filtre_donnees_animaux/temp.CSV",
                     table_name="Temperature", sep=",", on_bad_lines="skip", dtype=str)
    db.load_from_csv(r"filtre_donnees_animaux/dbo5.CSV",
                     table_name="DBO5", sep=",", on_bad_lines="skip", dtype=str)
    db.load_from_csv(r"filtre_donnees_animaux/fauneflore_94_protege.csv",
                     table_name="AnimauxProteges", sep=";", on_bad_lines="skip", dtype=str)
