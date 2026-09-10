// Publikasi Resmi BPS Kabupaten Mempawah: Kecamatan Dalam Angka 2026 (Ukuran A5)

#set page(
  paper: "a5",
  margin: (
    inside: 2.0cm,
    outside: 1.5cm,
    top: 2.0cm,
    bottom: 2.0cm,
  ),
  header: context {
    let page_num = counter(page).get().first()
    // Running header muncul setelah frontmatter (halaman 7 ke atas)
    if page_num >= 7 {
      if calc.even(page_num) {
        align(left, text(6.5pt, fill: rgb("#B45309"), weight: "bold")[KECAMATAN SUNGAI KUNYIT DALAM ANGKA 2026])
      } else {
        align(right, text(6.5pt, fill: rgb("#B45309"), weight: "bold")[BPS KABUPATEN MEMPAWAH])
      }
    }
  },
  footer: context {
    let page_num = counter(page).get().first()
    if page_num > 1 and page_num < 7 {
      // Halaman iii suppressed sesuai pedoman resmi KCDA
      if page_num != 3 {
        align(center, text(7.5pt)[#counter(page).display("i")])
      }
    } else if page_num >= 7 {
      if calc.even(page_num) {
        align(left, text(7.5pt, weight: "medium")[#counter(page).display("1")])
      } else {
        align(right, text(7.5pt, weight: "medium")[#counter(page).display("1")])
      }
    }
  }
)

#set text(font: ("Liberation Sans", "Arial"), size: 7.5pt, lang: "id")
#set par(justify: true, leading: 0.5em)


// ==========================================
// 1. KOVER DEPAN (FRONT COVER) - TEMPLATE PUSAT
// ==========================================
#page(
  margin: (top: 1.5cm, bottom: 1.5cm, left: 1.5cm, right: 1.5cm),
  fill: rgb("#737373"),
  header: none,
  footer: none,
)[
  // Pojok kanan atas: Katalog & ISSN
  #align(right)[
    #text(7.5pt, fill: rgb("#F3F4F6"))[
      #text(style: "italic")[Katalog/Catalogue:] \
      #text(weight: "bold")[1102001.6104060] \
      #text(style: "italic")[ISSN xxxx-xxxx]
    ]
  ]

  #v(0.8cm)

  // Judul Publikasi di Tengah Atas
  #align(center)[
    #text(16pt, weight: "bold", fill: white)[KECAMATAN SUNGAI KUNYIT] \
    #v(2pt)
    #text(15pt, weight: "bold", fill: white)[DALAM ANGKA] \
    #v(4pt)
    #text(11pt, style: "italic", fill: rgb("#F3F4F6"))[Sungai Kunyit District in Figures] \
    #v(3pt)
    #text(8.5pt, fill: rgb("#E5E7EB"))[Volume XX, 2026]
  ]

  // Lingkaran Putih Badge 2026 di kanan
  #place(top + right, dx: 0.2cm, dy: 3.8cm)[
    #circle(radius: 1.25cm, fill: white)[
      #align(center + horizon)[
        #text(15pt, weight: "bold", fill: rgb("#1F2937"))[2026]
      ]
    ]
  ]

  #v(1.0cm)

  // Placeholder Foto / Ilustrasi Kover Depan
  #align(center)[
    #rect(
      width: 6.8cm,
      height: 4.8cm,
      fill: rgb(255, 255, 255, 12%),
      stroke: (paint: rgb(255, 255, 255, 60%), thickness: 1pt, dash: "dashed"),
      radius: 6pt
    )[
      #align(center + horizon)[
        #text(28pt)[📷] \
        #v(4pt)
        #text(9pt, weight: "bold", fill: rgb("#E5E7EB"))[COVER DEPAN]
      ]
    ]
  ]

  #v(1.2cm)

  // Bawah Kover: Logo BPS & Nama Instansi
  #align(center)[
    #grid(
      columns: (auto, auto),
      column-gutter: 8pt,
      align: horizon,
      image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", height: 26pt),
      align(left)[
        #text(8pt, weight: "bold", fill: white)[BADAN PUSAT STATISTIK] \
        #text(8pt, weight: "bold", fill: white)[KABUPATEN MEMPAWAH] \
        #text(6.5pt, fill: rgb("#E5E7EB"))[BPS-STATISTICS OF MEMPAWAH REGENCY]
      ]
    )
  ]
]

#pagebreak()

// ==========================================
// 2. HALAMAN KATALOG & HAK CIPTA (HALAMAN ii)
// ==========================================
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: horizon,
  image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", height: 26pt),
  align(left)[
    #text(8pt, weight: "bold", fill: rgb("#00A0E9"))[BADAN PUSAT STATISTIK] \
    #text(8pt, weight: "bold", fill: rgb("#00A0E9"))[KABUPATEN MEMPAWAH] \
    #text(6.5pt, fill: rgb("#00A0E9"))[BPS-STATISTICS OF MEMPAWAH REGENCY]
  ]
)

#v(2pt)
#line(length: 100%, stroke: 0.5pt + rgb("#D1D5DB"))

#v(8pt)
#text(10.5pt, weight: "bold")[KECAMATAN SUNGAI KUNYIT DALAM ANGKA] \
#text(9.5pt, style: "italic")[Sungai Kunyit District in Figures] \
#text(9.5pt)[2026] \
#text(8pt, fill: luma(100))[Volume xx, 2026]

