// =============================================================================
// SURAT DINAS RESMI BPS KABUPATEN MEMPAWAH
// UNDANGAN PELATIHAN PETUGAS PENGOLAHAN PETA (WILKERSTAT) SE2026
// =============================================================================

#set document(
  title: "Surat Undangan Pelatihan Petugas Pengolahan Peta Wilkerstat SE2026",
  author: "BPS Kabupaten Mempawah"
)

#set text(font: "Liberation Sans", size: 10.5pt, lang: "id")
#set par(justify: true, leading: 0.65em)

// =============================================================================
// HALAMAN 1: SURAT DINAS UTAMA
// =============================================================================
#set page(
  paper: "a4",
  margin: (
    top: 4.4cm,
    bottom: 2.2cm,
    left: 2.2cm,
    right: 2.2cm
  ),
  header: [
    #v(0.6cm)
    #grid(
      columns: (56pt, 1fr, 88pt),
      gutter: 12pt,
      align: (center + horizon, left + horizon, right + horizon),
      image("/app/workspaces/bps-mempawah/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", width: 54pt),
      [
        #text(13pt, weight: "bold", style: "italic", font: "Liberation Sans", fill: rgb("#0a2540"))[BADAN PUSAT STATISTIK] \
        #text(13pt, weight: "bold", style: "italic", font: "Liberation Sans", fill: rgb("#0a2540"))[KABUPATEN MEMPAWAH] \
        #v(2pt)
        #text(8pt, font: "Liberation Sans", fill: rgb("#222222"))[Jalan Raden Kusno Nomor 59 Mempawah 78912; Telepon (0561) 691049;] \
        #text(8pt, font: "Liberation Sans", fill: rgb("#222222"))[Laman: https://mempawahkab.bps.go.id; Pos-el: bps6104\@bps.go.id]
      ],
      image("/app/workspaces/bps-mempawah/kegiatan/kecamatan-dalam-angka/2026/assets/logo_se2026.png", width: 86pt)
    )
    #v(3pt)
    #line(length: 100%, stroke: 2pt + rgb("#0a2540"))
  ]
)

#v(6pt)
#grid(
  columns: (1fr, 175pt),
  gutter: 10pt,
  [
    #grid(
      columns: (65pt, 8pt, 1fr),
      gutter: 3.5pt,
      [Nomor], [:], [B-1145/61040/VS.190/09/2026],
      [Sifat], [:], [Penting],
      [Lampiran], [:], [2 (dua) Berkas],
      [Hal], [:], [*Undangan Pelatihan Petugas Pengolahan Peta (Wilkerstat) Sensus Ekonomi 2026*]
    )
  ],
  [
    #align(right)[
      Mempawah, 22 September 2026
    ]
  ]
)

#v(10pt)
Yth. *Calon Petugas Pengolahan Peta Wilkerstat Sensus Ekonomi 2026:*
#v(2pt)
#pad(left: 14pt)[
  1. *Sdr. Rohmi*
  2. *Sdr. Yusron*
  3. *Sdri. Septiana Jumakhirus Siska, S.Sos*
]
#v(2pt)
di Tempat

#v(8pt)
Dengan hormat,

Dalam rangka persiapan pelaksanaan kegiatan Pengolahan Pemetaan dan Muatan Wilayah Kerja Statistik (Wilkerstat) Sensus Ekonomi 2026 (SE2026) di lingkungan Badan Pusat Statistik Kabupaten Mempawah, kami memandang perlu untuk meningkatkan kompetensi, pemahaman teknis, dan standardisasi kualitas spasial bagi calon petugas pengolahan peta digital.

Sehubungan dengan hal tersebut, Badan Pusat Statistik Kabupaten Mempawah mengundang Saudara/i untuk hadir secara langsung mengikuti *Pelatihan Petugas Pengolahan Peta (Wilkerstat) Sensus Ekonomi 2026* yang akan diselenggarakan pada:

#v(2pt)
#pad(left: 16pt)[
  #grid(
    columns: (95pt, 10pt, 1fr),
    gutter: 3.5pt,
    [*Hari, Tanggal*], [:], [*Rabu s.d. Kamis, 23 s.d. 24 September 2026*],
    [*Waktu*], [:], [08.00 s.d. 17.00 WIB (Hari I) \ 08.00 s.d. 16.30 WIB (Hari II)],
    [*Tempat*], [:], [*Kantor BPS Kabupaten Mempawah* \ Jalan Raden Kusno Nomor 59, Mempawah 78912],
    [*Agenda*], [:], [Pelatihan Teknis, Standardisasi Topologi Geometri, Praktik Mandiri Terbimbing, dan Evaluasi Akhir Pengolahan Wilkerstat SE2026],
    [*Pakaian*], [:], [Bebas Rapi Berkerah / Pakaian Dinas yang berlaku]
  )
]

