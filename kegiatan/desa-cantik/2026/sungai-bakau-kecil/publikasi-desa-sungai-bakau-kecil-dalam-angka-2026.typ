#set page(
  paper: "a4",
  margin: (x: 1.5cm, y: 2cm),
  header: align(right, text(8pt, fill: luma(120))[DESA SUNGAI BAKAU KECIL DALAM ANGKA 2026]),
  footer: [
    #align(center, text(9pt)[#context counter(page).display("1")])
  ]
)
#set text(font: "Liberation Sans", size: 10pt, lang: "id")
#set par(justify: true, leading: 0.65em)

// Cover Header
#align(center)[
  #block(
    fill: rgb("#0f4c81"),
    inset: 18pt,
    radius: 4pt,
    width: 100%,
    [
      #text(fill: white, weight: "bold", size: 20pt)[DESA SUNGAI BAKAU KECIL\ DALAM ANGKA 2026] \
      #v(6pt)
      #text(fill: white.darken(10%), weight: "medium", size: 12pt)[Kompilasi Data Potensi Kewilayahan Rukun Tetangga (RT)] \
      #text(fill: white.darken(20%), size: 10pt)[Program Desa Cantik — BPS Kabupaten Mempawah]
    ]
  )
]

#v(10pt)

// Katalog Meta
#rect(width: 100%, fill: rgb("#f4f6f8"), inset: 10pt, radius: 3pt)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    [ *Nomor Publikasi:* 61040.2026.001 ],
    [ *Ukuran Buku:* 21 cm x 29.7 cm ],
    [ *Tanggal Rilis:* Agustus 2026 ]
  )
]

#v(12pt)

== KATA PENGANTAR

Puji dan syukur kita panjatkan ke hadirat Tuhan Yang Maha Esa atas rahmat dan karunia-Nya, publikasi *"Desa Sungai Bakau Kecil Dalam Angka 2026"* ini dapat diselesaikan dengan baik. Publikasi ini merupakan hasil kompilasi data potensi desa berbasis Rukun Tetangga (RT) yang dikumpulkan melalui kegiatan Desa Cantik (Desa Cinta Statistik) BPS Kabupaten Mempawah bekerjasama dengan Pemerintah Desa Sungai Bakau Kecil.

Data yang disajikan mencakup kondisi demografi kependudukan, tingkat pendidikan, kepemilikan administrasi KTP-el, penerima bantuan sosial, hingga kelayakan bangunan dan perumahan di tingkat RT. Diharapkan publikasi ini dapat menjadi rujukan utama bagi Pemerintah Desa dan pemangku kepentingan dalam perencanaan pembangunan desa berbasis bukti (*evidence-based policy*).

Kepada semua pihak yang telah membantu terwujudnya publikasi ini, khususnya para Agen Statistik Desa dan Ketua RT se-Desa Sungai Bakau Kecil, kami sampaikan terima kasih dan penghargaan yang setinggi-tingginya.

#v(10pt)
#align(right)[
  Sungai Bakau Kecil, Agustus 2026 \
  *Kepala Desa Sungai Bakau Kecil* \
  bersama *Tim Pembina Desa Cantik BPS Kabupaten Mempawah*
]

#pagebreak()

== PENJELASAN TEKNIS & METODOLOGI

- *Ruang Lingkup:* Pendataan mencakup seluruh 37 Rukun Tetangga (RT) di Desa Sungai Bakau Kecil, Kecamatan Mempawah Timur, Kabupaten Mempawah. Responden terdiri dari Ketua RT serta pengamatan langsung sarana desa.
- *Pelaksanaan Pendataan:* Menggunakan metode CAPI (*Computer-Assisted Personal Interviewing*) berbasis aplikasi mobile *AppSheet* pada bulan Juni–Juli 2026.
- *Konsep & Definisi:*
  - *Sex Ratio:* Perbandingan jumlah penduduk laki-laki per 100 perempuan.
  - *Rata-rata ART:* Rata-rata banyaknya anggota keluarga per KK.
  - *Kepadatan Hunian:* Rata-rata jiwa per bumbung rumah.

#v(10pt)

== BAB I: GEOGRAFIS & PEMBAGIAN RT