#v(8pt)
#grid(
  columns: (1fr, 1.2fr),
  row-gutter: 5pt,
  [*Katalog/Catalogue:*], [1102001.6104060],
  [*ISSN:*], [-],
  [*Nomor Publikasi/Publication Number:*], [61040.26005],
  [], [],
  [*Ukuran Buku/Book Size:*], [14,8 cm x 21 cm],
  [*Jumlah Halaman/Number of Pages:*], [viii + 35 hal/pages],
  [], [],
  [*Penyusun Naskah/Manuscript Drafter:*], [BPS Kabupaten Mempawah \ BPS-Statistics of Mempawah Regency],
  [*Penyunting/Editor:*], [BPS Kabupaten Mempawah \ BPS-Statistics of Mempawah Regency],
  [*Pembuat Kover/Cover Designer:*], [BPS Kabupaten Mempawah \ BPS-Statistics of Mempawah Regency],
  [*Penerbit/Publisher:*], [© BPS Kabupaten Mempawah/BPS-Statistics of Mempawah Regency],
  [*Sumber Ilustrasi/Illustration Source:*], [-]
)

#v(10pt)
#text(6.5pt)[
  *Dilarang mereproduksi dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari Badan Pusat Statistik Kabupaten Mempawah.* \
  _It is prohibited to reproduce and/or duplicate part or all of this book for commercial purpose without permission from BPS-Statistics of Mempawah Regency._
]

#pagebreak()

// ==========================================
// 3. TIM PENYUSUN / COMPILERS (HALAMAN iii)
// ==========================================
#align(right)[
  #text(7pt, fill: luma(120))[ISSN xxxx-xxxx]
]

#v(0.6cm)

#align(center)[
  #text(10.5pt, weight: "bold")[TIM PENYUSUN/COMPILERS] \
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan Sungai Kunyit Dalam Angka 2026] \
  #text(8pt, style: "italic")[Sungai Kunyit District in Figures 2026] \
  #text(7.5pt)[Volume xx, 2026]
  
  #v(16pt)
  #text(8.5pt, weight: "bold")[Pengarah/Director] \
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penanggung Jawab/Persons in Charge] \
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penyunting/Editors] \
  #text(8pt)[Kurniawan #sym.circle.filled.small Sukma Andini]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Pengolah Data dan Penulis Naskah/Data Processor and Writers] \
  #text(8pt)[Sarah Pratiwi]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penata Letak/Layouters] \
  #text(8pt)[Tim IPDS BPS Kabupaten Mempawah]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penerjemah/Translators] \
  #text(8pt)[Tim IPDS BPS Kabupaten Mempawah]
]

#pagebreak()

// ==========================================
// 4. KONTRIBUTOR DATA (HALAMAN iv)
// ==========================================
#align(center)[
  #text(10.5pt, weight: "bold")[KONTRIBUTOR DATA/DATA CONTRIBUTORS]
]
#v(12pt)

#list(
  [Kantor Camat Sungai Kunyit],
  [Kementerian Agama],
  [Kementerian Pendidikan dan Kebudayaan],
  [Dinas Pendidikan, Pemuda, Olahraga dan Pariwisata],
  [Dinas Pertanian, Ketahanan Pangan dan Perikanan],
  [Dinas Kesehatan, Pengendalian Penduduk dan KB],
  [Dinas Perindustrian, Perdagangan dan Tenaga Kerja],
  [Dinas Kependudukan dan Pencatatan Sipil],
  [Badan Pusat Statistik]
)

#pagebreak()

// ==========================================
// 5. KATA PENGANTAR (HALAMAN v)
// ==========================================
#align(center)[
  #text(11pt, weight: "bold")[KATA PENGANTAR / PREFACE]
]
#v(10pt)

#grid(
  columns: (1fr, 1fr),
  column-gutter: 12pt,
  [
    #text(7.5pt)[
      Publikasi *Kecamatan Sungai Kunyit Dalam Angka 2026* merupakan seri tahunan BPS Kabupaten Mempawah yang menyajikan beragam data dari BPS, kecamatan, kelurahan/desa, serta instansi terkait. Publikasi ini memuat gambaran umum mengenai geografi, pemerintahan, serta kondisi sosial demografi dan perekonomian di Kecamatan Sungai Kunyit.

      Data yang disajikan diharapkan dapat menjadi indikator penting dalam mendukung perencanaan dan pengambilan kebijakan pembangunan daerah berbasis data akurat.

      Ucapan terima kasih disampaikan kepada Camat Sungai Kunyit, para Lurah/Kepala Desa se-Kecamatan Sungai Kunyit, serta seluruh pihak yang telah membantu dalam penyusunan publikasi ini. Kritik dan saran membangun sangat kami harapkan demi penyempurnaan edisi berikutnya.
    ]
  ],
  [
    #text(7.5pt, style: "italic")[
      *"Sungai Kunyit District in Figures 2026"* is an annual series issued by BPS-Statistics of Mempawah Regency, presenting various data collected from BPS, subdistrict offices, villages/urban villages, and related regional agencies. This publication provides a comprehensive overview of geography, governance, as well as social, demographic, and economic conditions across villages in Sungai Kunyit District.

      The data presented are expected to serve as vital empirical indicators to support evidence-based regional development planning and policy-making.

      We express our sincere gratitude to the Head of Sungai Kunyit District, village heads, and all collaborating institutions. Constructive feedback is warmly appreciated for continuous refinement.
    ]
  ]
)

#v(14pt)
#align(right)[
  #block(width: 60%)[
    #text(7.5pt)[
      Mempawah, September 2026 \
      *Kepala BPS Kabupaten Mempawah* \
      _Chief Statistician of Mempawah Regency_ \
      #v(1.4cm)
      *Munawir*
    ]
  ]
]

#pagebreak()

// ==========================================
// 6. DAFTAR ISI (HALAMAN vii)
// ==========================================
#text(11pt, weight: "bold")[DAFTAR ISI / CONTENTS]
#v(6pt)
#line(length: 100%, stroke: 0.5pt + rgb("#D1D5DB"))
#v(6pt)

