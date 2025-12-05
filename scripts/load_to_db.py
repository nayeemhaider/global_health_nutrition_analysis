# scripts/load_to_db.py
import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "db" / "global_health_nutrition.db"
CSV_PATH = ROOT / "data" / "raw" / "global_health_nutrition.csv"

SQL_SCHEMA_PATH = ROOT / "sql" / "01_create_table.sql"
SQL_CLEANING_PATH = ROOT / "sql" / "02_data_cleaning_views.sql"
SQL_FEATURES_PATH = ROOT / "sql" / "03_feature_aggregation.sql"

def run_sql_file(conn: sqlite3.Connection, path: Path) -> None:
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)

    print("Creating table schema...")
    run_sql_file(conn, SQL_SCHEMA_PATH)

    print(f"Loading CSV from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    print(f"Inserting {len(df):,} rows into table 'global_health_nutrition'...")
    df.to_sql("global_health_nutrition", conn, if_exists="append", index=False)

    print("Creating cleaning and feature views...")
    run_sql_file(conn, SQL_CLEANING_PATH)
    run_sql_file(conn, SQL_FEATURES_PATH)

    conn.commit()
    conn.close()
    print("Done. Database is ready with views defined.")

if __name__ == "__main__":
    main()
