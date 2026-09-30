# ---------------------------------------------------------------------------
# KONTEN INSIGHT — Food Price & Security Intelligence
# Sudut pandang: pemerintah / bank sentral / pelaku usaha yang menjaga
# stabilitas harga pangan & ketahanan pangan nasional.
#
# FORMAT v2 — setiap rekomendasi = Aksi + Langkah + Metrik sukses + Pemilik.
# Semua angka mengacu ke data NYATA project ini (World Bank, BPS, 2000–2025).
# ---------------------------------------------------------------------------
from insight import register

register(
    "kpi",
    kesimpulan=(
        "Inflasi pangan Indonesia 1.91% (2025) — terkendali di bawah ambang 5%. "
        "Namun impor pangan ~10.2% dari total impor menunjukkan ketergantungan "
        "yang membuat harga domestik rentan terhadap guncangan global & kurs."),
    rekomendasi=[
        {"aksi": "Jaga inflasi pangan di bawah ambang 5% lewat operasi pasar terjadwal",
         "langkah": [
             "Tetapkan kalender operasi pasar: minimal sebelum musim paceklik & hari besar (Januari, Desember).",
             "Siapkan anggaran operasi pasar setara 0,5–1% nilai konsumsi pangan bulanan.",
             "Jalankan dashboard pemantauan mingguan atas 5 indikator (inflasi, impor, produksi, kurs, harga beras).",
             "Eskalasi otomatis ke rapat koordinasi bila inflasi bulanan > 1% atau YoY > 5%.",
         ],
         "metrik": "Inflasi pangan tahunan ≤ 5%; tidak ada bulan dengan m-o-m > 1,5%",
         "pemilik": "Bapanas + Bulog (eksekusi), Bank Indonesia (monitoring kurs)"},
        {"aksi": "Turunkan ketergantungan impor pangan dari 10.2% secara bertahap",
         "langkah": [
             "Petakan 3 komoditas impor terbesar (gandum, kedelai, jagung) dan volumenya.",
             "Tetapkan target substitusi tiap komoditas (mis. turunkan impor 1–2 poin per tahun).",
             "Alokasikan insentif produksi domestik untuk komoditas prioritas.",
             "Publikasikan progres tahunan sebagai akuntabilitas.",
         ],
         "metrik": "food_import_pct turun dari 10.2% → 8% dalam 5 tahun",
         "pemilik": "Kementerian Pertanian + Kementerian Perdagangan"},
        {"aksi": "Lindungi harga dari gejolak kurs komoditas impor kunci",
         "langkah": [
             "Identifikasi komoditas impor dengan elastisitas harga tertinggi (gandum, kedelai).",
             "Negosiasikan kontrak pasokan berjangka 6–12 bulan untuk komoditas tersebut.",
             "Bangun buffer stock untuk 1–3 bulan konsumsi komoditas kunci.",
         ],
         "metrik": "Volatilitas harga komoditas impor kunci turun < 5% per kuartal",
         "pemilik": "Bulog + Kementerian BUMN"},
    ],
    risiko=(
        "Ketergantungan impor 10%+ berarti pelemahan rupiah 10% berpotensi "
        "menaikkan harga pangan domestik signifikan. Tanpa penguatan produksi, "
        "inflasi pangan bisa melonjak tiba-tiba saat guncangan global."),
    tingkat="sedang",
)

