// =============================================================================
// LAPORAN FASILITATOR / INSTRUKTUR DAERAH (INDA)
// PELATIHAN PETUGAS PENGOLAHAN PETA WILKERSTAT SE2026
// BPS KABUPATEN MEMPAWAH
// =============================================================================

#set document(
  title: "Laporan Pelatihan Petugas Pengolahan Peta Wilkerstat SE2026",
  author: "Ihza Fikri Zaki Karunia, S.Tr.Stat. - BPS Kabupaten Mempawah"
)

#set text(font: "Liberation Sans", size: 10pt, fill: rgb("#000000"), lang: "id")
#set par(justify: true, leading: 0.65em)

#let nama-inda = "Ihza Fikri Zaki Karunia, S.Tr.Stat."
#let nip-inda = "199910282023021005"
#let jabatan-inda = "Pranata Komputer Ahli Pertama"
#let satker = "BPS Kabupaten Mempawah"
#let tgl-pelatihan = "23 s.d. 24 September 2026"
#let tgl-laporan = "Mempawah, 07 Oktober 2026"

#set page(
  paper: "a4",
  numbering: "1",
  number-align: right
)

// =============================================================================
// HALAMAN 1: SURAT PENGANTAR LAPORAN (SESUAI TEMPLATE RESMI PUSDIKLAT BPS)
// =============================================================================
#set page(
  margin: (top: 2.2cm, bottom: 2.2cm, left: 2.5cm, right: 2.2cm),
  header: none
)

#align(center)[
  #text(11pt, weight: "bold")[
    LAPORAN PELATIHAN FASILITATOR PELATIHAN PETUGAS PENGOLAHAN PETA WILKERSTAT SE2026
  ]
]

#v(14pt)
#align(right)[
  #tgl-laporan
]
#v(6pt)

#grid(
  columns: (55pt, 8pt, 1fr),
  gutter: 3pt,
  [Perihal], [:], [*Laporan Pelatihan Petugas Pengolahan Peta Wilkerstat SE2026*]
)

#v(14pt)
Kepada Yang Terhormat: \
*Kepala Pusdiklat BPS* \
di \
#pad(left: 12pt)[Tempat]

#v(14pt)
Bersama ini kami sampaikan laporan Instruktur Daerah (Inda) pada Kelas Pelatihan Petugas Pengolahan Peta Wilkerstat SE2026 BPS Kabupaten Mempawah:

#v(6pt)
#pad(left: 14pt)[
  #grid(
    columns: (115pt, 10pt, 1fr),
    gutter: 4pt,
    [Nama Inda], [:], [*#nama-inda*],
    [NIP], [:], [#nip-inda],
    [Jabatan], [:], [#jabatan-inda],
    [Unit Kerja], [:], [#satker],
    [Waktu Pelatihan], [:], [#tgl-pelatihan],
    [Tempat Pelaksanaan], [:], [Kantor BPS Kabupaten Mempawah]
  )
]

#v(10pt)
Kelengkapan laporan terlampir sebagai berikut:
#pad(left: 14pt)[
  1. Screen Shoot Bahan Ajar, sesuai mata pelatihan sebanyak 4 slide, dapat dilihat pada *Lampiran 1*.
  2. Daftar hadir harian pengajar sesuai jadwal mengajar dapat dilihat pada *Lampiran 2*.
  3. Jadwal Pelatihan dapat dilihat pada *Lampiran 3*.
  4. Daftar Permasalahan (Q&A) atau Notulensi selama pelatihan dapat dilihat pada *Lampiran 4*.
  5. Foto/Screen Shoot selama sesi pelatihan yang diampu, dapat dilihat pada *Lampiran 5*.
]

#v(10pt)
Demikian laporan yang dapat disampaikan untuk dijadikan bahan evaluasi.

#v(12pt)
#grid(
  columns: (1fr, 220pt),
  gutter: 10pt,
  [
    #v(60pt)
    #text(8.5pt)[
      *Tembusan:* \
      Kepala BPS Kabupaten Mempawah
    ]
  ],
  [
    #align(left)[
      Instruktur Daerah Pelatihan Petugas \
      Pengolahan Wilkerstat SE2026 \
      BPS Kabupaten Mempawah,
      #v(2pt)
      #image("assets/ttd_ihza_karunia.png", width: 85pt)
      #v(2pt)
      #underline[*#nama-inda*] \
      NIP. #nip-inda
    ]
  ]
)

