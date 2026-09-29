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

-- Inflasi PANGAN bulanan per kota (BPS, var 1890)
CREATE TABLE IF NOT EXISTS stg_bps_food_inflation (
    wilayah_kode  VARCHAR NOT NULL,
    wilayah_nama  VARCHAR NOT NULL,
    year          INTEGER NOT NULL,
    periode       VARCHAR NOT NULL,     -- Januari..Desember / Tahunan
    turvar_label  VARCHAR,              -- kelompok: Makanan/Minuman/Rokok
    value         DOUBLE
);

-- Harga eceran beras per kota (BPS, var 79)
CREATE TABLE IF NOT EXISTS stg_bps_rice_price (
    wilayah_kode  VARCHAR NOT NULL,
    wilayah_nama  VARCHAR NOT NULL,
    year          INTEGER NOT NULL,
    value         DOUBLE                -- Rupiah/kg
);

-- Harga beras GROSIR bulanan (BPS var 295, 2020–2026) — data TERBARU
CREATE TABLE IF NOT EXISTS stg_bps_rice_wholesale (
    year          INTEGER NOT NULL,
    periode       VARCHAR,
    turtahun      VARCHAR,
    value         DOUBLE                -- Rupiah/kg
);

-- Inflasi BULANAN per kota (BPS var 1, 2020–2026) — data TERBARU
CREATE TABLE IF NOT EXISTS stg_bps_monthly_inflation (
    wilayah_kode  VARCHAR NOT NULL,
    wilayah_nama  VARCHAR NOT NULL,
    year          INTEGER NOT NULL,
    turtahun      VARCHAR,
    periode       VARCHAR,
    value         DOUBLE
);

-- ===========================================================================
-- MARTS: tabel siap-analisis (dibangun oleh transform.py)
-- ===========================================================================

-- Inflasi pangan bulanan per kota (kanonikal, hanya kelompok 'Makanan')
CREATE TABLE IF NOT EXISTS mart_food_inflation_monthly (
    wilayah_nama  VARCHAR,
    year          INTEGER,
    month_num     INTEGER,
    month         VARCHAR,
    inflation_pct DOUBLE,
    kel_semua     BOOLEAN               -- TRUE = baris 'Tahunan'
);

-- Ringkasan inflasi pangan tahunan per kota (rata-rata & volatilitas)
CREATE TABLE IF NOT EXISTS mart_food_inflation_city (
    wilayah_nama       VARCHAR,
    year               INTEGER,
    avg_inflation_pct  DOUBLE,
    max_inflation_pct  DOUBLE,
    min_inflation_pct  DOUBLE,
    volatility         DOUBLE,          -- stddev bulanan (proxy risiko)
    n_bulan            INTEGER,
    PRIMARY KEY (wilayah_nama, year)
);

-- Inflasi pangan nasional bulanan (rata-rata lintas kota)
CREATE TABLE IF NOT EXISTS mart_food_inflation_national (
    year          INTEGER,
    month_num     INTEGER,
    avg_inflation DOUBLE,
    n_kota        INTEGER,
    PRIMARY KEY (year, month_num)
);

-- Harga beras per kota per tahun
CREATE TABLE IF NOT EXISTS mart_rice_price (
    wilayah_nama  VARCHAR,
    year          INTEGER,
    harga_rp_kg   DOUBLE,
    PRIMARY KEY (wilayah_nama, year)
);

-- Harga beras GROSIR nasional bulanan (2020–2026, TERBARU)
CREATE TABLE IF NOT EXISTS mart_rice_wholesale (
    year        INTEGER,
    month_num   INTEGER,
    month       VARCHAR,
    harga_rp_kg DOUBLE,
    PRIMARY KEY (year, month_num)
);

-- Inflasi bulanan per kota (2020–2026, TERBARU)
CREATE TABLE IF NOT EXISTS mart_monthly_inflation (
    wilayah_nama  VARCHAR,
    year          INTEGER,
    month_num     INTEGER,
    month         VARCHAR,
    inflation_pct DOUBLE
);

-- Kota dengan inflasi terbaru tertinggi (tahun terakhir tersedia)
CREATE TABLE IF NOT EXISTS mart_city_latest (
    wilayah_nama        VARCHAR PRIMARY KEY,
    year                INTEGER,
    avg_inflation_pct   DOUBLE,
    max_inflation_pct   DOUBLE,
    n_bulan             INTEGER
);

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
