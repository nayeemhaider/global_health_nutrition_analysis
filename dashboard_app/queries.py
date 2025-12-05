from typing import Optional, List
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "db" / "global_health_nutrition.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

def get_year_range() -> List[int]:
    query = "SELECT DISTINCT year FROM v_health_access ORDER BY year;"
    with engine.connect() as conn:
        years = pd.read_sql(query, conn)["year"].tolist()
    return years

def get_countries() -> List[str]:
    query = "SELECT DISTINCT country FROM v_health_access ORDER BY country;"
    with engine.connect() as conn:
        countries = pd.read_sql(query, conn)["country"].tolist()
    return countries

def get_global_overview(year: int) -> pd.DataFrame:
    query = text("""
        SELECT
            country,
            life_expectancy,
            infant_mortality_rate,
            under5_mortality_rate,
            uhc_coverage
        FROM v_health_access
        WHERE year = :year
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"year": year})
    return df

def get_top_life_expectancy(year: int, limit: int = 10) -> pd.DataFrame:
    query = text("""
        SELECT country, life_expectancy
        FROM v_health_access
        WHERE year = :year
        ORDER BY life_expectancy DESC
        LIMIT :limit
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"year": year, "limit": limit})
    return df

def get_doctors_vs_mortality(end_year: int) -> pd.DataFrame:
    query = text("""
        SELECT
            country,
            AVG(doctors) AS doctors_avg,
            AVG(infant_mortality_rate) AS imr_avg
        FROM v_health_access
        WHERE year BETWEEN :start_year AND :end_year
        GROUP BY country
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"start_year": end_year - 4, "end_year": end_year})
    return df

def get_diet_vs_cvd(year: int) -> pd.DataFrame:
    query = text("""
        SELECT
            h.country,
            h.life_expectancy,
            h.infant_mortality_rate,
            d.animal_kcal,
            d.plant_kcal,
            d.fat_kcal,
            d.carb_kcal,
            d.total_fruit_consumption,
            c."% Death Cardiovascular" AS pct_death_cardiovascular
        FROM v_health_access h
        JOIN v_diet_profiles d
          ON h.country = d.country AND h.year = d.year
        JOIN global_health_nutrition c
          ON c.Country = h.country AND c.Year = h.year AND c.Gender = 'Both sexes'
        WHERE h.year = :year
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"year": year})
    return df

def get_gender_gap_year(year: int) -> pd.DataFrame:
    query = text("""
        SELECT
            country,
            le_female,
            le_male,
            le_gap_female_minus_male
        FROM v_gender_gap_life_expectancy
        WHERE year = :year
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"year": year})
    return df

def get_country_story(country: str) -> pd.DataFrame:
    query = text("""
        SELECT
            h.year,
            h.life_expectancy,
            h.infant_mortality_rate,
            h.under5_mortality_rate,
            h.uhc_coverage,
            h.doctors,
            h.basic_water,
            h.basic_sanitation_total,
            d.animal_kcal,
            d.plant_kcal,
            d.fat_kcal,
            d.carb_kcal,
            d.total_fruit_consumption
        FROM v_health_access h
        LEFT JOIN v_diet_profiles d
          ON h.country = d.country AND h.year = d.year
        WHERE h.country = :country
        ORDER BY h.year
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"country": country})
    return df