#grid(
  columns: (1fr, auto),
  row-gutter: 6pt,
  [*Halaman Judul / Title Page*], [i],
  [*Halaman Katalog & Hak Cipta / Catalog and Copyright*], [ii],
  [*Tim Penyusun / Compilers*], [iii],
  [*Kontributor Data / Data Contributors*], [iv],
  [*Kata Pengantar / Preface*], [v],
  [*Daftar Isi / Table of Contents*], [vii],
  [*Bab 1: Geografi dan Iklim / Geography and Climate*], [1],
  [*Bab 2: Pemerintahan / Government*], [5],
  [*Bab 3: Kependudukan / Population*], [9],
  [*Bab 4: Sosial dan Kesejahteraan Rakyat / Social and Welfare*], [11],
  [*Bab 5: Pertanian / Agriculture*], [19],
  [*Bab 6: Pariwisata, Transportasi & Komunikasi / Tourism, Transport & Comm.*], [25],
  [*Bab 7: Perbankan, Koperasi & Perdagangan / Banking, Cooperative & Trade*], [28]
)

#pagebreak()


// ==========================================
// BAB 1: GEOGRAFI DAN IKLIM
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 1: GEOGRAFI DAN IKLIM] \
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 1: GEOGRAPHY AND CLIMATE]
  ]
)
#v(10pt)

#text(8.5pt)[
Kecamatan Sungai Kunyit secara astronomis dan geografis terletak di wilayah pesisir dan daratan Kabupaten Mempawah, Provinsi Kalimantan Barat dengan ibukota kecamatan berada di Sungai Kunyit Laut. Wilayah ini terbagi ke dalam 12 desa/kelurahan dengan akses perhubungan darat dan air yang menghubungkan pusat-pusat kegiatan ekonomi lokal dengan ibukota kabupaten.
]

#v(8pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 1.1: Luas Daerah Menurut Desa/Kelurahan di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 1.1: Total Area by Village/Subdistrict in Sungai Kunyit Subdistrict, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.5fr, 1.3fr, 1.2fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Luas Daerah
Total Area (km²)*], [*Persentase
Percentage (%)*], [(1)], [(2)], [(3)]),
  [Semudun], [2.938], [9,51],
  [Semparong Parit Raden], [2.196], [7,11],
  [Mendalok], [2.124], [6,88],
  [Sungai Dungun], [2.351], [7,61],
  [Sungai Limau], [2.195], [7,11],
  [Sungai Kunyit Laut], [3.255], [10,54],
  [Sungai Kunyit Dalam], [1.682], [5,44],
  [Sungai Kunyit Hulu], [3.900], [12,62],
  [Bukit Batu], [2.972], [9,62],
  [Sungai Bundung Laut], [2.241], [7,25],
  [Sungai Duri I], [2.603], [8,43],
  [Sungai Duri II], [2.436], [7,89]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Dinas Kependudukan dan Pencatatan Sipil / BAPEDDA Kabupaten Mempawah]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 1.2: Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten Menurut Desa/Kelurahan di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 1.2: Distance to Subdistrict and Regency Capital by Village in Sungai Kunyit Subdistrict, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.5fr, 1.3fr, 1.3fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Ke Ibukota Kec.
To District Capital (km)*], [*Ke Ibukota Kab.
To Regency Capital (km)*], [(1)], [(2)], [(3)]),
  [Semudun], [...], [...],
  [Semparong Parit Raden], [...], [...],
  [Mendalok], [...], [...],
  [Sungai Dungun], [...], [...],
  [Sungai Limau], [...], [...],
  [Sungai Kunyit Laut], [...], [...],
  [Sungai Kunyit Dalam], [...], [...],
  [Sungai Kunyit Hulu], [...], [...],
  [Bukit Batu], [...], [...],
  [Sungai Bundung Laut], [...], [...],
  [Sungai Duri I], [...], [...],
  [Sungai Duri II], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Sungai Kunyit]
#v(8pt)

#v(10pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 1.3: Batas Administrasi Kecamatan Sungai Kunyit Menurut Arah Mata Angin, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 1.3: Administrative Borders of Sungai Kunyit Subdistrict by Cardinal Direction, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (0.6fr, 1.8fr, 3.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*No*], [*Arah Mata Angin
Wind Direction*], [*Berbatasan Dengan
Bordering With*], [(1)], [(2)], [(3)]),
  [1], [Utara/North], [...],
  [2], [Selatan/South], [...],
  [3], [Barat/West], [...],
  [4], [Timur/East], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Sungai Kunyit / Bagian Tata Pemerintahan Setda Mempawah]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 1.4: Jarak Kantor Camat Sungai Kunyit dengan Kota dan Tempat Penting Lainnya, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 1.4: Distance from Sungai Kunyit Subdistrict Office to Other Important Places, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (0.6fr, 3.2fr, 1.2fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*No*], [*Nama Kota dan Tempat Penting
Other Important Places*], [*Jarak
Distance (km)*], [(1)], [(2)], [(3)]),
  [1], [Ibukota Provinsi Kalimantan Barat 
(Kota Pontianak)], [...],
  [2], [Pusat Pemerintahan Kabupaten 
Mempawah (Mempawah Hilir)], [...],
  [3], [Makam Juang Mandor], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Sungai Kunyit]
#v(8pt)

#pagebreak()


// ==========================================
// BAB 2: PEMERINTAHAN
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 2: PEMERINTAHAN] \
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 2: GOVERNMENT]
  ]
)
#v(10pt)

#text(8.5pt)[
Secara administratif, Kecamatan Sungai Kunyit terbagi menjadi 12 desa/kelurahan yang dipimpin oleh kepala desa dan lurah definitif, didukung oleh aparatur pemerintah desa, Badan Permusyawaratan Desa (BPD), serta kelembagaan RT dan RW sebagai garda terdepan pelayanan kemasyarakatan.
]

