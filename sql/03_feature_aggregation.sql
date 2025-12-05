DROP VIEW IF EXISTS v_gender_gap_life_expectancy;

CREATE VIEW v_gender_gap_life_expectancy AS
SELECT
    country,
    year,
    MAX(CASE WHEN gender = 'Female' THEN life_expectancy END) AS le_female,
    MAX(CASE WHEN gender = 'Male' THEN life_expectancy END) AS le_male,
    MAX(CASE WHEN gender = 'Both sexes' THEN life_expectancy END) AS le_both,
    MAX(CASE WHEN gender = 'Female' THEN life_expectancy END)
      - MAX(CASE WHEN gender = 'Male' THEN life_expectancy END) AS le_gap_female_minus_male
FROM v_core_clean
GROUP BY country, year;

DROP VIEW IF EXISTS v_diet_profiles;

CREATE VIEW v_diet_profiles AS
SELECT
    country,
    year,
    AVG(kcal_animal) AS animal_kcal,
    AVG(kcal_plant) AS plant_kcal,
    AVG(kcal_fat) AS fat_kcal,
    AVG(kcal_carb) AS carb_kcal,
    AVG(
        COALESCE(fruit_bananas,0) +
        COALESCE(fruit_oranges,0) +
        COALESCE(fruit_apples,0) +
        COALESCE(fruit_lemons_limes,0) +
        COALESCE(fruit_grapes,0) +
        COALESCE(fruit_grapefruit,0) +
        COALESCE(fruit_pineapples,0)
    ) AS total_fruit_consumption
FROM v_core_clean
GROUP BY country, year;

DROP VIEW IF EXISTS v_health_access;

CREATE VIEW v_health_access AS
SELECT
    country,
    year,
    AVG(life_expectancy) AS life_expectancy,
    AVG(infant_mortality_rate) AS infant_mortality_rate,
    AVG(under5_mortality_rate) AS under5_mortality_rate,
    AVG(neonatal_mortality_rate) AS neonatal_mortality_rate,
    AVG(uhc_coverage) AS uhc_coverage,
    AVG(doctors) AS doctors,
    AVG(nurses_midwifes) AS nurses_midwifes,
    AVG(basic_water) AS basic_water,
    AVG(basic_sanitation_total) AS basic_sanitation_total,
    AVG(safely_sanitation_total) AS safely_sanitation_total,
    AVG(clean_fuel) AS clean_fuel
FROM v_core_clean
GROUP BY country, year;

DROP VIEW IF EXISTS v_health_diet_join;

CREATE VIEW v_health_diet_join AS
SELECT
    h.country,
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
    d.total_fruit_consumption,
    g.le_gap_female_minus_male
FROM v_health_access h
LEFT JOIN v_diet_profiles d
    ON h.country = d.country AND h.year = d.year
LEFT JOIN v_gender_gap_life_expectancy g
    ON h.country = g.country AND h.year = g.year;
