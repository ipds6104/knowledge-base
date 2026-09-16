// Surat Dinas Permintaan dan Konfirmasi Data KCDA 2026 BPS Kabupaten Mempawah
// Ditujukan kepada Camat Kecamatan Mempawah Hilir

#set page(
  paper: "a4",
  margin: (
    top: 2.2cm,
    bottom: 2.2cm,
    left: 2.2cm,
    right: 2.2cm
  ),
  header: context {
    let page_num = counter(page).get().first()
    if page_num > 1 {
      grid(
        columns: (1fr, auto),
        align: (left, right),
        text(7pt, fill: rgb("#4B5563"), font: "Myriad Pro")[Lampiran Surat Konfirmasi Data KCDA 2026 | BPS Kabupaten Mempawah - Kecamatan Mempawah Hilir],
        text(7pt, fill: rgb("#4B5563"), font: "Myriad Pro")[Halaman #page_num]
      )
      line(length: 100%, stroke: 0.3pt + luma(180))
    }
  },
  footer: context {
    let page_num = counter(page).get().first()
    if page_num == 1 {
      align(center, text(7pt, fill: luma(120), font: "Myriad Pro")[BPS Kabupaten Mempawah — Menghasilkan Data Statistik Berkualitas untuk Indonesia Maju])
    }
  }
)

#set text(font: ("Myriad Pro", "Metropolis"), size: 9.5pt, lang: "id")
#set par(justify: true, leading: 0.6em)

// =============================================================================
// KOP SURAT RESMI BPS KABUPATEN MEMPAWAH
// =============================================================================
#grid(
  columns: (65pt, 1fr),
  gutter: 12pt,
  align: (center + horizon, center + horizon),
  image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", width: 56pt),
  [
    #text(13.5pt, weight: "bold", font: "Metropolis", fill: rgb("#0F294A"))[BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH] \
    #v(1pt)
    #text(8.5pt, fill: rgb("#1F2937"))[Jl. Raden Kusno No. 1, Mempawah 79511] \
    #text(8pt, fill: rgb("#374151"))[Telepon: (0561) 691030 | Pos-el: bps6104\@bps.go.id | Laman: https://mempawahkab.bps.go.id]
  ]
)
#v(4pt)
#line(length: 100%, stroke: 1.8pt + rgb("#0F294A"))
#v(-5.5pt)
#line(length: 100%, stroke: 0.6pt + rgb("#0F294A"))
#v(12pt)

// =============================================================================
// METADATA SURAT DINAS
// =============================================================================
#grid(
  columns: (1fr, 150pt),
  gutter: 10pt,
  [
    #grid(
      columns: (60pt, 8pt, 1fr),
      gutter: 3pt,
      [Nomor], [:], [B-155/61040/VS.100/09/2026],
      [Sifat], [:], [Biasa],
      [Lampiran], [:], [1 (satu) Berkas],
      [Hal], [:], [*Permintaan dan Konfirmasi Data Kecamatan Dalam Angka (KCDA) 2026*]
    )
  ],
  [
    #align(right)[
      Mempawah, 16 September 2026
    ]
  ]
)

#v(10pt)
Yth. *Camat Kecamatan Mempawah Hilir* \
di Tempat

#v(10pt)
Dengan hormat,

#set par(first-line-indent: 1.8em, leading: 0.65em)
Dalam rangka pelaksanaan amanat Undang-Undang Nomor 16 Tahun 1997 tentang Statistik dan Peraturan Presiden Nomor 39 Tahun 2019 tentang Satu Data Indonesia, Badan Pusat Statistik (BPS) Kabupaten Mempawah saat ini sedang menyusun publikasi statistik tahunan *"Kecamatan Mempawah Hilir Dalam Angka 2026"*. Publikasi ini menyajikan data statistik sektoral komprehensif tingkat kecamatan dan desa/kelurahan yang menjadi rujukan penting bagi perencanaan, pemantauan, serta evaluasi program pembangunan di Kabupaten Mempawah.

Sehubungan dengan hal tersebut, bersama ini kami sampaikan lembar data acuan (*baseline*) tahun sebelumnya sebagaimana terlampir, yang mencakup data pejabat camat, kepala desa/lurah, serta profil kepegawaian aparatur sipil negara di lingkungan Kecamatan Mempawah Hilir.

Guna menjamin akurasi dan kemutakhiran data publikasi edisi 2026, kami sangat mengharapkan bantuan dan kerja sama Bapak/Ibu Camat beserta jajaran untuk dapat melakukan pemeriksaan, verifikasi, serta pengisian koreksi data mutakhir pada kolom konfirmasi yang telah disediakan.

Berkas konfirmasi data yang telah diverifikasi kiranya dapat disampaikan kembali kepada BPS Kabupaten Mempawah selambat-lambatnya pada hari *Senin, 21 September 2026*. Apabila memerlukan informasi teknis lebih lanjut atau untuk konfirmasi pemutakhiran data secara langsung, Bapak/Ibu dapat menghubungi narahubung kami:

