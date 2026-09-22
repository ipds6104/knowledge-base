// Surat Dinas Permintaan dan Konfirmasi Data KCDA 2026 BPS Kabupaten Mempawah
// Ditujukan kepada Camat Kecamatan Segedong

#set page(
  paper: "a4",
  margin: (
    top: 4.8cm,
    bottom: 2.0cm,
    left: 2.0cm,
    right: 2.0cm
  ),
  header: locate(loc => {
    v(0.8cm)
    grid(
      columns: (58pt, 1fr, 95pt),
      gutter: 10pt,
      align: (center + horizon, left + horizon, right + horizon),
      image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", width: 56pt),
      [
        #text(13.8pt, weight: "bold", style: "italic", font: "Metropolis", fill: black)[BADAN PUSAT STATISTIK] \
        #text(13.8pt, weight: "bold", style: "italic", font: "Metropolis", fill: black)[KABUPATEN MEMPAWAH] \
        #v(2.5pt)
        #text(8.2pt, font: "Arial", fill: black)[Jalan Raden Kusno Nomor 59 Mempawah 78912; Telepon (0561) 691049;] \
        #text(8.2pt, font: "Arial", fill: black)[Laman https://mempawahkab.bps.go.id; Pos-el bps6104\@bps.go.id.]
      ],
      image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_se2026.png", width: 92pt)
    )
    v(3pt)
    line(length: 100%, stroke: 2.2pt + black)
  })
)

#set text(font: "Arial", size: 12pt, lang: "id")
#set par(justify: true, leading: 0.65em)

// =============================================================================
// METADATA SURAT DINAS (HALAMAN 1)
// =============================================================================
#v(4pt)
#grid(
  columns: (1fr, 175pt),
  gutter: 8pt,
  [
    #grid(
      columns: (65pt, 8pt, 1fr),
      gutter: 3pt,
      [Nomor], [:], [B-1095/61046/HM.310/2026],
      [Sifat], [:], [Biasa],
      [Lampiran], [:], [1 (satu) Berkas],
      [Hal], [:], [*Permintaan dan Konfirmasi Data KCDA 2026*]
    )
  ],
  [
    #align(right)[
      Mempawah, 17 September 2026
    ]
  ]
)

#v(10pt)
Yth. *Camat Kecamatan Segedong* \
di Tempat

#v(10pt)
Dengan hormat,

#set par(first-line-indent: 1.8em, leading: 0.65em)
Sehubungan dengan penyusunan Publikasi Kecamatan Segedong Dalam Angka 2026, kami bermaksud mengajukan permohonan data nama camat, kepala desa/lurah, kepala dusun, serta profil kepegawaian aparatur sipil negara di lingkungan Pemerintah Kecamatan Segedong sesuai format terlampir.

Pengisian data dapat dilakukan secara daring melalui tautan lembar kerja berikut: #link("https://s.bps.go.id/kcda26-segedong")[#text(fill: rgb("#0055D4"), weight: "bold")[https://s.bps.go.id/kcda26-segedong]]. Besar harapan kami data tersebut dapat kami terima selambat-lambatnya pada *Senin, 21 September 2026*. Apabila memerlukan koordinasi lebih lanjut, Bapak/Ibu dapat menghubungi narahubung kami, *Sukma Andini, S.Tr.Stat.* (WhatsApp: *082234120921*).

Demikian permohonan ini kami sampaikan. Atas perhatian dan kerja sama Bapak/Ibu, kami ucapkan terima kasih.

#v(18pt)
#set par(first-line-indent: 0pt)
#align(right)[
  #block(width: 220pt, breakable: false)[
    #align(left)[
      Kepala Badan Pusat Statistik \
      Kabupaten Mempawah, \
      #v(4pt)
      #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 42pt) \
      #v(4pt)
      *Munawir*
    ]
  ]
]

// =============================================================================
// HALAMAN LAMPIRAN TABEL KONFIRMASI DATA
// =============================================================================
#pagebreak()

#v(4pt)
#grid(
  columns: (65pt, 8pt, 1fr),
  gutter: 3.5pt,
  [Lampiran 1], [], [],
  [Nomor], [:], [B-1095/61046/HM.310/2026],
  [Tanggal], [:], [17 September 2026]
)

#v(8pt)
#align(center)[
  #text(11pt, weight: "bold")[Lembar Konfirmasi dan Pemutakhiran Data Sektoral \ Kecamatan Segedong Dalam Angka 2026]
]
#v(6pt)

#rect(fill: rgb("#EFF6FF"), stroke: 0.6pt + rgb("#93C5FD"), radius: 3pt, inset: (x: 10pt, y: 6pt))[
  #text(8.5pt)[
    *Petunjuk Pengisian & Konfirmasi Data:*
    + Periksa data acuan (*baseline*) tahun sebelumnya yang tercantum pada tabel lampiran di bawah ini.
    + Pengisian atau konfirmasi data kondisi terkini dilakukan langsung melalui lembar kerja online (*Google Sheets*) pada tautan: #link("https://s.bps.go.id/kcda26-segedong")[#text(fill: rgb("#0055D4"), weight: "bold")[https://s.bps.go.id/kcda26-segedong]].
    + Pada lembar kerja online, pengisian difokuskan pada kolom/sel yang diberi tanda *garis tepi merah (border merah)*.
  ]
]