#v(4pt)
Mengingat sangat pentingnya kegiatan ini guna menjamin akurasi dan validitas peta digital SLS/Non-SLS (_zero error topology_), Saudara/i dimohon untuk hadir tepat waktu sesuai jadwal terlampir. Akomodasi konsumsi selama pelatihan disediakan oleh BPS Kabupaten Mempawah.

Demikian undangan ini kami sampaikan. Atas perhatian, kesiapan, dan kerja sama Saudara/i, kami ucapkan terima kasih.

#v(14pt)
#set par(first-line-indent: 0pt)
#align(right)[
  #block(width: 230pt, breakable: false)[
    #align(left)[
      Kepala Badan Pusat Statistik \
      Kabupaten Mempawah, \
      #v(2pt)
      #image("/app/workspaces/bps-mempawah/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 44pt) \
      #v(2pt)
      *Munawir, S.E., M.M.*
    ]
  ]
]

// =============================================================================
// HALAMAN 2: LAMPIRAN I (DAFTAR PESERTA PELATIHAN)
// =============================================================================
#pagebreak()
#set page(
  margin: (
    top: 2.5cm,
    bottom: 2.2cm,
    left: 2.2cm,
    right: 2.2cm
  ),
  header: none
)

#grid(
  columns: (70pt, 8pt, 1fr),
  gutter: 3pt,
  [Lampiran I], [:], [Surat Undangan Pelatihan Petugas Pengolahan Peta SE2026],
  [Nomor], [:], [B-1145/61040/VS.190/09/2026],
  [Tanggal], [:], [22 September 2026]
)

#v(14pt)
#align(center)[
  #text(11pt, weight: "bold")[DAFTAR PESERTA PELATIHAN PETUGAS PENGOLAHAN PETA \ WILKERSTAT SENSUS EKONOMI 2026 (SE2026)] \
  #text(9.5pt, style: "italic")[BPS Kabupaten Mempawah]
]
#v(12pt)

#set text(size: 9pt)
#table(
  columns: (30pt, 160pt, 90pt, 140pt, 75pt),
  inset: (x: 6pt, y: 7pt),
  align: (center + horizon, left + horizon, center + horizon, left + horizon, center + horizon),
  fill: (col, row) => if row == 0 { rgb("#0a2540") } else if calc.even(row) { rgb("#f8fafc") } else { none },
  stroke: (x, y) => 0.5pt + rgb("#cbd5e1"),
  
  // Header Table (Ukuran font konsisten 9pt)
  table.header(
    [#text(fill: white, weight: "bold")[No]],
    [#text(fill: white, weight: "bold")[Nama Lengkap]],
    [#text(fill: white, weight: "bold")[ID SOBAT]],
    [#text(fill: white, weight: "bold")[Alamat Domisili]],
    [#text(fill: white, weight: "bold")[Keterangan]]
  ),
  
  // Data Rows (Ukuran font konsisten 9pt)
  [1],
  [*Rohmi*],
  [610422100188],
  [Kelurahan Tengah, Kec. Mempawah Hilir],
  [Peserta],
  
  [2],
  [*Yusron*],
  [610422040002],
  [Desa Antibar, Kec. Mempawah Timur],
  [Peserta],
  
  [3],
  [*Septiana Jumakhirus Siska, S.Sos*],
  [610425110042],
  [Kelurahan Tengah, Kec. Mempawah Hilir],
  [Peserta]
)

#v(14pt)
#text(9pt, weight: "bold")[Catatan Peserta:]
#pad(left: 10pt)[
  #text(9pt)[
    1. Peserta diwajibkan hadir tepat waktu sesuai dengan jadwal dan rundown yang telah ditetapkan.
    2. Peserta mematuhi seluruh tata tertib kegiatan pelatihan serta arahan dari panitia dan instruktur.
  ]
]

// =============================================================================
// HALAMAN 3: LAMPIRAN II (JADWAL & RUNDOWN PELATIHAN)
// =============================================================================
#pagebreak()
#set page(
  margin: (
    top: 2.2cm,
    bottom: 2.0cm,
    left: 2.2cm,
    right: 2.2cm
  ),
  header: none
)

#grid(
  columns: (70pt, 8pt, 1fr),
  gutter: 3pt,
  [Lampiran II], [:], [Jadwal & Rundown Pelatihan Petugas Pengolahan Peta SE2026],
  [Nomor], [:], [B-1145/61040/VS.190/09/2026],
  [Tanggal], [:], [22 September 2026]
)

#v(8pt)
#align(center)[
  #text(11pt, weight: "bold")[JADWAL DAN RUNDOWN PELATIHAN PETUGAS PENGOLAHAN \ WILKERSTAT SENSUS EKONOMI 2026 (SE2026)] \
  #text(9pt, style: "italic")[Tanggal 23 s.d. 24 September 2026 | Kantor BPS Kabupaten Mempawah]
]
#v(8pt)

#text(9.5pt, weight: "bold", fill: rgb("#0a2540"))[Hari ke-1: Rabu, 23 September 2026]
#v(2pt)

