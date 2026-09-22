// Surat Dinas Permintaan dan Konfirmasi Data KCDA 2026 BPS Kabupaten Mempawah
// Ditujukan kepada Camat Kecamatan Jongkat

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
      [Nomor], [:], [B-1098/61046/HM.310/2026],
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
Yth. *Camat Kecamatan Jongkat* \
di Tempat

#v(10pt)
Dengan hormat,

#set par(first-line-indent: 1.8em, leading: 0.65em)
Sehubungan dengan penyusunan Publikasi Kecamatan Jongkat Dalam Angka 2026, kami bermaksud mengajukan permohonan data nama camat, kepala desa/lurah, kepala dusun, serta profil kepegawaian aparatur sipil negara di lingkungan Pemerintah Kecamatan Jongkat sesuai format terlampir.

Pengisian data dapat dilakukan secara daring melalui tautan lembar kerja berikut: #link("https://s.bps.go.id/kcda26-jongkat")[#text(fill: rgb("#0055D4"), weight: "bold")[https://s.bps.go.id/kcda26-jongkat]]. Besar harapan kami data tersebut dapat kami terima selambat-lambatnya pada *Senin, 21 September 2026*. Apabila memerlukan koordinasi lebih lanjut, Bapak/Ibu dapat menghubungi narahubung kami, *Sukma Andini, S.Tr.Stat.* (WhatsApp: *082234120921*).

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
  [Nomor], [:], [B-1098/61046/HM.310/2026],
  [Tanggal], [:], [17 September 2026]
)

#v(8pt)
#align(center)[
  #text(11pt, weight: "bold")[Lembar Konfirmasi dan Pemutakhiran Data Sektoral \ Kecamatan Jongkat Dalam Angka 2026]
]
#v(6pt)

#rect(fill: rgb("#EFF6FF"), stroke: 0.6pt + rgb("#93C5FD"), radius: 3pt, inset: (x: 10pt, y: 6pt))[
  #text(8.5pt)[
    *Petunjuk Pengisian & Konfirmasi Data:*
    + Periksa data acuan (*baseline*) tahun sebelumnya yang tercantum pada tabel lampiran di bawah ini.
    + Pengisian atau konfirmasi data kondisi terkini dilakukan langsung melalui lembar kerja online (*Google Sheets*) pada tautan: #link("https://s.bps.go.id/kcda26-jongkat")[#text(fill: rgb("#0055D4"), weight: "bold")[https://s.bps.go.id/kcda26-jongkat]].
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
    let top_b = if row == 0 { 0.8pt + black } else if row == 26 { red_b } else { norm }
    let bot_b = if row == 0 { 1.2pt + black } else if row == 26 { red_b } else { norm }
    let left_b = if row == 26 and col == 0 { red_b } else { norm }
    let right_b = if row == 26 and col == 2 { red_b } else { norm }
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  },
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  table.header(
    [*No*], [*Nama-Nama Camat*], [*Periode Jabatan*]
  ),
  [1], [Muhammad Syarif], [1950-1956],
  [2], [Muhammad Saidi Said], [1956-1958],
  [3], [Sy.Yusup al Idrus], [1958-1964],
  [4], [Abdul Hamid], [1964-1971],
  [5], [R.Suharko,B.A], [1971-1973],
  [6], [Urai Rukiat ,B.A], [1973-1974],
  [7], [H.Mustafa H.Zawawi], [1974-1975],
  [8], [Maximus Maon, B.A], [1975-1978],
  [9], [Ramli.H.Ahmad, B.A], [1978-1981],
  [10], [Ya’ Amir Hamzah], [1981-1982],
  [11], [Laurentius Bakweng, B.A], [1982-1983],
  [12], [Abdul Malik, B.A], [1983-1986],
  [13], [Drs.M.Ralibi], [1986-1988],
  [14], [Drs. H.M.Djawawi], [1988-1995],
  [15], [Drs.H.M.Idrus], [1995-1998],
  [16], [Drs.Abang Rasmansyah], [1998-2000],
  [17], [Drs.Imansyah.], [2000-2002],
  [18], [Drs.Nuradi.], [2002-2005],
  [19], [Muhammad Shaleh,S.Sos], [2005-2008],
  [20], [Drs.Herman,M.Si], [2009-2011],
  [21], [Enok Yurniati,S.Ip], [2011-2016],
  [22], [Drs.Iskandar], [2016-2019],
  [23], [Drs.M.Erfiza,M.Si], [2019-2020],
  [24], [Reno Prawira,S.STP.M.A], [2020-2024],
  [25], [Mahmud Hasan,S.Ag.M.Pd.], [2024-2025],
  [26], [*Camat Baru* #text(size: 7.5pt, fill: rgb("#DC2626"))[\ (Tuliskan nama camat baru di sini jika ada pergantian jabatan)]], [],
)

