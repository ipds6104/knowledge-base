// Surat Dinas Permintaan Data KCDA 2026 ke Baperidda Kabupaten Mempawah
#set page(
  paper: "a4",
  margin: (
    top: 4.4cm,
    bottom: 2.0cm,
    left: 2.2cm,
    right: 2.2cm
  ),
  header: locate(loc => {
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
#v(6pt)
#grid(
  columns: (1fr, 170pt),
  gutter: 10pt,
  [
    #grid(
      columns: (65pt, 8pt, 1fr),
      gutter: 4pt,
      [Nomor], [:], [B-1084/61046/HM.310/2026],
      [Sifat], [:], [Biasa],
      [Lampiran], [:], [1 (satu) Berkas],
      [Hal], [:], [*Permintaan Data Untuk Publikasi Kecamatan Dalam Angka 2026*]
    )
  ],
  [
    #align(right)[
      Mempawah, 8 September 2026
    ]
  ]
)

#v(14pt)
Yth. *Kepala Badan Perencanaan Pembangunan,* \
#h(20pt)*Riset dan Inovasi Daerah Kabupaten Mempawah* \
di Mempawah

#v(14pt)
Dengan hormat,

Sehubungan dengan penyusunan Publikasi Kecamatan Dalam Angka 2026, kami bermaksud mengajukan permohonan data *Luas Wilayah menurut desa/kelurahan di Kabupaten Mempawah tahun 2025* sesuai format terlampir.

Data tersebut dapat disampaikan ke Kantor BPS Kabupaten Mempawah maupun dikirimkan dalam bentuk salinan digital (_softcopy_) melalui narahubung kami. Besar harapan kami data dimaksud dapat kami terima sebelum *Jumat, 18 September 2026*. Untuk koordinasi lebih lanjut, Bapak/Ibu dapat menghubungi narahubung kami, *Sukma Andini, S.Tr.Stat.* (WhatsApp: 0858-1547-2475).

Demikian permintaan data ini kami sampaikan, atas perhatian dan kerjasamanya kami ucapkan terima kasih.

#v(20pt)

#align(right)[
  #block(width: 220pt)[
    #align(center)[
      Kepala Badan Pusat Statistik \
      Kabupaten Mempawah,
      #v(60pt)
      *Munawir*
    ]
  ]
]

// =============================================================================
// HALAMAN LAMPIRAN
// =============================================================================
#pagebreak()

#v(4pt)
#grid(
  columns: (65pt, 8pt, 1fr),
  gutter: 3.5pt,
  [Lampiran 1], [], [],
  [Nomor], [:], [B-1084/61046/HM.310/2026],
  [Tanggal], [:], [8 September 2026]
)

#v(10pt)
#align(center)[
  #text(11pt, weight: "bold")[Luas Wilayah menurut Desa/Kelurahan di Kabupaten Mempawah Tahun 2025]
]
#v(6pt)