// =============================================================================
// HALAMAN 2: LAMPIRAN 1 - SCREEN SHOOT BAHAN AJAR (4 SLIDE)
// =============================================================================
#pagebreak()
#set page(
  margin: (top: 2.0cm, bottom: 2.0cm, left: 2.2cm, right: 2.2cm),
  header: [
    #align(right)[
      #text(8.5pt, fill: rgb("#555555"))[Lampiran 1: Bahan Ajar Pelatihan Inda Wilkerstat SE2026]
    ]
    #v(2pt)
    #line(length: 100%, stroke: 0.5pt + rgb("#aaaaaa"))
  ]
)

#v(4pt)
#align(center)[
  #text(10.5pt, weight: "bold")[LAMPIRAN 1: SCREEN SHOOT BAHAN AJAR (4 SLIDE)] \
  #text(9pt)[Pelatihan Petugas Pengolahan Peta Wilkerstat SE2026 BPS Kabupaten Mempawah]
]
#v(10pt)

#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  
  // SLIDE 1
  block(
    stroke: 0.5pt + rgb("#777777"),
    inset: 4pt,
    width: 100%,
    [
      #image("assets/slides/slide_modul_01-01.png", width: 100%)
      #v(3pt)
      #text(8pt, weight: "bold")[Slide 1: Modul 01 - Pendahuluan & Organisasi Pengolahan] \
      #text(7.5pt)[Pengenalan kerangka geospasial Wilkerstat SE2026 dan peran tim pengolahan peta digital.]
    ]
  ),

  // SLIDE 2
  block(
    stroke: 0.5pt + rgb("#777777"),
    inset: 4pt,
    width: 100%,
    [
      #image("assets/slides/slide_modul_02-04.png", width: 100%)
      #v(3pt)
      #text(8pt, weight: "bold")[Slide 2: Modul 02 - Konsep & Definisi Wilayah Kerja] \
      #text(7.5pt)[Kaidah penetapan batas Satuan Lingkungan Setempat (SLS), Sub-SLS, dan Non-SLS.]
    ]
  ),

  // SLIDE 3
  block(
    stroke: 0.5pt + rgb("#777777"),
    inset: 4pt,
    width: 100%,
    [
      #image("assets/slides/slide_modul_07_1-08.png", width: 100%)
      #v(3pt)
      #text(8pt, weight: "bold")[Slide 3: Modul 07 - Editing Peta & Snapping Geometri] \
      #text(7.5pt)[Praktik digitasi di QGIS, konfigurasi snapping tolerance, dan pemotongan poligon batas.]
    ]
  ),

  // SLIDE 4
  block(
    stroke: 0.5pt + rgb("#777777"),
    inset: 4pt,
    width: 100%,
    [
      #image("assets/slides/slide_modul_07_2-15.png", width: 100%)
      #v(3pt)
      #text(8pt, weight: "bold")[Slide 4: Modul 07 - Validasi Topologi Geometri] \
      #text(7.5pt)[Pemeriksaan kesalahan batas menggunakan Topology Checker (target Zero Error topologi).]
    ]
  )
)

// =============================================================================
// HALAMAN 3: LAMPIRAN 2 - DAFTAR HADIR HARIAN PENGAJAR (18 OJP)
// =============================================================================
#pagebreak()
#set page(
  margin: (top: 2.0cm, bottom: 2.0cm, left: 2.2cm, right: 2.2cm),
  header: [
    #align(right)[
      #text(8.5pt, fill: rgb("#555555"))[Lampiran 2: Daftar Hadir Harian Pengajar Pelatihan Wilkerstat SE2026]
    ]
    #v(2pt)
    #line(length: 100%, stroke: 0.5pt + rgb("#aaaaaa"))
  ]
)

#v(4pt)
#align(center)[
  #text(10.5pt, weight: "bold")[LAMPIRAN 2: DAFTAR HADIR HARIAN PENGAJAR (18 OJP)] \
  #text(9pt)[Pelatihan Petugas Pengolahan Peta Wilkerstat SE2026 BPS Kabupaten Mempawah]
]
#v(10pt)

