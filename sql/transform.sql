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

-- ===========================================================================
-- 5. INFLASI PANGAN BULANAN PER KOTA (BPS)
-- ===========================================================================
DELETE FROM mart_food_inflation_monthly;
INSERT INTO mart_food_inflation_monthly
SELECT
    wilayah_nama,
    year,
    CASE lower(periode)
        WHEN 'januari' THEN 1 WHEN 'februari' THEN 2 WHEN 'maret' THEN 3
        WHEN 'april' THEN 4 WHEN 'mei' THEN 5 WHEN 'juni' THEN 6
        WHEN 'juli' THEN 7 WHEN 'agustus' THEN 8 WHEN 'september' THEN 9
        WHEN 'oktober' THEN 10 WHEN 'november' THEN 11 WHEN 'desember' THEN 12
        ELSE NULL END AS month_num,
    periode AS month,
    value AS inflation_pct,
    (lower(periode) = 'tahunan') AS kel_semua
FROM stg_bps_food_inflation
WHERE lower(turvar_label) = 'makanan'      -- hanya kelompok MAKANAN
  AND value IS NOT NULL;

-- Ringkasan tahunan per kota (rata-rata & volatilitas bulanan)
DELETE FROM mart_food_inflation_city;
INSERT INTO mart_food_inflation_city
SELECT
    wilayah_nama,
    year,
    round(avg(inflation_pct), 3)  AS avg_inflation_pct,
    round(max(inflation_pct), 3)  AS max_inflation_pct,
    round(min(inflation_pct), 3)  AS min_inflation_pct,
    round(stddev_pop(inflation_pct), 3) AS volatility,
    count(*)                      AS n_bulan
FROM mart_food_inflation_monthly
WHERE month_num IS NOT NULL
GROUP BY wilayah_nama, year;

-- Inflasi pangan nasional bulanan (rata-rata lintas kota)
DELETE FROM mart_food_inflation_national;
INSERT INTO mart_food_inflation_national
SELECT
    year, month_num,
    round(avg(inflation_pct), 3) AS avg_inflation,
    count(DISTINCT wilayah_nama) AS n_kota
FROM mart_food_inflation_monthly
WHERE month_num IS NOT NULL
GROUP BY year, month_num;

-- ===========================================================================
-- 6. HARGA BERAS PER KOTA
-- ===========================================================================
DELETE FROM mart_rice_price;
INSERT INTO mart_rice_price
SELECT wilayah_nama, year, round(value, 0) AS harga_rp_kg
FROM stg_bps_rice_price
WHERE value IS NOT NULL;


-- ===========================================================================
-- 7. HARGA BERAS GROSIR BULANAN (2020-2026, TERBARU)
-- ===========================================================================
DELETE FROM mart_rice_wholesale;
INSERT INTO mart_rice_wholesale
SELECT
    year,
    CASE lower(periode)
        WHEN 'januari' THEN 1 WHEN 'februari' THEN 2 WHEN 'maret' THEN 3
        WHEN 'april' THEN 4 WHEN 'mei' THEN 5 WHEN 'juni' THEN 6
        WHEN 'juli' THEN 7 WHEN 'agustus' THEN 8 WHEN 'september' THEN 9
        WHEN 'oktober' THEN 10 WHEN 'november' THEN 11 WHEN 'desember' THEN 12
        ELSE NULL END AS month_num,
    periode AS month,
    value AS harga_rp_kg
FROM stg_bps_rice_wholesale
WHERE value IS NOT NULL
  AND lower(periode) IN ('januari','februari','maret','april','mei','juni',
                         'juli','agustus','september','oktober','november',
                         'desember');

-- ===========================================================================
-- 8. INFLASI BULANAN PER KOTA (2020-2026, TERBARU)
-- ===========================================================================
DELETE FROM mart_monthly_inflation;
INSERT INTO mart_monthly_inflation
SELECT
    wilayah_nama,
    year,
    CASE lower(periode)
        WHEN 'januari' THEN 1 WHEN 'februari' THEN 2 WHEN 'maret' THEN 3
        WHEN 'april' THEN 4 WHEN 'mei' THEN 5 WHEN 'juni' THEN 6
        WHEN 'juli' THEN 7 WHEN 'agustus' THEN 8 WHEN 'september' THEN 9
        WHEN 'oktober' THEN 10 WHEN 'november' THEN 11 WHEN 'desember' THEN 12
        ELSE NULL END AS month_num,
    periode AS month,
    value AS inflation_pct
FROM stg_bps_monthly_inflation
WHERE value IS NOT NULL
  AND lower(periode) IN ('januari','februari','maret','april','mei','juni',
                         'juli','agustus','september','oktober','november',
                         'desember');

-- Kota: ringkasan inflasi tahun TERAKHIR yang tersedia
DELETE FROM mart_city_latest;
INSERT INTO mart_city_latest
SELECT
    wilayah_nama,
    max(year) AS year,
    round(avg(inflation_pct), 3) AS avg_inflation_pct,
    round(max(inflation_pct), 3) AS max_inflation_pct,
    count(*) AS n_bulan
FROM mart_monthly_inflation
WHERE year = (SELECT max(year) FROM mart_monthly_inflation)
GROUP BY wilayah_nama;
