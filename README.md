# global_health_nutrition_analysis
The work is an end-to-end analytics project using a global health and nutrition dataset to explore how diet, healthcare access and environment shape life expectancy and mortality. Includes advanced SQL-powered EDA, data quality checks, correlation mapping, and an interactive dashboard with narrative storytelling views.

# Project Highlights
✔ Automated schema builder that generates SQLite table definitions from the CSV (no manual typing of 150 columns)
✔ Structured SQL modeling layer (v_core_clean, v_health_access, v_diet_profiles, v_gender_gap_life_expectancy, v_health_diet_join)
✔ End-to-end ETL pipeline using Python + SQLite
✔ Processed analytical datasets ready for machine learning or BI tools
✔ Four detailed EDA notebooks
✔ Interactive Streamlit dashboard with multi-dimensional insights
✔ Story queries that drive narrative insights per country
✔ Production-style repository structure

# Project Architecture
            +---------------------------+
            |   Raw CSV (150 columns)   |
            |  global_health_nutrition  |
            +-------------+-------------+
                          |
                          v
        +--------------------------------------+
        |  generate_sql_schema.py               |
        |  Auto-builds SQL CREATE TABLE schema  |
        +-------------------+------------------+
                          |
                          v
        +--------------------------------------+
        |          load_to_db.py                |
        | Loads CSV → SQLite table              |
        | Applies SQL models (views)            |
        +-------------------+------------------+
                          |
                          v
       +---------------------------------------+
       |  SQL Modeling Layer (Data Warehouse)   |
       |----------------------------------------|
       |  v_core_clean                          |
       |  v_health_access                       |
       |  v_diet_profiles                       |
       |  v_gender_gap_life_expectancy          |
       |  v_health_diet_join                    |
       +-------------------+-------------------+
                          |
                          v
        +--------------------------------------+
        |      export_analytic_tables.py        |
        |  Exports clean datasets to CSVs       |
        +-------------------+------------------+
                          |
          +---------------+----------------+
          |                                |
          v                                v
+-----------------------+      +------------------------+
|  EDA Notebooks        |      |  Streamlit Dashboard   |
|  01_overview          |      |  Multi-page insights   |
|  02_health_access     |      |  Country stories       |
|  03_diet_cvd          |      |  Trend analyses        |
|  04_gender_gap        |      +------------------------+
+-----------------------+

# Folder Structure
global_health_nutrition_analysis/
│
├── data/
│   ├── raw/
│   │   └── global_health_nutrition.csv
│   ├── processed/
│   └── db/
│       └── global_health_nutrition.db
│
├── sql/
│   ├── 01_create_table.sql
│   ├── 02_data_cleaning_views.sql
│   ├── 03_feature_aggregation.sql
│   └── 04_story_queries.sql
│
├── scripts/
│   ├── generate_sql_schema.py
│   ├── load_to_db.py
│   └── export_analytic_tables.py
│
├── notebooks/
│   ├── 01_eda_overview.ipynb
│   ├── 02_health_vs_access.ipynb
│   ├── 03_diet_vs_cardiovascular.ipynb
│   └── 04_gender_and_inequality.ipynb
│
├── dashboard_app/
│   ├── app_streamlit.py
│   ├── queries.py
│   └── __init__.py
│
└── README.md

# SQL Modeling Layer (Data Warehouse Views)
1) v_core_clean

Renamed, cleaned, standardized analytical base
Filters years 1990–2020
Removes null life expectancy
Extracts ~50 core indicators used for analysis

2) v_health_access

Aggregates healthcare & sanitation indicators per country-year:
Doctors, nurses
Drinking water
Basic & safe sanitation
Clean fuel
UHC coverage
Mortality summaries

3) v_diet_profiles

Builds a nutrition profile:
Animal protein kcal
Plant protein kcal
Fat & carb kcal
Total fruit consumption (from 7 fruit variables)

4) v_gender_gap_life_expectancy

Pivot + feature engineering:
female life expectancy
male life expectancy
female − male gap

5) v_health_diet_join

A unified analytical model for dashboard visualization and EDA.

# EDA Notebooks (Exploratory Data Stories)
### 01_eda_overview.ipynb

Global trends in life expectancy

Mortality distributions

Correlation maps

Outlier diagnostics

Exporting cleaned subsets

### 02_health_vs_access.ipynb

Doctors vs infant mortality

Sanitation vs under-5 mortality

UHC coverage bins

Country case studies

### 03_diet_vs_cardiovascular.ipynb

Animal protein vs cardiovascular mortality

Carbohydrate/fat profiles

Diet composition clusters

Trend analysis for selected countries

### 04_gender_and_inequality.ipynb

Life expectancy gaps

Dumbbell charts

Gender gap vs access indicators

Time series inequality analysis

# Streamlit Dashboard
streamlit run dashboard_app/app_streamlit.py

# Dashboard Features
🟦 1. Global Overview

Trends in LE, mortality
Global indicators
Top-10 comparisons

🟩 2. Access & Mortality

Doctors vs mortality
Water/sanitation inequalities
Country heatmaps

🟧 3. Diet & Cardiovascular Health

Scatterplots
Fruit consumption impact
Dietary clusters

🟥 4. Gender & Inequality

Visual gap analytics
Cross-country comparisons

🟪 5. Country Storytelling Module

Dynamic narrative includes:
Life expectancy improvement
Mortality evolution
Diet patterns
Access changes
Automatically generated insights

# How to Run the Project (Step-by-Step)
1. Create environment
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

2. Generate SQL schema automatically
python scripts/generate_sql_schema.py

3. Build the database
python scripts/load_to_db.py

4. Export analytical datasets (optional)
python scripts/export_analytic_tables.py

5. Run the notebooks
jupyter notebook

6. Launch dashboard
streamlit run dashboard_app/app_streamlit.py