#set text(size: 8.5pt)
#v(8pt)
== Tabel 1: Nama-Nama Camat yang Pernah dan Masih Menjabat
#text(7.5pt, fill: rgb("#4B5563"))[Sumber: Kantor Camat / Publikasi KCDA BPS]
#v(4pt)
#table(
  columns: (32pt, 1.9fr, 1.2fr),
  inset: 4.5pt,
  align: (center, left, center),
  stroke: (col, row) => {
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let top_b = if row == 0 { 0.8pt + black } else if row == 7 { red_b } else { norm }
    let bot_b = if row == 0 { 1.2pt + black } else if row == 7 { red_b } else { norm }
    let left_b = if row == 7 and col == 0 { red_b } else { norm }
    let right_b = if row == 7 and col == 2 { red_b } else { norm }
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  },
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  table.header(
    [*No*], [*Nama-Nama Camat*], [*Periode Jabatan*]
  ),
  [1], [Drs. Herman, M.Si], [2006 – 2008],
  [2], [Enok Yuniarti, S.IP], [2009 – 2010],
  [3], [Sukarjo, S.Sos], [2010 – 2013],
  [4], [Abdul Malik, SH, M.Si], [2013 – 2018],
  [5], [H. Iskandar, S.Sos], [2018 – 2021],
  [6], [H. Arifin, S.Pd, M.Pd], [2021 – 2025],
  [7], [*Camat Baru* #text(size: 7.5pt, fill: rgb("#DC2626"))[\ (Tuliskan nama camat baru di sini jika ada pergantian jabatan)]], [],
)

#v(8pt)
== Tabel 2: Nama-Nama Kepala Desa / Lurah
#text(7.5pt, fill: rgb("#4B5563"))[Sumber: Kantor Camat / Pemerintah Desa]
#v(4pt)
#table(
  columns: (30pt, 1.2fr, 1.4fr, 1.5fr),
  inset: 4.5pt,
  align: (center, left, left, left),
  stroke: (col, row) => {
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let left_b = if col == 3 { red_b } else { norm }
    let right_b = if col == 3 { red_b } else { norm }
    let top_b = if row == 0 { if col == 3 { red_b } else { 0.8pt + black } } else { norm }
    let bot_b = if row == 0 { 1.2pt + black } else if row == 6 { if col == 3 { red_b } else { norm } } else { norm }
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  },
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  table.header(
    [*No*], [*Desa / Kelurahan*], [*Nama Kades / Lurah (Kondisi 2025)*], [*Nama Kades / Lurah (Kondisi 2026 / Terkini)*]
  ),
  [1], [Peniti Dalam I], [Ramli], [],
  [2], [Sungai Burung], [Dedi Suryadi, SH.], [],
  [3], [Sungai Purun Besar], [Basuni], [],
  [4], [Parit Bugis], [Khairul Wahyudi], [],
  [5], [Peniti Besar], [Kasdik, A.Md.Kep.], [],
  [6], [Peniti Dalam II], [Agustini], [],
)

#pagebreak()

