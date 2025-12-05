from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------
# Setup paths
# ----------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "db" / "global_health_nutrition.db"
OUT_DIR = ROOT / "reports" / "countries"
PLOTS_DIR = OUT_DIR / "plots"

OUT_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------
# Load unified analytical dataset
# ----------------------------------------------------
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM v_health_diet_join;", conn)
conn.close()

countries = sorted(df["country"].unique())

print(f"Generating reports for {len(countries)} countries...")

# ----------------------------------------------------
# Helper to write a markdown file
# ----------------------------------------------------
def write_md(path, lines):
    path.write_text("\n".join(lines), encoding="utf-8")


def fmt(val):
    if pd.isna(val):
        return "N/A"
    try:
        return f"{float(val):.2f}"
    except Exception:
        return str(val)


def make_slug(country: str) -> str:
    slug = country.replace(" ", "_")
    slug = slug.replace("/", "_").replace("(", "").replace(")", "")
    return slug


# ----------------------------------------------------
# Generate report for each country
# ----------------------------------------------------
for country in countries:
    df_c = df[df["country"] == country].sort_values("year")

    if df_c.empty:
        continue

    slug = make_slug(country)

    # Latest year
    latest = df_c["year"].max()
    row_latest = df_c[df_c["year"] == latest].iloc[0]

    md = []

    # ----------------------------------------------------
    # Section 1 — Header
    # ----------------------------------------------------
    md.append(f"# 🇨🇺 Country Report: **{country}**")
    md.append("")
    md.append(f"**Years Covered:** {df_c['year'].min()} – {df_c['year'].max()}")
    md.append(f"**Latest Data Year:** {latest}")
    md.append("")
    md.append("---")
    md.append("")

    # ----------------------------------------------------
    # Section 2 — Key Indicators (Latest Year)
    # ----------------------------------------------------
    md.append("## 📊 Key Indicators (Latest Year)")
    md.append("")
    md.append(f"- **Life expectancy:** {fmt(row_latest.get('life_expectancy'))}")
    md.append(f"- **Infant mortality:** {fmt(row_latest.get('infant_mortality_rate'))}")
    md.append(f"- **Under-5 mortality:** {fmt(row_latest.get('under5_mortality_rate'))}")
    md.append(f"- **Doctors per 1,000:** {fmt(row_latest.get('doctors'))}")
    md.append(f"- **UHC coverage:** {fmt(row_latest.get('uhc_coverage'))}")
    md.append(f"- **Basic water access:** {fmt(row_latest.get('basic_water'))}")
    md.append(f"- **Basic sanitation:** {fmt(row_latest.get('basic_sanitation_total'))}")
    md.append(f"- **Clean fuel access:** {fmt(row_latest.get('clean_fuel'))}")
    md.append(f"- **GDP per capita:** {fmt(row_latest.get('gdp_per_capita'))}")
    md.append("")
    md.append("---")
    md.append("")

    # ----------------------------------------------------
    # Section 3 — Gender Gap
    # ----------------------------------------------------
    md.append("## 🚻 Gender Gap in Life Expectancy")
    md.append("")

    if "le_gap_female_minus_male" in df_c.columns:
        series_gap = df_c["le_gap_female_minus_male"].dropna()
        if not series_gap.empty:
            md.append(f"- **Latest Gap (Female − Male):** {fmt(series_gap.iloc[-1])} years")
            md.append(f"- **Max gap:** {fmt(series_gap.max())}")
            md.append(f"- **Min gap:** {fmt(series_gap.min())}")
        else:
            md.append("No gender gap data available.")
    else:
        md.append("Gender gap column missing from dataset.")

    md.append("")
    md.append("---")
    md.append("")

    # ----------------------------------------------------
    # Section 4 — Diet Profile Summary
    # ----------------------------------------------------
    md.append("## 🍽️ Diet Profile (Average kcal per capita per day)")
    md.append("")

    for col in ["animal_kcal", "plant_kcal", "fat_kcal", "carb_kcal", "total_fruit_consumption"]:
        if col in df_c.columns:
            md.append(f"- **{col.replace('_',' ').title()}:** {fmt(df_c[col].mean())}")
    md.append("")
    md.append("---")
    md.append("")

    # ----------------------------------------------------
    # Section 5 — Trend Narratives (auto-generated)
    # ----------------------------------------------------
    md.append("## 📈 Trend Summary")
    md.append("")

    try:
        le_change = df_c["life_expectancy"].iloc[-1] - df_c["life_expectancy"].iloc[0]
        md.append(f"- Life expectancy changed by **{le_change:.2f} years** over the dataset.")
    except Exception:
        pass

    try:
        u5_change = df_c["under5_mortality_rate"].iloc[-1] - df_c["under5_mortality_rate"].iloc[0]
        md.append(f"- Under-5 mortality changed by **{u5_change:.2f} per 1,000**.")
    except Exception:
        pass

    if "doctors" in df_c.columns:
        try:
            doc_change = df_c["doctors"].iloc[-1] - df_c["doctors"].iloc[0]
            md.append(f"- Doctors per 1,000 changed by **{doc_change:.2f}**.")
        except Exception:
            pass

    md.append("")
    md.append("---")
    md.append("")

    # ----------------------------------------------------
    # Section 6 — Plots
    # ----------------------------------------------------
    md.append("## 📉 Key Trends (Charts)")
    md.append("")
    md.append("_These charts are generated from the modeled analytical dataset (v_health_diet_join)._")
    md.append("")

    # 6.1 Life expectancy trend
    if "life_expectancy" in df_c.columns:
        plt.figure(figsize=(8, 4))
        plt.plot(df_c["year"], df_c["life_expectancy"], marker="o")
        plt.title(f"Life Expectancy Over Time — {country}")
        plt.xlabel("Year")
        plt.ylabel("Life Expectancy (years)")
        plt.tight_layout()
        plot_path = PLOTS_DIR / f"{slug}_life_expectancy.png"
        plt.savefig(plot_path, dpi=120)
        plt.close()
        md.append(f"![Life Expectancy](plots/{plot_path.name})")
        md.append("")

    # 6.2 Under-5 mortality trend
    if "under5_mortality_rate" in df_c.columns:
        plt.figure(figsize=(8, 4))
        plt.plot(df_c["year"], df_c["under5_mortality_rate"], marker="o", color="tab:red")
        plt.title(f"Under-5 Mortality Over Time — {country}")
        plt.xlabel("Year")
        plt.ylabel("Under-5 Mortality (per 1,000)")
        plt.tight_layout()
        plot_path = PLOTS_DIR / f"{slug}_under5_mortality.png"
        plt.savefig(plot_path, dpi=120)
        plt.close()
        md.append(f"![Under-5 Mortality](plots/{plot_path.name})")
        md.append("")

    # 6.3 Doctors trend
    if "doctors" in df_c.columns:
        plt.figure(figsize=(8, 4))
        plt.plot(df_c["year"], df_c["doctors"], marker="o", color="tab:green")
        plt.title(f"Doctors per 1,000 Over Time — {country}")
        plt.xlabel("Year")
        plt.ylabel("Doctors per 1,000 people")
        plt.tight_layout()
        plot_path = PLOTS_DIR / f"{slug}_doctors.png"
        plt.savefig(plot_path, dpi=120)
        plt.close()
        md.append(f"![Doctors per 1,000](plots/{plot_path.name})")
        md.append("")

    # 6.4 Diet composition trend
    diet_cols = [c for c in ["animal_kcal", "plant_kcal", "fat_kcal", "carb_kcal"] if c in df_c.columns]
    if diet_cols:
        plt.figure(figsize=(8, 4))
        for col in diet_cols:
            plt.plot(df_c["year"], df_c[col], marker="o", label=col)
        plt.title(f"Diet Composition Over Time — {country}")
        plt.xlabel("Year")
        plt.ylabel("kcal per capita per day")
        plt.legend()
        plt.tight_layout()
        plot_path = PLOTS_DIR / f"{slug}_diet.png"
        plt.savefig(plot_path, dpi=120)
        plt.close()
        md.append(f"![Diet Composition](plots/{plot_path.name})")
        md.append("")

    md.append("")
    md.append("---")
    md.append("")
    md.append("_This report was auto-generated from the analytical SQL models and processed data pipeline._")
    md.append("")

    # ----------------------------------------------------
    # Save the Markdown Report
    # ----------------------------------------------------
    filename = f"{slug}.md"
    write_md(OUT_DIR / filename, md)

print("\nAll country reports (with plots) generated successfully!")