#set par(first-line-indent: 0pt)
#align(center)[
  #rect(fill: rgb("#F8FAFC"), stroke: 0.8pt + rgb("#CBD5E1"), radius: 4pt, inset: (x: 14pt, y: 8pt))[
    #text(9pt)[
      *Sukma (Sukma Andini, S.Tr.Stat.)* \
      Staf Fungsi Integrasi Pengolahan dan Diseminasi Statistik (IPDS) BPS Kabupaten Mempawah \
      WhatsApp / Kontak: *0812-5853-2420* (+62 812-5853-2420) \
      #v(2pt)
      Lembar Kerja Pengisian Data (Google Sheets): \
      #link("https://docs.google.com/spreadsheets/d/1VB3k9opurqMccOdBMC4uKoP9UBiMOkzCroJEl7zriq4")[#text(size: 8pt, fill: rgb("#1D4ED8"), weight: "bold")[https://docs.google.com/spreadsheets/d/1VB3k9opurqMccOdBMC4uKoP9UBiMOkzCroJEl7zriq4]]
    ]
  ]
]

#set par(first-line-indent: 1.8em)
Demikian permohonan ini kami sampaikan. Atas perhatian, dukungan, dan kerja sama yang baik dari Bapak/Ibu Camat demi terwujudnya data statistik daerah yang berkualitas dan akuntabel, kami ucapkan terima kasih.

#v(12pt)
#set par(first-line-indent: 0pt)
#grid(
  columns: (1fr, 210pt),
  gutter: 10pt,
  [],
  [
    #align(left)[
      Kepala Badan Pusat Statistik \
      Kabupaten Mempawah, \
      #v(2pt)
      #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 42pt) \
      #v(2pt)
      *MUNAWIR, S.E., M.M.* \
      Pembina Tk. I (IV/b)
    ]
  ]
)

#v(8pt)
#text(8pt, fill: rgb("#374151"))[
  *Tembusan Yth:* \
  1. Bupati Mempawah (sebagai laporan) \
  2. Arsip BPS Kabupaten Mempawah
]

// =============================================================================
// HALAMAN LAMPIRAN TABEL KONFIRMASI DATA
// =============================================================================
#pagebreak()

#align(center)[
  #text(11pt, weight: "bold", font: "Metropolis")[LAMPIRAN SURAT DINAS KEPALA BPS KABUPATEN MEMPAWAH] \
  #text(9pt)[Nomor: B-155/61040/VS.100/09/2026 | Tanggal: 16 September 2026] \
  #v(2pt)
  #text(10pt, weight: "bold", fill: rgb("#0F294A"))[LEMBAR KONFIRMASI DAN PEMUTAKHIRAN DATA SEKTORAL \ KECAMATAN MEMPAWAH HILIR DALAM ANGKA 2026]
]
#v(6pt)

#rect(fill: rgb("#EFF6FF"), stroke: 0.6pt + rgb("#93C5FD"), radius: 3pt, inset: (x: 10pt, y: 7pt))[
  #text(8pt)[
    *Petunjuk Pengisian & Konfirmasi Data:*
    + Periksa data acuan (*baseline*) tahun sebelumnya yang tercantum pada tabel lampiran di bawah ini sebagai gambaran data yang perlu dikonfirmasi.
    + Pengisian perbaikan atau konfirmasi kondisi terkini dapat dilakukan langsung secara digital melalui tautan Google Spreadsheet kecamatan yang telah disediakan di atas.
    + Apabila terdapat perubahan nama, pemekaran wilayah, atau pergantian pejabat terkini, silakan perbarui pada lembar kerja online atau hubungi narahubung kami.
  ]
]

#v(10pt)
== Tabel 1: Nama-Nama Camat yang Pernah dan Masih Menjabat
#text(7.5pt, fill: rgb("#4B5563"))[Sumber: Kantor Camat / Publikasi KCDA]
#v(4pt)
#table(
  columns: (30pt, 1.4fr, 110pt, 1.2fr),
  inset: 4.5pt,
  align: (center, left, center, left),
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },
  table.header(
    [*No*], [*Nama-Nama Camat*], [*Periode Jabatan (Acuan)*], [*Koreksi / Perubahan Nama / Status*]
  ),
  [1], [Saidi Said], [1949 – 1953], [],
  [2], [T.A.A Samaun], [1953 – 1957], [],
  [3], [M. Yusuf Abdul Rahim], [1957 – 1961], [],
  [4], [Abdul Wahab H Jamaludin], [1961 – 1965], [],
  [5], [M Yusuf Abdul Rahim], [1965 – 1969], [],
  [6], [Abdul Jabar], [1969 – 1973], [],
  [7], [Gusti Amirudin Hamid], [1973 – 1977], [],
  [8], [Abdul Majid Rani], [1977 – 1981], [],
  [9], [Syarif Ismail Abdullah], [1981 – 1985], [],
  [10], [Drs. Daeng Syarifuddin], [1985 – 1989], [],
  [11], [Drs. A . Malik], [1989 – 1993], [],
  [12], [Drs. Suhardi Sakim], [1993 – 1998], [],
  [13], [Dra. Hj. Syarkiah Sani], [1998 – 2002], [],
  [14], [H. Gusti Sabrani Ali, BA], [2002 – 2003], [],
  [15], [Gusti Hadriyani, S.Sos], [2003 – 2005], [],
  [16], [Erna Yunianingsih, BA], [2005 – 2009], [],
  [17], [Drs. Suwanda, M.Si], [2009 – 2012], [],
  [18], [Drs. Rohmat Effendi, MM], [2012 – 2016], [],
  [19], [Elly Trisnartiny, S IP], [2016 – 2019], [],
  [20], [Kuntum Indah P N, S IP, M.Si], [2019 - 2021], [],
  [21], [Drs. Daeng Dicky Armeina], [2021-2022], [],
  [22], [Drs. Ismayuda, MM], [2022-2024], [],
  [+], [#text(style: "italic", fill: luma(100))[Camat Baru (jika ada)]], [], [],
)

