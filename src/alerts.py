"""
alerts.py — deteksi lonjakan harga/inflasi pangan & hasilkan laporan alert.

Aturan (deterministik, dari config):
  · Inflasi pangan tahunan >= ALERT_INFLATION_PCT (default 5%) → alert
  · YoY indeks harga >= ALERT_YOY_PCT (default 7%) → alert 'spike'
  · Kenaikan YoY dibanding tahun sebelumnya (akselerasi) → 'accelerating'

Output:
  reports/alerts.json      — daftar alert terstruktur (machine-readable)
  reports/alerts.md        — ringkasan manusiawi (untuk PR / notifikasi)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duckdb

from config import ALERT_INFLATION_PCT, ALERT_YOY_PCT, DB_FILE, REPORTS


def build_alerts(con: duckdb.DuckDBPyConnection) -> list[dict]:
    alerts = []

    # 1. inflasi tinggi (tahun terbaru yang tersedia per negara)
    rows = con.execute("""
        WITH latest AS (
            SELECT country_iso, country, year, inflation_pct,
                   ROW_NUMBER() OVER (PARTITION BY country_iso
                                      ORDER BY year DESC) AS rn
            FROM mart_inflation WHERE inflation_pct IS NOT NULL
        )
        SELECT country, year, inflation_pct FROM latest
        WHERE rn = 1 AND inflation_pct >= ?
        ORDER BY inflation_pct DESC
    """, [ALERT_INFLATION_PCT]).fetchall()
    for c, y, v in rows:
        alerts.append({"jenis": "inflasi_tinggi", "severity": "high"
                       if v >= 10 else "medium",
                       "country": c, "year": y, "value": round(v, 2),
                       "pesan": f"{c} {y}: inflasi pangan {v:.2f}% "
                                f"≥ ambang {ALERT_INFLATION_PCT}%"})

    # 2. spike YoY pada 3 tahun terakhir
    rows = con.execute("""
        SELECT country, year, yoy_pct FROM mart_food_price_index
        WHERE yoy_flag = 'spike' AND year >= 2022
        ORDER BY yoy_pct DESC
    """).fetchall()
    for c, y, v in rows:
        alerts.append({"jenis": "lonjakan_harga", "severity": "high",
                       "country": c, "year": y, "value": round(v, 2),
                       "pesan": f"{c} {y}: indeks harga naik {v:.1f}% YoY "
                                f"≥ ambang {ALERT_YOY_PCT}%"})

    # 3. akselerasi inflasi (naik dibanding tahun sebelumnya)
    rows = con.execute("""
        WITH s AS (
            SELECT country, year, inflation_pct,
                   LAG(inflation_pct) OVER (PARTITION BY country_iso
                                            ORDER BY year) prev
            FROM mart_inflation WHERE inflation_pct IS NOT NULL
        )
        SELECT country, year, inflation_pct, prev FROM s
        WHERE prev IS NOT NULL AND inflation_pct - prev >= 2
          AND year >= 2022
        ORDER BY (inflation_pct - prev) DESC
    """).fetchall()
    for c, y, v, p in rows:
        alerts.append({"jenis": "akselerasi", "severity": "medium",
                       "country": c, "year": y, "value": round(v, 2),
                       "pesan": f"{c} {y}: inflasi naik {v-p:.1f} poin "
                                f"({p:.1f}% → {v:.1f}%)"})

    return alerts


def main() -> None:
    con = duckdb.connect(str(DB_FILE), read_only=True)
    alerts = build_alerts(con)
    con.close()

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "thresholds": {"inflation_pct": ALERT_INFLATION_PCT,
                       "yoy_pct": ALERT_YOY_PCT},
        "count": len(alerts),
        "alerts": alerts,
    }
    (REPORTS / "alerts.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [f"# Food Price Alerts — {datetime.now(timezone.utc):%Y-%m-%d}",
             "",
             f"Ambang: inflasi ≥ {ALERT_INFLATION_PCT}%, "
             f"YoY ≥ {ALERT_YOY_PCT}%. Total: **{len(alerts)}** alert.", ""]
    if alerts:
        lines.append("| Severity | Negara | Tahun | Nilai | Pesan |")
        lines.append("|---|---|---|---|---|")
        for a in sorted(alerts, key=lambda x: (x["severity"] != "high",
                                                -x["value"])):
            lines.append(f"| {a['severity']} | {a['country']} | {a['year']} | "
                         f"{a['value']} | {a['pesan']} |")
    else:
        lines.append("_Tidak ada alert — semua indikator dalam ambang wajar._")
    (REPORTS / "alerts.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"[alerts] {len(alerts)} alert → reports/alerts.json, alerts.md")
    for a in alerts:
        print(f"   [{a['severity']:6}] {a['pesan']}")


if __name__ == "__main__":
    main()
