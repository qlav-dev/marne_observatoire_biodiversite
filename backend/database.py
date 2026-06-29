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
        csv_data = pd.read_csv(csv_path, **kwargs)
        
        cursor = self.conn.cursor()
        
        columns = ', '.join(csv_data.columns)
        placeholders = ', '.join(['?'] * len(csv_data.columns))  # Use ? for SQLite
        
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
        DB_PATH = f"{Path(__file__).parent}/naiades_database.db",
        SCHEMA_PATH = Path(__file__).parent / "schema.sql"
    )

    db.load_from_csv(r"Naiades_filter/stations.csv", table_name="Stations", sep = ";", on_bad_lines="skip", dtype=str)

