"""
ingest.py — INGEST LAYER: tarik data mentah dari sumber publik → data/staging.

Prinsip:
  · Sumber publik, tanpa API key → siapa pun bisa reproduksi.
  · Idempoten: aman dijalankan berulang; menimpa staging dengan data terbaru.
  · Menyimpan metadata run (timestamp, sumber) untuk audit/lineage.
  · Tidak ada transformasi bisnis di sini — hanya pengambilan & normalisasi
    bentuk minimal (long format: country, year, indicator, value).

Output:
  data/staging/wb_indicators.parquet   — semua indikator, semua negara
  data/staging/fx_usd_idr.parquet      — kurs USD→IDR harian (Frankfurter)
  data/staging/_ingest_meta.json       — metadata run (lineage)
"""

from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

from config import (COUNTRIES, INDICATORS, RAW, STAGING, WB_BASE, YEAR_MIN)

UA = {"User-Agent": "food-price-intelligence/1.0 (portfolio; contact: local)",
      "Accept": "application/json"}


def _get_json(url: str, retries: int = 3) -> object:
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"gagal ambil {url}: {last}")


def fetch_worldbank() -> pd.DataFrame:
    """
    Ambil semua indikator untuk semua negara, flatten ke long format.
    World Bank mengembalikan [meta, rows].
    """
    rows = []
    for iso, name in COUNTRIES.items():
        for ind, meta in INDICATORS.items():
            url = (f"{WB_BASE}/country/{iso}/indicator/{ind}"
                   f"?format=json&per_page=1000")
            data = _get_json(url)
            if not isinstance(data, list) or len(data) < 2 or data[1] is None:
                print(f"  [wb] {iso}/{ind}: tidak ada data")
                continue
            n = 0
            for rec in data[1]:
                year = int(rec["date"])
                if year < YEAR_MIN:
                    continue
                rows.append({
                    "country_iso": iso,
                    "country": name,
                    "indicator_code": ind,
                    "indicator_name": meta["nama"],
                    "category": meta["kategori"],
                    "year": year,
                    "value": rec["value"],          # None = missing (dibiarkan)
                })
                n += 1
            print(f"  [wb] {iso}/{ind}: {n} baris")
    df = pd.DataFrame(rows)
    return df


def fetch_fx() -> pd.DataFrame:
    """
    Kurs USD→IDR dari Frankfurter (data ECB, publik). Ambil rentang sejak 2000.
    """
    start = f"{YEAR_MIN}-01-01"
    url = f"https://api.frankfurter.app/{start}..?from=USD&to=IDR"
    data = _get_json(url)
    rates = data.get("rates", {})
    rows = [{"date": d, "usd_idr": v.get("IDR")} for d, v in rates.items()]
    df = pd.DataFrame(rows).dropna()
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def main() -> None:
    t0 = time.time()
    print("[ingest] mulai")

    print("[ingest] World Bank...")
    wb = fetch_worldbank()
    if wb.empty:
        raise SystemExit("World Bank tidak mengembalikan data — periksa koneksi")
    # hanya nilai non-null untuk staging bersih; null tetap tercatat di meta
    wb_nonnull = wb.dropna(subset=["value"]).copy()
    wb.to_parquet(STAGING / "wb_indicators_raw.parquet", index=False)
    wb_nonnull.to_parquet(STAGING / "wb_indicators.parquet", index=False)
    print(f"  → {len(wb_nonnull)} nilai valid dari {len(wb)} baris")

    print("[ingest] kurs USD/IDR...")
    try:
        fx = fetch_fx()
        fx.to_parquet(STAGING / "fx_usd_idr.parquet", index=False)
        print(f"  → {len(fx)} hari kurs ({fx.date.min().date()}…{fx.date.max().date()})")
    except Exception as e:  # noqa: BLE001
        print(f"  ! kurs gagal ({e}) — dilewati, tidak fatal")
        fx = pd.DataFrame()

    meta = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "source_worldbank": WB_BASE,
        "source_fx": "https://api.frankfurter.app",
        "indicators": list(INDICATORS),
        "countries": dict(COUNTRIES),
        "rows_wb_valid": int(len(wb_nonnull)),
        "rows_fx": int(len(fx)),
        "duration_sec": round(time.time() - t0, 2),
    }
    (STAGING / "_ingest_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[ingest] selesai dalam {meta['duration_sec']}s")


if __name__ == "__main__":
    main()