#v(8pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 2.1.1: Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 2.1.1: Number of Hamlets, RW, and RT by Village/Subdistrict in Sungai Kunyit Subdistrict, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Jumlah Dusun
Hamlets*], [*Rukun Warga
(RW)*], [*Rukun Tetangga
(RT)*], [(1)], [(2)], [(3)], [(4)]),
  [Semudun], [...], [...], [...],
  [Semparong Parit Raden], [...], [...], [...],
  [Mendalok], [...], [...], [...],
  [Sungai Dungun], [...], [...], [...],
  [Sungai Limau], [...], [...], [...],
  [Sungai Kunyit Laut], [...], [...], [...],
  [Sungai Kunyit Dalam], [...], [...], [...],
  [Sungai Kunyit Hulu], [...], [...], [...],
  [Bukit Batu], [...], [...], [...],
  [Sungai Bundung Laut], [...], [...], [...],
  [Sungai Duri I], [...], [...], [...],
  [Sungai Duri II], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Sungai Kunyit]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 2.1.2: Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan Sungai Kunyit] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 2.1.2: Names of District Heads of Sungai Kunyit Subdistrict]
#v(2pt)
#align(center)[
#table(
  columns: (0.6fr, 2.8fr, 1.6fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*No*], [*Nama Camat
Name of District Head*], [*Periode Menjabat
Period*], [(1)], [(2)], [(3)]),
  [1], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Sungai Kunyit]
#v(8pt)

#v(10pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 2.1.3: Nama-Nama Kepala Desa/Lurah di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 2.1.3: Names of Village Heads in Sungai Kunyit Subdistrict, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (0.6fr, 2.2fr, 2.8fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*No*], [*Desa/Kelurahan
Village/Subdistrict*], [*Nama Kepala Desa / Lurah
Name of Village Head*], [(1)], [(2)], [(3)]),
  [1], [Semudun], [...],
  [2], [Semparong Parit Raden], [...],
  [3], [Mendalok], [...],
  [4], [Sungai Dungun], [...],
  [5], [Sungai Limau], [...],
  [6], [Sungai Kunyit Laut], [...],
  [7], [Sungai Kunyit Dalam], [...],
  [8], [Sungai Kunyit Hulu], [...],
  [9], [Bukit Batu], [...],
  [10], [Sungai Bundung Laut], [...],
  [11], [Sungai Duri I], [...],
  [12], [Sungai Duri II], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Sungai Kunyit]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 2.1.6: Status Desa Berdasarkan Indeks Desa Membangun (IDM) di Kecamatan Sungai Kunyit, 2024/2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 2.1.6: Village Status Based on Developing Village Index (IDM) in Sungai Kunyit Subdistrict, 2024/2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.5fr, 1.2fr, 1.5fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Skor IDM
IDM Score*], [*Status IDM
IDM Status*], [(1)], [(2)], [(3)]),
  [Semudun], [...], [...],
  [Semparong Parit Raden], [...], [...],
  [Mendalok], [...], [...],
  [Sungai Dungun], [...], [...],
  [Sungai Limau], [...], [...],
  [Sungai Kunyit Laut], [...], [...],
  [Sungai Kunyit Dalam], [...], [...],
  [Sungai Kunyit Hulu], [...], [...],
  [Bukit Batu], [...], [...],
  [Sungai Bundung Laut], [...], [...],
  [Sungai Duri I], [...], [...],
  [Sungai Duri II], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kementerian Desa, Pembangunan Daerah Tertinggal, dan Transmigrasi]
#v(8pt)

#v(10pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 2.2.1: Jumlah Pegawai Negeri Sipil Pemerintah Daerah Kecamatan Menurut Golongan di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 2.2.1: Number of Civil Servants in Sungai Kunyit Subdistrict Office by Rank/Class, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Golongan
Rank / Class*], [*Laki-laki
Male*], [*Perempuan
Female*], [*Jumlah
Total*], [(1)], [(2)], [(3)], [(4)]),
  [Golongan I], [...], [...], [...],
  [Golongan II], [...], [...], [...],
  [Golongan III], [...], [...], [...],
  [Golongan IV], [...], [...], [...],
  [Jumlah / Total], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Sungai Kunyit]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 2.2.2: Jumlah Pegawai Negeri Sipil Pemerintah Daerah Kecamatan Menurut Tingkat Pendidikan di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 2.2.2: Number of Civil Servants in Sungai Kunyit Subdistrict Office by Education Level, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Tingkat Pendidikan
Education Level*], [*Laki-laki
Male*], [*Perempuan
Female*], [*Jumlah
Total*], [(1)], [(2)], [(3)], [(4)]),
  [≤ SMP / Junior High], [...], [...], [...],
  [SMA / Senior High], [...], [...], [...],
  [Diploma I/II/III], [...], [...], [...],
  [S1 / D-IV (Bachelor)], [...], [...], [...],
  [S2 / Master], [...], [...], [...],
  [Jumlah / Total], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Sungai Kunyit]
#v(8pt)

#pagebreak()


// ==========================================
// BAB 3: KEPENDUDUKAN
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 3: KEPENDUDUKAN] \
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 3: POPULATION]
  ]
)
#v(10pt)

#text(8.5pt)[
Berdasarkan data registrasi semester II tahun 2025 dari Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah, jumlah penduduk Kecamatan Sungai Kunyit terdistribusi di 12 desa/kelurahan dengan struktur demografi yang produktif. Komposisi penduduk laki-laki dan perempuan relatif berimbang, mencerminkan kestabilan demografis wilayah.
]