register(
    "price_index",
    kesimpulan=(
        "Indeks harga pangan (2010=100) menunjukkan Indonesia bergerak naik "
        "seiring negara ASEAN lain, tetapi dengan lonjakan yang lebih tajam di "
        "periode krisis (2008, 2022). Pola bersama ini menandakan guncangan "
        "bersifat GLOBAL, bukan lokal."),
    rekomendasi=[
        {"aksi": "Bangun cadangan pangan strategis penyerap 6–12 bulan guncangan",
         "langkah": [
             "Hitung kebutuhan cadangan: 6–12 bulan × konsumsi bulanan komoditas kunci (beras, gandum, kedelai).",
             "Tentukan lokasi gudang di 5 titik rawan logistik (termasuk Indonesia timur).",
             "Tetapkan aturan rilis cadangan: lepas stok bila harga naik > 10% dalam 1 bulan.",
             "Audit kapasitas & mutu cadangan tiap kuartal.",
         ],
         "metrik": "Cadangan menutup ≥ 6 bulan konsumsi; waktu respons pelepasan ≤ 7 hari",
         "pemilik": "Bulog (pengelola), Bapanas (kebijakan)"},
        {"aksi": "Koordinasikan respons guncangan dengan negara ASEAN",
         "langkah": [
             "Inisiasi forum data-harga pangan ASEAN bulanan (berbagi indeks & stok).",
             "Sepakati protokol larangan pembatasan ekspor mendadak saat krisis.",
             "Simulasi tanggap darurat bersama 1×/tahun.",
         ],
         "metrik": "Kesepakatan berbagi data dengan ≥ 4 negara ASEAN dalam 12 bulan",
         "pemilik": "Kementerian Luar Negeri + Sekretariat ASEAN"},
        {"aksi": "Bangun sistem peringatan dini harga global",
         "langkah": [
             "Pantau 3 indikator dunia: harga gandum, pupuk, dan minyak (bulanan).",
             "Tetapkan ambang pemicu: kenaikan > 15% dalam sebulan = status siaga.",
             "Integrasikan sinyal global ke keputusan impor & cadangan.",
         ],
         "metrik": "Sinyal peringatan keluar ≥ 4 minggu sebelum harga domestik naik",
         "pemilik": "Bank Indonesia + Bapanas"},
    ],
    risiko=(
        "Tanpa cadangan & koordinasi, setiap guncangan global (seperti 2008 & "
        "2022) akan langsung diteruskan ke konsumen domestik — memicu inflasi "
        "tinggi dan tekanan daya beli kelompok rentan."),
    tingkat="tinggi",
)

register(
    "inflation",
    kesimpulan=(
        "Inflasi tahunan Indonesia memuncak di 2022 (4.21%) lalu turun ke 1.91% "
        "(2025). Puncak 2022 sejalan dengan seluruh ASEAN — konsekuensi guncangan "
        "pasca-COVID & perang Ukraina, bukan kegagalan kebijakan domestik."),
    rekomendasi=[
        {"aksi": "Pertahankan kebijakan moneter penyerap guncangan global",
         "langkah": [
             "Dokumentasikan bauran kebijakan 2022→2025 yang menurunkan inflasi 4.21%→1.91%.",
             "Jadikan dokumen itu playbook resmi untuk guncangan berikutnya.",
             "Pertahankan koordinasi fiskal-moneter bulanan (TPIP/TPID).",
         ],
         "metrik": "Inflasi tetap dalam sasaran BI (2,5%±1%) selama 4 kuartal berturut",
         "pemilik": "Bank Indonesia + Kementerian Keuangan"},
        {"aksi": "Siapkan protokol respons cepat saat inflasi mendekati 5%",
         "langkah": [
             "Tetapkan 3 tahap respons: siaga (4%), waspada (4,5%), darurat (5%).",
             "Siapkan paket operasi pasar + subsidi terarah per tahap.",
             "Uji simulasi protokol sebelum benar-benar dibutuhkan.",
         ],
         "metrik": "Waktu dari deteksi 4,5% → aksi pasar ≤ 14 hari",
         "pemilik": "TPID (Tim Pengendalian Inflasi Daerah)"},
        {"aksi": "Dokumentasikan faktor penurun inflasi sebagai rujukan",
         "langkah": [
             "Analisis dekomposisi inflasi 2022–2025 (global vs domestik).",
             "Pisahkan faktor eksternal (harga dunia) dari kebijakan domestik.",
             "Jadikan temuan dasar perencanaan tahunan.",
         ],
         "metrik": "Laporan dekomposisi diterbitkan tahunan",
         "pemilik": "BPS + Bank Indonesia"},
    ],
    risiko=(
        "Menganggap inflasi rendah saat ini sebagai 'normal permanen' berbahaya. "
        "Guncangan global bisa datang kapan saja; tanpa protokol respons, "
        "kenaikan bisa tak terkendali sebelum kebijakan diambil."),
    tingkat="sedang",
)

