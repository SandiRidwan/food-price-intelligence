"""
transform.py — TRANSFORM LAYER: jalankan SQL marts & ekspor hasil.

Staging (DuckDB) → marts (DuckDB) → ekspor Parquet/CSV ke data/marts.
Semua logika analitik ada di sql/transform.sql (SQL murni, dapat diaudit).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duckdb

from config import DB_FILE, MARTS, SQL

MARTS_TABLES = [
    "mart_food_price_index",
    "mart_inflation",
    "mart_food_security",
    "mart_asean_ranking",
    "mart_food_inflation_monthly",
    "mart_food_inflation_city",
    "mart_food_inflation_national",
    "mart_rice_price",
    "mart_rice_wholesale",
    "mart_monthly_inflation",
    "mart_city_latest",
]


def main() -> None:
    con = duckdb.connect(str(DB_FILE))
    print("[transform] menjalankan sql/transform.sql")
    con.execute((SQL / "transform.sql").read_text(encoding="utf-8"))

    print("[transform] verifikasi marts:")
    for t in MARTS_TABLES:
        n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        print(f"   {t:24} {n:5} baris")
        # ekspor TERURUT agar fallback (baca Parquet) menghasilkan garis chart
        # yang benar tanpa perlu ORDER BY. Deteksi kolom urut yang tersedia.
        cols = [r[1] for r in con.execute(f"PRAGMA table_info('{t}')").fetchall()]
        order = [c for c in ("country_iso", "country", "wilayah_nama", "year",
                             "month_num") if c in cols]
        order_sql = f" ORDER BY {', '.join(order)}" if order else ""
        con.execute(f"""
            COPY (SELECT * FROM {t}{order_sql})
            TO '{(MARTS / (t + '.parquet')).as_posix()}' (FORMAT PARQUET)
        """)
        con.execute(f"""
            COPY (SELECT * FROM {t}{order_sql})
            TO '{(MARTS / (t + '.csv')).as_posix()}' (HEADER, DELIMITER ',')
        """)

    # sorotan: inflasi pangan Indonesia terbaru & anomali
    print("\n[transform] Indonesia — 5 tahun terakhir:")
    rows = con.execute("""
        SELECT year, ROUND(inflation_pct,2) AS inflasi,
               ROUND(food_prod_index,1) AS produksi,
               ROUND(food_import_pct,1) AS impor_pct
        FROM mart_food_security WHERE country_iso='IDN'
        ORDER BY year DESC LIMIT 5
    """).fetchall()
    print(f"   {'tahun':>5} {'inflasi%':>9} {'produksi':>9} {'impor%':>7}")
    for r in rows:
        print(f"   {r[0]:>5} {str(r[1]):>9} {str(r[2]):>9} {str(r[3]):>7}")

    print("\n[transform] anomali harga (flag spike):")
    spikes = con.execute("""
        SELECT country, year, ROUND(yoy_pct,1) FROM mart_food_price_index
        WHERE yoy_flag='spike' ORDER BY yoy_pct DESC LIMIT 8
    """).fetchall()
    for r in spikes:
        print(f"   {r[0]:12} {r[1]}  +{r[2]}%")
    con.close()


if __name__ == "__main__":
    main()
