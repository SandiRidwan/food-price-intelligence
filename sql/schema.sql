-- schema.sql — Skema database (DuckDB).
-- Lapisan: raw/staging (data mentah) → marts (analitik siap-pakai).

-- ===========================================================================
-- STAGING: data mentah yang sudah dinormalisasi bentuknya (long format)
-- ===========================================================================
CREATE TABLE IF NOT EXISTS stg_wb_indicators (
    country_iso      VARCHAR NOT NULL,
    country          VARCHAR NOT NULL,
    indicator_code   VARCHAR NOT NULL,
    indicator_name   VARCHAR NOT NULL,
    category         VARCHAR NOT NULL,
    year             INTEGER NOT NULL,
    value            DOUBLE,
    PRIMARY KEY (country_iso, indicator_code, year)
);

CREATE TABLE IF NOT EXISTS stg_fx (
    date     DATE PRIMARY KEY,
    usd_idr  DOUBLE
);

-- ===========================================================================
-- MARTS: tabel siap-analisis (dibangun oleh transform.py)
-- ===========================================================================

-- Indeks harga pangan (2010=100) per negara per tahun + pertumbuhan YoY
CREATE TABLE IF NOT EXISTS mart_food_price_index (
    country_iso    VARCHAR,
    country        VARCHAR,
    year           INTEGER,
    price_index    DOUBLE,
    yoy_pct        DOUBLE,
    yoy_flag       VARCHAR,      -- 'spike' | 'elevated' | 'normal'
    PRIMARY KEY (country_iso, year)
);

-- Inflasi harga konsumen (%) per negara per tahun
CREATE TABLE IF NOT EXISTS mart_inflation (
    country_iso   VARCHAR,
    country       VARCHAR,
    year          INTEGER,
    inflation_pct DOUBLE,
    alert         BOOLEAN,
    PRIMARY KEY (country_iso, year)
);

-- Papan ketahanan pangan: gabungan semua indikator per negara-tahun
CREATE TABLE IF NOT EXISTS mart_food_security (
    country_iso        VARCHAR,
    country            VARCHAR,
    year               INTEGER,
    price_index        DOUBLE,
    inflation_pct      DOUBLE,
    food_prod_index    DOUBLE,
    food_import_pct    DOUBLE,
    fertilizer_per_ha  DOUBLE,
    pop_growth_pct     DOUBLE,
    PRIMARY KEY (country_iso, year)
);

-- Peringkat ASEAN per tahun (berdasar inflasi pangan terendah & produksi)
CREATE TABLE IF NOT EXISTS mart_asean_ranking (
    year               INTEGER,
    country_iso        VARCHAR,
    country            VARCHAR,
    inflation_pct      DOUBLE,
    food_prod_index    DOUBLE,
    rank_inflation     INTEGER,   -- 1 = inflasi terendah (terbaik)
    rank_production    INTEGER,   -- 1 = produksi tertinggi
    PRIMARY KEY (year, country_iso)
);