register(
    "production",
    kesimpulan=(
        "Indeks produksi pangan Indonesia menunjukkan tren naik jangka panjang "
        "(di atas basis 2014-2016), menandakan kapasitas produksi membaik. Namun "
        "data 2023-2025 belum dirilis World Bank — ada GAP informasi untuk "
        "keputusan terkini."),
    rekomendasi=[
        {"aksi": "Ganti basis data produksi ke sumber domestik yang mutakhir",
         "langkah": [
             "Hentikan penggunaan data produksi World Bank untuk keputusan pasokan terkini.",
             "Integrasikan data BPS (produksi padi/jagung/kedelai bulanan) ke pipeline.",
             "Sinkronkan definisi & satuan agar dapat dibandingkan lintas sumber.",
         ],
         "metrik": "Lag data produksi < 3 bulan (dari 1–2 tahun)",
         "pemilik": "Kementerian Pertanian + BPS"},
        {"aksi": "Investasi irigasi & teknologi benih untuk menjaga tren naik",
         "langkah": [
             "Identifikasi area dengan produktivitas di bawah rata-rata nasional.",
             "Alokasikan anggaran irigasi prioritas ke area tersebut.",
             "Distribusikan benih unggul bersertifikat tepat waktu musim tanam.",
         ],
         "metrik": "Indeks produksi pangan +5% dalam 5 tahun",
         "pemilik": "Kementerian Pertanian + Pemerintah Daerah"},
        {"aksi": "Bangun sistem pelaporan produksi internal tanpa lag",
         "langkah": [
             "Terapkan pelaporan produksi dasarian (10-harian) berbasis digital.",
             "Validasi silang dengan citra satelit luas panen.",
             "Publikasikan dasbor produksi internal bulanan.",
         ],
         "metrik": "Akurasi laporan vs realisasi panen ±10%",
         "pemilik": "BPS + Kementerian Pertanian"},
    ],
    risiko=(
        "Membuat keputusan pasokan berdasarkan data produksi 2022 (terakhir) "
        "selama 2025 berisiko salah hitung kebutuhan impor — bisa kurang "
        "(kelangkaan) atau berlebih (pemborosan devisa)."),
    tingkat="sedang",
)

register(
    "imports",
    kesimpulan=(
        "Impor pangan Indonesia stabil ~10-12% dari total impor sejak 2000. "
        "Kestabilan ini menenangkan, tetapi juga berarti tidak ada perbaikan "
        "kemandirian selama 25 tahun — ketergantungan bertahan struktural."),
    rekomendasi=[
        {"aksi": "Tetapkan target penurunan ketergantungan impor yang terukur",
         "langkah": [
             "Formalkan target: food_import_pct dari 10.2% → 8% dalam 5 tahun.",
             "Pecah target per komoditas (gandum, kedelai, jagung).",
             "Kaitkan anggaran produksi ke pencapaian target tiap tahun.",
         ],
         "metrik": "Penurunan ≥ 0,4 poin/tahun; tercapai 8% dalam 5 tahun",
         "pemilik": "Kementerian Pertanian + Bappenas"},
        {"aksi": "Substitusi pada komoditas impor terbesar",
         "langkah": [
             "Urutkan komoditas impor berdasarkan volume & nilai.",
             "Fokus riset & insentif pada 3 teratas.",
             "Bangun kemitraan petani–industri untuk jaminan serapan.",
         ],
         "metrik": "Volume impor 3 komoditas teratas turun ≥ 15% dalam 5 tahun",
         "pemilik": "Kementerian Pertanian + Kemendag"},
        {"aksi": "Diversifikasi sumber impor",
         "langkah": [
             "Petakan ketergantungan per negara asal (HHI konsentrasi).",
             "Tetapkan aturan: tidak ada satu negara > 40% impor satu komoditas.",
             "Jajaki pemasok alternatif (Amerika Latin, Afrika, Asia Selatan).",
         ],
         "metrik": "HHI impor per komoditas < 0,25",
         "pemilik": "Kementerian Perdagangan"},
    ],
    risiko=(
        "Ketergantungan struktural yang dibiarkan berarti setiap krisis pangan "
        "global langsung memukul Indonesia. 'Stabil 25 tahun' bisa berubah jadi "
        "krisis saat pasokan global terganggu (pandemi, perang, cuaca ekstrem)."),
    tingkat="tinggi",
)

