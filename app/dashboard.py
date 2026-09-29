"""
dashboard.py — Streamlit dashboard untuk Food Price & Security Intelligence.

Menampilkan: KPI, tren indeks harga, peta ketahanan, peringkat ASEAN, alert.
Data dibaca langsung dari DuckDB (marts).

Jalankan: streamlit run app/dashboard.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from config import COLORS as C, DB_FILE, MARTS, REPORTS  # noqa: E402
import explanations as X  # noqa: E402

st.set_page_config(page_title="Food Price & Security Intelligence",
                   page_icon="🌾", layout="wide")

CTRY_COLOR = {"Indonesia": "#C0392B", "Malaysia": "#1F5C3D",
              "Thailand": "#E4A11B", "Vietnam": "#2E6F95",
              "Philippines": "#6A4C93"}


def _ensure_data() -> None:
    """
    Bootstrap HANYA bila tak ada DB maupun marts. Di cloud, marts Parquet
    (yg di-commit) sudah ada → tak perlu pipeline/kredensial.
    """
    if _SRC != "none":
        return
    try:
        with st.spinner("Membangun database dari sumber (~60–90s)..."):
            r = subprocess.run(
                [sys.executable, str(ROOT / "src" / "run_pipeline.py")],
                cwd=str(ROOT), capture_output=True, text=True)
        if r.returncode != 0:
            st.error("Bootstrap gagal. Lihat `reports/_bootstrap.log`. "
                     "Jika di cloud: set `BPS_API_KEY` di Streamlit Secrets, "
                     "atau (disarankan) gunakan marts Parquet yang di-commit.")
    except Exception as e:  # noqa: BLE001
        st.error(f"Bootstrap error: {e}")


def _data_source() -> str:
    """
    Sumber data berprioritas:
      · 'db'    → DuckDB lokal (hasil pipeline)
      · 'marts' → Parquet marts di-commit (cloud tanpa kredensial/DB)
      · 'none'  → belum ada; jalankan pipeline
    """
    if DB_FILE.exists():
        return "db"
    if (MARTS / "mart_food_security.parquet").exists():
        return "marts"
    return "none"


_SRC = _data_source()
_ensure_data()


@st.cache_data(show_spinner="Membaca data...")
def q(sql: str) -> pd.DataFrame:
    """
    Jalankan query. DB ada → DuckDB. Tidak → baca Parquet marts langsung
    (fallback cloud tanpa kredensial). Query dipetakan ke tabel via nama
    'FROM <tabel>' agar transparan.
    """
    if _SRC == "db":
        con = duckdb.connect(str(DB_FILE), read_only=True)
        df = con.execute(sql).df()
        con.close()
        return df
    # fallback: kenali tabel dari klausa FROM
    import re
    m = re.search(r"\bFROM\s+(\w+)", sql, re.IGNORECASE)
    if m:
        p = MARTS / f"{m.group(1)}.parquet"
        if p.exists():
            return pd.read_parquet(p)
    return pd.DataFrame()


def style(fig, h=430):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=54, b=10),
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#D5DBE1"),
                      title=dict(font=dict(size=16, color="#fff")),
                      legend=dict(bgcolor="rgba(0,0,0,0)"))
    fig.update_xaxes(gridcolor="#2A3038", zeroline=False)
    fig.update_yaxes(gridcolor="#2A3038", zeroline=False)
    return fig


def kpi(col, label, value, sub, color):
    col.markdown(
        f"""<div style="background:#1A1F2B;border-left:4px solid {color};
        padding:14px 16px;border-radius:10px;height:120px;">
        <div style="color:#9AA7B4;font-size:.76rem;text-transform:uppercase;
        letter-spacing:.06em;">{label}</div>
        <div style="color:{color};font-size:1.6rem;font-weight:700;
        margin-top:6px;">{value}</div>
        <div style="color:#6B7885;font-size:.75rem;">{sub}</div></div>""",
        unsafe_allow_html=True)


# ---- data ----------------------------------------------------------------
sec = q("SELECT * FROM mart_food_security ORDER BY country, year")
price = q("SELECT * FROM mart_food_price_index ORDER BY country, year")
rank = q("SELECT * FROM mart_asean_ranking ORDER BY year, rank_inflation")
try:
    food_nat = q("SELECT * FROM mart_food_inflation_national ORDER BY year, month_num")
    food_city = q("SELECT * FROM mart_food_inflation_city ORDER BY year, avg_inflation_pct DESC")
    rice = q("SELECT * FROM mart_rice_price ORDER BY year, harga_rp_kg DESC")
    rice_ws = q("SELECT * FROM mart_rice_wholesale ORDER BY year, month_num")
    month_infl = q("SELECT * FROM mart_monthly_inflation ORDER BY year, month_num")
    city_latest = q("SELECT * FROM mart_city_latest ORDER BY avg_inflation_pct DESC")
except Exception:
    food_nat = food_city = rice = pd.DataFrame()
    rice_ws = month_infl = city_latest = pd.DataFrame()
try:
    alerts = json.loads((REPORTS / "alerts.json").read_text(encoding="utf-8"))
except Exception:
    alerts = {"alerts": [], "count": 0}

latest_year = int(sec["year"].max())

# ---- header --------------------------------------------------------------
st.markdown(
    f"""<div style="background:linear-gradient(100deg,{C['primary']},{C['blue']});
    padding:22px 26px;border-radius:14px;margin-bottom:18px;">
    <div style="font-size:1.7rem;font-weight:800;color:white;">
    🌾 Food Price & Security Intelligence</div>
    <div style="color:#D7E4DC;font-size:.9rem;margin-top:4px;">
    Ketahanan pangan ASEAN · World Bank Open Data · pipeline DuckDB ·
    by <b>Sandi Ridwan</b></div></div>""",
    unsafe_allow_html=True)

# ---- sidebar -------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Filter")
countries = sorted(sec["country"].unique())
sel = st.sidebar.multiselect("Negara", countries, default=countries)
y0, y1 = int(sec["year"].min()), latest_year
sel_y = st.sidebar.slider("Rentang tahun", y0, y1, (y0, y1))
st.sidebar.markdown("---")
st.sidebar.caption(
    "Sumber: **World Bank Open Data** (tahunan) + **BPS WebAPI** "
    "(inflasi pangan & harga beras bulanan per kota, s/d 2026). Pipeline: "
    "ingest → DuckDB → SQL marts → dashboard. Uji kualitas data & alert "
    "tersedia di `tests/` dan `src/alerts.py`.")

mask = (sec["country"].isin(sel) if sel else True)
d = sec[sec["country"].isin(sel)] if sel else sec
d = d[(d["year"] >= sel_y[0]) & (d["year"] <= sel_y[1])]

# ---- KPI -----------------------------------------------------------------
X.render("kpi", st=st)
idn = sec[(sec["country_iso"] == "IDN") &
          (sec["year"] == sec[sec.country_iso == "IDN"]["year"].max())]
k1, k2, k3, k4 = st.columns(4)
if len(idn):
    r = idn.iloc[0]
    kpi(k1, "Inflasi pangan ID", f"{r.inflation_pct:.2f}%" if pd.notna(r.inflation_pct) else "n/a",
        f"tahun {int(r.year)}", C["red"] if (pd.notna(r.inflation_pct) and r.inflation_pct >= 5) else C["primary"])
    kpi(k2, "Impor pangan ID", f"{r.food_import_pct:.1f}%" if pd.notna(r.food_import_pct) else "n/a",
        "dari total impor", C["blue"])
    kpi(k3, "Indeks harga ID", f"{r.price_index:.1f}" if pd.notna(r.price_index) else "n/a",
        "2010 = 100", C["purple"])
    kpi(k4, "Index produksi ID", f"{r.food_prod_index:.1f}" if pd.notna(r.food_prod_index) else "n/a",
        "2014-2016 = 100", C["accent"])
else:
    st.warning("Data Indonesia tidak ditemukan untuk filter ini.")
st.write("")

t1, t2, t_bps, t3, t4 = st.tabs(["📈 Tren", "🏆 Peringkat ASEAN",
                                 "🇮🇩 Inflasi Pangan (BPS)",
                                 "🚨 Alert", "🔬 Metodologi"])

with t1:
    st.markdown("#### Indeks harga pangan (2010 = 100)")
    X.render("price_index", st=st)
    p = price[price["country"].isin(sel)] if sel else price
    fig = px.line(p, x="year", y="price_index", color="country",
                  color_discrete_map=CTRY_COLOR, markers=True)
    style(fig, 420).update_layout(title="Indeks Harga Pangan",
                                  xaxis_title="Tahun", yaxis_title="Indeks")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Inflasi harga konsumen tahunan (%)")
    X.render("inflation", st=st)
    fig = px.line(d, x="year", y="inflation_pct", color="country",
                  color_discrete_map=CTRY_COLOR, markers=True)
    fig.add_hline(y=5.0, line_dash="dash", line_color="#C0392B",
                  annotation_text="ambang alert 5%")
    style(fig, 420).update_layout(title="Inflasi Tahunan",
                                  xaxis_title="Tahun", yaxis_title="%")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        X.render("production", st=st)
        fig = px.line(d, x="year", y="food_prod_index", color="country",
                      color_discrete_map=CTRY_COLOR, markers=True)
        style(fig, 400).update_layout(title="Indeks Produksi Pangan")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        X.render("imports", st=st)
        fig = px.line(d, x="year", y="food_import_pct", color="country",
                      color_discrete_map=CTRY_COLOR, markers=True)
        style(fig, 400).update_layout(title="Impor Pangan (% total impor)")
        st.plotly_chart(fig, use_container_width=True)

with t2:
    st.markdown(f"#### Peringkat ASEAN {latest_year} — inflasi pangan terendah (terbaik)")
    X.render("ranking", st=st)
    rk = rank[rank["year"] == latest_year].sort_values("rank_inflation")
    fig = px.bar(rk, x="inflation_pct", y="country", orientation="h",
                 color="inflation_pct", color_continuous_scale="RdYlGn_r",
                 text=rk["inflation_pct"].round(2))
    style(fig, 400).update_layout(coloraxis_showscale=False,
                                  title=f"Inflasi Pangan {latest_year}",
                                  xaxis_title="%", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(rk[["year", "country", "inflation_pct", "food_prod_index",
                     "rank_inflation", "rank_production"]],
                 use_container_width=True, hide_index=True)

    st.markdown("#### Evolusi peringkat inflasi (1 = terbaik)")
    X.render("rank_evolution", st=st)
    piv = rank.pivot_table(index="year", columns="country",
                           values="rank_inflation")
    fig = px.imshow(piv.T, aspect="auto", color_continuous_scale="RdYlGn_r",
                    labels=dict(color="peringkat"))
    style(fig, 360).update_layout(title="Peringkat Inflasi per Tahun")
    st.plotly_chart(fig, use_container_width=True)

with t_bps:
    st.markdown("#### Inflasi pangan nasional (bulanan, rata-rata 91 kota)")
    X.render("bps_food", st=st)
    st.caption("Sumber: **BPS WebAPI** — inflasi kelompok Makanan, Minuman & "
               "Tembakau per kota (2020–2023), inflasi bulanan & harga beras "
               "grosir **s/d 2026** (data terbaru). Jauh lebih rinci dari "
               "agregat tahunan World Bank.")
    if food_nat.empty:
        st.info("Data BPS belum tersedia. Jalankan `python src/ingest_bps.py` "
                "(butuh BPS_API_KEY di .env).")
    else:
        fn = food_nat.copy()
        fn["label"] = fn["year"].astype(str) + "-" + fn["month_num"].astype(str).str.zfill(2)
        fig = px.bar(fn, x="label", y="avg_inflation",
                     color="avg_inflation", color_continuous_scale="RdYlGn_r")
        style(fig, 400).update_layout(coloraxis_showscale=False,
                                      title="Inflasi Pangan Nasional Bulanan (%)",
                                      xaxis_title="", yaxis_title="% (m-to-m)")
        st.plotly_chart(fig, use_container_width=True)

        yb = st.selectbox("Tahun (perbandingan kota)",
                          sorted(food_city["year"].unique(), reverse=True))
        fc = food_city[food_city["year"] == yb]
        c1, c2 = st.columns(2)
        with c1:
            top = fc.nlargest(15, "avg_inflation_pct")[
                ["wilayah_nama", "avg_inflation_pct"]]
            fig = px.bar(top.iloc[::-1], x="avg_inflation_pct", y="wilayah_nama",
                         orientation="h", color_discrete_sequence=[C["red"]])
            style(fig, 500).update_layout(title=f"15 Kota Inflasi Pangan Tertinggi {yb}",
                                          xaxis_title="rata-rata %", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            vol = fc.nlargest(15, "volatility")[["wilayah_nama", "volatility"]]
            fig = px.bar(vol.iloc[::-1], x="volatility", y="wilayah_nama",
                         orientation="h", color_discrete_sequence=[C["purple"]])
            style(fig, 500).update_layout(title=f"15 Kota Paling BERGEJOLAK {yb} "
                                                 f"(volatilitas harga)",
                                          xaxis_title="stddev %", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)

        if not rice_ws.empty:
            st.markdown("#### 🌾 Harga beras grosir — TERBARU (2020–2026)")
            X.render("rice_2026", st=st)
            rw = rice_ws.copy()
            rw["label"] = (rw["year"].astype(str) + "-"
                           + rw["month_num"].astype(str).str.zfill(2))
            fig = px.line(rw, x="label", y="harga_rp_kg", markers=True,
                          color_discrete_sequence=[C["accent"]])
            style(fig, 400).update_layout(
                title="Harga Beras Grosir Bulanan (Rp/kg)",
                xaxis_title="", yaxis_title="Rp/kg")
            st.plotly_chart(fig, use_container_width=True)
            ylast = int(rw["year"].max())
            rl = rw[rw["year"] == ylast]
            if len(rl):
                latest = rl.iloc[-1]
                prev_yr = rw[rw["year"] == ylast - 1]
                delta = None
                if len(prev_yr):
                    delta = latest["harga_rp_kg"] - prev_yr["harga_rp_kg"].mean()
                st.metric(f"Harga beras grosir terakhir ({latest['month']} {ylast})",
                          f"Rp {latest['harga_rp_kg']:,.0f}/kg",
                          f"{delta:+,.0f} vs rata-rata {ylast-1}" if delta else None)

        if not city_latest.empty:
            st.markdown("#### Inflasi bulanan per kota — tahun terbaru")
            ytop = int(city_latest["year"].max())
            top = city_latest.nlargest(15, "avg_inflation_pct")
            fig = px.bar(top.iloc[::-1], x="avg_inflation_pct", y="wilayah_nama",
                         orientation="h", color_discrete_sequence=[C["red"]])
            style(fig, 480).update_layout(
                title=f"15 Kota Inflasi Bulanan Tertinggi {ytop}",
                xaxis_title="rata-rata %", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)

        if not rice.empty:
            st.markdown("#### Harga eceran beras historis per kota (Rp/kg)")
            st.caption("Data historis BPS var 79 (2000–2016). Untuk harga "
                       "terbaru gunakan bagian 'Harga beras grosir' di atas.")
            ry = st.selectbox("Tahun harga beras historis",
                              sorted(rice["year"].unique(), reverse=True),
                              key="rice_year")
            rr = rice[rice["year"] == ry].nlargest(15, "harga_rp_kg")
            fig = px.bar(rr.iloc[::-1], x="harga_rp_kg", y="wilayah_nama",
                         orientation="h", color_discrete_sequence=[C["accent"]])
            style(fig, 440).update_layout(title=f"Harga Beras Eceran Tertinggi {ry} (Rp/kg)",
                                          xaxis_title="Rp/kg", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)

with t3:
    st.markdown(f"#### Alert otomatis — {alerts.get('count', 0)} terdeteksi")
    X.render("alert", st=st)
    thr = alerts.get("thresholds", {})
    st.caption(f"Ambang: inflasi ≥ {thr.get('inflation_pct')}%, "
               f"YoY ≥ {thr.get('yoy_pct')}%")
    al = alerts.get("alerts", [])
    if al:
        st.dataframe(pd.DataFrame(al)[["severity", "jenis", "country",
                                       "year", "value", "pesan"]],
                     use_container_width=True, hide_index=True)
    else:
        st.success("Tidak ada alert — semua indikator dalam ambang wajar.")

    st.markdown("#### Anomali harga historis (flag spike, YoY ≥ 7%)")
    X.render("spike", st=st)
    sp = price[price["yoy_flag"] == "spike"].sort_values("yoy_pct",
                                                         ascending=False)
    if len(sp):
        fig = px.bar(sp.head(12), x="yoy_pct", y="country", color="year",
                     orientation="h", text=sp.head(12)["yoy_pct"].round(1))
        style(fig, 420).update_layout(title="Lonjakan Harga Terbesar")
        st.plotly_chart(fig, use_container_width=True)

with t4:
    st.markdown("#### Arsitektur pipeline")
    X.render("architecture", st=st)
    st.code("""