#v(8pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 3.1: Penduduk, Distribusi Persentase, dan Kepadatan Penduduk Menurut Desa/Kelurahan di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 3.1: Population, Percentage Distribution, and Density by Village/Subdistrict in Sungai Kunyit Subdistrict, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.0fr, 1.0fr, 1.0fr, 1.1fr, 1.0fr, 1.2fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Laki-laki
Male*], [*Perempuan
Female*], [*Jumlah
Total*], [*Persentase
Percentage (%)*], [*Kepadatan
Density (jiwa/km²)*], [(1)], [(2)], [(3)], [(4)], [(5)], [(6)]),
  [Semudun], [1.527], [1.411], [2.938], [9,51], [262,20],
  [Semparong Parit Raden], [1.085], [1.111], [2.196], [7,11], [118,93],
  [Mendalok], [1.103], [1.021], [2.124], [6,88], [396,58],
  [Sungai Dungun], [1.202], [1.149], [2.351], [7,61], [327,00],
  [Sungai Limau], [1.108], [1.087], [2.195], [7,11], [1.068,23],
  [Sungai Kunyit Laut], [1.672], [1.583], [3.255], [10,54], [1.065,36],
  [Sungai Kunyit Dalam], [843], [839], [1.682], [5,44], [423,54],
  [Sungai Kunyit Hulu], [1.991], [1.909], [3.900], [12,62], [168,93],
  [Bukit Batu], [1.538], [1.434], [2.972], [9,62], [69,01],
  [Sungai Bundung Laut], [1.140], [1.101], [2.241], [7,25], [464,00],
  [Sungai Duri I], [1.326], [1.277], [2.603], [8,43], [1.517,08],
  [Sungai Duri II], [1.277], [1.159], [2.436], [7,89], [465,25]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah (Semester II 2025)]
#v(8pt)

#pagebreak()


// ==========================================
// BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT] \
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 4: SOCIAL AND WELFARE]
  ]
)
#v(10pt)

#text(8.5pt)[
Pembangunan bidang sosial kemasyarakatan di Kecamatan Sungai Kunyit ditopang oleh perluasan aksesibilitas sarana pendidikan dasar hingga menengah, peningkatan mutu fasilitas kesehatan masyarakat, ketersediaan energi penerangan rumah tangga, serta kesiapsiagaan dalam menghadapi potensi bencana lingkungan hidup.
]

#v(8pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 4.1.1: Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 4.1.1: Number of Villages Having Educational Facilities by Level in Sungai Kunyit Subdistrict, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.1fr, 1.1fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*SD / MI*], [*SMP / MTs*], [*SMA / SMK / MA*], [*Akademi / PT*], [(1)], [(2)], [(3)], [(4)], [(5)]),
  [Semudun], [...], [...], [...], [...],
  [Semparong Parit Raden], [...], [...], [...], [...],
  [Mendalok], [...], [...], [...], [...],
  [Sungai Dungun], [...], [...], [...], [...],
  [Sungai Limau], [...], [...], [...], [...],
  [Sungai Kunyit Laut], [...], [...], [...], [...],
  [Sungai Kunyit Dalam], [...], [...], [...], [...],
  [Sungai Kunyit Hulu], [...], [...], [...], [...],
  [Bukit Batu], [...], [...], [...], [...],
  [Sungai Bundung Laut], [...], [...], [...], [...],
  [Sungai Duri I], [...], [...], [...], [...],
  [Sungai Duri II], [...], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 4.1.2: Jumlah Satuan Pendidikan Menurut Tingkat Pendidikan di Kecamatan Sungai Kunyit, 2024/2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 4.1.2: Number of Educational Units by Education Level in Sungai Kunyit Subdistrict, 2024/2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Tingkat Pendidikan
Educational Level*], [*Negeri
Public*], [*Swasta
Private*], [*Jumlah
Total*], [(1)], [(2)], [(3)], [(4)]),
  [Taman Kanak-Kanak (TK)], [...], [...], [...],
  [Raudatul Athfal (RA)], [...], [...], [...],
  [Sekolah Dasar (SD)], [...], [...], [...],
  [Madrasah Ibtidaiyah (MI)], [...], [...], [...],
  [Sekolah Menengah Pertama (SMP)], [...], [...], [...],
  [Madrasah Tsanawiyah (MTs)], [...], [...], [...],
  [Sekolah Menengah Atas (SMA)], [...], [...], [...],
  [Sekolah Menengah Kejuruan (SMK)], [...], [...], [...],
  [Madrasah Aliyah (MA)], [...], [...], [...],
  [Jumlah / Total], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama]
#v(8pt)

#v(10pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 4.1.3: Jumlah Kepala Sekolah dan Guru Menurut Tingkat Pendidikan di Kecamatan Sungai Kunyit, 2024/2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 4.1.3: Number of Principals and Teachers by Education Level in Sungai Kunyit Subdistrict, 2024/2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Tingkat Pendidikan
Educational Level*], [*Negeri
Public*], [*Swasta
Private*], [*Jumlah
Total*], [(1)], [(2)], [(3)], [(4)]),
  [Taman Kanak-Kanak (TK)], [...], [...], [...],
  [Raudatul Athfal (RA)], [...], [...], [...],
  [Sekolah Dasar (SD)], [...], [...], [...],
  [Madrasah Ibtidaiyah (MI)], [...], [...], [...],
  [Sekolah Menengah Pertama (SMP)], [...], [...], [...],
  [Madrasah Tsanawiyah (MTs)], [...], [...], [...],
  [Sekolah Menengah Atas (SMA)], [...], [...], [...],
  [Sekolah Menengah Kejuruan (SMK)], [...], [...], [...],
  [Madrasah Aliyah (MA)], [...], [...], [...],
  [Jumlah / Total], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 4.1.4: Jumlah Peserta Didik Menurut Tingkat Pendidikan di Kecamatan Sungai Kunyit, 2024/2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 4.1.4: Number of Students by Education Level in Sungai Kunyit Subdistrict, 2024/2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Tingkat Pendidikan
Educational Level*], [*Negeri
Public*], [*Swasta
Private*], [*Jumlah
Total*], [(1)], [(2)], [(3)], [(4)]),
  [Taman Kanak-Kanak (TK)], [...], [...], [...],
  [Raudatul Athfal (RA)], [...], [...], [...],
  [Sekolah Dasar (SD)], [...], [...], [...],
  [Madrasah Ibtidaiyah (MI)], [...], [...], [...],
  [Sekolah Menengah Pertama (SMP)], [...], [...], [...],
  [Madrasah Tsanawiyah (MTs)], [...], [...], [...],
  [Sekolah Menengah Atas (SMA)], [...], [...], [...],
  [Sekolah Menengah Kejuruan (SMK)], [...], [...], [...],
  [Madrasah Aliyah (MA)], [...], [...], [...],
  [Jumlah / Total], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama]
