-- Top 10 countries by life expectancy in a given year
SELECT country, life_expectancy
FROM v_health_access
WHERE year = :year
ORDER BY life_expectancy DESC
LIMIT 10;

-- Doctors vs infant mortality for last 5 years
SELECT
    country,
    AVG(doctors) AS doctors_avg,
    AVG(infant_mortality_rate) AS imr_avg
FROM v_health_access
WHERE year BETWEEN :end_year - 4 AND :end_year
GROUP BY country;

-- Fastest improvement in under-5 mortality between two periods
WITH period_stats AS (
    SELECT
        country,
        CASE WHEN year <= :mid_year THEN 'early' ELSE 'late' END AS period,
        AVG(under5_mortality_rate) AS u5_avg
    FROM v_health_access
    WHERE year BETWEEN :start_year AND :end_year
    GROUP BY country, period
)
SELECT
    e.country,
    e.u5_avg AS u5_early,
    l.u5_avg AS u5_late,
    (e.u5_avg - l.u5_avg) AS u5_improvement
FROM period_stats e
JOIN period_stats l
  ON e.country = l.country
 AND e.period = 'early'
 AND l.period = 'late'
ORDER BY u5_improvement DESC;

-- Diet vs cardiovascular deaths
SELECT
    h.country,
    h.year,
    h.life_expectancy,
    h.infant_mortality_rate,
    h.under5_mortality_rate,
    h.uhc_coverage,
    d.animal_kcal,
    d.plant_kcal,
    d.fat_kcal,
    d.carb_kcal,
    d.total_fruit_consumption,
    c."% Death Cardiovascular" AS pct_death_cardiovascular
FROM v_health_diet_join d
JOIN v_health_access h
  ON d.country = h.country AND d.year = h.year
JOIN global_health_nutrition c
  ON c.Country = h.country AND c.Year = h.year AND c.Gender = 'Both sexes';
