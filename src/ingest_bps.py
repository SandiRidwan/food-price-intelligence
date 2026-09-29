"""
ingest_bps.py — INGEST BPS: inflasi PANGAN bulanan per kota + harga beras.

Temuan verifikasi (lihat docs/ADR.md):
  · var 1890 = inflasi kelompok Makanan, Minuman & Tembakau per KOTA,
    BULANAN (Jan–Des + Tahunan), 91 kota, tahun 2020–2023.
  · var 79   = harga eceran BERAS di pasar tradisional, 33 kota, 2000–2016.
  · var 1    = inflasi bulanan umum (M-to-M).

Kunci datacontent BPS bersifat gabungan (vervar+turvar+var+turtahun+th) —
panjang bervariasi. Kita memakai order kolom dari metadata respons untuk
mendekode: vervar, turvar, var, turtahun, th. Karena panjang kunci tidak
selalu tetap, pendekatan paling aman: gunakan posisi vervar (prefix) yang
diketahui dari daftar `vervar`, lalu posisi turtahun dari `turtahun`.

Output: data/staging/bps_food_inflation.parquet  (bulanan, per kota)
        data/staging/bps_rice_price.parquet      (tahunan, per kota)
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

from config import (BPS_API_KEY, BPS_BASE, BPS_VARS, BPS_YEARS_FOOD,
                    BPS_YEARS_INFL, BPS_YEARS_RICE,
                    BPS_YEARS_RICE_WHOLESALE, STAGING)

H = {"User-Agent": "food-price-intelligence/1.0", "Accept": "application/json"}


def _get(path: str, retries: int = 3):
    for i in range(retries):
        try:
            req = urllib.request.Request(BPS_BASE + path, headers=H)
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read())
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(1.5 * (i + 1))
    return None


def _decode(datacontent: dict, vervar: dict, turvar: dict,
            turtahun: dict, var_id: int, th: int) -> list[dict]:
    """
    Dekode datacontent BPS. Bentuk kunci (temuan verifikasi, 100% cocok):
        <vervar> + <var> + <turvar> + <th(3)> + <turtahun>
    Panjang vervar & var bervariasi (mis. var 295 → vervar='1' 1 digit;
    var 1 → var='1' 1 digit). Kita dekode dengan mencocokkan komponen
    terhadap daftar nilai VALID dari metadata (bukan asumsi panjang tetap),
    lalu sisa = th(3) + turtahun.
    """
    vkeys = sorted(vervar, key=len, reverse=True)
    tkeys = sorted(turvar, key=len, reverse=True)
    vid = str(var_id)
    rows = []
    for key, val in datacontent.items():
        vk = next((v for v in vkeys if key.startswith(v)), None)
        if vk is None:
            continue
        rest = key[len(vk):]
        if not rest.startswith(vid):
            continue
        rest = rest[len(vid):]
        tk = next((t for t in tkeys if rest.startswith(t)), None)
        if tk:
            rest = rest[len(tk):]
        th_code = rest[:3]
        tt = rest[3:] or None
        rows.append({
            "var_id": var_id, "th": th, "vervar": vk, "turvar": tk,
            "turtahun": tt, "value": val,
        })
    return rows


def fetch_var(var_id: int, years: dict[int, int]) -> pd.DataFrame:
    rows = []
    for th, year in years.items():
        try:
            j = _get(f"/list/model/data/domain/0000/var/{var_id}/th/{th}/"
                     f"key/{BPS_API_KEY}/")
        except Exception as e:  # noqa: BLE001
            print(f"  ! var{var_id} th{th}: {str(e)[:60]}")
            continue
        dc = j.get("datacontent") or {}
        if not dc:
            continue
        vervar = {str(x["val"]): x["label"] for x in j.get("vervar", [])}
        turvar = {str(x["val"]): x["label"] for x in j.get("turvar", [])}
        turtahun = {str(x["val"]): x["label"] for x in j.get("turtahun", [])}
        decoded = _decode(dc, vervar, turvar, turtahun, var_id, th)
        for r in decoded:
            r["year"] = year
            r["wilayah_kode"] = r.pop("vervar")
            r["wilayah_nama"] = vervar.get(r["wilayah_kode"])
            r["turvar_label"] = turvar.get(str(r["turvar"]))
            r["periode"] = turtahun.get(str(r["turtahun"]), "Tahunan")
        rows += decoded
        print(f"  var{var_id} th{th} ({year}): {len(decoded)} nilai")
    return pd.DataFrame(rows)


def main() -> None:
    t0 = time.time()
    if not BPS_API_KEY:
        raise SystemExit("BPS_API_KEY kosong — isi .env")

    print("[bps] inflasi PANGAN per kota (bulanan, 2020–2023)...")
    food = fetch_var(BPS_VARS["food_inflation_city"], BPS_YEARS_FOOD)
    if not food.empty:
        food.to_parquet(STAGING / "bps_food_inflation.parquet", index=False)
        print(f"  → {len(food)} baris, {food['wilayah_nama'].nunique()} kota")

    print("[bps] inflasi BULANAN per kota (2020–2026, TERBARU)...")
    infl = fetch_var(BPS_VARS["monthly_inflation"], BPS_YEARS_INFL)
    if not infl.empty:
        infl.to_parquet(STAGING / "bps_monthly_inflation.parquet", index=False)
        print(f"  → {len(infl)} baris, {infl['wilayah_nama'].nunique()} kota")

    print("[bps] harga BERAS grosir (2020–2026, TERBARU)...")
    rw = fetch_var(BPS_VARS["rice_wholesale"], BPS_YEARS_RICE_WHOLESALE)
    if not rw.empty:
        rw.to_parquet(STAGING / "bps_rice_wholesale.parquet", index=False)
        print(f"  → {len(rw)} baris")

    print("[bps] harga BERAS eceran historis (2000–2016)...")
    rice = fetch_var(BPS_VARS["rice_price"], BPS_YEARS_RICE)
    if not rice.empty:
        rice.to_parquet(STAGING / "bps_rice_price.parquet", index=False)
        print(f"  → {len(rice)} baris")

    meta = {
        "rows_food": int(len(food)),
        "rows_monthly_infl": int(len(infl)),
        "rows_rice_wholesale": int(len(rw)),
        "rows_rice_historical": int(len(rice)),
        "latest_year": max(BPS_YEARS_INFL.values()),
        "duration_sec": round(time.time() - t0, 1),
    }
    (STAGING / "_bps_food_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[bps] selesai dalam {meta['duration_sec']}s — "
          f"data terbaru s/d {meta['latest_year']}")


if __name__ == "__main__":
    main()