#v(8pt)

#v(10pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 4.2.1: Banyaknya Sarana Kesehatan Menurut Jenis Sarana di Kecamatan Sungai Kunyit, 2023–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 4.2.1: Number of Health Facilities by Type in Sungai Kunyit Subdistrict, 2023–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Sarana Kesehatan
Type of Health Facility*], [*2023*], [*2024*], [*2025*], [(1)], [(2)], [(3)], [(4)]),
  [Rumah Sakit / Hospital], [...], [...], [...],
  [Puskesmas Rawat Inap / Inpatient PHC], [...], [...], [...],
  [Puskesmas Tanpa Rawat Inap / Outpatient PHC], [...], [...], [...],
  [Puskesmas Pembantu (Pustu)], [...], [...], [...],
  [Poliklinik / Balai Pengobatan], [...], [...], [...],
  [Apotek / Pharmacy], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Dinas Kesehatan, Pengendalian Penduduk dan KB Kabupaten Mempawah / Podes 2025]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 4.3.1: Banyaknya Keluarga Menurut Sumber Penerangan Utama di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 4.3.1: Number of Families by Main Electricity Source in Sungai Kunyit Subdistrict, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Listrik PLN*], [*Listrik Non-PLN*], [*Bukan Listrik*], [(1)], [(2)], [(3)], [(4)]),
  [Semudun], [...], [...], [...],
  [Semparong Parit Raden], [...], [...], [...],
  [Mendalok], [...], [...], [...],
  [Sungai Dungun], [...], [...], [...],
  [Sungai Limau], [...], [...], [...],
  [Sungai Kunyit Laut], [...], [...], [...],
  [Sungai Kunyit Dalam], [...], [...], [...],
  [Sungai Kunyit Hulu], [...], [...], [...],
  [Bukit Batu], [...], [...], [...],
  [Sungai Bundung Laut], [...], [...], [...],
  [Sungai Duri I], [...], [...], [...],
  [Sungai Duri II], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(8pt)

#v(10pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 4.4.1: Banyaknya Kejadian Bencana Alam Menurut Jenis Bencana di Kecamatan Sungai Kunyit, 2023–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 4.4.1: Number of Natural Disaster Events by Type in Sungai Kunyit Subdistrict, 2023–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Bencana Alam
Type of Disaster*], [*2023*], [*2024*], [*2025*], [(1)], [(2)], [(3)], [(4)]),
  [Tanah Longsor / Landslide], [...], [...], [...],
  [Banjir / Flood], [...], [...], [...],
  [Banjir Bandang / Flash Flood], [...], [...], [...],
  [Gempa Bumi / Earthquake], [...], [...], [...],
  [Gelombang Pasang Laut / Tidal Wave], [...], [...], [...],
  [Angin Puyuh / Puting Beliung], [...], [...], [...],
  [Kebakaran Hutan dan Lahan / Forest Fire], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Badan Penanggulangan Bencana Daerah (BPBD) Kabupaten Mempawah / Podes 2025]
#v(8pt)

#pagebreak()


// ==========================================
// BAB 5: PERTANIAN
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 5: PERTANIAN] \
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 5: AGRICULTURE]
  ]
)
#v(10pt)

#text(8.5pt)[
Sektor pertanian merupakan salah satu pilar penopang perekonomian masyarakat di Kecamatan Sungai Kunyit. Komoditas sayuran semusim, tanaman biofarmaka, serta buah-buahan tahunan dibudidayakan secara intensif oleh rumah tangga petani guna memenuhi kebutuhan pasar domestik dan regional Kabupaten Mempawah.
]

#v(8pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 5.1: Luas Panen Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Sungai Kunyit, 2022–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 5.1: Harvested Area of Seasonal Vegetables and Fruits by Kind of Plants in Sungai Kunyit Subdistrict, 2022–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Tanaman
Kind of Plants*], [*2022 (ha)*], [*2023 (ha)*], [*2024 (ha)*], [*2025 (ha)*], [(1)], [(2)], [(3)], [(4)], [(5)]),
  [Bawang Merah / Shallots], [...], [...], [...], [...],
  [Cabai Besar / Big Chili], [...], [...], [...], [...],
  [Cabai Rawit / Cayenne Pepper], [...], [...], [...], [...],
  [Tomat / Tomato], [...], [...], [...], [...],
  [Terung / Eggplant], [...], [...], [...], [...],
  [Kacang Panjang / Long Beans], [...], [...], [...], [...],
  [Ketimun / Cucumber], [...], [...], [...], [...],
  [Kangkung / Water Spinach], [...], [...], [...], [...],
  [Bayam / Spinach], [...], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS)]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 5.2: Produksi Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Sungai Kunyit, 2022–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 5.2: Production of Seasonal Vegetables and Fruits by Kind of Plants in Sungai Kunyit Subdistrict, 2022–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Tanaman
Kind of Plants*], [*2022 (ku)*], [*2023 (ku)*], [*2024 (ku)*], [*2025 (ku)*], [(1)], [(2)], [(3)], [(4)], [(5)]),
  [Bawang Merah / Shallots], [...], [...], [...], [...],
  [Cabai Besar / Big Chili], [...], [...], [...], [...],
  [Cabai Rawit / Cayenne Pepper], [...], [...], [...], [...],
  [Tomat / Tomato], [...], [...], [...], [...],
  [Terung / Eggplant], [...], [...], [...], [...],
  [Kacang Panjang / Long Beans], [...], [...], [...], [...],
  [Ketimun / Cucumber], [...], [...], [...], [...],
  [Kangkung / Water Spinach], [...], [...], [...], [...],
  [Bayam / Spinach], [...], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS)]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 5.3: Luas Panen Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Sungai Kunyit, 2022–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 5.3: Harvested Area of Medicinal Plants by Kind of Plants in Sungai Kunyit Subdistrict, 2022–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Tanaman