register(
    "ranking",
    kesimpulan=(
        "Peringkat inflasi pangan ASEAN 2025: Thailand paling rendah (-0.13%), "
        "Vietnam tertinggi (3.31%), Indonesia di posisi 4 dari 5 (1.91%). "
        "Indonesia di bawah rata-rata tapi bukan yang terbaik."),
    rekomendasi=[
        {"aksi": "Pelajari kebijakan Thailand (inflasi terendah, -0.13%)",
         "langkah": [
             "Kaji pola produksi & distribusi pangan Thailand.",
             "Identifikasi 3 praktik yang dapat diadopsi Indonesia.",
             "Pilot project adopsi di 1 provinsi.",
         ],
         "metrik": "1 pilot adopsi berjalan dalam 12 bulan",
         "pemilik": "Bapanas + Kementerian Pertanian"},
        {"aksi": "Waspadai kasus Vietnam sebagai peringatan",
         "langkah": [
             "Analisis mengapa Vietnam (produsen beras besar) malah inflasi tertinggi.",
             "Petakan risiko serupa di Indonesia (distribusi, ekspor, kurs).",
             "Perkuat pengawasan distribusi domestik.",
         ],
         "metrik": "Laporan analisis risiko distribusi diterbitkan",
         "pemilik": "Bapanas"},
        {"aksi": "Gunakan peringkat regional sebagai tolok ukur target",
         "langkah": [
             "Tetapkan target: masuk 2 terbaik ASEAN dalam 3 tahun.",
             "Pantau posisi relatif bulanan.",
             "Sesuaikan kebijakan bila peringkat stagnan 2 kuartal berturut.",
         ],
         "metrik": "Peringkat inflasi ASEAN ≤ 2",
         "pemilik": "TPID Nasional"},
    ],
    risiko=(
        "Berpuas diri dengan 'di bawah ambang 5%' padahal masih kalah dari 3 "
        "tetangga berarti langkah kebijakan tidak kompetitif. Tanpa benchmark "
        "regional, stagnasi kebijakan tidak terdeteksi."),
    tingkat="rendah",
)

register(
    "bps_food",
    kesimpulan=(
        "Data bulanan BPS (91 kota) mengungkap gejolak yang TIDAK terlihat di "
        "agregat tahunan: inflasi pangan melonjak di Januari & Desember (hari "
        "besar) dan deflasi di Agustus (musim panen). Inflasi 2026 terkonsentrasi "
        "di Indonesia timur (Luwuk, Kolaka, Tual)."),
    rekomendasi=[
        {"aksi": "Jadwalkan operasi pasar SEBELUM puncak musiman",
         "langkah": [
             "Tandai bulan puncak dari data: Desember–Januari (hari besar).",
             "Jadwalkan operasi pasar 2–4 pekan sebelum puncak tersebut.",
             "Sinkronkan pasokan tambahan dengan jadwal tersebut, bukan reaktif.",
         ],
         "metrik": "Operasi pasar terlaksana ≥ 2 pekan sebelum puncak di semua kota",
         "pemilik": "Bulog + Pemerintah Daerah"},
        {"aksi": "Prioritaskan stabilisasi di Indonesia timur",
         "langkah": [
             "Fokuskan 3 kota inflasi tertinggi: Luwuk, Kolaka, Tual.",
             "Subsidi biaya logistik ke wilayah Indonesia timur.",
             "Bangun stok penyangga regional di sana.",
         ],
         "metrik": "Selisih inflasi timur vs nasional turun < 1 poin",
         "pemilik": "Kementerian Perhubungan + Bulog"},
        {"aksi": "Gunakan data bulanan untuk respons cepat",
         "langkah": [
             "Ganti siklus keputusan dari tahunan ke bulanan.",
             "Tetapkan ambang aksi bulanan (m-o-m > 1%).",
             "Kirim laporan bulanan ke pengambil keputusan.",
         ],
         "metrik": "Waktu deteksi→aksi ≤ 30 hari",
         "pemilik": "TPID + BPS"},
    ],
    risiko=(
        "Bereaksi berdasarkan data tahunan berarti intervensi selalu terlambat: "
        "harga sudah naik sebelum operasi pasar dilakukan. Pola musiman yang "
        "sebenarnya bisa diantisipasi malah mengejutkan setiap tahun."),
    tingkat="tinggi",
)