#grid(
  columns: (95pt, 8pt, 1fr),
  gutter: 3pt,
  [Nama Pengajar], [:], [*#nama-inda*],
  [NIP], [:], [#nip-inda],
  [Jabatan], [:], [#jabatan-inda],
  [Waktu Pelaksanaan], [:], [#tgl-pelatihan],
  [Tempat], [:], [Kantor BPS Kabupaten Mempawah]
)

#v(10pt)
#set text(size: 8.5pt)
#table(
  columns: (22pt, 80pt, 65pt, 1fr, 32pt, 65pt),
  inset: (x: 5pt, y: 5pt),
  align: (center + horizon, left + horizon, center + horizon, left + horizon, center + horizon, center + horizon),
  stroke: (x, y) => 0.5pt + rgb("#000000"),
  
  table.header(
    [*No*], [*Hari, Tanggal*], [*Waktu (WIB)*], [*Materi / Pokok Bahasan*], [*OJP*], [*Tanda Tangan*]
  ),
  
  [1], [Rabu, 23 Sept 2026], [08.30 - 09.30], [Pembukaan & Pre-Test Pemetaan Spasial], [2], [ttd],
  [2], [Rabu, 23 Sept 2026], [09.30 - 10.30], [Modul 01 - 03: Konsep Wilkerstat & Batas SLS], [2], [ttd],
  [3], [Rabu, 23 Sept 2026], [10.30 - 12.00], [Modul 05: Master SLS & Kodifikasi Wilayah], [2], [ttd],
  [4], [Rabu, 23 Sept 2026], [13.00 - 14.30], [Modul 04: Setup QGIS 3.44 & CRS EPSG:4326], [2], [ttd],
  [5], [Rabu, 23 Sept 2026], [14.30 - 17.00], [Modul 07: Praktik Digitasi & Snap Geometri], [2], [ttd],
  [6], [Kamis, 24 Sept 2026], [08.30 - 10.00], [Bedah Kasus: Pemekaran SLS, Batas Gap/Overlap], [2], [ttd],
  [7], [Kamis, 24 Sept 2026], [10.00 - 12.00], [Modul 07: Praktik Mandiri Pengolahan Peta], [2], [ttd],
  [8], [Kamis, 24 Sept 2026], [13.00 - 14.30], [Validasi Topologi Geometri (Target 0 Error)], [2], [ttd],
  [9], [Kamis, 24 Sept 2026], [14.30 - 16.30], [Post-Test, Evaluasi Hasil, Penutupan & BA], [2], [ttd],

  table.cell(colspan: 4, align: right + horizon)[*Total Jam Pelajaran (OJP) Mengajar:*],
  table.cell(align: center + horizon)[*18*],
  table.cell(align: center + horizon)[*Lengkap*]
)

#v(14pt)
#align(right)[
  #block(width: 220pt)[
    #align(center)[
      Mempawah, 24 September 2026 \
      *Instruktur Daerah (Inda)*
      #v(2pt)
      #image("assets/ttd_ihza_karunia.png", width: 85pt)
      #v(2pt)
      #underline[*#nama-inda*] \
      NIP. #nip-inda
    ]
  ]
]

// =============================================================================
// HALAMAN 4: LAMPIRAN 2 (LANJUTAN) - BUKTI FISIK SCAN DAFTAR HADIR
// =============================================================================
#pagebreak()
#set page(
  margin: (top: 2.0cm, bottom: 2.0cm, left: 2.2cm, right: 2.2cm),
  header: [
    #align(right)[
      #text(8.5pt, fill: rgb("#555555"))[Lampiran 2 (Lanjutan): Bukti Fisik Lembar Daftar Hadir]
    ]
    #v(2pt)
    #line(length: 100%, stroke: 0.5pt + rgb("#aaaaaa"))
  ]
)

#v(4pt)
#align(center)[
  #text(10.5pt, weight: "bold")[BUKTI FISIK LEMBAR DAFTAR HADIR PELATIHAN TATAP MUKA] \
  #text(9pt)[Hari ke-1 (23 September 2026) & Hari ke-2 (24 September 2026) | BPS Kabupaten Mempawah]
]
#v(8pt)

#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  [
    #align(center)[
      #text(8.5pt, weight: "bold")[Hari ke-1: Rabu, 23 September 2026]
      #v(3pt)
      #block(
        stroke: 0.5pt + rgb("#777777"),
        inset: 2pt,
        image("assets/daftar_hadir_23_september.jpg", width: 100%, height: 490pt, fit: "contain")
      )
    ]
  ],
  [
    #align(center)[
      #text(8.5pt, weight: "bold")[Hari ke-2: Kamis, 24 September 2026]
      #v(3pt)
      #block(
        stroke: 0.5pt + rgb("#777777"),
        inset: 2pt,
        image("assets/daftar_hadir_24_september.jpg", width: 100%, height: 490pt, fit: "contain")
      )
    ]
  ]
)