Kind of Plants*], [*2022 (m²)*], [*2023 (m²)*], [*2024 (m²)*], [*2025 (m²)*], [(1)], [(2)], [(3)], [(4)], [(5)]),
  [Jahe / Ginger], [...], [...], [...], [...],
  [Lengkuas / Galangal], [...], [...], [...], [...],
  [Kencur / East Indian Galangal], [...], [...], [...], [...],
  [Kunyit / Turmeric], [...], [...], [...], [...],
  [Lempuyang], [...], [...], [...], [...],
  [Temulawak / Java Turmeric], [...], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF)]
#v(8pt)

#v(10pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 5.4: Produksi Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Sungai Kunyit, 2022–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 5.4: Production of Medicinal Plants by Kind of Plants in Sungai Kunyit Subdistrict, 2022–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Tanaman
Kind of Plants*], [*2022 (kg)*], [*2023 (kg)*], [*2024 (kg)*], [*2025 (kg)*], [(1)], [(2)], [(3)], [(4)], [(5)]),
  [Jahe / Ginger], [...], [...], [...], [...],
  [Lengkuas / Galangal], [...], [...], [...], [...],
  [Kencur / East Indian Galangal], [...], [...], [...], [...],
  [Kunyit / Turmeric], [...], [...], [...], [...],
  [Lempuyang], [...], [...], [...], [...],
  [Temulawak / Java Turmeric], [...], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF)]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 5.7: Produksi Buah-Buahan dan Sayuran Tahunan Menurut Jenis Tanaman di Kecamatan Sungai Kunyit, 2022–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 5.7: Production of Annual Fruits and Vegetables by Kind of Plants in Sungai Kunyit Subdistrict, 2022–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Tanaman
Kind of Plants*], [*2022 (ku)*], [*2023 (ku)*], [*2024 (ku)*], [*2025 (ku)*], [(1)], [(2)], [(3)], [(4)], [(5)]),
  [Durian / Durian], [...], [...], [...], [...],
  [Mangga / Mango], [...], [...], [...], [...],
  [Jeruk Siam / Siamese Orange], [...], [...], [...], [...],
  [Pisang / Banana], [...], [...], [...], [...],
  [Pepaya / Papaya], [...], [...], [...], [...],
  [Nanas / Pineapple], [...], [...], [...], [...],
  [Rambutan / Rambutan], [...], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)]
#v(8pt)

#pagebreak()


// ==========================================
// BAB 6: PARIWISATA, TRANSPORTASI & KOMUNIKASI
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 6: PARIWISATA, TRANSPORTASI & KOMUNIKASI] \
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 6: TOURISM, TRANSPORTATION AND COMMUNICATION]
  ]
)
#v(10pt)

#text(8.5pt)[
Konektivitas wilayah di Kecamatan Sungai Kunyit terhubung oleh jaringan jalan darat antardesa yang dapat dilalui kendaraan roda empat sepanjang tahun. Selain itu, penetrasi infrastruktur telekomunikasi bergerak (seluler) dan jaringan internet berkecepatan tinggi terus meluas, mempercepat arus informasi dan transaksi digital masyarakat.
]

#v(8pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 6.1.1: Banyaknya Desa/Kelurahan Menurut Keberadaan Sarana Transportasi Antardesa di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 6.1.1: Number of Villages by Inter-Village Transportation Infrastructure in Sungai Kunyit Subdistrict, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.2fr, 1.1fr, 1.2fr, 1.1fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Jenis Lalu Lintas*], [*Jenis Permukaan Jalan*], [*Dapat Dilalui Roda 4+*], [(1)], [(2)], [(3)], [(4)]),
  [Semudun], [...], [...], [...],
  [Semparong Parit Raden], [...], [...], [...],
  [Mendalok], [...], [...], [...],
  [Sungai Dungun], [...], [...], [...],
  [Sungai Limau], [...], [...], [...],
  [Sungai Kunyit Laut], [...], [...], [...],
  [Sungai Kunyit Dalam], [...], [...], [...],
  [Sungai Kunyit Hulu], [...], [...], [...],
  [Bukit Batu], [...], [...], [...],
  [Sungai Bundung Laut], [...], [...], [...],
  [Sungai Duri I], [...], [...], [...],
  [Sungai Duri II], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 6.2.1: Banyaknya Desa/Kelurahan Menurut Keberadaan Kantor Pos dan Ekspedisi Swasta di Kecamatan Sungai Kunyit, 2023–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 6.2.1: Number of Villages by Availability of Post Office and Private Courier in Sungai Kunyit Subdistrict, 2023–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.8fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Fasilitas Pos / Logistik
Type of Postal/Courier Facility*], [*2023*], [*2024*], [*2025*], [(1)], [(2)], [(3)], [(4)]),
  [Kantor Pos / Pos Pembantu / Rumah Pos], [...], [...], [...],
  [Perusahaan / Agen Jasa Ekspedisi Swasta], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(8pt)

#v(10pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 6.3.1: Banyaknya Menara BTS dan Kekuatan Sinyal Internet Seluler Menurut Desa di Kecamatan Sungai Kunyit, 2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 6.3.1: Number of BTS Towers and Cellular Internet Signal Strength by Village in Sungai Kunyit Subdistrict, 2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.2fr, 1.2fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Jumlah Menara BTS*], [*Sinyal Telepon Seluler*], [*Sinyal Internet (4G/5G)*], [(1)], [(2)], [(3)], [(4)]),
  [Semudun], [...], [...], [...],
  [Semparong Parit Raden], [...], [...], [...],
  [Mendalok], [...], [...], [...],
  [Sungai Dungun], [...], [...], [...],
  [Sungai Limau], [...], [...], [...],
  [Sungai Kunyit Laut], [...], [...], [...],
  [Sungai Kunyit Dalam], [...], [...], [...],
  [Sungai Kunyit Hulu], [...], [...], [...],
  [Bukit Batu], [...], [...], [...],
  [Sungai Bundung Laut], [...], [...], [...],
  [Sungai Duri I], [...], [...], [...],
  [Sungai Duri II], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(8pt)