#pagebreak()

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
    let bot_b = if row == 0 { 1.2pt + black } else if row == 5 { if col == 3 { red_b } else { norm } } else { norm }
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  },
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  table.header(
    [*No*], [*Desa / Kelurahan*], [*Nama Kades / Lurah (Kondisi 2025)*], [*Nama Kades / Lurah (Kondisi 2026 / Terkini)*]
  ),
  [1], [Sungai Nipah], [Agus Surapati], [],
  [2], [Jungkat], [Ramlan], [],
  [3], [Wajok Hilir], [Abdul Majid], [],
  [4], [Wajok Hulu], [H. Basri], [],
  [5], [Peniti Luar], [Kantor], [],
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
    let bot_b = if row == 0 { 1.2pt + black } else if row == 29 { if col == 4 { red_b } else { norm } } else { norm }
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  },
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  table.header(
    [*No*], [*Desa / Kelurahan*], [*Nama Dusun*], [*Nama Kadus (Acuan 2025)*], [*Nama Kadus (Kondisi 2026 / Terkini)*]
  ),
  [1], [Sungai Nipah], [Dusun Mawar], [Muhlis], [],
  [2], [Sungai Nipah], [Dusun Melati], [Syarif Muslimat], [],
  [3], [Jungkat], [Dusun Pangsuma], [Nor Uzeizi], [],
  [4], [Jungkat], [Dusun Uray Bawadi], [Widi Apriadi, S.Sos], [],
  [5], [Jungkat], [Dusun Raden Wijaya], [Muhammad Ridek], [],
  [6], [Jungkat], [Dusun Sultan Muhammad], [Abdul Halim], [],
  [7], [Jungkat], [Dusun Pangeran Adipati], [Wahyu], [],
  [8], [Jungkat], [Dusun Daeng Manambon], [Annizar], [],
  [9], [Jungkat], [Dusun Rahadi Usman], [Imran], [],
  [10], [Jungkat], [Dusun Raden Taufik], [Aditia Anugrah Pratama], [],
  [11], [Jungkat], [Dusun Alianyang], [Darmawan], [],
  [12], [Jungkat], [Dusun Sultan Abdurrahman], [Noto Wahono], [],
  [13], [Wajok Hilir], [Dusun Palawija], [Jalaludin], [],
  [14], [Wajok Hilir], [Dusun Coklat], [Nasri], [],
  [15], [Wajok Hilir], [Dusun Kelapa], [Jamaludin], [],
  [16], [Wajok Hilir], [Dusun Kopi], [Hendi Sumaryo], [],
  [17], [Wajok Hilir], [Dusun Padi], [Abdul Rais], [],
  [18], [Wajok Hilir], [Dusun Jeruk], [Ida Marlina], [],
  [19], [Wajok Hilir], [Dusun Nanas], [Jailani], [],
  [20], [Wajok Hulu], [Dusun Lapan], [Meriyanah], [],
  [21], [Wajok Hulu], [Dusun Brahima], [Muhammad Yusuf], [],
  [22], [Wajok Hulu], [Dusun Pandan], [Dulasis], [],
  [23], [Wajok Hulu], [Dusun Kunyit], [Fawaid], [],
  [24], [Wajok Hulu], [Dusun Telok Dalam], [Jamal], [],
  [25], [Wajok Hulu], [Dusun Durian], [Muhammad Yusuf], [],
  [26], [Wajok Hulu], [Dusun Mambo], [Aswanto], [],
  [27], [Peniti Luar], [Dusun Panca Bhakti], [Muhammad Daud], [],
  [28], [Peniti Luar], [Dusun Taruna Bhakti], [Hidayat], [],
  [29], [Peniti Luar], [Dusun Karya Bhakti], [Adriansyah, S.Pd], [],
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
    let bot_b = if row == 0 { 1.2pt + black } else if row == 6 { if col in (2, 3, 4) { red_b } else { norm } } else { norm }
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  },
  fill: (col, row) => if row == 0 { rgb("#F3F4F6") } else { none },
  table.header(
    [*No*], [*Pemerintah Daerah / Instansi*], [*Laki-Laki*], [*Perempuan*], [*Jumlah*]
  ),
  [1], [Pemerintah Daerah Kecamatan Jongkat], [], [], [],
  [2], [Sungai Nipah], [], [], [],
  [3], [Jungkat], [], [], [],
  [4], [Wajok Hilir], [], [], [],
  [5], [Wajok Hulu], [], [], [],
  [6], [Peniti Luar], [], [], [],
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