#v(6pt)
#align(center)[
  #text(8pt, style: "italic")[
    Lembar presensi resmi memuat tanda tangan lengkap peserta mitra (Septiana Jumakhirus S., Rohmi, Yusron), \
    pengajar/Inda (Ihza Fikri Zaki Karunia, S.Tr.Stat.), dan pembuat daftar (Akma Bamsyia J.).
  ]
]

// =============================================================================
// HALAMAN 5: LAMPIRAN 3 - JADWAL PELATIHAN
// =============================================================================
#pagebreak()
#set page(
  margin: (top: 2.0cm, bottom: 2.0cm, left: 2.2cm, right: 2.2cm),
  header: [
    #align(right)[
      #text(8.5pt, fill: rgb("#555555"))[Lampiran 3: Jadwal Pelatihan Wilkerstat SE2026]
    ]
    #v(2pt)
    #line(length: 100%, stroke: 0.5pt + rgb("#aaaaaa"))
  ]
)

#v(4pt)
#align(center)[
  #text(10.5pt, weight: "bold")[LAMPIRAN 3: JADWAL PELATIHAN PETUGAS PENGOLAHAN PETA] \
  #text(9pt)[Pelatihan Wilkerstat Sensus Ekonomi 2026 (SE2026) BPS Kabupaten Mempawah]
]
#v(8pt)

#text(8.5pt, weight: "bold")[Hari ke-1: Rabu, 23 September 2026]
#v(2pt)

#set text(size: 8pt)
#table(
  columns: (70pt, 1fr, 110pt, 65pt),
  inset: (x: 4.5pt, y: 3.5pt),
  align: (center + horizon, left + horizon, left + horizon, center + horizon),
  stroke: (x, y) => 0.5pt + rgb("#000000"),
  
  table.header(
    [*Waktu (WIB)*], [*Materi / Aktivitas Pelatihan*], [*Fasilitator / PJ*], [*Metode*]
  ),
  
  [08.00 - 08.30], [Registrasi Peserta, Administrasi, & Pembagian Starter Kit], [Panitia Pelatihan], [Tatap Muka],
  [08.30 - 09.00], [Pembukaan Resmi Pelatihan & Arahan Kebijakan SE2026], [Kepala BPS Kab. Mempawah], [Pleno],
  [09.00 - 09.30], [Pre-Test Pemahaman Konsep Pemetaan & Geometri Spasial], [Instruktur Daerah], [Ujian Mandiri],
  [09.30 - 10.30], [Modul 01 - 03: Konsep Wilkerstat, Batas SLS/Non-SLS, Regulasi], [Instruktur Daerah], [Paparan & Tanya Jawab],
  [10.30 - 12.00], [Modul 05: Master SLS, Kodifikasi ID SLS, dan Landmark], [Instruktur Daerah], [Simulasi Data],
  [12.00 - 13.00], [ISHOMA (Istirahat, Sholat, dan Makan Siang Bersama)], [Panitia & Peserta], [Istirahat],
  [13.00 - 14.30], [Modul 04: Setup GIS, Instalasi QGIS 3.44, CRS EPSG:4326], [Instruktur Daerah], [Praktik Komputer],
  [14.30 - 16.30], [Modul 07: Teknik Digitasi, Editing Batas, Snap Geometri], [Instruktur Daerah], [Praktik Mandiri],
  [16.30 - 17.00], [Review Hasil Hari 1, Evaluasi Geometri, dan Tugas Mandiri], [Instruktur Daerah], [Evaluasi]
)

#v(8pt)
#text(8.5pt, weight: "bold")[Hari ke-2: Kamis, 24 September 2026]
#v(2pt)

#table(
  columns: (70pt, 1fr, 110pt, 65pt),
  inset: (x: 4.5pt, y: 3.5pt),
  align: (center + horizon, left + horizon, left + horizon, center + horizon),
  stroke: (x, y) => 0.5pt + rgb("#000000"),
  
  table.header(
    [*Waktu (WIB)*], [*Materi / Aktivitas Pelatihan*], [*Fasilitator / PJ*], [*Metode*]
  ),
  
  [08.00 - 08.30], [Presensi Peserta & Pembahasan Tugas Mandiri], [Instruktur Daerah], [Diskusi Kelas],
  [08.30 - 10.00], [Pembahasan Kasus Khusus: Pemekaran SLS, Batas Gap & Overlap], [Instruktur Daerah], [Bedah Kasus],
  [10.00 - 12.00], [Modul 07: Praktik Mandiri Terbimbing Pengolahan Peta], [Instruktur Daerah], [Praktik Mandiri],
  [12.00 - 13.00], [ISHOMA (Istirahat, Sholat, dan Makan Siang Bersama)], [Panitia & Peserta], [Istirahat],
  [13.00 - 14.30], [Validasi Topologi Geometri (Target 0 Error) & Kendali Mutu], [Instruktur Daerah], [Quality Control],
  [14.30 - 15.30], [Evaluasi Akhir & Post-Test Kompetensi Pengolahan Wilkerstat], [Instruktur Daerah], [Ujian Mandiri],
  [15.30 - 16.30], [Penutupan Resmi Pelatihan, Penandatanganan BA, & Foto Bersama], [Kepala BPS & Inda], [Pleno]
)