#pagebreak()


// ==========================================
// BAB 7: PERBANKAN, KOPERASI & PERDAGANGAN
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 7: PERBANKAN, KOPERASI & PERDAGANGAN] \
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 7: BANKING, COOPERATIVES AND TRADE]
  ]
)
#v(10pt)

#text(8.5pt)[
Aktivitas perniagaan di Kecamatan Sungai Kunyit berkembang dinamis didukung oleh sarana perdagangan tradisional (pasar dan warung rakyat) serta jaringan minimarket modern. Keberadaan lembaga perbankan, koperasi, dan lembaga keuangan mikro memegang peranan krusial dalam memperluas inklusi keuangan serta akses permodalan bagi usaha mikro, kecil, dan menengah (UMKM).
]

#v(8pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 7.1: Banyaknya Sarana Perdagangan Menurut Jenis Sarana di Kecamatan Sungai Kunyit, 2023–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 7.1: Number of Trade Facilities by Type in Sungai Kunyit Subdistrict, 2023–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Sarana Perdagangan
Type of Trade Facility*], [*2023*], [*2024*], [*2025*], [(1)], [(2)], [(3)], [(4)]),
  [Pasar dengan Bangunan Permanen], [...], [...], [...],
  [Pasar dengan Bangunan Semi Permanen], [...], [...], [...],
  [Pasar Tanpa Bangunan], [...], [...], [...],
  [Kelompok Pertokoan / Ruko], [...], [...], [...],
  [Minimarket / Supermarket], [...], [...], [...],
  [Restoran / Rumah Makan / Warung Makan], [...], [...], [...],
  [Hotel / Penginapan / Losmen], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Dinas Perindagnaker Kab. Mempawah / Podes 2025]
#v(8pt)

#pagebreak()


#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 7.2: Banyaknya Koperasi Aktif Menurut Jenis Koperasi di Kecamatan Sungai Kunyit, 2023–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 7.2: Number of Active Cooperatives by Type in Sungai Kunyit Subdistrict, 2023–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Koperasi
Type of Cooperative*], [*2023*], [*2024*], [*2025*], [(1)], [(2)], [(3)], [(4)]),
  [Koperasi Unit Desa (KUD)], [...], [...], [...],
  [Koperasi Simpan Pinjam (KSP)], [...], [...], [...],
  [Koperasi Lainnya (Non-KUD)], [...], [...], [...],
  [Jumlah / Total], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Dinas Perindagnaker Kab. Mempawah / Podes 2025]
#v(8pt)

#v(10pt)

#v(6pt)
#text(7.5pt, weight: "bold")[Tabel 7.3: Banyaknya Lembaga Keuangan Menurut Jenis Lembaga di Kecamatan Sungai Kunyit, 2023–2025] \
#text(6.5pt, style: "italic", fill: rgb("#78350F"))[Table 7.3: Number of Financial Institutions by Type in Sungai Kunyit Subdistrict, 2023–2025]
#v(2pt)
#align(center)[
#table(
  columns: (2.8fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 { (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 0.8pt + rgb("#000000")) }
                    else { (bottom: 0.3pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Jenis Lembaga Keuangan
Type of Financial Institution*], [*2023*], [*2024*], [*2025*], [(1)], [(2)], [(3)], [(4)]),
  [Bank Umum Pemerintah (BRI, Mandiri, BNI, BTN, dll.)], [...], [...], [...],
  [Bank Umum Swasta], [...], [...], [...],
  [Bank Perekonomian Rakyat (BPR)], [...], [...], [...],
  [Kantor Pegadaian], [...], [...], [...]
)
]
#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* Otoritas Jasa Keuangan (OJK) / Podes 2025]
#v(8pt)

#pagebreak()


// ==========================================
// KOVER BELAKANG (BACK COVER)
// ==========================================
#align(center)[
  #v(3cm)
  #block(
    fill: rgb("#FEF3C7"),
    inset: 15pt,
    radius: 4pt,
    stroke: 1pt + rgb("#D97706"),
    [
      #text(14pt, weight: "bold", fill: rgb("#B45309"))[KECAMATAN SUNGAI KUNYIT DALAM ANGKA 2026] \
      #v(6pt)
      #text(10pt, fill: rgb("#92400E"))[Satu Data Statistik Sektoral Kecamatan Mempawah] \
      #text(8.5pt, fill: rgb("#92400E"))[Mencerdaskan Bangsa Melalui Data Akurat dan Terpercaya]
    ]
  )
  
  #v(8cm)
  #rect(fill: rgb("#F9FAFB"), inset: 12pt, radius: 4pt, stroke: 0.5pt + rgb("#D1D5DB"))[
    #grid(
      columns: (1fr, 1fr, 1fr),
      align: center + horizon,
      [*SENSUS EKONOMI 2026* \
      #text(7pt)[BPS Republik Indonesia]],
      [*Core Values ASN* \
      #text(7pt)[BerAKHLAK]],
      [*Bangga Melayani Bangsa* \
      #text(7pt)[KemenPAN-RB]]
    )
  ]
  
  #v(1cm)
  #text(9pt, weight: "bold", fill: rgb("#1F2937"))[BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH] \
  #text(8pt, fill: rgb("#4B5563"))[Jl. Raden Kusno No. 1, Mempawah, Kalimantan Barat 79511] \
  #text(8pt, fill: rgb("#4B5563"))[Pos-el: #link("mailto:bps6104@bps.go.id")[bps6104\@bps.go.id] | Laman: #link("https://mempawahkab.bps.go.id")]
]
