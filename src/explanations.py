"""
explanations.py — narasi Kenapa · Tujuan · Dampak untuk setiap elemen.

STANDAR WAJIB (portofolio): setiap metrik/chart/tabel harus menjelaskan
  · KENAPA dipilih      — masalah & konteks yang membuatnya relevan
  · TUJUAN              — pertanyaan (bisnis/kebijakan) yang dijawab
  · DAMPAK              — implikasi & keputusan yang bisa timbul
  · CARA BACA           — (opsional) panduan bila tidak intuitif

Prinsip: dashboard tanpa narasi adalah angka tanpa makna. Klien tidak membeli
SQL — mereka membeli kemampuan menjelaskan apa artinya.
"""

from __future__ import annotations

EXPLAIN: dict[str, dict] = {
    # ---------------------------------------------------------------- KPI --
    "kpi": {
        "judul": "Metrik Ringkas (KPI)",
        "kenapa": "Sebelum masuk detail, pembaca butuh 4 angka tunggal yang "
                  "merangkum kondisi: seberapa mahal pangan, seberapa bergantung "
                  "pada impor, dan bagaimana produksi domestik.",
        "tujuan": "Menjawab secepat mungkin: apakah pangan Indonesia sedang "
                  "di bawah tekanan, dan seberapa rentan terhadap guncangan global?",
        "dampak": "Inflasi pangan tinggi (>5%) → tekanan daya beli & risiko "
                  "sosial; impor tinggi → kerentanan kurs & pasokan global. "
                  "Angka ini menentukan apakah perlu intervensi.",
        "baca": "Nilai per tahun terbaru yang tersedia per negara (World Bank).",
    },
    # ------------------------------------------------------------ TREN -----
    "price_index": {
        "judul": "Indeks Harga Pangan (2010 = 100)",
        "kenapa": "Inflasi tahunan bisa naik-turun; indeks memberi garis dasar "
                  "kumulatif — seberapa mahal pangan hari ini dibanding 2010.",
        "tujuan": "Membandingkan tingkat harga antar negara pada skala sama, "
                  "dan melihat arah jangka panjang (bukan hanya satu tahun).",
        "dampak": "Negara dengan indeks jauh di atas 100 mengalami inflasi "
                  "kumulatif besar → biaya hidup & upah tertekan berkepanjangan. "
                  "Gap antar negara menandakan perbedaan kebijakan moneter/pangan.",
        "baca": "Semua garis mulai dari basis 100 (tahun 2010). Garis lebih "
                "tinggi = harga relatif lebih mahal sejak 2010.",
    },
    "inflation": {
        "judul": "Inflasi Harga Konsumen Tahunan (%)",
        "kenapa": "Inflasi adalah sinyal paling langsung tekanan harga. "
                  "Ambang 5% dipakai luas sebagai batas 'nyaman' bagi ekonomi "
                  "berkembang.",
        "tujuan": "Menemukan tahun-tahun lonjakan (krisis) dan apakah tiap "
                  "negara mampu menjinakkan inflasi setelah guncangan.",
        "dampak": "Melewati ambang 5% → daya beli tergerus & tekanan sosial. "
                  "Pola naik-turun bersama menandakan guncangan global "
                  "(mis. 2008, 2022) yang butuh respons terkoordinasi.",
        "baca": "Garis putus = ambang alert 5%. Perhatikan tahun lonjakan bersama.",
    },
    "production": {
        "judul": "Indeks Produksi Pangan (2014-2016 = 100)",
        "kenapa": "Harga ditentukan pasokan & permintaan. Produksi domestik "
                  "menunjukkan kapasitas menyerap guncangan tanpa impor.",
        "tujuan": "Menilai apakah negara memperkuat atau melemahkan "
                  "kemandirian pangannya seiring waktu.",
        "dampak": "Produksi naik + impor stabil → ketahanan membaik. "
                  "Produksi stagnan sementara inflasi naik → ketergantungan "
                  "impor & kerentanan tinggi.",
        "baca": "Di atas 100 = produksi lebih tinggi dari rata-rata 2014-2016. "
                "Perhatikan: World Bank belum merilis 2023–2025 (data null).",
    },
    "imports": {
        "judul": "Impor Pangan (% dari total impor)",
        "kenapa": "Tingkat impor pangan menunjukkan seberapa bergantung suatu "
                  "negara pada pasar global untuk kebutuhan pokok.",
        "tujuan": "Mengukur kerentanan terhadap guncangan harga pangan dunia, "
                  "gangguan rantai pasok, dan fluktuasi kurs.",
        "dampak": "Impor pangan tinggi → kenaikan harga global langsung "
                  "merambat ke dalam negeri; pelemahan kurs memperparah. "
                  "Basis untuk kebijakan diversifikasi & swasembada.",
        "baca": "Persentase dari total nilai impor barang. Naik = makin "
                "bergantung pada luar negeri.",
    },
    # --------------------------------------------------------- RANKING ----
    "ranking": {
        "judul": "Peringkat ASEAN — Inflasi Pangan",
        "kenapa": "Angka absolut sulit dimaknai tanpa pembanding. Negara "
                  "tetangga dengan struktur ekonomi mirip memberi konteks.",
        "tujuan": "Menjawab: di mana posisi tiap negara relatif terhadap "
                  "ASEAN, dan siapa yang paling berhasil menahan harga?",
        "dampak": "Peringkat rendah (inflasi tinggi) → tekanan publik & "
                  "sorotan kebijakan; peringkat atas → praktik yang bisa "
                  "dipelajari. Basis untuk benchmark & kerja sama regional.",
        "baca": "Peringkat 1 = inflasi terendah (terbaik). Warna merah = "
                "inflasi relatif tinggi di antara negara pembanding.",
    },
    "rank_evolution": {
        "judul": "Evolusi Peringkat per Tahun",
        "kenapa": "Satu potret tahun menyesatkan — negara bisa jatuh/naik "
                  "peringkat karena kebijakan atau guncangan. Tren lebih penting.",
        "tujuan": "Melihat siapa yang konsisten kuat vs yang naik-turun, "
                  "dan kapan sebuah negara keluar dari jalur.",
        "dampak": "Pola perbaikan stabil → kebijakan berhasil; peringkat "
                  "yang berbalik tajam → sinyal krisis atau reformasi. "
                  "Menuntun evaluasi kebijakan jangka panjang.",
        "baca": "Warna hijau = posisi baik (peringkat rendah). "
                "Baris yang bergeser cepat = perubahan besar.",
    },
    # ----------------------------------------------------------- ALERT ----
    "alert": {
        "judul": "Alert Otomatis (Ambang Deterministik)",
        "kenapa": "Manusia tak bisa memantau semua indikator sepanjang waktu. "
                  "Ambang eksplisit (inflasi ≥5%, YoY ≥7%) membuat peringatan "
                  "dapat dipertanggungjawabkan — bukan kotak hitam.",
        "tujuan": "Menangkap lonjakan harga & inflasi secara otomatis dan "
                  "membedakan yang mendesak (severity tinggi) dari yang perlu dipantau.",
        "dampak": "Alert severity tinggi → prioritas mitigasi (operasi pasar, "
                  "stabilisasi pasokan). Karena aturannya terbuka, keputusan "
                  "berbasis alert dapat diaudit & disesuaikan.",
        "baca": "Ambang diatur di src/config.py. Mengubah ambang = mengubah "
                "sensitivitas tanpa mengubah kode analitik.",
    },
    "spike": {
        "judul": "Anomali Harga Historis (flag spike)",
        "kenapa": "Preseden penting: tahun-tahun ketika harga melonjak tajam "
                  "menunjukkan kerentanan struktural yang bisa terulang.",
        "tujuan": "Mengidentifikasi pola lonjakan historis (mis. krisis 2008) "
                  "sebagai pembelajaran dan kalibrasi kesiapsiagaan.",
        "dampak": "Jika lonjakan berulang pada periode/pemicu sama, "
                  "kebijakan dapat diarahkan ke akar masalah (produksi, "
                  "cadangan, logistik) alih-alih reaksi ad-hoc.",
        "baca": "Flag 'spike' muncul bila kenaikan YoY indeks harga ≥7%. "
                "Batang lebih panjang = lonjakan lebih ekstrem.",
    },
    # ------------------------------------------------------ METODOLOGI ---
    "marts": {
        "judul": "Marts — Tabel Siap-Analisis",
        "kenapa": "Data mentah tidak siap dipakai berulang. Marts menyatukan "
                  "dan menstandarkan data lintas sumber lewat SQL yang dapat diaudit.",
        "tujuan": "Menyediakan satu sumber kebenaran (single source of truth) "
                  "bagi dashboard, alert, dan analisis lanjutan — konsisten & teruji.",
        "dampak": "Perubahan definisi (mis. cara hitung YoY) cukup di satu "
                  "tempat; semua konsumen ikut menyesuaikan. Mempercepat dan "
                  "mengurangi kesalahan pelaporan.",
        "baca": "Dibangun oleh sql/transform.sql dari staging; diuji oleh "
                "tests/test_data_quality.py.",
    },
    "coverage": {
        "judul": "Cakupan Data",
        "kenapa": "Analisis hanya sekuat datanya. Pembaca harus tahu apa yang "
                  "tercakup dan apa yang tidak, agar tidak menyimpulkan berlebihan.",
        "tujuan": "Menampilkan negara, jumlah indikator, dan rentang tahun yang "
                  "tersedia — sekaligus menandai keterbatasan.",
        "dampak": "Menjaga kesimpulan tetap dalam batas data (mis. hanya 5 "
                  "negara ASEAN, granularitas tahunan). Mencegah overgeneralization.",
        "baca": "Kolom indikator = jumlah indikator tersedia per negara; "
                "y0–y1 = rentang tahun.",
    },
    "limitations": {
        "judul": "Keterbatasan yang Diakui Terbuka",
        "kenapa": "Kejujuran metodologis adalah bagian dari kualitas. "
                  "Menyembunyikan batas data menyesatkan pengambil keputusan.",
        "tujuan": "Menyatakan secara eksplisit apa yang tidak bisa disimpulkan: "
                  "harian vs tahunan, proksi inflasi, lag publikasi, cakupan negara.",
        "dampak": "Pembaca memperlakukan temuan dengan tepat — dan tahu "
                  "langkah lanjutan (mis. data mikro harian) yang dibutuhkan "
                  "untuk keputusan yang lebih presisi.",
        "baca": "Lihat docs/ADR.md untuk detail investigasi sumber & keputusan.",
    },
    "architecture": {
        "judul": "Arsitektur Pipeline",
        "kenapa": "Analisis yang bisa direproduksi memerlukan alur yang jelas "
                  "dari sumber → penyimpanan → transformasi → penyajian.",
        "tujuan": "Menunjukkan bahwa hasil bukan kebetulan: setiap angka dapat "
                  "ditelusuri balik ke sumber publiknya, dan dijalankan ulang.",
        "dampak": "Siapa pun dapat menjalankan ulang dan memverifikasi. "
                  "Menambah kepercayaan & memudahkan pemeliharaan.",
        "baca": "Jalankan `python src/run_pipeline.py` untuk membangun ulang "
                "seluruh alur dari nol.",
    },
    "bps_food": {
        "judul": "Inflasi Pangan Bulanan per Kota (BPS)",
        "kenapa": "Agregat tahunan nasional menyembunyikan gejolak yang "
                  "sesungguhnya terjadi BULANAN di tiap kota. Harga pangan "
                  "bergerak mengikuti panen, hari besar, dan gangguan pasokan — "
                  "semuanya berskala bulanan, bukan tahunan.",
        "tujuan": "Menemukan KAPAN (bulan) dan DI MANA (kota) harga pangan "
                  "melonjak, serta kota mana yang paling bergejolak.",
        "dampak": "Bulan lonjakan → waktu operasi pasar/intervensi; kota "
                  "bergejolak tinggi → prioritas stabilisasi. Ini mengubah "
                  "kebijakan dari reaktif-tahunan menjadi antisipatif-bulanan.",
        "baca": "Inflasi m-to-m (bulan ke bulan) %. Batang hijau = harga turun, "
                "merah = naik. Volatilitas = simpangan baku bulanan (risiko).",
    },
    "rice_2026": {
        "judul": "Harga Beras Grosir — Data TERBARU (2020–2026)",
        "kenapa": "Beras adalah komoditas pangan paling politis di Indonesia. "
                  "Harga grosir bulanan menunjukkan tekanan harga terkini — "
                  "sesuatu yang agregat tahunan tidak bisa ungkap.",
        "tujuan": "Melacak arah harga beras terkini dan mendeteksi kenaikan "
                  "tajam lebih awal.",
        "dampak": "Kenaikan beruntun → sinyal tekanan inflasi pangan & risiko "
                  "daya beli. Pemerintah/pelaku usaha dapat mengantisipasi "
                  "(operasi pasar, kontrak pasokan) sebelum harga eceran naik.",
        "baca": "Rp/kg di tingkat perdagangan besar. Garis naik konsisten = "
                "tren kenaikan; lonjakan tajam = perlu perhatian.",
    },
}