#table(
  columns: (2.5fr, 1.5fr, 1fr),
  fill: (x, y) => if y == 0 { rgb("#0f4c81") } else if calc.even(y) { rgb("#f9fafb") } else { white },
  stroke: 0.5pt + rgb("#d1d5db"),
  align: (col, row) => if row == 0 { center + horizon } else { left + horizon },
  [*Batas Wilayah*], [*Desa / Kelurahan / Laut*], [*Kecamatan*],
  [Sebelah Utara], [Desa Pasir Palembang], [Mempawah Timur],
  [Sebelah Selatan], [Laut Natuna / Selat Karimata], [-],
  [Sebelah Timur], [Desa Sungai Bakau Besar], [Mempawah Timur],
  [Sebelah Barat], [Kelurahan Pasir Wan Salim], [Mempawah Timur]
)

#v(10pt)

=== Daftar Ketua RT & Petugas Pendata (37 RT)

#table(
  columns: (2.5fr, 2fr, 1.8fr),
  fill: (x, y) => if y == 0 { rgb("#0f4c81") } else if calc.even(y) { rgb("#f9fafb") } else { white },
  stroke: 0.3pt + rgb("#e5e7eb"),
  align: (col, row) => if row == 0 { center + horizon } else { left + horizon },
  table.header([*Nama RT*], [*Nama Ketua RT*], [*Petugas Pendata (PPL)*]),
  [RT 001 RW 01 DUSUN SENGGIRING], [SY. JAMALUDDIN], [Haqqi Wirakaryadi],
  [RT 002 RW 01 DUSUN SENGGIIRING], [MURSID, S.Pd], [Haqqi Wirakaryadi],
  [RT 003 RW 01 DUSUN SENGGIRING], [M. NAWI], [Haqqi Wirakaryadi],
  [RT 004 RW 02 DUSUN BENTENG RAYA], [HARFANSYAH], [Haqqi Wirakaryadi],
  [RT 005 RW 02 DUSUN BENTENG RAYA], [SATIAT], [Haqqi Wirakaryadi],
  [RT 006 RW 02 DUSUN BENTENG RAYA], [EFFENDI RAUPE], [Haqqi Wirakaryadi],
  [RT 007 RW 03 DUSUN BENTENG TIMUR], [SULAIMAN], [Haqqi Wirakaryadi],
  [RT 008 RW 03 DUSUN BENTENG TIMUR], [NURHAYATI], [Haqqi Wirakaryadi],
  [RT 009 RW 03 DUSUN BENTENG TIMUR], [BURHANI], [Haqqi Wirakaryadi],
  [RT 010 RW 03 DUSUN SEPAKAT TENGAH], [HARIANTO], [Haqqi Wirakaryadi],
  [RT 011 RW 03 DUSUN SEPAKAT TENGAH], [JUNAIDI], [Haqqi Wirakaryadi],
  [RT 012 RW 04 DUSUN SEPAKAT TENGAH], [MARINO], [Haqqi Wirakaryadi],
  [RT 013 RW 04 DUSUN SEPAKAT TENGAH], [KHOLIS], [Haqqi Wirakaryadi],
  [RT 014 RW 04 DUSUN SEPAKAT TENGAH], [MARTILAM], [Haqqi Wirakaryadi],
  [RT 015 RW 05 DUSUN SEPAKAT DARAT], [MAHRUJI], [Sahrul Rozi],
  [RT 016 RW 05 DUSUN SEPAKAT DARAT], [SIRI], [Sahrul Rozi],
  [RT 017 RW 05 DUSUN SEPAKAT DARAT], [SAFURI], [Haqqi Wirakaryadi],
  [RT 018 RW 03 DUSUN BENTENG TIMUR], [EFENDI], [Haqqi Wirakaryadi],
  [RT 019 RW 04 DUSUN SEPAKAT TENGAH], [MARJUKI], [Haqqi Wirakaryadi],
  [RT 020 RW 01 DUSUN SENGGIRING], [DG. RIVA'IE], [Haqqi Wirakaryadi],
  [RT 021 RW 06 DUSUN KEDAUNG], [PULIAN], [Haqqi Wirakaryadi],
  [RT 022 RW 06 DUSUN KEDAUNG], [MARSULI], [Haqqi Wirakaryadi],
  [RT 023 RW 06 DUSUN KEDAUNG], [SYAHRUDDIN], [Haqqi Wirakaryadi],
  [RT 024 RW 07 DUSUN SENAMBANG], [MAT RAIS], [Haqqi Wirakaryadi],
  [RT 025 RW 07 DUSUN SENAMBANG], [HASANUDIN], [Haqqi Wirakaryadi],
  [RT 026 RW 07 DUSUN SENAMBANG], [SAHRUJI], [Haqqi Wirakaryadi],
  [RT 027 RW 08 DUSUN KONSASI], [MARSYAD], [Haqqi Wirakaryadi],
  [RT 028 RW 08 DUSUN KONSASI], [SARUKI], [Haqqi Wirakaryadi],
  [RT 029 RW 08 DUSUN KONSASI], [MARSYAD], [Haqqi Wirakaryadi],
  [RT 030 RW 05 DUSUN SEPAKAT DARAT], [MARSALIM], [Haqqi Wirakaryadi],
  [RT 031 RW 02 DUSUN BENTENG RAYA], [RUDHI KHAIRUDDIN], [Haqqi Wirakaryadi],
  [RT 032 RW 07 DUSUN SENAMBANG], [M. ALI], [Haqqi Wirakaryadi],
  [RT 033 RW 04 DUSUN SEPAKAT TENGAH], [FIRDAUS], [Sahrul Rozi],
  [RT 034 RW 05 DUSUN SEPAKAT DARAT], [SADRA'I], [Sahrul Rozi],
  [RT 035 RW 04 DUSUN SEPAKAT TENGAH], [JOHAN], [Sahrul Rozi],
  [RT 036 RW 03 DUSUN BENTENG TIMUR], [JULIADI], [Haqqi Wirakaryadi],
  [RT 037 RW 05 DUSUN SEPAKAT DARAT], [MUNAKI], [Haqqi Wirakaryadi],

)

#pagebreak()

== BAB II: KEPENDUDUKAN & KELOMPOK RENTAN

- *Total Penduduk:* *5,701 jiwa* (Laki-laki: *2,902*, Perempuan: *2,799*)
- *Sex Ratio Desa:* *103.68*
- *Total Kartu Keluarga:* *1,661 KK* (Rata-rata ART: *3.43 jiwa/KK*)

#v(8pt)

=== Tabel Penduduk, Sex Ratio, KK, & Lansia per RT

#table(
  columns: (2.2fr, 0.8fr, 0.8fr, 1fr, 0.8fr, 0.8fr, 0.8fr),
  fill: (x, y) => if y == 0 { rgb("#0f4c81") } else if y == 38 { rgb("#e5e7eb") } else if calc.even(y) { rgb("#f9fafb") } else { white },
  stroke: 0.3pt + rgb("#e5e7eb"),
  align: (col, row) => if row == 0 { center + horizon } else if col == 0 { left + horizon } else { center + horizon },
  table.header([*Nama RT*], [*L*], [*P*], [*Total*], [*SR*], [*KK*], [*Lansia*]),
  [RT 001 RW 01 DUSUN SENGGIRING], [98], [96], [194], [102.1], [58], [15],
  [RT 002 RW 01 DUSUN SENGGIIRING], [67], [73], [140], [91.8], [41], [17],
  [RT 003 RW 01 DUSUN SENGGIRING], [59], [64], [123], [92.2], [37], [6],
  [RT 004 RW 02 DUSUN BENTENG RAYA], [57], [64], [121], [89.1], [40], [11],
  [RT 005 RW 02 DUSUN BENTENG RAYA], [143], [106], [249], [134.9], [62], [9],
  [RT 006 RW 02 DUSUN BENTENG RAYA], [108], [92], [200], [117.4], [57], [14],
  [RT 007 RW 03 DUSUN BENTENG TIMUR], [76], [81], [157], [93.8], [50], [16],
  [RT 008 RW 03 DUSUN BENTENG TIMUR], [52], [77], [129], [67.5], [50], [2],
  [RT 009 RW 03 DUSUN BENTENG TIMUR], [64], [74], [138], [86.5], [46], [9],
  [RT 010 RW 03 DUSUN SEPAKAT TENGAH], [66], [72], [138], [91.7], [39], [10],
  [RT 011 RW 03 DUSUN SEPAKAT TENGAH], [54], [51], [105], [105.9], [32], [24],
  [RT 012 RW 04 DUSUN SEPAKAT TENGAH], [146], [124], [270], [117.7], [72], [41],
  [RT 013 RW 04 DUSUN SEPAKAT TENGAH], [70], [62], [132], [112.9], [37], [6],
  [RT 014 RW 04 DUSUN SEPAKAT TENGAH], [71], [83], [154], [85.5], [37], [16],
  [RT 015 RW 05 DUSUN SEPAKAT DARAT], [82], [76], [158], [107.9], [41], [11],
  [RT 016 RW 05 DUSUN SEPAKAT DARAT], [92], [105], [197], [87.6], [47], [14],
  [RT 017 RW 05 DUSUN SEPAKAT DARAT], [95], [90], [185], [105.6], [50], [10],
  [RT 018 RW 03 DUSUN BENTENG TIMUR], [105], [85], [190], [123.5], [65], [10],
  [RT 019 RW 04 DUSUN SEPAKAT TENGAH], [79], [60], [139], [131.7], [37], [8],
  [RT 020 RW 01 DUSUN SENGGIRING], [82], [75], [157], [109.3], [53], [16],
  [RT 021 RW 06 DUSUN KEDAUNG], [66], [66], [132], [100.0], [37], [15],
  [RT 022 RW 06 DUSUN KEDAUNG], [44], [36], [80], [122.2], [23], [5],
  [RT 023 RW 06 DUSUN KEDAUNG], [111], [95], [206], [116.8], [56], [0],
  [RT 024 RW 07 DUSUN SENAMBANG], [57], [51], [108], [111.8], [34], [2],
  [RT 025 RW 07 DUSUN SENAMBANG], [71], [67], [138], [106.0], [33], [12],
  [RT 026 RW 07 DUSUN SENAMBANG], [101], [111], [212], [91.0], [47], [21],
  [RT 027 RW 08 DUSUN KONSASI], [65], [54], [119], [120.4], [36], [10],
  [RT 028 RW 08 DUSUN KONSASI], [86], [70], [156], [122.9], [35], [15],
  [RT 029 RW 08 DUSUN KONSASI], [56], [52], [108], [107.7], [34], [13],
  [RT 030 RW 05 DUSUN SEPAKAT DARAT], [54], [38], [92], [142.1], [33], [14],
  [RT 031 RW 02 DUSUN BENTENG RAYA], [39], [38], [77], [102.6], [38], [10],
  [RT 032 RW 07 DUSUN SENAMBANG], [71], [68], [139], [104.4], [33], [18],
  [RT 033 RW 04 DUSUN SEPAKAT TENGAH], [95], [100], [195], [95.0], [50], [14],
  [RT 034 RW 05 DUSUN SEPAKAT DARAT], [86], [115], [201], [74.8], [45], [9],
  [RT 035 RW 04 DUSUN SEPAKAT TENGAH], [79], [79], [158], [100.0], [50], [15],
  [RT 036 RW 03 DUSUN BENTENG TIMUR], [115], [98], [213], [117.3], [63], [7],
  [RT 037 RW 05 DUSUN SEPAKAT DARAT], [40], [51], [91], [78.4], [63], [19],
  [*TOTAL DESA*], [*2902*], [*2799*], [*5701*], [*103.7*], [*1661*], [*464*]
)

