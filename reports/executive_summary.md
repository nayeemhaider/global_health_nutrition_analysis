# Global Health & Nutrition Atlas — Executive Summary

This project analyses how health systems, water and sanitation, and nutrition patterns relate to life expectancy and mortality across countries and over time.

## Key questions

1. How has global life expectancy changed over the last decades and where is child mortality still high?
2. How do healthcare resources and access to basic services relate to mortality outcomes?
3. How does diet composition relate to cardiovascular deaths and overall health?
4. Where do gender gaps and inequality in access remain largest?

## Data and methods

The analysis uses a wide multi-year dataset with:

• Country, year and gender as identifiers  
• More than 150 features covering mortality, infectious disease, healthcare access, water and sanitation, demographics and nutrition  

Steps:

1. Data loading and schema definition in a SQLite database  
2. Data cleaning and feature engineering using SQL views  
3. Exploratory data analysis and visualisation in Jupyter notebooks  
4. Construction of analytic views that join health outcomes, access indicators and diet patterns  
5. Storytelling dashboard in Streamlit for interactive exploration

## High-level insights

• Life expectancy has increased globally but remains low in countries with high child mortality and limited sanitation coverage.  
• Infant and under-5 mortality are strongly associated with basic water and sanitation indicators, and less strongly with doctor density alone.  
• Countries with high calories from animal protein tend to show higher shares of deaths from cardiovascular causes, although there is substantial variation.  
• Female life expectancy is higher than male life expectancy in nearly all countries, but the size of the gap and its trend over time differ widely.

These insights are meant as a starting point and should be refined as the analysis deepens.