def text(key: str) -> str:
    """Render narasi sebagai teks markdown (untuk README/laporan)."""
    e = EXPLAIN.get(key)
    if not e:
        return ""
    parts = [f"**{e['judul']}**",
             f"- **Kenapa:** {e['kenapa']}",
             f"- **Tujuan:** {e['tujuan']}",
             f"- **Dampak:** {e['dampak']}"]
    if e.get("baca"):
        parts.append(f"- **Cara baca:** {e['baca']}")
    return "\n".join(parts)


def render(key: str, expanded: bool = False, st=None) -> None:
    """Render expander 'Kenapa · Tujuan · Dampak' di Streamlit."""
    if st is None:
        import streamlit as st  # noqa
    e = EXPLAIN.get(key)
    if not e:
        return
    with st.expander(f"💡 {e['judul']} — Kenapa · Tujuan · Dampak",
                     expanded=expanded):
        st.markdown(
            f"**🔎 Kenapa** — {e['kenapa']}\n\n"
            f"**🎯 Tujuan** — {e['tujuan']}\n\n"
            f"**📈 Dampak** — {e['dampak']}")
        if e.get("baca"):
            st.caption(f"👁️ Cara baca: {e['baca']}")


def audit(verbose: bool = True) -> bool:
    """Pastikan setiap entri punya kenapa/tujuan/dampak (tidak ada yang kosong)."""
    ok = True
    for k, v in EXPLAIN.items():
        miss = [f for f in ("kenapa", "tujuan", "dampak") if not v.get(f)]
        if miss:
            ok = False
            if verbose:
                print(f"  MISSING {k}: {miss}")
    if verbose:
        print(f"Penjelasan: {len(EXPLAIN)} | "
              f"{'SEMUA LENGKAP' if ok else 'ADA YANG KURANG'}")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if audit() else 1)