#pagebreak()

== BAB III: PENDIDIKAN & BANTUAN SOSIAL

- *Jenjang Pendidikan:* TK (94), SD (460), SMP (259), SMA (216), Sarjana (16)
- *Anak Putus Sekolah (7-18 Th):* *32 anak*
- *Keluarga Penerima Bansos:* PKH (70), BPNT (62), BST (8), BLT (7)

#v(8pt)

=== Tabel Pendidikan, Putus Sekolah, KTP-el, & Bansos per RT

#table(
  columns: (2fr, 0.6fr, 0.6fr, 0.6fr, 0.6fr, 0.6fr, 0.8fr, 1fr),
  fill: (x, y) => if y == 0 { rgb("#0f4c81") } else if y == 38 { rgb("#e5e7eb") } else if calc.even(y) { rgb("#f9fafb") } else { white },
  stroke: 0.3pt + rgb("#e5e7eb"),
  align: (col, row) => if row == 0 { center + horizon } else if col == 0 { left + horizon } else { center + horizon },
  table.header([*Nama RT*], [*SD*], [*SMP*], [*SMA*], [*S1*], [*Putus*], [*KTP*], [*Bansos*]),
  [RT 001 RW 01 DUSUN SENGGIRING], [11], [1], [7], [0], [0], [160], [0],
  [RT 002 RW 01 DUSUN SENGGIIRING], [9], [2], [7], [1], [3], [105], [4],
  [RT 003 RW 01 DUSUN SENGGIRING], [22], [5], [10], [0], [0], [85], [0],
  [RT 004 RW 02 DUSUN BENTENG RAYA], [16], [4], [4], [0], [0], [83], [9],
  [RT 005 RW 02 DUSUN BENTENG RAYA], [13], [9], [6], [0], [0], [109], [6],
  [RT 006 RW 02 DUSUN BENTENG RAYA], [8], [5], [3], [0], [0], [156], [2],
  [RT 007 RW 03 DUSUN BENTENG TIMUR], [9], [6], [6], [0], [2], [125], [0],
  [RT 008 RW 03 DUSUN BENTENG TIMUR], [20], [10], [5], [0], [0], [74], [0],
  [RT 009 RW 03 DUSUN BENTENG TIMUR], [5], [5], [9], [0], [0], [102], [0],
  [RT 010 RW 03 DUSUN SEPAKAT TENGAH], [5], [6], [11], [0], [0], [104], [0],
  [RT 011 RW 03 DUSUN SEPAKAT TENGAH], [4], [6], [2], [3], [0], [0], [6],
  [RT 012 RW 04 DUSUN SEPAKAT TENGAH], [3], [11], [9], [0], [0], [229], [0],
  [RT 013 RW 04 DUSUN SEPAKAT TENGAH], [11], [8], [5], [3], [5], [84], [12],
  [RT 014 RW 04 DUSUN SEPAKAT TENGAH], [15], [5], [3], [0], [1], [84], [14],
  [RT 015 RW 05 DUSUN SEPAKAT DARAT], [23], [11], [5], [2], [5], [109], [23],
  [RT 016 RW 05 DUSUN SEPAKAT DARAT], [20], [7], [3], [0], [6], [152], [4],
  [RT 017 RW 05 DUSUN SEPAKAT DARAT], [11], [15], [4], [2], [2], [146], [0],
  [RT 018 RW 03 DUSUN BENTENG TIMUR], [20], [6], [8], [0], [0], [137], [0],
  [RT 019 RW 04 DUSUN SEPAKAT TENGAH], [6], [6], [10], [0], [0], [102], [0],
  [RT 020 RW 01 DUSUN SENGGIRING], [11], [4], [1], [0], [0], [121], [0],
  [RT 021 RW 06 DUSUN KEDAUNG], [18], [11], [8], [0], [0], [95], [2],
  [RT 022 RW 06 DUSUN KEDAUNG], [8], [6], [3], [0], [0], [58], [0],
  [RT 023 RW 06 DUSUN KEDAUNG], [12], [11], [12], [0], [0], [128], [0],
  [RT 024 RW 07 DUSUN SENAMBANG], [5], [8], [2], [0], [0], [98], [0],
  [RT 025 RW 07 DUSUN SENAMBANG], [14], [8], [5], [0], [0], [111], [0],
  [RT 026 RW 07 DUSUN SENAMBANG], [10], [11], [15], [0], [0], [172], [0],
  [RT 027 RW 08 DUSUN KONSASI], [14], [3], [7], [0], [0], [80], [5],
  [RT 028 RW 08 DUSUN KONSASI], [20], [16], [7], [0], [0], [117], [0],
  [RT 029 RW 08 DUSUN KONSASI], [6], [2], [1], [0], [7], [59], [20],
  [RT 030 RW 05 DUSUN SEPAKAT DARAT], [2], [3], [1], [0], [0], [78], [0],
  [RT 031 RW 02 DUSUN BENTENG RAYA], [9], [2], [2], [0], [0], [55], [0],
  [RT 032 RW 07 DUSUN SENAMBANG], [7], [12], [4], [0], [0], [115], [0],
  [RT 033 RW 04 DUSUN SEPAKAT TENGAH], [28], [10], [5], [1], [0], [105], [17],
  [RT 034 RW 05 DUSUN SEPAKAT DARAT], [16], [3], [4], [1], [0], [87], [14],
  [RT 035 RW 04 DUSUN SEPAKAT TENGAH], [10], [5], [7], [1], [1], [143], [9],
  [RT 036 RW 03 DUSUN BENTENG TIMUR], [19], [13], [9], [2], [0], [137], [0],
  [RT 037 RW 05 DUSUN SEPAKAT DARAT], [20], [3], [6], [0], [0], [116], [0],
  [*TOTAL DESA*], [*460*], [*259*], [*216*], [*16*], [*32*], [*4021*], [*147*]
)

#v(15pt)

== BAB IV: PERUMAHAN & INFRASTRUKTUR

- *Total Bumbung Rumah:* *1,371 unit*
- *Kepadatan Hunian Desa:* *4.16 jiwa per rumah*

#v(20pt)

#align(center)[
  #text(weight: "bold", size: 12pt, fill: rgb("#0f4c81"))[MENCERDASKAN BANGSA DENGAN DATA STATISTIK DESA]
]