#v(8pt)
== Tabel 3: Nama-Nama Kepala Dusun di Wilayah Kecamatan
#text(7.5pt, fill: rgb("#4B5563"))[Sumber: Kantor Camat / Pemerintah Desa]
#v(4pt)
#table(
  columns: (28pt, 1.1fr, 1.1fr, 1.3fr, 1.4fr),
  inset: 4pt,
  align: (center, left, left, left, left),
  stroke: (col, row) => {
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let left_b = if col == 4 { red_b } else { norm }
    let right_b = if col == 4 { red_b } else { norm }
    let top_b = if row == 0 { if col == 4 { red_b } else { 0.8pt + black } } else { norm }
    let bot_b = if row == 0 { 1.2pt + black } else if row == 22 { if col == 4 { red_b } else { norm } } else { norm }
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  },
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  table.header(
    [*No*], [*Desa / Kelurahan*], [*Nama Dusun*], [*Nama Kadus (Acuan 2025)*], [*Nama Kadus (Kondisi 2026 / Terkini)*]
  ),
  [1], [Peniti Dalam I], [Dusun Sy. Abu Bakar], [Dedi Suryadi], [],
  [2], [Peniti Dalam I], [Dusun Wak Paik], [M. Ali], [],
  [3], [Peniti Dalam I], [Dusun Ambo Pinang], [Tri Agustono], [],
  [4], [Sungai Burung], [Dusun Subur 1], [Desi], [],
  [5], [Sungai Burung], [Dusun Subur 2], [Abdul Rozak], [],
  [6], [Sungai Purun Besar], [Dusun Nelayan], [Fitriana], [],
  [7], [Sungai Purun Besar], [Dusun Kemuning], [Rino], [],
  [8], [Sungai Purun Besar], [Dusun Makmur], [Muhammad Safe'i], [],
  [9], [Sungai Purun Besar], [Dusun Pelita], [Mulyadi Syarif], [],
  [10], [Parit Bugis], [Dusun Keranji], [Muhamaddah], [],
  [11], [Parit Bugis], [Dusun Asam], [Isra Nur Hidayat], [],
  [12], [Peniti Besar], [Dusun Suka Damai], [Suryani], [],
  [13], [Peniti Besar], [Dusun Karya Bakti], [Nurul Hidayah], [],
  [14], [Peniti Besar], [Dusun Suka Maju], [Turiman], [],
  [15], [Peniti Besar], [Dusun Karya Bersama], [Hermansyah], [],
  [16], [Peniti Besar], [Dusun Tani Makmur], [M.Yani], [],
  [17], [Peniti Besar], [Dusun Karya Utama], [Udin], [],
  [18], [Peniti Besar], [Dusun Sabar Menanti], [Junaidi], [],
  [19], [Peniti Dalam II], [Dusun Karya Utama], [Mulyadi], [],
  [20], [Peniti Dalam II], [Dusun Cahaya Intan], [Ardian], [],
  [21], [Peniti Dalam II], [Dusun Lembah Hijau], [Nasrullah], [],
  [22], [Peniti Dalam II], [Dusun Tunas Baru], [Sahirin], [],
)

#pagebreak()

#v(8pt)
== Tabel 4: Jumlah Pegawai Negeri Sipil (PNS) Kantor Camat dan Desa/Kelurahan Tahun 2025
#text(7.5pt, fill: rgb("#4B5563"))[Sumber: Kantor Camat / Badan Kepegawaian dan Pengembangan SDM]
#v(4pt)
#table(
  columns: (32pt, 1fr, 75pt, 75pt, 75pt),
  inset: 4.5pt,
  align: (center, left, center, center, center),
  stroke: (col, row) => {
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let left_b = if col == 2 { red_b } else { norm }
    let right_b = if col == 4 { red_b } else { norm }
    let top_b = if row == 0 { if col in (2, 3, 4) { red_b } else { 0.8pt + black } } else { norm }
    let bot_b = if row == 0 { 1.2pt + black } else if row == 8 { if col in (2, 3, 4) { red_b } else { norm } } else { norm }
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  },
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  table.header(
    [*No*], [*Pemerintah Daerah / Instansi*], [*Laki-Laki*], [*Perempuan*], [*Jumlah*]
  ),
  [1], [Pemerintah Daerah Kecamatan Segedong], [], [], [],
  [2], [Peniti Dalam I], [], [], [],
  [3], [Sungai Burung], [], [], [],
  [4], [Sungai Purun Besar], [], [], [],
  [5], [Parit Bugis], [], [], [],
  [6], [Peniti Besar], [], [], [],
  [7], [Peniti Dalam Ii], [], [], [],
  table.cell(colspan: 2, align: center)[*Jumlah Total*], [], [], [],
)

#v(10pt)

#v(8pt)
== Tabel 5: Jumlah PNS Kantor Camat Menurut Tingkat Pendidikan dan Jenis Kelamin Tahun 2025
#text(7.5pt, fill: rgb("#4B5563"))[Sumber: Kantor Camat]
#v(4pt)
#table(
  columns: (32pt, 1fr, 75pt, 75pt, 75pt),
  inset: 4.5pt,
  align: (center, left, center, center, center),
  stroke: (col, row) => {
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let left_b = if col == 2 { red_b } else { norm }
    let right_b = if col == 4 { red_b } else { norm }
    let top_b = if row == 0 { if col in (2, 3, 4) { red_b } else { 0.8pt + black } } else { norm }
    let bot_b = if row == 0 { 1.2pt + black } else if row == 11 { if col in (2, 3, 4) { red_b } else { norm } } else { norm }
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  },
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  table.header(
    [*No*], [*Tingkat Pendidikan*], [*Laki-Laki*], [*Perempuan*], [*Jumlah*]
  ),
  [1], [Sekolah Dasar (SD)], [], [], [],
  [2], [SMP/Sederajat], [], [], [],
  [3], [SMA/Sederajat], [], [], [],
  [4], [Diploma I/Akta I], [], [], [],
  [5], [Diploma II/Akta II], [], [], [],
  [6], [Diploma III/Akta III], [], [], [],
  [7], [Diploma IV/Akta IV], [], [], [],
  [8], [S1/Sarjana], [], [], [],
  [9], [S2/Pasca Sarjana], [], [], [],
  [10], [S3/Doktor/Ph.D], [], [], [],
  table.cell(colspan: 2, align: center)[*Jumlah Total*], [], [], [],
)
