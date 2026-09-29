"""
load_db.py — muat staging (Parquet) ke database DuckDB.

Lapisan DB: schema → staging tables. Idempoten (DROP+CREATE staging dulu).
Jalankan setelah ingest, sebelum transform.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duckdb

from config import DB_FILE, SQL, STAGING


def main() -> None:
    con = duckdb.connect(str(DB_FILE))
    print(f"[load] database → {DB_FILE}")

    # 1. schema
    con.execute((SQL / "schema.sql").read_text(encoding="utf-8"))

    # 2. staging: replace
    wb = STAGING / "wb_indicators.parquet"
    fx = STAGING / "fx_usd_idr.parquet"
    if not wb.exists():
        raise SystemExit("staging wb tidak ada — jalankan ingest.py dulu")

    con.execute("DELETE FROM stg_wb_indicators")
    con.execute(f"""
        INSERT INTO stg_wb_indicators
        SELECT country_iso, country, indicator_code, indicator_name,
               category, year, value
        FROM read_parquet('{wb.as_posix()}')
    """)
    n_wb = con.execute("SELECT count(*) FROM stg_wb_indicators").fetchone()[0]

    n_fx = 0
    if fx.exists():
        con.execute("DELETE FROM stg_fx")
        con.execute(f"""
            INSERT INTO stg_fx SELECT date, usd_idr
            FROM read_parquet('{fx.as_posix()}')
        """)
        n_fx = con.execute("SELECT count(*) FROM stg_fx").fetchone()[0]

    # BPS: inflasi pangan bulanan + harga beras (opsional, ada bila key diset)
    food = STAGING / "bps_food_inflation.parquet"
    rice = STAGING / "bps_rice_price.parquet"
    infl = STAGING / "bps_monthly_inflation.parquet"
    rw = STAGING / "bps_rice_wholesale.parquet"
    n_food = n_rice = n_infl = n_rw = 0
    if food.exists():
        con.execute("DELETE FROM stg_bps_food_inflation")
        con.execute(f"""
            INSERT INTO stg_bps_food_inflation
            SELECT wilayah_kode, wilayah_nama, year, periode, turvar_label, value
            FROM read_parquet('{food.as_posix()}')
        """)
        n_food = con.execute("SELECT count(*) FROM stg_bps_food_inflation").fetchone()[0]
    if rice.exists():
        con.execute("DELETE FROM stg_bps_rice_price")
        con.execute(f"""
            INSERT INTO stg_bps_rice_price
            SELECT wilayah_kode, wilayah_nama, year, value
            FROM read_parquet('{rice.as_posix()}')
        """)
        n_rice = con.execute("SELECT count(*) FROM stg_bps_rice_price").fetchone()[0]
    if infl.exists():
        con.execute("DELETE FROM stg_bps_monthly_inflation")
        con.execute(f"""
            INSERT INTO stg_bps_monthly_inflation
            SELECT wilayah_kode, wilayah_nama, year, turtahun, periode, value
            FROM read_parquet('{infl.as_posix()}')
        """)
        n_infl = con.execute("SELECT count(*) FROM stg_bps_monthly_inflation").fetchone()[0]
    if rw.exists():
        con.execute("DELETE FROM stg_bps_rice_wholesale")
        con.execute(f"""
            INSERT INTO stg_bps_rice_wholesale
            SELECT year, periode, turtahun, value
            FROM read_parquet('{rw.as_posix()}')
        """)
        n_rw = con.execute("SELECT count(*) FROM stg_bps_rice_wholesale").fetchone()[0]

    print(f"[load] stg_wb_indicators: {n_wb} baris")
    print(f"[load] stg_fx           : {n_fx} baris")
    if n_food or n_rice or n_infl or n_rw:
        print(f"[load] stg_bps_food_inflation : {n_food} baris")
        print(f"[load] stg_bps_rice_price     : {n_rice} baris")
        print(f"[load] stg_bps_monthly_infl   : {n_infl} baris")
        print(f"[load] stg_bps_rice_wholesale : {n_rw} baris")

    # ringkasan
    rows = con.execute("""
        SELECT country, count(DISTINCT indicator_code) AS ind,
               min(year) AS y0, max(year) AS y1
        FROM stg_wb_indicators GROUP BY country ORDER BY country
    """).fetchall()
    print("[load] cakupan:")
    for r in rows:
        print(f"   {r[0]:12} {r[1]} indikator  {r[2]}–{r[3]}")
    con.close()


if __name__ == "__main__":
    main()
