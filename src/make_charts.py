"""
make_charts.py — hasilkan chart PNG statis untuk README (dari marts).

Membaca DuckDB (marts) → matplotlib → reports/figures/*.png.
Tidak butuh Streamlit; deterministik.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from config import COLORS as C, DB_FILE, FIGURES

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.bbox": "tight",
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})

CTRY = {"Indonesia": C["red"], "Malaysia": C["primary"],
        "Thailand": C["accent"], "Vietnam": C["blue"],
        "Philippines": C["purple"]}


def q(sql: str) -> pd.DataFrame:
    con = duckdb.connect(str(DB_FILE), read_only=True)
    df = con.execute(sql).df()
    con.close()
    return df


def chart_price_trend() -> None:
    df = q("""SELECT country, year, price_index FROM mart_food_price_index
              ORDER BY country, year""")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for c, g in df.groupby("country"):
        ax.plot(g["year"], g["price_index"], marker="o", ms=3,
                label=c, color=CTRY.get(c, "#888"), lw=1.8)
    ax.set_title("Indeks Harga Pangan ASEAN (2010 = 100)", fontweight="bold")
    ax.set_xlabel("Tahun"); ax.set_ylabel("Indeks")
    ax.legend(fontsize=8, ncol=2)
    fig.savefig(FIGURES / "01_price_index.png")
    plt.close(fig)
    print("  ✓ 01_price_index.png")


def chart_inflation() -> None:
    df = q("""SELECT country, year, inflation_pct FROM mart_inflation
              ORDER BY country, year""")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for c, g in df.groupby("country"):
        ax.plot(g["year"], g["inflation_pct"], marker="o", ms=3,
                label=c, color=CTRY.get(c, "#888"), lw=1.8)
    ax.axhline(5.0, ls="--", color=C["red"], lw=1.2,
               label="ambang alert 5%")
    ax.set_title("Inflasi Harga Konsumen Tahunan (%)", fontweight="bold")
    ax.set_xlabel("Tahun"); ax.set_ylabel("Persen (%)")
    ax.legend(fontsize=8, ncol=2)
    fig.savefig(FIGURES / "02_inflation.png")
    plt.close(fig)
    print("  ✓ 02_inflation.png")


def chart_ranking() -> None:
    y = q("SELECT max(year) y FROM mart_asean_ranking").iloc[0]["y"]
    df = q(f"""SELECT country, inflation_pct, rank_inflation
               FROM mart_asean_ranking WHERE year={int(y)}
               ORDER BY rank_inflation""")
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(df["country"], df["inflation_pct"],
                   color=[CTRY.get(c, "#888") for c in df["country"]])
    ax.invert_yaxis()
    for b, v in zip(bars, df["inflation_pct"]):
        ax.text(v + 0.05, b.get_y() + b.get_height() / 2,
                f"{v:.2f}%", va="center", fontsize=9)
    ax.axvline(0, color="#888", lw=0.8)
    ax.set_title(f"Peringkat Inflasi Pangan ASEAN {int(y)} "
                 f"(1 = terbaik)", fontweight="bold")
    ax.set_xlabel("Inflasi (%)")
    fig.savefig(FIGURES / "03_asean_ranking.png")
    plt.close(fig)
    print("  ✓ 03_asean_ranking.png")


def chart_security() -> None:
    df = q("""SELECT country, year, food_prod_index, food_import_pct
              FROM mart_food_security WHERE year >= 2010
              ORDER BY country, year""")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    for c, g in df.groupby("country"):
        a1.plot(g["year"], g["food_prod_index"], marker="o", ms=2.5,
                label=c, color=CTRY.get(c, "#888"), lw=1.6)
        a2.plot(g["year"], g["food_import_pct"], marker="o", ms=2.5,
                label=c, color=CTRY.get(c, "#888"), lw=1.6)
    a1.set_title("Indeks Produksi Pangan", fontweight="bold")
    a1.set_xlabel("Tahun"); a1.set_ylabel("2014-2016 = 100")
    a2.set_title("Impor Pangan (% total impor)", fontweight="bold")
    a2.set_xlabel("Tahun"); a2.set_ylabel("%")
    a1.legend(fontsize=7)
    fig.savefig(FIGURES / "04_food_security.png")
    plt.close(fig)
    print("  ✓ 04_food_security.png")


def chart_spikes() -> None:
    df = q("""SELECT country, year, yoy_pct FROM mart_food_price_index
              WHERE yoy_flag='spike' ORDER BY yoy_pct DESC LIMIT 10""")
    if df.empty:
        print("  (tidak ada spike)"); return
    fig, ax = plt.subplots(figsize=(9, 4))
    lbl = [f"{r.country} {r.year}" for r in df.itertuples()]
    ax.barh(lbl[::-1], df["yoy_pct"][::-1],
            color=[CTRY.get(c, "#888") for c in df["country"][::-1]])
    for i, v in enumerate(df["yoy_pct"][::-1]):
        ax.text(v + 0.2, i, f"+{v:.1f}%", va="center", fontsize=8)
    ax.set_title("Lonjakan Harga Pangan Terbesar (YoY ≥ 7%)",
                 fontweight="bold")
    ax.set_xlabel("Kenaikan YoY (%)")
    fig.savefig(FIGURES / "05_spikes.png")
    plt.close(fig)
    print("  ✓ 05_spikes.png")


def chart_rank_evolution() -> None:
    df = q("""SELECT year, country, rank_inflation FROM mart_asean_ranking
              ORDER BY year""")
    piv = df.pivot(index="country", columns="year",
                   values="rank_inflation")
    fig, ax = plt.subplots(figsize=(11, 3.6))
    im = ax.imshow(piv.values, aspect="auto", cmap="RdYlGn_r")
    ax.set_yticks(range(len(piv.index)))
    ax.set_yticklabels(piv.index, fontsize=8)
    steps = max(1, len(piv.columns) // 12)
    ax.set_xticks(range(0, len(piv.columns), steps))
    ax.set_xticklabels([str(c) for c in piv.columns[::steps]],
                       rotation=45, fontsize=8)
    for i in range(len(piv.index)):
        for j in range(len(piv.columns)):
            v = piv.values[i, j]
            if pd.notna(v):
                ax.text(j, i, int(v), ha="center", va="center", fontsize=6.5)
    fig.colorbar(im, label="peringkat", shrink=0.8)
    ax.set_title("Evolusi Peringkat Inflasi per Tahun (1 = terbaik)",
                 fontweight="bold")
    fig.savefig(FIGURES / "06_rank_evolution.png")
    plt.close(fig)
    print("  ✓ 06_rank_evolution.png")


def main() -> None:
    if not DB_FILE.exists():
        raise SystemExit("DB belum ada — jalankan: python src/run_pipeline.py")
    print("[charts] menghasilkan PNG untuk README:")
    chart_price_trend()
    chart_inflation()
    chart_ranking()
    chart_security()
    chart_spikes()
    chart_rank_evolution()
    print(f"[charts] selesai → {FIGURES}")


if __name__ == "__main__":
    main()
