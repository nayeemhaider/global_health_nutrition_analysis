import pandas as pd
from pathlib import Path

CSV_PATH = Path("data/raw/global_health_nutrition.csv")
OUTPUT_SQL = Path("sql/01_create_table.sql")

df = pd.read_csv(CSV_PATH, nrows=5)  # read small sample for column names

columns = df.columns.tolist()

sql_lines = []
sql_lines.append("DROP TABLE IF EXISTS global_health_nutrition;")
sql_lines.append("")
sql_lines.append("CREATE TABLE global_health_nutrition (")

for i, col in enumerate(columns):
    col_sql = f'    "{col}" REAL'
    if i < len(columns) - 1:
        col_sql += ","
    sql_lines.append(col_sql)

sql_lines.append(");")

OUTPUT_SQL.write_text("\n".join(sql_lines), encoding="utf-8")

print(f"Schema created at: {OUTPUT_SQL}")
print("Column count:", len(columns))
