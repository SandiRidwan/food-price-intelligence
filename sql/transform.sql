-- transform.sql — STAGING → MARTS (logika analitik dalam SQL murni).
-- Dijalankan oleh transform.py setelah load_db.py.

-- ===========================================================================
-- 1. INDEKS HARGA PANGAN + YoY + flag anomali
-- ===========================================================================
DELETE FROM mart_food_price_index;
INSERT INTO mart_food_price_index
WITH base AS (
    SELECT country_iso, country, year, value AS price_index
    FROM stg_wb_indicators
    WHERE indicator_code = 'FP.CPI.TOTL' AND value IS NOT NULL
),
with_prev AS (
    SELECT *,
           LAG(price_index) OVER (PARTITION BY country_iso ORDER BY year) AS prev
    FROM base
)
SELECT
    country_iso,
    country,
    year,
    price_index,
    CASE WHEN prev IS NULL OR prev = 0 THEN NULL
         ELSE ROUND((price_index - prev) / prev * 100, 2) END AS yoy_pct,
    CASE
        WHEN prev IS NULL OR prev = 0 THEN 'normal'
        WHEN (price_index - prev) / prev * 100 >= 7 THEN 'spike'
        WHEN (price_index - prev) / prev * 100 >= 3 THEN 'elevated'
        ELSE 'normal'
    END AS yoy_flag
FROM with_prev;

-- ===========================================================================
-- 2. INFLASI + alert
-- ===========================================================================
DELETE FROM mart_inflation;
INSERT INTO mart_inflation
SELECT
    country_iso, country, year, value AS inflation_pct,
    (value >= 5.0) AS alert
FROM stg_wb_indicators
WHERE indicator_code = 'FP.CPI.TOTL.ZG' AND value IS NOT NULL;

-- ===========================================================================
-- 3. PAPAN KETAHANAN PANGAN (pivot semua indikator)
-- ===========================================================================
DELETE FROM mart_food_security;
INSERT INTO mart_food_security
SELECT
    country_iso, country, year,
    MAX(CASE WHEN indicator_code='FP.CPI.TOTL'        THEN value END) AS price_index,
    MAX(CASE WHEN indicator_code='FP.CPI.TOTL.ZG'     THEN value END) AS inflation_pct,
    MAX(CASE WHEN indicator_code='AG.PRD.FOOD.XD'     THEN value END) AS food_prod_index,
    MAX(CASE WHEN indicator_code='TM.VAL.FOOD.ZS.UN'  THEN value END) AS food_import_pct,
    MAX(CASE WHEN indicator_code='AG.CON.FERT.ZS'     THEN value END) AS fertilizer_per_ha,
    MAX(CASE WHEN indicator_code='SP.POP.GROW'        THEN value END) AS pop_growth_pct
FROM stg_wb_indicators
GROUP BY country_iso, country, year;

-- ===========================================================================
-- 4. PERINGKAT ASEAN per tahun
-- ===========================================================================
DELETE FROM mart_asean_ranking;
INSERT INTO mart_asean_ranking
SELECT
    year, country_iso, country, inflation_pct, food_prod_index,
    CASE WHEN inflation_pct IS NULL THEN NULL
         ELSE RANK() OVER (PARTITION BY year ORDER BY inflation_pct ASC) END
        AS rank_inflation,
    CASE WHEN food_prod_index IS NULL THEN NULL
         ELSE RANK() OVER (PARTITION BY year ORDER BY food_prod_index DESC) END
        AS rank_production
FROM mart_food_security;
