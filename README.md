# global_health_nutrition_analysis
The work is an end-to-end analytics project using a global health and nutrition dataset to explore how diet, healthcare access and environment shape life expectancy and mortality. Includes advanced SQL-powered EDA, data quality checks, correlation mapping, and an interactive dashboard with narrative storytelling views.

# Global Health & Nutrition Atlas

An end-to-end data analysis project exploring how health systems, water and sanitation, and nutrition patterns relate to life expectancy and mortality across the world.

The project uses a global health and nutrition dataset with 150 features and more than 20,000 country–year–gender records. It combines SQL, Python and an interactive Streamlit dashboard to tell a data story about health, access and inequality.

## Objectives

• Clean and model a wide multi-year health dataset using SQL and Python  
• Explore relationships between life expectancy, child mortality and health infrastructure  
• Analyse how diet and nutrition relate to cardiovascular deaths and overall health  
• Study gender gaps and inequality in access to basic services  
• Build an interactive dashboard for storytelling and country-level exploration  

## Dataset

The main dataset is stored in:

`data/raw/global_health_nutrition.csv`

Rows represent combinations of:

• Country  
• Year  
• Gender  

Example feature groups:

• Health outcomes:  
  Life Expectancy, Infant Mortality Rate, Under 5 Mortality Rate, Neonatal Mortality Rate, Suicides Rate, Road Traffic Deaths, % Injury Deaths, Death Rate  

• Environment and pollution:  
  Air Pollution Death Rate (stroke, ischaemic heart disease, COPD, lower respiratory infections) with confidence intervals  

• Infectious disease and interventions:  
  Hepatitis B Surface Antigen, Intervention Against NTDs, Malaria, Tuberculosis  

• Health system access:  
  Universal Heath Care Coverage, Births attended by skilled health personnel, Doctors, Nurses and Midwifes, Dentists, Pharmacists  

• Water, sanitation and hygiene:  
  Basic Drinking Water Services, Basic Sanization Services (total, urban, rural), Safely Sanitation (total, urban, rural), Basic Hand Washing (total, urban, rural), Clean Fuel and Technology  

• Demographics and SDG-style indicators:  
  Population 10 Percentage SDG (total, urban, rural), Population 25 Percentage SDG (total, urban, rural), Reproductive Age Women, Adolescent Birth Rate, Birth Rate, Battle Related Deaths  

• Nutrition and diet:  
  Fruit Consumption (Bananas, Oranges, Apples, Lemons and Limes, Grapes, Grapefruit, Pineapples)  
  Cereal Consumption (Oats, Rye, Barley, Sorghum, Maize, Wheat, Rice)  
  Diet Calories Animal Protein, Diet Calories Plant Protein, Diet Calories Fat, Diet Calories Carbohydrates  

## Project structure

data/                 Raw CSV, cleaned CSVs, SQLite DB
sql/                  Database schema, cleaning views, feature aggregations, story queries
notebooks/            Jupyter notebooks for detailed EDA and analysis
dashboard_app/        Streamlit application for interactive storytelling
scripts/              Utility scripts (load CSV to DB, export analytic tables)
reports/              Executive summary and country-level story outputs
assets/images/        Screenshots for README and documentation


# To run the dashboard

## 1. Create and activate a virtual environment
pip install -r requirements.txt

## 2. Load the CSV into a local SQLite database
python scripts/load_to_db.py

## 3. Launch the dashboard
streamlit run dashboard_app/app_streamlit.py