#v(10pt)
== Tabel 2: Nama-Nama Kepala Desa / Lurah
#text(7.5pt, fill: rgb("#4B5563"))[Sumber: Kantor Camat / Pemerintah Desa]
#v(4pt)
#table(
  columns: (30pt, 1.1fr, 1.4fr, 1.4fr),
  inset: 4.5pt,
  align: (center, left, left, left),
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },
  table.header(
    [*No*], [*Desa / Kelurahan*], [*Nama Kepala Desa / Lurah (Acuan)*], [*Nama Kepala Desa / Pj Terkini*]
  ),
  [1], [Tanjung], [Syarif Hilman Noviardi, S.Kom], [],
  [2], [Kuala Secapah], [Mawardi], [],
  [3], [Tengah], [Friant Adhitya, S.IP, MAP], [],
  [4], [Terusan], [Hendi Permana, S.STP, M.A.B], [],
  [5], [Pasir], [–], [],
  [6], [Penibung], [Evi Junita, S.Pd.I], [],
  [7], [Sengkubang], [Alfian], [],
  [8], [Malikian], [Akhmad], [],
)

#pagebreak()

#v(10pt)
== Tabel 3: Jumlah Pegawai Negeri Sipil (PNS) Kantor Camat dan Desa/Kelurahan
#text(7.5pt, fill: rgb("#4B5563"))[Sumber: Kantor Camat / Badan Kepegawaian dan Pengembangan SDM]
#v(4pt)
#table(
  columns: (30pt, 1.6fr, 65pt, 65pt, 65pt, 1fr),
  inset: 4.5pt,
  align: (center, left, center, center, center, left),
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },
  table.header(
    [*No*], [*Pemerintah Daerah / Kantor*], [*Laki-Laki*], [*Perempuan*], [*Jumlah*], [*Keterangan / Non-PNS*]
  ),
  [1], [Pemerintah Daerah Kecamatan Mempawah Hilir], [], [], [], [],
  [2], [Pemerintah Daerah Kelurahan Tanjung], [], [], [], [],
  [3], [Pemerintah Daerah Desa Kuala Secapah], [], [], [], [],
  [4], [Pemerintah Daerah Kelurahan Tengah], [], [], [], [],
  [5], [Pemerintah Daerah Kelurahan Terusan], [], [], [], [],
  [6], [Pemerintah Daerah Desa Pasir], [], [], [], [],
  [7], [Pemerintah Daerah Desa Penibung], [], [], [], [],
  [8], [Pemerintah Daerah Desa Sengkubang], [], [], [], [],
  [9], [Pemerintah Daerah Desa Malikian], [], [], [], [],
)

#v(10pt)
== Tabel 4: Jumlah PNS Kantor Camat Menurut Tingkat Pendidikan dan Jenis Kelamin
#text(7.5pt, fill: rgb("#4B5563"))[Sumber: Kantor Camat]
#v(4pt)
#table(
  columns: (30pt, 1.6fr, 70pt, 70pt, 70pt, 1fr),
  inset: 4.5pt,
  align: (center, left, center, center, center, left),
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },
  table.header(
    [*No*], [*Tingkat Pendidikan*], [*Laki-Laki*], [*Perempuan*], [*Jumlah*], [*Keterangan*]
  ),
  [1], [Sekolah Dasar (SD)], [], [], [], [],
  [2], [SMP/Sederajat], [], [], [], [],
  [3], [SMA/Sederajat], [], [], [], [],
  [4], [Diploma II/Akta II], [], [], [], [],
  [5], [Diploma III/Akta III], [], [], [], [],
  [6], [Diploma IV/Akta IV], [], [], [], [],
  [7], [S1/Sarjana], [], [], [], [],
  [8], [S2/Pasca Sarjana], [], [], [], [],
  [9], [S3/Doktor/Ph.D], [], [], [], [],
  table.cell(colspan: 2, align: center)[*Jumlah Total*], [], [], [], [],
)
