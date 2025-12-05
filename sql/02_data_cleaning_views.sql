-- Cleans and renames columns into a nice analytical base view.

DROP VIEW IF EXISTS v_core_clean;

CREATE VIEW v_core_clean AS
SELECT
    TRIM(Country) AS country,
    Year AS year,
    Gender AS gender,
    "Life Expectancy" AS life_expectancy,
    "Infant Mortality Rate" AS infant_mortality_rate,
    "Under 5 Mortality Rate" AS under5_mortality_rate,
    "Suicides Rate" AS suicides_rate,
    "Road Traffic Deaths" AS road_traffic_deaths,
    "Death Rate" AS death_rate,
    "Universal Heath Care Coverage" AS uhc_coverage,
    "Doctors" AS doctors,
    "Nurses and Midwifes" AS nurses_midwifes,
    "Dentists" AS dentists,
    "Pharmacists" AS pharmacists,
    "Basic Drinking Water Services" AS basic_water,
    "Basic Sanization Services Total" AS basic_sanitation_total,
    "Basic Sanization Services Urban" AS basic_sanitation_urban,
    "Basic Sanization Services Rural" AS basic_sanitation_rural,
    "Safely Sanitation Total" AS safely_sanitation_total,
    "Safely Sanitation Urban" AS safely_sanitation_urban,
    "Safely Sanitation Rural" AS safely_sanitation_rural,
    "Basic Hand Washing Total" AS handwashing_total,
    "Clean Fuel and Technology" AS clean_fuel,
    "GDP per Capita" AS gdp_per_capita,
    "Fruit Consumption Bananas" AS fruit_bananas,
    "Fruit Consumption Oranges and Mandarins" AS fruit_oranges,
    "Fruit Consumption Apples" AS fruit_apples,
    "Fruit Consumption Lemons And Limes" AS fruit_lemons_limes,
    "Fruit Consumption Grapes" AS fruit_grapes,
    "Fruit Consumption Grapefruit" AS fruit_grapefruit,
    "Fruit Consumption Pineapples" AS fruit_pineapples,
    "Cereal Consumption Oats" AS cereal_oats,
    "Cereal Consumption Rye" AS cereal_rye,
    "Cereal Consumption Barley" AS cereal_barley,
    "Cereal Consumption Sorghum" AS cereal_sorghum,
    "Cereal Consumption Maize" AS cereal_maize,
    "Cereal Consumption Wheat" AS cereal_wheat,
    "Cereal Consumption Rice" AS cereal_rice,
    "Diet Calories Animal Protein" AS kcal_animal,
    "Diet Calories Plant Protein" AS kcal_plant,
    "Diet Calories Fat" AS kcal_fat,
    "Diet Calories Carbohydrates" AS kcal_carb,
    "% Death Cardiovascular" AS pct_death_cardiovascular,
    "Air Pollution Death Rate Total" AS air_pollution_death_total
FROM global_health_nutrition
WHERE Year BETWEEN 1990 AND 2020
  AND "Life Expectancy" IS NOT NULL;