// =============================================================================
// HALAMAN 6: LAMPIRAN 4 - DAFTAR PERMASALAHAN (Q&A) & NOTULENSI
// =============================================================================
#pagebreak()
#set page(
  margin: (top: 2.0cm, bottom: 2.0cm, left: 2.2cm, right: 2.2cm),
  header: [
    #align(right)[
      #text(8.5pt, fill: rgb("#555555"))[Lampiran 4: Notulensi & Q&A Pelatihan Wilkerstat SE2026]
    ]
    #v(2pt)
    #line(length: 100%, stroke: 0.5pt + rgb("#aaaaaa"))
  ]
)

#v(4pt)
#align(center)[
  #text(10.5pt, weight: "bold")[LAMPIRAN 4: DAFTAR PERMASALAHAN (Q&A) DAN NOTULENSI] \
  #text(9pt)[Pelatihan Petugas Pengolahan Peta Wilkerstat SE2026 BPS Kabupaten Mempawah]
]
#v(10pt)

#set text(size: 8.5pt)

#block(stroke: 0.5pt + rgb("#000000"), inset: 6pt, width: 100%)[
  *1. Penanganan Tumpang Tindih (Overlap) dan Celah (Gap) Batas SLS* \
  #v(2pt)
  *Pertanyaan Peserta (Sdr. Rohmi):* \
  Bagaimana cara tercepat dan paling aman saat membagi atau mendigitasi wilayah RT yang baru mekar tanpa memicu error overlap atau gap dengan RT tetangga?
  #v(2pt)
  *Tanggapan & Solusi Inda (Ihza Fikri Zaki Karunia, S.Tr.Stat.):* \
  Gunakan fitur Snapping Toolbar di QGIS. Pastikan opsi Snapping aktif pada mode *Vertex and Segment*, toleransi diatur 5 s.d. 10 piksel, serta centang opsi *Avoid Overlap on Active Layer*. Untuk memotong poligon induk, gunakan alat *Split Features*, bukan menggambar poligon baru dari awal, sehingga batas garis antar-poligon otomatis saling menempel sempurna (zero gap).
]
#v(6pt)

#block(stroke: 0.5pt + rgb("#000000"), inset: 6pt, width: 100%)[
  *2. Inkonsistensi Sistem Referensi Koordinat (CRS) Layer dan Citra Satelit* \
  #v(2pt)
  *Pertanyaan Peserta (Sdr. Yusron):* \
  Saat memasukkan basemap citra satelit Google atau OSM ke dalam peta kerja, layer batas SLS terlihat bergeser sejauh puluhan meter. Apa penyebabnya dan bagaimana standarnya?
  #v(2pt)
  *Tanggapan & Solusi Inda (Ihza Fikri Zaki Karunia, S.Tr.Stat.):* \
  Pergeseran terjadi karena perbedaan referensi CRS antara project QGIS (misal Pseudo-Mercator EPSG:3857) dan Shapefile Wilkerstat. Sesuai juknis resmi BPS RI, seluruh layer batas wilayah statistik wajib menggunakan Geographic CRS *WGS 84 / EPSG:4326*. Petugas diarahkan menyelaraskan CRS project ke EPSG:4326 dan mengaktifkan transformasi on-the-fly agar layer terproyeksikan secara presisi.
]
#v(6pt)

