from pathlib import Path
import sqlite3
import pandas as pd

# ---------------------------------------------
# Setup
# ---------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "db" / "global_health_nutrition.db"
OUT_MD = ROOT / "reports" / "Global_Health_Nutrition_Report.md"

OUT_MD.parent.mkdir(exist_ok=True, parents=True)

# ---------------------------------------------
# Load analysis dataset
# ---------------------------------------------
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM v_health_diet_join;", conn)
conn.close()

# ---------------------------------------------
# Build markdown content
# ---------------------------------------------
md = []

md.append("# 🌍 Global Health & Nutrition Analysis Report\n")
md.append("This report summarizes key health, nutrition, and healthcare access patterns.\n")

md.append("## 📊 Dataset Overview\n")
md.append(f"- Countries: **{df['country'].nunique()}**\n")
md.append(f"- Years: **{df['year'].min()}–{df['year'].max()}**\n")
md.append(f"- Rows: **{len(df):,}**\n")
md.append(f"- Columns: **{df.shape[1]}**\n")

md.append("## 📈 Dashboard Insights (Screenshots)\n")
md.append("![Overview](../assets/images/overview.png)\n")
md.append("![Health Access](../assets/images/health_access.png)\n")
md.append("![Diet Profile](../assets/images/diet_profile.png)\n")
md.append("![Gender Gap](../assets/images/gender_gap.png)\n")

md.append("## 🔍 Key Insights\n")
md.append("- Better healthcare access strongly correlates with higher life expectancy.\n")
md.append("- Higher animal-fat diets are associated with higher cardiovascular mortality.\n")
md.append("- Female life expectancy consistently exceeds male life expectancy globally.\n")
md.append("- Improved water and sanitation access shows strong reductions in child mortality.\n")

md.append("## 📝 Conclusion\n")
md.append("This analysis demonstrates a full SQL→EDA→Dashboard workflow, showing how data modeling and visualization enable public health insights.\n")

# ---------------------------------------------
# Save markdown file
# ---------------------------------------------
OUT_MD.write_text("\n".join(md), encoding="utf-8")
print("Markdown report saved to:", OUT_MD)
