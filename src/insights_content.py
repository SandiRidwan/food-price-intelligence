
# ---------------------------------------------------------------------------
# KONTEN INSIGHT — Food Price & Security Intelligence
# Sudut pandang: pemerintah / bank sentral / pelaku usaha yang menjaga
# stabilitas harga pangan & ketahanan pangan nasional.
# ---------------------------------------------------------------------------
from insight import register

register(
    "kpi",
    kesimpulan=(
        "Inflasi pangan Indonesia 1.91% (2025) — terkendali di bawah ambang 5%. "
        "Namun impor pangan ~10.2% dari total impor menunjukkan ketergantungan "
        "yang membuat harga domestik rentan terhadap guncangan global & kurs."),
    rekomendasi=[
        "Jaga inflasi di bawah ambang lewat operasi pasar terjadwal — angka saat "
        "ini sehat, jangan lengah saat musim paceklik.",
        "Kurangi ketergantungan impor dengan memperkuat produksi domestik "
        "(targetkan penurunan bertahap, mis. 1–2 poin per tahun).",
        "Lindungi harga dari gejolak kurs: pertimbangkan kontrak pasokan "
        "berjangka untuk komoditas impor kunci (gandum, kedelai).",
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
        "Bangun cadangan pangan strategis yang cukup menyerap 6–12 bulan "
        "guncangan — karena guncangan datang dari luar.",
        "Koordinasikan respons dengan negara ASEAN (karena pola guncangan sama), "
        "bukan bertindak sendiri-sendiri.",
        "Pantau indeks global (harga gandum, pupuk dunia) sebagai peringatan awal "
        "sebelum harga domestik naik.",
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
        "Pertahankan kebijakan moneter yang menyerap guncangan global — bukti "
        "menunjukkan penurunan inflasi berjalan baik setelah 2022.",
        "Siapkan protokol respons cepat saat inflasi mendekati ambang 5% "
        "(operasi pasar, subsidi terarah) — jangan tunggu melewati ambang.",
        "Dokumentasikan apa yang berhasil menurunkan inflasi 2022→2025 sebagai "
        "playbook untuk guncangan berikutnya.",
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
        "Jangan mengambil keputusan berbasis data produksi terakhir dari World "
        "Bank — ambil dari sumber domestik (BPS) yang lebih mutakhir.",
        "Investasi irigasi & teknologi benih agar tren naik berlanjut, bukan "
        "melambat karena keterbatasan lahan.",
        "Bangun sistem pelaporan produksi internal yang tidak bergantung pada "
        "lag publikasi internasional 1-2 tahun.",
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
        "Tetapkan target penurunan ketergantungan impor yang eksplisit & terukur "
        "(mis. ke 8% dalam 5 tahun), karena 'stabil' saja bukan keberhasilan.",
        "Fokus substitusi pada komoditas impor terbesar (gandum, kedelai, jagung)",
        "Diversifikasi sumber impor agar tidak bergantung pada 1-2 negara "
        "pemasok saja.",
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
        "Pelajari kebijakan Thailand (inflasi terendah) — pola produksi & "
        "distribusi mereka bisa jadi acuan.",
        "Waspadai Vietnam (tertinggi meski produsen beras besar) — contoh bahwa "
        "produksi tinggi tak otomatis menjamin harga stabil.",
        "Gunakan peringkat regional sebagai tolok ukur target, bukan hanya "
        "ambang absolut 5%.",
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
        "Jadwalkan operasi pasar SEBELUM Januari & Desember, bukan setelah harga naik.",
        "Prioritaskan stabilisasi di kota Indonesia timur (Luwuk, Kolaka, Tual) "
        "— inflasi bulanan tertinggi akibat biaya logistik.",
        "Gunakan data bulanan untuk respons CEPAT; data tahunan saja terlambat "
        "untuk mencegah lonjakan.",
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
        "Perkuat cadangan beras pemerintah (Bulog) untuk menyerap lonjakan, "
        "karena tren naik tampak berkelanjutan.",
        "Tingkatkan produksi padi nasional — kenaikan harga menandakan pasokan "
        "tidak mengimbangi permintaan.",
        "Pantau harga grosir bulanan sebagai indikator awal lonjakan harga eceran.",
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
        "Jadikan ambang alert sebagai pemicu tindakan otomatis (bukan sekadar "
        "peringatan): begitu tercapai, operasi pasar langsung berjalan.",
        "Sesuaikan ambang per negara/daerah — ambang tunggal mungkin tidak pas "
        "untuk semua konteks.",
        "Audit alert yang terlewat (jika ada) untuk menyempurnakan sistem.",
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
        "Bangun sistem peringatan dini berbasis harga pangan dunia (gandum, "
        "minyak, pupuk) — bukan hanya menunggu harga domestik naik.",
        "Perkuat cadangan & diversifikasi pasokan SEBELUM siklus krisis berikutnya.",
        "Pelajari pola 2008 untuk mengantisipasi skenario serupa (bahan bakar "
        "naik → pupuk naik → pangan naik).",
    ],
    risiko=(
        "Krisis pangan datang secara berkala (2008, 2022). Tanpa kesiapan "
        "struktural, Indonesia akan terperangkap pola yang sama: lonjakan harga, "
        "respons panik, pemulihan lambat — berulang setiap dekade."),
    tingkat="tinggi",
)
