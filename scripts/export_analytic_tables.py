# scripts/export_analytic_tables.py
import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "db" / "global_health_nutrition.db"
PROCESSED_DIR = ROOT / "data" / "processed"

VIEWS_TO_EXPORT = {
    "v_core_clean": "global_health_nutrition_clean.csv",
    "v_health_access": "health_access.csv",
    "v_diet_profiles": "diet_profiles.csv",
    "v_gender_gap_life_expectancy": "gender_gap_life_expectancy.csv",
    "v_health_diet_join": "health_diet_join.csv",
}

def export_view(conn: sqlite3.Connection, view_name: str, filename: str) -> None:
    query = f"SELECT * FROM {view_name};"
    df = pd.read_sql_query(query, conn)
    out_path = PROCESSED_DIR / filename
    df.to_csv(out_path, index=False)
    print(f"Exported {view_name} -> {out_path} ({len(df):,} rows)")

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)

    for view_name, fname in VIEWS_TO_EXPORT.items():
        try:
            export_view(conn, view_name, fname)
        except Exception as e:
            print(f"Skipping {view_name} due to error: {e}")

    conn.close()
    print("Export complete.")

if __name__ == "__main__":
    main()
