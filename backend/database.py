import sqlite3
from pathlib import Path

class database:
    DB_PATH = f"{Path(__file__).parent}/naiades_database.db"
    SCHEMA_PATH = Path(__file__).parent / "schema.sql"

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self,conn: sqlite3.Connection) -> None:
        schema = self.SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema)

    def main(self) -> None:
        with self.get_connection() as conn:
            self.init_db(conn)
            conn.commit()
        print(f"Base de données prête : {self.DB_PATH}")


if __name__ == "__main__":
    database().main()