register(
    "rice_2026",
    kesimpulan=(
        "Harga beras grosir naik konsisten dari Rp12.261 (2020) ke Rp14.901/kg "
        "(Agu 2026) — kenaikan ~21% dalam 6 tahun. Tren naik yang stabil berarti "
        "inflasi pangan belum terkendali untuk komoditas pokok paling strategis."),
    rekomendasi=[
        {"aksi": "Perkuat cadangan beras pemerintah untuk menyerap lonjakan",
         "langkah": [
             "Dengan tren +21%/6 tahun, hitung kebutuhan cadangan beras 6–12 bulan konsumsi.",
             "Tingkatkan kapasitas gudang Bulog sesuai hitungan.",
             "Tetapkan aturan rilis: lepas stok bila harga grosir naik > 5% dalam sebulan.",
         ],
         "metrik": "Cadangan beras ≥ 6 bulan konsumsi; harga grosir stabil ±5%",
         "pemilik": "Bulog (pengelola), Bapanas (kebijakan)"},
        {"aksi": "Tingkatkan produksi padi nasional",
         "langkah": [
             "Karena harga naik menandakan pasokan tak mengimbangi permintaan, targetkan kenaikan produksi.",
             "Fokus pada peningkatan produktivitas (benih, irigasi, mekanisasi).",
             "Kurangi alih fungsi lahan sawah produktif.",
         ],
         "metrik": "Produksi padi +3%/tahun; harga grosir stabil",
         "pemilik": "Kementerian Pertanian"},
        {"aksi": "Pantau harga grosir bulanan sebagai indikator awal",
         "langkah": [
             "Jadikan harga grosir (leading) indikator sebelum harga eceran.",
             "Tetapkan ambang peringatan dini (kenaikan > 3% sebulan).",
             "Sebarkan sinyal ke TPID regional.",
         ],
         "metrik": "Sinyal keluar ≥ 30 hari sebelum lonjakan eceran",
         "pemilik": "BPS + Bapanas"},
    ],
    risiko=(
        "Beras adalah komoditas paling politis & berpengaruh terhadap inflasi. "
        "Kenaikan berkelanjutan tanpa intervensi berisiko memicu lonjakan harga "
        "eceran, tekanan daya beli, dan ketidakstabilan sosial."),
    tingkat="kritis",
)

register(
    "alert",
    kesimpulan=(
        "Sistem alert otomatis mendeteksi akselerasi inflasi pangan: Thailand "
        "(+4.8 poin, 2022) dan Indonesia (+2.6 poin, 2022). Tidak ada alert "
        "untuk periode terkini, menandakan kondisi 2024-2026 relatif stabil."),
    rekomendasi=[
        {"aksi": "Jadikan ambang alert sebagai pemicu tindakan otomatis",
         "langkah": [
             "Hubungkan alert ke alur kerja operasi pasar (bukan sekadar peringatan).",
             "Definisikan aksi otomatis per tingkat alert.",
             "Uji end-to-end alert→aksi tahunan.",
         ],
         "metrik": "100% alert kritis memicu aksi dalam ≤ 7 hari",
         "pemilik": "TPID + Bapanas"},
        {"aksi": "Sesuaikan ambang alert per negara/daerah",
         "langkah": [
             "Hitung volatilitas historis tiap negara/daerah.",
             "Tetapkan ambang kontekstual (bukan satu ambang global).",
             "Kalibrasi ulang setiap semester.",
         ],
         "metrik": "False alarm turun < 10%",
         "pemilik": "Tim data Bapanas"},
        {"aksi": "Audit alert yang terlewat",
         "langkah": [
             "Bandingkan alert dengan kejadian inflasi aktual.",
             "Identifikasi false negative dan penyebabnya.",
             "Perbaiki aturan deteksi.",
         ],
         "metrik": "Tidak ada lonjakan besar tanpa alert sebelumnya",
         "pemilik": "Tim data Bapanas"},
    ],
    risiko=(
        "Alert tanpa tindakan hanyalah informasi. Jika pemicu diabaikan saat "
        "akselerasi terjadi, momen kritis berlalu sebelum kebijakan diambil — "
        "persis saat intervensi paling dibutuhkan."),
    tingkat="sedang",
)

