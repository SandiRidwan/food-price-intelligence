"""
config.py — satu sumber kebenaran: path, sumber data, konstanta.

Project: Indonesia Food Price & Security Intelligence
Sumber (semua publik/resmi):
  · World Bank Open Data  — indikator ketahanan pangan (tahunan, tanpa key)
  · BPS WebAPI            — inflasi PANGAN bulanan per kota + harga beras (key)
  · Frankfurter           — kurs USD/IDR (tanpa key)
"""

from __future__ import annotations

import os
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


# ---- Kredensial (dari .env, JANGAN hardcode) -------------------------------
def _load_env() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


_load_env()
BPS_API_KEY = os.environ.get("BPS_API_KEY", "")
BPS_BASE = "https://webapi.bps.go.id/v1/api"

# Variabel BPS yang ditarik (temuan verifikasi):
#   1890 = Inflasi kelompok Makanan, Minuman & Tembakau per KOTA (bulanan)
#   295  = Harga BERAS grosir (perdagangan besar) — TERBARU s/d 2026
#   1    = Inflasi bulanan umum (M-to-M) per kota — s/d 2026
#   79   = Harga eceran beras 33 kota (historis, 2000–2016)
BPS_VARS = {
    "food_inflation_city": 1890,   # inflasi pangan bulanan per kota (2020-2023)
    "monthly_inflation": 1,        # inflasi bulanan per kota (2020-2026)
    "rice_wholesale": 295,         # harga beras grosir (2020-2026, TERBARU)
    "rice_price": 79,              # harga beras eceran (2000-2016, historis)
}
# Tahun BPS (kode th → label) untuk masing-masing var.
BPS_YEARS_FOOD = {120: 2020, 121: 2021, 122: 2022, 123: 2023}
BPS_YEARS_INFL = {120: 2020, 121: 2021, 122: 2022, 123: 2023,
                  124: 2024, 125: 2025, 126: 2026}
BPS_YEARS_RICE_WHOLESALE = {120: 2020, 121: 2021, 122: 2022, 123: 2023,
                            124: 2024, 125: 2025, 126: 2026}
BPS_YEARS_RICE = {100: 2000, 105: 2005, 110: 2010, 115: 2015, 116: 2016}

# Nama bulan BPS (turtahun) → nomor bulan
BPS_MONTHS = {
    "1": "Januari", "2": "Februari", "3": "Maret", "4": "April",
    "5": "Mei", "6": "Juni", "7": "Juli", "8": "Agustus",
    "9": "September", "10": "Oktober", "11": "November", "12": "Desember",
    "13": "Tahunan",
}

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

# ---- Palet warna (konsisten antara chart & dashboard) ----------------------
COLORS = {
    "primary": "#1F5C3D",   # hijau — aman/positif
    "accent": "#E4A11B",    # kuning — perhatian
    "dark": "#1B2A33",      # teks
    "grey": "#8B9AA6",      # abu
    "red": "#C0392B",       # merah — alert/negatif
    "blue": "#2E6F95",      # biru — sekunder
    "purple": "#6A4C93",    # ungu — aksen
}
SERIES = ["#1F5C3D", "#2E6F95", "#E4A11B", "#C0392B", "#6A4C93",
          "#2A9D8F", "#E76F51", "#264653"]
