<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=900&size=38&duration=3000&pause=1000&color=1F5C3D&center=true&vCenter=true&width=900&height=70&lines=FOOD+PRICE+%26+SECURITY+INTELLIGENCE" alt="Food Price & Security Intelligence" />

![Python](https://img.shields.io/badge/Python-3.10+-1F5C3D?style=for-the-badge&logo=python&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-SQL_OLAP-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Data](https://img.shields.io/badge/Source-World_Bank-0071BC?style=for-the-badge)
![Tests](https://img.shields.io/badge/Data_Quality-16_tests-2E6F95?style=for-the-badge)

</div>

---

## 🌾 Apa ini?

**Data platform end-to-end** (bukan notebook) untuk memantau **harga & ketahanan
pangan ASEAN**: pipeline otomatis dari API publik → database → SQL marts →
dashboard + alert.

Fokus project ini **bukan** visualisasi saja, melainkan **rekayasa data**:
lapisan ingest/transform/test yang dapat direproduksi, diaudit, dan dijalankan
ulang oleh siapa pun tanpa kredensial.

```bash
python src/run_pipeline.py     # ingest → load → transform → tests → alerts
streamlit run app/dashboard.py # dashboard interaktif
```

---

## 🏗️ Arsitektur

```
 World Bank API ─┐
                 ├─► ingest.py ─► data/staging (Parquet, long format)
 Frankfurter ────┘                        │
                                          ▼
                                 load_db.py ─► DuckDB (staging tables)
                                          │
                                          ▼
                        sql/transform.sql ─► marts (DuckDB + Parquet)
                                          │
                    ┌─────────────────────┼──────────────────────┐
                    ▼                     ▼                      ▼
             dashboard.py            alerts.py        tests/test_data_quality.py
```

| Lapisan | File | Peran |
|---|---|---|
| **Ingest** | `src/ingest.py` | Tarik World Bank + kurs → Parquet (idempoten) |
| **Load** | `src/load_db.py`, `sql/schema.sql` | Muat ke DuckDB |
| **Transform** | `sql/transform.sql`, `src/transform.py` | SQL murni: YoY, flag, pivot, ranking |
| **Quality** | `tests/test_data_quality.py` | 16 uji: unik, lengkap, rentang, konsistensi, kesegaran |
| **Alert** | `src/alerts.py` | Deteksi inflasi tinggi, lonjakan harga, akselerasi |
| **Serve** | `app/dashboard.py` | Dashboard Streamlit |
| **Orchestrate** | `src/run_pipeline.py` | Jalankan seluruh pipeline |

---

## 📊 Data & Cakupan

| Aspek | Nilai |
|---|---|
| Sumber | **World Bank Open Data** (publik, tanpa API key) + Frankfurter (kurs) |
| Negara | Indonesia, Malaysia, Thailand, Vietnam, Philippines (ASEAN) |
| Rentang | 2000–2025 (26 tahun) |
| Indikator | 6 (indeks harga, inflasi, produksi pangan, impor pangan, pupuk, populasi) |
| Baris valid | 751 nilai indikator + 6.844 hari kurs |
| Uji kualitas | **16/16 lulus** |

**Indikator:** `FP.CPI.TOTL`, `FP.CPI.TOTL.ZG`, `AG.PRD.FOOD.XD`,
`TM.VAL.FOOD.ZS.UN`, `AG.CON.FERT.ZS`, `SP.POP.GROW`

---

## 🔍 Temuan (dari pipeline ini)

1. **Indonesia inflasi pangan 1.91% (2025)** — turun dari puncak 4.21% (2022).
2. **Krisis pangan 2008 terdeteksi otomatis**: Vietnam +23.1%, Indonesia +10.2% (YoY indeks harga).
3. **Akselerasi 2022**: Thailand naik 4.8 poin (1.2%→6.1%), Indonesia 2.6 poin — konsisten dengan guncangan pasca-COVID + perang Ukraina.
4. **Impor pangan Indonesia ~10–12%** dari total impor (stabil sejak 2000).
5. **Gap data**: indeks produksi pangan World Bank belum tersedia 2023–2025 (null) — dilaporkan sebagai missing, bukan nol.

---

## ⚠️ Keterbatasan yang diakui terbuka

- **Data tahunan, bukan harian.** Harga mikro harian Indonesia (Bapanas/BPS)
  **terkunci**: endpoint harga Bapanas balas 401, BPS webapi di balik WAF.
  Lihat [`docs/ADR.md`](docs/ADR.md) ADR-001 untuk investigasi lengkap.
- **Inflasi = CPI umum**, bukan indeks pangan khusus (proksi tekanan harga).
- **Lag publikasi**: beberapa indikator World Bank tertinggal 1–2 tahun.
- **5 negara ASEAN** saja (ketersediaan seragam), bukan seluruh dunia.
- Ambang alert **deterministik** (bukan ML) — dijelaskan di ADR-005.

> Daripada menyembunyikan data yang tak tersedia, project ini
> **mendokumentasikan jalan buntukannya** (ADR) dan **menguji** apa yang ada.

---

## 🧪 Kualitas data (contoh)

```
PASS  stg_wb PK unik
PASS  YoY konsisten dgn rumus
PASS  flag spike konsisten
PASS  ranking referensial ke security
PASS  data segar (<= 2 tahun)
...
[dq] 16 lulus, 0 gagal → [dq] SEMUA UJI LULUS
```

Uji berjalan sebagai **gerbang wajib** di akhir pipeline.

---

## 📁 Struktur

```
food-price-intelligence/
├── src/
│   ├── config.py            # path, sumber, ambang alert
│   ├── ingest.py            # World Bank + kurs → staging
│   ├── load_db.py           # staging → DuckDB
│   ├── transform.py         # SQL marts → Parquet
│   ├── alerts.py            # deteksi lonjakan
│   └── run_pipeline.py      # orkestrator end-to-end
├── sql/
│   ├── schema.sql           # skema staging + marts
│   └── transform.sql        # logika analitik (SQL murni)
├── tests/
│   └── test_data_quality.py # 16 uji kualitas data
├── app/dashboard.py         # Streamlit
├── docs/
│   ├── ADR.md               # keputusan arsitektur (jujur)
│   └── ERD.md               # relasi & lineage
├── data/{raw,staging,marts}/
├── db/                      # food.duckdb
└── reports/                 # alerts.json · alerts.md · figures
```

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python src/run_pipeline.py          # pipeline penuh (~90s karena ingest)
streamlit run app/dashboard.py      # buka http://localhost:8501
```

Jalankan cepat (staging sudah ada, tanpa re-fetch):
```bash
python src/run_pipeline.py --no-ingest
```

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|---|---|
| **Sumber** | World Bank Open Data API · Frankfurter (ECB rates) |
| **Ingest** | Python stdlib `urllib` + pandas + pyarrow |
| **Database** | **DuckDB** (embedded OLAP, SQL penuh) |
| **Transform** | SQL murni (CTE, window functions) |
| **Quality** | Uji kustom berbasis DuckDB (CI-friendly) |
| **Dashboard** | Streamlit + Plotly |
| **Orkestrasi** | `run_pipeline.py` (subprocess, exit-code gating) |

---

## 👤 Author

<div align="center">

**Sandi Ridwan** — Data Analyst · Data Automation Engineer · Python

📍 Palu, Central Sulawesi, Indonesia

[![Upwork](https://img.shields.io/badge/Upwork-Hire_Me-6A4C93?style=for-the-badge&logo=upwork&logoColor=white)](https://www.upwork.com/freelancers/~011f6d0fbb4a372974)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/sandi-ridwan)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SandiRidwan)

</div>

## 📄 License

MIT — Educational & portfolio. Data © World Bank (CC BY 4.0).