register(
    "spike",
    kesimpulan=(
        "Lonjakan harga historis terbesar: Vietnam 2008 (+23.1%), Indonesia 2006 "
        "(+13.1%). Semua lonjakan terbesar terjadi pada periode krisis pangan "
        "global (2007-2008) — menegaskan kerentanan struktural terhadap guncangan "
        "eksternal."),
    rekomendasi=[
        {"aksi": "Bangun sistem peringatan dini berbasis harga pangan dunia",
         "langkah": [
             "Pantau harga gandum, minyak, dan pupuk dunia bulanan.",
             "Tetapkan ambang pemicu (kenaikan > 15%/bulan).",
             "Terjemahkan sinyal global menjadi proyeksi harga domestik.",
         ],
         "metrik": "Peringatan keluar ≥ 1 bulan sebelum harga domestik naik",
         "pemilik": "Bank Indonesia + Bapanas"},
        {"aksi": "Perkuat cadangan & diversifikasi SEBELUM siklus krisis berikutnya",
         "langkah": [
             "Karena krisis berulang ~per dekade (2008, 2022), jadwalkan pengisian cadangan di periode tenang.",
             "Diversifikasi pemasok jauh sebelum krisis.",
             "Simulasi skenario krisis setiap 2 tahun.",
         ],
         "metrik": "Cadangan penuh sebelum musim krisis berikutnya",
         "pemilik": "Bulog + Kemendag"},
        {"aksi": "Pelajari pola 2008 untuk antisipasi skenario serupa",
         "langkah": [
             "Petakan rantai: bahan bakar naik → pupuk naik → pangan naik.",
             "Identifikasi titik intervensi paling efektif dalam rantai itu.",
             "Siapkan kebijakan mitigasi di titik tersebut.",
         ],
         "metrik": "Playbook krisis pangan diperbarui & diuji",
         "pemilik": "Bappenas + Bapanas"},
    ],
    risiko=(
        "Krisis pangan datang secara berkala (2008, 2022). Tanpa kesiapan "
        "struktural, Indonesia akan terperangkap pola yang sama: lonjakan harga, "
        "respons panik, pemulihan lambat — berulang setiap dekade."),
    tingkat="tinggi",
)

# --- Decision engine: keputusan terukur (skor + tier + justifikasi) ---
register(
    "decision",
    kesimpulan=(
        "Selain narasi, sistem kini menghasilkan SKOR KEPUTUSAN numerik per item "
        "(anomali/negara/ticker/metrik) berbasis sinyal berbobot, lalu memetakan "
        "ke TIER AKSI via ambang. Keputusan dapat dibandingkan & diurutkan."),
    rekomendasi=[
        {"aksi": "Jalankan item dengan tier prioritas tertinggi lebih dulu",
         "langkah": [
             "Urutkan skor keputusan menurun.",
             "Alokasikan sumber daya ke tier tertinggi lebih dulu.",
             "Catat tindak lanjut per item.",
         ],
         "metrik": "100% item tier tertinggi ditindaklanjuti ≤ 14 hari",
         "pemilik": "Manajer program"},
        {"aksi": "Sesuaikan bobot sinyal & ambang tier sesuai kebijakan",
         "langkah": [
             "Tinjau bobot sinyal bersama pemangku kepentingan.",
             "Uji sensitivitas keputusan terhadap perubahan bobot.",
             "Perbarui ambang tier di config.",
         ],
         "metrik": "Dokumentasi bobot & ambang diperbarui semesteran",
         "pemilik": "Tim analitik"},
        {"aksi": "Audit tiap keputusan lewat skor & justifikasi",
         "langkah": [
             "Simpan skor + justifikasi setiap keputusan.",
             "Tinjau kasus di mana skor tinggi tak ditindaklanjuti.",
             "Perbaiki formulasi sinyal bila perlu.",
         ],
         "metrik": "Jejak audit lengkap untuk 100% keputusan",
         "pemilik": "Tim audit internal"},
    ],
    risiko=(
        "Keputusan tanpa skor terukur cenderung subjektif & tidak konsisten. "
        "Namun skor pun bisa salah bila formulasi sinyal keliru — karena itu "
        "setiap keputusan menyertakan justifikasi yang dapat diaudit."),
    tingkat="tinggi",
)