World Bank API ─┐
                ├─► ingest.py ─► data/staging (Parquet)
Frankfurter ────┘                      │
                                       ▼
                              load_db.py ─► DuckDB (staging)
                                       │
                                       ▼
                         sql/transform.sql ─► marts (DuckDB + Parquet)
                                       │
                     ┌─────────────────┼──────────────────┐
                     ▼                 ▼                  ▼
              dashboard.py       alerts.py       tests/test_data_quality.py
    """, language="text")

    st.markdown("#### Marts — tabel siap-analisis")
    X.render("marts", st=st)
    # bangun ringkasan dari pembacaan tiap mart (kompatibel db & fallback)
    _tabs = ["mart_food_security", "mart_food_price_index", "mart_inflation",
             "mart_asean_ranking", "mart_food_inflation_city",
             "mart_monthly_inflation", "mart_rice_wholesale", "mart_city_latest"]
    marts_cov = pd.DataFrame([
        {"tabel": t, "baris": len(q(f"SELECT * FROM {t}"))} for t in _tabs
        if len(q(f"SELECT * FROM {t}")) > 0
    ])
    st.dataframe(marts_cov, use_container_width=True, hide_index=True)

    st.markdown("#### Cakupan data")
    X.render("coverage", st=st)
    cov = (sec.groupby("country")["year"].agg(["min", "max", "count"])
              .reset_index()
              .rename(columns={"min": "tahun_awal", "max": "tahun_akhir",
                               "count": "baris"}))
    st.dataframe(cov, use_container_width=True, hide_index=True)

    st.markdown("#### Catatan keterbatasan (jujur)")
    X.render("limitations", st=st)
    st.markdown(
        "- **Data tahunan, bukan harian.** World Bank memberi agregat tahunan; "
        "harga pangan mikro harian Indonesia (Bapanas/BPS) **terkunci** "
        "(endpoint harga butuh auth; BPS webapi di balik WAF berbayar). "
        "Lihat `docs/ADR.md`.\n"
        "- **Lag publikasi.** Indeks produksi pangan World Bank belum tersedia "
        "untuk 2023–2025 (null) — ditangani sebagai missing, bukan nol.\n"
        "- **Definisi inflasi** = CPI umum, bukan indeks pangan khusus; "
        "dipakai sebagai proksi tekanan harga.\n"
        "- **5 negara ASEAN** saja (ketersediaan data seragam).")

st.markdown(
    f"""<hr style="border-color:#2A3038;">
    <div style="color:#8B9AA6;font-size:.8rem;text-align:center;">
    🌾 Food Price & Security Intelligence · World Bank Open Data ·
    pipeline DuckDB + SQL · oleh <b>Sandi Ridwan</b><br>
    Analisis edukasional. Bukan saran investasi/kebijakan.</div>""",
    unsafe_allow_html=True)