#block(stroke: 0.5pt + rgb("#000000"), inset: 6pt, width: 100%)[
  *3. Identifikasi Kawasan Perumahan Baru / Non-SLS Tanpa Pengurus RT Definitif* \
  #v(2pt)
  *Pertanyaan Peserta (Sdri. Septiana Jumakhirus Siska, S.Sos):* \
  Di kawasan pemukiman berkembang seperti Mempawah Hilir, terdapat perumahan baru yang sudah dihuni warga tetapi belum memiliki struktur RT resmi dari kelurahan. Bagaimana penanganannya?
  #v(2pt)
  *Tanggapan & Solusi Inda (Ihza Fikri Zaki Karunia, S.Tr.Stat.):* \
  Kawasan tersebut dikategorikan sebagai *Satuan Pemukiman / Non-SLS* atau dimasukkan sementara ke SLS induk yang menaungi secara administratif. Buat batas indikatif mengikuti fitur fisik terluar (jalan atau saluran air) dan berikan kode ID Non-SLS khusus (format sub-SLS 09xx) serta beri catatan khusus pada tabel atribut untuk diverifikasi saat listing lapangan SE2026.
]
#v(6pt)

#block(stroke: 0.5pt + rgb("#000000"), inset: 6pt, width: 100%)[
  *4. Validasi Geometri Peta Menggunakan Plugin Topology Checker Sebelum Submit* \
  #v(2pt)
  *Notulensi Evaluasi Akhir Kelas:* \
  Sebelum file Shapefile / GeoPackage diserahkan, seluruh peserta diwajibkan menjalankan plugin Topology Checker dengan 3 kaidah wajib: (1) _must not have duplicates_, (2) _must not have overlaps_, dan (3) _must not have gaps_. Pada akhir sesi praktik hari ke-2, seluruh petugas berhasil mencapai status *Zero Error (0 Kesalahan Topologi)*.
]

// =============================================================================
// HALAMAN 7: LAMPIRAN 5 - FOTO DOKUMENTASI PELATIHAN
// =============================================================================
#pagebreak()
#set page(
  margin: (top: 2.0cm, bottom: 2.0cm, left: 2.2cm, right: 2.2cm),
  header: [
    #align(right)[
      #text(8.5pt, fill: rgb("#555555"))[Lampiran 5: Foto Dokumentasi Pelatihan Wilkerstat SE2026]
    ]
    #v(2pt)
    #line(length: 100%, stroke: 0.5pt + rgb("#aaaaaa"))
  ]
)

#v(4pt)
#align(center)[
  #text(10.5pt, weight: "bold")[LAMPIRAN 5: FOTO DOKUMENTASI SESI PELATIHAN] \
  #text(9pt)[Pelatihan Petugas Pengolahan Peta Wilkerstat SE2026 BPS Kabupaten Mempawah]
]
#v(8pt)

#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  
  // FOTO 1
  block(
    stroke: 0.5pt + rgb("#777777"),
    inset: 4pt,
    [
      #image("assets/foto_hari_1_paparan.jpg", width: 100%, height: 135pt, fit: "cover")
      #v(3pt)
      #text(7.5pt, weight: "bold")[Foto 1: Sesi Paparan Materi & Regulasi Spasial (Hari 1)] \
      #text(7pt)[
        Instruktur Daerah Ihza Fikri Zaki Karunia memaparkan konsep Wilkerstat dan regulasi batas SLS melalui LCD proyektor di Ruang Rapat BPS Kabupaten Mempawah.
      ]
    ]
  ),
  
  // FOTO 2
  block(
    stroke: 0.5pt + rgb("#777777"),
    inset: 4pt,
    [
      #image("assets/foto_hari_1_praktik.jpg", width: 100%, height: 135pt, fit: "cover")
      #v(3pt)
      #text(7.5pt, weight: "bold")[Foto 2: Pendampingan Praktik Mandiri Komputer (Hari 1)] \
      #text(7pt)[
        Inda mendampingi langsung calon petugas dalam instalasi QGIS, konfigurasi snapping tolerance, dan simulasi digitasi poligon batas SLS.
      ]
    ]
  )
)

#v(10pt)

// FOTO 3
#align(center)[
  #block(
    stroke: 0.5pt + rgb("#777777"),
    inset: 5pt,
    width: 82%,
    [
      #image("assets/foto_hari_2_selfie.jpg", width: 100%, height: 160pt, fit: "cover")
      #v(4pt)
      #text(8pt, weight: "bold")[Foto 3: Sesi Praktik Terbimbing dan Evaluasi Akhir Bersama Peserta (Hari 2)] \
      #text(7.5pt)[
        Instruktur Daerah Ihza Fikri Zaki Karunia bersama peserta pengolahan peta (Rohmi, Yusron, Septiana Jumakhirus Siska) saat evaluasi akhir topologi geometri 0 error dan penutupan pelatihan.
      ]
    ]
  )
]
