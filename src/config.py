"""
config.py — satu sumber kebenaran: path, sumber data, konstanta.

Project: Indonesia Food Price & Security Intelligence
Sumber: World Bank Open Data (publik, tanpa API key) + kurs (Frankfurter).
"""

from __future__ import annotations

from pathlib import Path

# ---- Path -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
STAGING = DATA / "staging"
MARTS = DATA / "marts"
DB = ROOT / "db"
SQL = ROOT / "sql"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

for _p in (RAW, STAGING, MARTS, DB, REPORTS, FIGURES):
    _p.mkdir(parents=True, exist_ok=True)

DB_FILE = DB / "food.duckdb"

# ---- Sumber data (semua publik, tanpa API key) -----------------------------
WB_BASE = "https://api.worldbank.org/v2"

# Indikator World Bank untuk analisis ketahanan pangan.
# Setiap entri: kode indikator → metadata.
INDICATORS = {
    "FP.CPI.TOTL": {
        "nama": "Consumer price index (2010=100)",
        "kategori": "Harga",
    },
    "FP.CPI.TOTL.ZG": {
        "nama": "Inflation, consumer prices (annual %)",
        "kategori": "Harga",
    },
    "AG.PRD.FOOD.XD": {
        "nama": "Food production index (2014-2016=100)",
        "kategori": "Produksi",
    },
    "TM.VAL.FOOD.ZS.UN": {
        "nama": "Food imports (% of merchandise imports)",
        "kategori": "Perdagangan",
    },
    "AG.CON.FERT.ZS": {
        "nama": "Fertilizer consumption (kg per ha arable land)",
        "kategori": "Input",
    },
    "SP.POP.GROW": {
        "nama": "Population growth (annual %)",
        "kategori": "Demografi",
    },
}

# Negara pembanding (Indonesia + ASEAN utama)
COUNTRIES = {
    "IDN": "Indonesia",
    "MYS": "Malaysia",
    "THA": "Thailand",
    "VNM": "Vietnam",
    "PHL": "Philippines",
}

# Rentang tahun (World Bank kadang punya data mundur jauh)
YEAR_MIN = 2000

# ---- Ambang alert ----------------------------------------------------------
# Inflasi pangan tahunan (%) yang dianggap "lonjakan" & butuh perhatian.
ALERT_INFLATION_PCT = 5.0
# Perubahan YoY indeks harga yang dianggap anomali (%).
ALERT_YOY_PCT = 7.0
