"""
decide_actions.py — decision engine untuk ketahanan pangan.

Mengubah indikator pangan menjadi SKOR PRIORITAS INTERVENSI per negara,
berbasis 3 sinyal terukur:
  · inflation_pressure — tingkat inflasi pangan (dinormalisasi)
  · import_dependence  — ketergantungan impor (kerentanan)
  · food_stress        — kebalikan indeks produksi (semakin rendah produksi,
                          semakin tinggi stres)
Bobot: 0.4 / 0.3 / 0.3. Tier: intervensi_segera (>=0.6) · pantau_ketat (>=0.35)
· normal (<0.35).
Output: marts/mart_decisions.parquet
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duckdb
import pandas as pd

from config import DB_FILE, MARTS
from decision import decide, normalize, score_signals, tier_of

WEIGHTS = {"inflation_pressure": 0.4, "import_dependence": 0.3, "food_stress": 0.3}
THRESHOLDS = {"intervensi_segera": 0.60, "pantau_ketat": 0.35}
OUT = "mart_decisions"


def main() -> None:
    con = duckdb.connect(str(DB_FILE))
    # ambil nilai terbaru per negara
    df = con.execute("""
        SELECT country_iso, country, year,
               inflation_pct, food_import_pct, food_prod_index
        FROM mart_food_security
        WHERE year = (SELECT max(year) FROM mart_food_security)
    """).df()

    if df.empty:
        print("[decision] data kosong")
        con.close()
        return

    # normalisasi sinyal lintas-negara
    inf_lo, inf_hi = df.inflation_pct.min(), df.inflation_pct.max()
    imp_lo, imp_hi = df.food_import_pct.min(), df.food_import_pct.max()
    prod_lo, prod_hi = df.food_prod_index.min(), df.food_prod_index.max()

    payload = []
    for _, r in df.iterrows():
        prod = r.food_prod_index
        # Sinyal yang datanya HILANG dinetralkan (0.5) + ditandai, bukan
        # dianggap 0 — mencegah keputusan tinggi dari data kosong.
        miss = []
        if pd.isna(r.inflation_pct):
            inf_sig, miss = 0.5, miss + ["inflasi"]
        else:
            inf_sig = normalize(r.inflation_pct, inf_lo, inf_hi)
        if pd.isna(r.food_import_pct):
            imp_sig, miss = 0.5, miss + ["impor"]
        else:
            imp_sig = normalize(r.food_import_pct, imp_lo, imp_hi)
        if pd.isna(prod):
            str_sig, miss = 0.5, miss + ["produksi"]
        else:
            str_sig = 1 - normalize(prod, prod_lo, prod_hi)
        payload.append({
            "id": r.country,
            "source": r.country_iso,
            "signals": {
                "inflation_pressure": inf_sig,
                "import_dependence": imp_sig,
                "food_stress": str_sig,
            },
            "weights": WEIGHTS,
            "thresholds": THRESHOLDS,
            "inflation_pct": r.inflation_pct,
            "food_import_pct": r.food_import_pct,
            "food_prod_index": prod,
            "year": int(r.year),
            "data_hilang": ",".join(miss) if miss else "",
        })

    dec = decide(payload)
    con.execute(f"DROP TABLE IF EXISTS {OUT}")
    con.execute(f"CREATE TABLE {OUT} AS SELECT * FROM dec")
    n = con.execute(f"SELECT count(*) FROM {OUT}").fetchone()[0]
    con.execute(f"""COPY {OUT} TO '{(MARTS / (OUT + '.parquet')).as_posix()}'
        (FORMAT PARQUET)""")
    con.close()

    print(f"[decision] {n} negara diberi skor prioritas intervensi ({int(df.year.iloc[0])}):")
    for _, r in dec.iterrows():
        print(f"   [{r['tier']:18}] skor={r['skor']:.2f}  {r['id']:12} "
              f"inflasi={r['inflation_pct']:.2f}%  impor={r['food_import_pct']:.1f}%")
        print(f"      {r['justifikasi']}")


if __name__ == "__main__":
    main()
