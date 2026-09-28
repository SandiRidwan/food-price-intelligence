# ADR — Architecture Decision Records

Catatan keputusan arsitektur + **alasan jujur** (termasuk jalan buntu).

---

## ADR-001: Sumber data — World Bank, bukan Bapanas/BPS

**Status:** Diputuskan
**Konteks:** Project awalnya dirancang sebagai "harga pangan mikro harian
Indonesia" dari Panel Harga Bapanas / PIHPS Bank Indonesia / BPS.

**Investigasi (fakta lapangan):**

| Sumber | Hasil uji | Status |
|---|---|---|
| `panelharga.badanpangan.go.id/api/front/harga-*` | HTTP **401** (butuh auth) | ❌ terkunci |
| `bi.go.id/hargapangan/*` | 404 / koneksi diputus | ❌ tak tersedia |
| `hargapangan.id` | HTTP 522 | ❌ mati |
| `webapi.bps.go.id` | **WAF block** ("LTM WAF Block") | ❌ butuh key berbayar |
| `api.worldbank.org` (Indonesia) | HTTP **200**, JSON bersih | ✅ **dipakai** |
| `api.frankfurter.app` (kurs) | HTTP **200** | ✅ dipakai |

**Keputusan:** Pakai **World Bank Open Data** + **Frankfurter**.
**Alasan:** publik, tanpa API key, stabil, legal, dan reproducible oleh siapa pun
(tujuan portofolio). Data harian mikro memang lebih "seksi", tetapi tidak dapat
direproduksi tanpa kredensial → gagal prinsip project.
**Konsekuensi:** granularitas turun dari harian→tahunan; harga spesifik
(cabai, beras) tidak tersedia — diganti indikator ketahanan pangan agregat.

---

## ADR-002: DuckDB, bukan PostgreSQL

**Status:** Diputuskan
**Konteks:** Butuh database untuk menunjukkan skill SQL & pipeline.
**Opsi:** PostgreSQL (server) vs DuckDB (embedded) vs SQLite.

**Keputusan:** DuckDB.
**Alasan:**
- **Portabel**: file tunggal (`db/food.duckdb`), jalan tanpa server → portofolio
  bisa di-clone & dijalankan siapa pun dalam 1 perintah.
- **SQL analitik kuat**: window functions, CTE, `read_parquet` — lebih dari
  cukup untuk OLAP; SQL-nya **transferable** ke PostgreSQL/BigQuery.
- **Nol infra**: tidak perlu Docker/kredensial → menghilangkan hambatan
  reproduksi (pelajaran dari ADR-001).
**Konsekuensi:** tidak menunjukkan skill administrasi server (role, backup,
replikasi). Jika target lamaran spesifik "PostgreSQL admin", tambahkan opsi
koneksi — skema & SQL yang sama 90% berlaku.

---

## ADR-003: Logika analitik di SQL, orkestrasi di Python

**Status:** Diputuskan
**Konteks:** Transformasi bisa ditulis di pandas atau SQL.
**Keputusan:** Transformasi bisnis (YoY, ranking, pivot, flag) di **SQL murni**
(`sql/transform.sql`); Python hanya orkestrasi.
**Alasan:** SQL dapat **diaudit & ditinjau** tanpa membaca kode Python; mudah
dipindah ke dbt; menunjukkan kompetensi SQL yang dicari di job desc analis.
**Konsekuensi:** logika bercabang kompleks lebih repot di SQL — dihindari
dengan menjaga transformasi tetap deklaratif.

---

## ADR-004: Uji kualitas data sebagai gerbang pipeline

**Status:** Diputuskan
**Konteks:** Data publik punya missing (mis. indeks produksi pangan ID
2023–2025 = null).
**Keputusan:** `tests/test_data_quality.py` dijalankan sebagai **langkah terakhir
wajib** pipeline; exit code != 0 menghentikan pipeline.
**Alasan:** mencegah "sampah masuk, grafik keluar". Missing **dilaporkan**,
tidak diisi paksa dengan nol (nol ≠ tidak ada data).
**Konsekuensi:** uji harus dipelihara saat skema berubah.

---

## ADR-005: Alert deterministik, bukan model ML

**Status:** Diputuskan
**Konteks:** Deteksi lonjakan harga bisa pakai threshold atau model anomali.
**Keputusan:** Ambang deterministik dari `config.py` (inflasi ≥ 5%, YoY ≥ 7%),
dapat diubah & diaudit.
**Alasan:** transparan, dapat dijelaskan ke pemangku kepentingan, tidak
memerlukan data latih. Sesuai semangat project: **jujur & reproducible**.
**Konsekuensi:** ambang tetap tidak menyesuaikan diri per negara; bisa
ditingkatkan ke deteksi anomali statistik (z-score/IQR) di iterasi lanjutan.