#set text(size: 8.5pt)
#table(
  columns: (75pt, 1fr, 120pt, 65pt),
  inset: (x: 5pt, y: 4pt),
  align: (center + horizon, left + horizon, left + horizon, center + horizon),
  fill: (col, row) => if row == 0 { rgb("#0a2540") } else if calc.even(row) { rgb("#f8fafc") } else { none },
  stroke: (x, y) => 0.4pt + rgb("#cbd5e1"),
  
  // Header Table (Ukuran font konsisten 8.5pt)
  table.header(
    [#text(fill: white, weight: "bold")[Waktu (WIB)]],
    [#text(fill: white, weight: "bold")[Materi / Aktivitas Pelatihan]],
    [#text(fill: white, weight: "bold")[Narasumber / Fasilitator]],
    [#text(fill: white, weight: "bold")[Metode]]
  ),
  
  // Data Rows (Ukuran font konsisten 8.5pt)
  [08.00 - 08.30], [Registrasi Peserta, Administrasi, & Pembagian Starter Kit], [Panitia Pelatihan], [Tatap Muka],
  [08.30 - 09.00], [*Pembukaan Resmi Pelatihan* & Arahan Kebijakan SE2026], [Kepala BPS Kab. Mempawah], [Pleno],
  [09.00 - 09.30], [Pre-Test Pemahaman Konsep Pemetaan & Geometri Spasial], [Instruktur Pemetaan], [Ujian Mandiri],
  [09.30 - 10.30], [*Modul 01 - 03:* Konsep Wilkerstat, Batas SLS/Non-SLS, dan Regulasi], [Instruktur Daerah], [Paparan & Diskusi],
  [10.30 - 12.00], [*Modul 05:* Master SLS, Kodifikasi ID SLS, dan Pengenalan Landmark], [Instruktur Daerah], [Simulasi Data],
  [12.00 - 13.00], [*ISHOMA* (Istirahat, Sholat, dan Makan Siang Bersama)], [Panitia & Seluruh Peserta], [Istirahat],
  [13.00 - 14.30], [*Modul 04:* Setup Lingkungan GIS, QGIS 3.44 LTR, dan CRS EPSG:4326], [Tim IT & Fasilitator GIS], [Praktik Komputer],
  [14.30 - 16.30], [*Modul 07:* Teknik Digitasi, Editing Batas SLS, dan Snap Geometri], [Fasilitator GIS], [Praktik Mandiri],
  [16.30 - 17.00], [Review Hasil Hari 1, Evaluasi Geometri, dan Tugas Asynchronous], [Fasilitator GIS], [Evaluasi]
)

#v(8pt)
#text(9.5pt, weight: "bold", fill: rgb("#0a2540"))[Hari ke-2: Kamis, 24 September 2026]
#v(2pt)

#table(
  columns: (75pt, 1fr, 120pt, 65pt),
  inset: (x: 5pt, y: 4pt),
  align: (center + horizon, left + horizon, left + horizon, center + horizon),
  fill: (col, row) => if row == 0 { rgb("#0a2540") } else if calc.even(row) { rgb("#f8fafc") } else { none },
  stroke: (x, y) => 0.4pt + rgb("#cbd5e1"),
  
  // Header Table (Ukuran font konsisten 8.5pt)
  table.header(
    [#text(fill: white, weight: "bold")[Waktu (WIB)]],
    [#text(fill: white, weight: "bold")[Materi / Aktivitas Pelatihan]],
    [#text(fill: white, weight: "bold")[Narasumber / Fasilitator]],
    [#text(fill: white, weight: "bold")[Metode]]
  ),
  
  // Data Rows (Ukuran font konsisten 8.5pt)
  [08.00 - 08.30], [Presensi Peserta & Pembahasan Tugas Mandiri (Asynchronous)], [Fasilitator GIS], [Diskusi Kelas],
  [08.30 - 10.00], [Pembahasan Kasus Khusus: Pemekaran SLS, Batas, Gap & Overlap], [Instruktur Daerah], [Bedah Kasus],
  [10.00 - 12.00], [*Modul 07:* Praktik Mandiri Terbimbing Pengolahan Peta Digital], [Petugas & Pendamping], [Praktik Mandiri],
  [12.00 - 13.00], [*ISHOMA* (Istirahat, Sholat, dan Makan Siang Bersama)], [Panitia & Seluruh Peserta], [Istirahat],
  [13.00 - 14.30], [*Validasi Topologi Geometri* (Target 0 Error) & Kendali Mutu], [Fasilitator GIS], [Quality Control],
  [14.30 - 15.30], [*Evaluasi Akhir & Post-Test* Kompetensi Pengolahan Wilkerstat], [Tim Penilai BPS], [Ujian Mandiri],
  [15.30 - 16.30], [*Penutupan Resmi Pelatihan*, Penandatanganan BA, & Foto Bersama], [Kepala BPS Kab. Mempawah], [Pleno]
)
