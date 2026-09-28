"""
test_data_quality.py — Uji kualitas data (data quality tests).

Menjalankan assertions atas DATABASE (bukan file) — memverifikasi integritas
staging & marts. Keluar dengan kode != 0 bila ada yang gagal (CI-friendly).

Uji dikelompokkan:
  · Keunikan (primary key tidak duplikat)
  · Kelengkapan (tidak ada null pada kolom wajib; missing dilaporkan)
  · Rentang (nilai dalam batas wajar)
  · Konsistensi (referensial & logika turunan, mis. YoY = (now-prev)/prev)
  · Kesegaran (data terbaru tidak lebih tua dari N tahun)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import duckdb

from config import DB_FILE

FAILS: list[str] = []
PASSES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        PASSES.append(name)
        print(f"  PASS  {name}")
    else:
        FAILS.append(f"{name} — {detail}")
        print(f"  FAIL  {name}  {detail}")


def main() -> int:
    con = duckdb.connect(str(DB_FILE), read_only=True)
    print("[dq] menjalankan uji kualitas data\n")

    # ---- 1. Keunikan ------------------------------------------------------
    n = con.execute("SELECT count(*) FROM stg_wb_indicators").fetchone()[0]
    u = con.execute("""SELECT count(*) FROM (SELECT DISTINCT country_iso,
                      indicator_code, year FROM stg_wb_indicators)""").fetchone()[0]
    check("stg_wb PK unik", n == u, f"{n} vs {u}")

    n = con.execute("SELECT count(*) FROM stg_fx").fetchone()[0]
    u = con.execute("SELECT count(DISTINCT date) FROM stg_fx").fetchone()[0]
    check("stg_fx date unik", n == u, f"{n} vs {u}")

    # ---- 2. Kelengkapan ---------------------------------------------------
    null_iso = con.execute(
        "SELECT count(*) FROM stg_wb_indicators WHERE country_iso IS NULL"
    ).fetchone()[0]
    check("country_iso tidak null", null_iso == 0, f"{null_iso} null")

    null_val = con.execute(
        "SELECT count(*) FROM stg_wb_indicators WHERE value IS NULL"
    ).fetchone()[0]
    check("staging tanpa nilai null", null_val == 0, f"{null_val} null (ingest harus drop null)")

    # semua marts punya kolom negara & tahun
    for t in ("mart_food_price_index", "mart_inflation",
              "mart_food_security", "mart_asean_ranking"):
        bad = con.execute(
            f"SELECT count(*) FROM {t} WHERE country_iso IS NULL OR year IS NULL"
        ).fetchone()[0]
        check(f"{t} key lengkap", bad == 0, f"{bad} baris cacat")

    # ---- 3. Rentang -------------------------------------------------------
    bad_year = con.execute("""
        SELECT count(*) FROM stg_wb_indicators WHERE year < 1900 OR year > 2100
    """).fetchone()[0]
    check("tahun dalam rentang wajar", bad_year == 0, f"{bad_year} aneh")

    neg_price = con.execute("""
        SELECT count(*) FROM mart_food_price_index WHERE price_index <= 0
    """).fetchone()[0]
    check("indeks harga > 0", neg_price == 0, f"{neg_price} non-positif")

    bad_pop = con.execute("""
        SELECT count(*) FROM mart_food_security
        WHERE pop_growth_pct IS NOT NULL AND pop_growth_pct > 10
    """).fetchone()[0]
    check("pertumbuhan populasi wajar (<10%)", bad_pop == 0, f"{bad_pop} ekstrem")

    # ---- 4. Konsistensi ---------------------------------------------------
    # YoY harus konsisten dengan (now-prev)/prev
    bad_yoy = con.execute("""
        WITH chk AS (
            SELECT year, price_index,
                   LAG(price_index) OVER (PARTITION BY country_iso ORDER BY year) prev,
                   yoy_pct
            FROM mart_food_price_index
        )
        SELECT count(*) FROM chk
        WHERE prev IS NOT NULL AND prev <> 0
          AND abs(yoy_pct - round((price_index-prev)/prev*100, 2)) > 0.01
    """).fetchone()[0]
    check("YoY konsisten dgn rumus", bad_yoy == 0, f"{bad_yoy} inkonsisten")

    # setiap negara di ranking harus ada di food_security
    orphan = con.execute("""
        SELECT count(*) FROM mart_asean_ranking r
        LEFT JOIN mart_food_security f
          ON r.country_iso = f.country_iso AND r.year = f.year
        WHERE f.country_iso IS NULL
    """).fetchone()[0]
    check("ranking referensial ke security", orphan == 0, f"{orphan} orphan")

    # flag spike harus benar (yoy >= 7 iff flag='spike')
    bad_flag = con.execute("""
        SELECT count(*) FROM mart_food_price_index
        WHERE yoy_pct IS NOT NULL
          AND ((yoy_pct >= 7 AND yoy_flag <> 'spike')
               OR (yoy_pct < 7 AND yoy_flag = 'spike'))
    """).fetchone()[0]
    check("flag spike konsisten", bad_flag == 0, f"{bad_flag} salah flag")

    # ---- 5. Kesegaran -----------------------------------------------------
    maxy = con.execute("SELECT max(year) FROM mart_inflation").fetchone()[0]
    check("data segar (<= 2 tahun)", maxy is not None and maxy >= 2024,
          f"tahun max = {maxy}")

    # ---- 6. Cakupan -------------------------------------------------------
    n_country = con.execute(
        "SELECT count(DISTINCT country_iso) FROM mart_food_security"
    ).fetchone()[0]
    check("cakupan 5 negara ASEAN", n_country == 5, f"{n_country} negara")

    con.close()

    print(f"\n[dq] {len(PASSES)} lulus, {len(FAILS)} gagal")
    if FAILS:
        print("\nGAGAL:")
        for f in FAILS:
            print("  -", f)
        return 1
    print("[dq] SEMUA UJI LULUS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