# --------------------------------------------------------------------------
# Chart ECharts (v2) — insight & rekomendasi.
# --------------------------------------------------------------------------

register(
    "echarts_boxplot",
    kesimpulan=(
        "Boxplot inflasi pangan antar-negara per tahun menunjukkan MEDIAN, "
        "SEBARAN, dan PENCILAN. Kotak tinggi = inflasi antar-negara sangat "
        "beragam (satu negara melonjak saat lain tenang); titik jauh = negara "
        "dengan kejutan inflasi ekstrem. Ini mengungkap ketidakseragaman yang "
        "tak terlihat dari rata-rata ASEAN."),
    rekomendasi=[
        {"aksi": "Identifikasi tahun dengan sebaran terlebar sebagai periode risiko regional",
         "langkah": [
             "Hitung rentang antar-kuartil tiap tahun.",
             "Tandai tahun dengan IQR tertinggi (mis. 2008, 2022).",
             "Perkuat koordinasi kebijakan pada periode serupa.",
         ],
         "metrik": "Rencana kesiapan regional siap sebelum periode risiko berikutnya",
         "pemilik": "Sekretariat ASEAN + Bapanas"},
        {"aksi": "Selidiki negara pencilan tiap tahun",
         "langkah": [
             "Tandai titik di luar whisker sebagai pencilan.",
             "Analisis pemicu (gagal panen, kebijakan ekspor, kurs).",
             "Dokumentasikan pelajaran.",
         ],
         "metrik": "Laporan analisis pencilan tahunan",
         "pemilik": "Tim riset Bapanas"},
        {"aksi": "Gunakan sebaran, bukan rata-rata, untuk ambang peringatan",
         "langkah": [
             "Hitung sebaran antar-negara tiap periode.",
             "Tetapkan ambang berbasis persentil, bukan rata-rata.",
             "Tinjau ambang berkala.",
         ],
         "metrik": "Ambang peringatan selaras dengan sebaran aktual",
         "pemilik": "Tim data Bapanas"},
    ],
    risiko=(
        "Kebijakan berbasis rata-rata ASEAN mengabaikan negara yang paling "
        "terpukul. Bantuan/antisipasi bisa salah sasaran saat sebaran justru "
        "sedang paling lebar."),
    tingkat="tinggi",
)

register(
    "echarts_parallel",
    kesimpulan=(
        "Parallel coordinates membandingkan inflasi, produksi pangan, dan "
        "ketergantungan impor sekaligus untuk tiap negara. Garis yang menyilang "
        "tajam menandakan kombinasi tak biasa — mis. inflasi rendah tetapi impor "
        "tinggi (rentan guncangan global) atau produksi tinggi namun inflasi "
        "tetap naik (masalah distribusi)."),
    rekomendasi=[
        {"aksi": "Tandai negara paling rentan (impor tinggi + produksi rendah)",
         "langkah": [
             "Plot profil tiap negara pada 3 dimensi.",
             "Identifikasi kuadran impor-tinggi/produksi-rendah.",
             "Prioritaskan bantuan teknis ke negara tersebut.",
         ],
         "metrik": "Daftar negara rentan dipublikasikan tahunan",
         "pemilik": "Sekretariat ASEAN"},
        {"aksi": "Bandingkan profil antar-tahun",
         "langkah": [
             "Simpan profil multi-indikator tiap tahun.",
             "Deteksi negara yang membaik/memburuk struktural.",
             "Fokuskan intervensi pada yang memburuk.",
         ],
         "metrik": "Tren profil dipantau tahunan",
         "pemilik": "Tim data regional"},
        {"aksi": "Susun prioritas kerja sama pangan regional dari profil ini",
         "langkah": [
             "Kelompokkan negara berdasarkan profil serupa.",
             "Rancang program kerja sama per kelompok.",
             "Tetapkan target bersama.",
         ],
         "metrik": "Program kerja sama berbasis profil dijalankan",
         "pemilik": "Kementerian Luar Negeri"},
    ],
    risiko=(
        "Menilai ketahanan pangan dari satu indikator (mis. inflasi saja) "
        "menyesatkan. Negara bisa tampak aman di inflasi namun sangat bergantung "
        "impor — rentan saat pasokan global terganggu."),
    tingkat="sedang",
)