#set text(size: 9pt)
#table(
  columns: (32pt, 1.3fr, 1.7fr, 1.2fr),
  inset: 4.5pt,
  align: (center, left, left, right),
  stroke: (col, row) => {
    let red_b = 1.3pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let top_b = if row == 0 { 1pt + black } else if row == 2 { 1pt + black } else { norm }
    let bot_b = if row == 1 { 1pt + black } else if row == 69 { 1.2pt + black } else { norm }
    
    // Border merah outer pada kolom isian (kolom 3 / Luas Total Area)
    let is_val_row = (row >= 2 and row < 69)
    let r_top = if row == 2 and col == 3 { red_b } else { top_b }
    let r_bot = if row == 68 and col == 3 { red_b } else { bot_b }
    let r_left = if is_val_row and col == 3 { red_b } else { norm }
    let r_right = if is_val_row and col == 3 { red_b } else { norm }
    
    (top: r_top, bottom: r_bot, left: r_left, right: r_right)
  },
  fill: (col, row) => {
    if row == 0 or row == 1 {
      rgb("#F3F4F6")
    } else if row == 69 {
      rgb("#F9FAFB")
    } else if col == 3 {
      rgb("#FEF2F2")
    } else {
      none
    }
  },
    table.header([*No*], [*Kecamatan*], [*Desa/Kelurahan*], [*Luas Total Area (km#super[2])*], [*(1)*], [*(2)*], [*(3)*], [*(4)*]),
    [1], [*Jongkat*], [Sungai Nipah], [],
    [2], [], [Jungkat], [],
    [3], [], [Wajok Hilir], [],
    [4], [], [Wajok Hulu], [],
    [5], [], [Peniti Luar], [],
    [6], [*Segedong*], [Peniti Dalam I], [],
    [7], [], [Sungai Burung], [],
    [8], [], [Sungai Purun Besar], [],
    [9], [], [Parit Bugis], [],
    [10], [], [Peniti Besar], [],
    [11], [], [Peniti Dalam II], [],
    [12], [*Sungai Pinyuh*], [Sungai Purun Kecil], [],
    [13], [], [Peniraman], [],
    [14], [], [Nusapati], [],
    [15], [], [Galang], [],
    [16], [], [Sungai Rasau], [],
    [17], [], [Sungai Pinyuh], [],
    [18], [], [Sungai Batang], [],
    [19], [], [Sungai Bakau Besar Laut], [],
    [20], [], [Sungai Bakau Besar Darat], [],
    [21], [*Anjongan*], [Anjungan Melancar], [],
    [22], [], [Anjungan Dalam], [],
    [23], [], [Pak Bulu], [],
    [24], [], [Dema], [],
    [25], [], [Kepayang], [],
    [26], [*Mempawah Hilir*], [Tanjung], [],
    [27], [], [Kuala Secapah], [],
    [28], [], [Tengah], [],
    [29], [], [Terusan], [],
    [30], [], [Pasir], [],
    [31], [], [Penibung], [],
    [32], [], [Sengkubang], [],
    [33], [], [Malikian], [],
    [34], [*Mempawah Timur*], [Pasir Wan Salim], [],
    [35], [], [Sungai Bakau Kecil], [],
    [36], [], [Pasir Panjang], [],
    [37], [], [Pasir Palembang], [],
    [38], [], [Pulau Pedalaman], [],
    [39], [], [Antibar], [],
    [40], [], [Sejegi], [],
    [41], [], [Parit Banjar], [],
    [42], [*Sungai Kunyit*], [Semudun], [],
    [43], [], [Semparong Parit Raden], [],
    [44], [], [Mendalok], [],
    [45], [], [Sungai Dungun], [],
    [46], [], [Sungai Limau], [],
    [47], [], [Sungai Kunyit Laut], [],
    [48], [], [Sungai Kunyit Dalam], [],
    [49], [], [Sungai Kunyit Hulu], [],
    [50], [], [Bukit Batu], [],
    [51], [], [Sungai Bundung Laut], [],
    [52], [], [Sungai Duri I], [],
    [53], [], [Sungai Duri II], [],
    [54], [*Toho*], [Sambora], [],
    [55], [], [Benuang], [],
    [56], [], [Pak Utan], [],
    [57], [], [Sepang], [],
    [58], [], [Pak Laheng], [],
    [59], [], [Terap], [],
    [60], [], [Kecurit], [],
    [61], [], [Toho Ilir], [],
    [62], [*Sadaniang*], [Pentek], [],
    [63], [], [Sekabuk], [],
    [64], [], [Bumbun], [],
    [65], [], [Amawang], [],
    [66], [], [Ansiap], [],
    [67], [], [Suak Barangan], [],
    [], [*TOTAL*], [], [],
)

#v(6pt)
#text(8pt, style: "italic", fill: rgb("#4B5563"))[Catatan: Kolom (4) dapat diisi luas wilayah dalam kilometer persegi (km²).]