register(
    "echarts_calendar",
    kesimpulan=(
        "Calendar heatmap memetakan inflasi pangan BULANAN: pola musiman "
        "(lonjakan menjelang Ramadan/Idul Fitri, musim tanam) langsung terlihat "
        "sebagai blok merah berulang. Ini mengubah inflasi dari angka tahunan "
        "menjadi pola yang bisa diantisipasi."),
    rekomendasi=[
        {"aksi": "Siapkan stok penyangga sebelum bulan berpola lonjakan",
         "langkah": [
             "Ekstrak bulan dengan inflasi tertinggi dari data bulanan.",
             "Jadwalkan pengisian stok 2–4 pekan sebelum bulan itu.",
             "Pastikan logistik siap di wilayah rawan.",
         ],
         "metrik": "Stok penyangga penuh sebelum bulan puncak",
         "pemilik": "Bulog + Pemda"},
        {"aksi": "Bandingkan pola musiman antar-tahun",
         "langkah": [
             "Susun calendar heatmap multi-tahun.",
             "Deteksi apakah musiman tetap atau bergeser.",
             "Sesuaikan jadwal intervensi bila bergeser.",
         ],
         "metrik": "Jadwal intervensi diperbarui tiap tahun",
         "pemilik": "Tim data Bapanas"},
        {"aksi": "Fokuskan pemantauan pada bulan berisiko tinggi",
         "langkah": [
             "Tingkatkan frekuensi pemantauan di bulan puncak.",
             "Siapkan tim siaga pada periode tersebut.",
             "Laporkan harian saat bulan puncak.",
         ],
         "metrik": "Pemantauan harian aktif di bulan puncak",
         "pemilik": "TPID"},
    ],
    risiko=(
        "Membaca inflasi hanya tahunan menyembunyikan puncak musiman. Tanpa "
        "antisipasi bulanan, lonjakan harga bisa terjadi sebelum intervensi "
        "(terlambat) dan lebih lama dirasakan konsumen."),
    tingkat="sedang",
)

# --------------------------------------------------------------------------
# Perbaikan: key yang dipanggil dashboard tapi belum terdaftar (kotak insight
# sebelumnya kosong diam-diam).
# --------------------------------------------------------------------------

register(
    "rank_evolution",
    kesimpulan=(
        "Peta evolusi peringkat inflasi per tahun memperlihatkan konsistensi: "
        "negara yang peringkatnya relatif stabil punya rezim harga yang mapan, "
        "sementara naik-turun tajam menandakan kerentanan terhadap guncangan "
        "(pangan global, kurs, kebijakan). Peringkat mengabstraksi besaran, jadi "
        "selalu baca bersama angka inflasinya."),
    rekomendasi=[
        {"aksi": "Tandai negara dengan peringkat berfluktuasi sebagai prioritas pantau",
         "langkah": [
             "Hitung rentang peringkat tiap negara 5 tahun terakhir.",
             "Negara dengan rentang > 2 tingkat masuk daftar pantau.",
             "Selidiki sumber ketidakstabilannya.",
         ],
         "metrik": "Daftar pantau diperbarui tahunan",
         "pemilik": "Tim data regional"},
        {"aksi": "Gali praktik negara yang membaik konsisten",
         "langkah": [
             "Identifikasi negara yang peringkatnya naik konsisten.",
             "Kaji kebijakan harga pangannya.",
             "Jadikan kandidat pembelajaran regional.",
         ],
         "metrik": "Minimal 1 studi kasus kebijakan per tahun",
         "pemilik": "Bapanas"},
        {"aksi": "Jangan ambil keputusan hanya dari peringkat",
         "langkah": [
             "Selalu validasi dengan besaran inflasi aktual.",
             "Bedakan peringkat 1 dari 5 dengan selisih tipis vs lebar.",
             "Sertakan margin selisih dalam laporan.",
         ],
         "metrik": "Laporan selalu menyertakan selisih absolut, bukan hanya peringkat",
         "pemilik": "Tim analitik"},
    ],
    risiko=(
        "Peringkat menyembunyikan jarak antar-negara: perubahan peringkat bisa "
        "terjadi tanpa perubahan inflasi yang berarti. Mengandalkan peringkat "
        "saja berisiko salah membaca stabilitas."),
    tingkat="sedang",
)
