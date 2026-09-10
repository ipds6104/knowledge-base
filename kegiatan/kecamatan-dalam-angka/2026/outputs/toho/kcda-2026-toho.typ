// Publikasi Resmi BPS Kabupaten Mempawah: Kecamatan Dalam Angka 2026

#set page(
  paper: "a4",
  margin: (
    inside: 2.5cm,
    outside: 1.5cm,
    top: 2.0cm,
    bottom: 2.0cm,
  ),
  header: context {
    let page_num = counter(page).get().first()
    // Running header hanya muncul pada halaman Arab bab isi (setelah frontmatter)
    if page_num >= 7 {
      if calc.even(page_num) {
        align(left, text(8pt, fill: rgb("#D97706"), weight: "bold")[KECAMATAN TOHO DALAM ANGKA 2026])
      } else {
        align(right, text(8pt, fill: rgb("#D97706"), weight: "bold")[BPS KABUPATEN MEMPAWAH])
      }
    }
  },
  footer: context {
    let page_num = counter(page).get().first()
    if page_num > 1 and page_num < 7 {
      // Halaman iii suppressed sesuai pedoman KCDA 2026
      if page_num != 3 {
        align(center, text(9pt)[#counter(page).display("i")])
      }
    } else if page_num >= 7 {
      if calc.even(page_num) {
        align(left, text(9pt, weight: "medium")[#counter(page).display("1")])
      } else {
        align(right, text(9pt, weight: "medium")[#counter(page).display("1")])
      }
    }
  }
)

#set text(font: ("Liberation Sans", "Arial"), size: 8.5pt, lang: "id")
#set par(justify: true, leading: 0.55em)


// ==========================================
// 1. KOVER DEPAN (FRONT COVER)
// ==========================================
#align(center)[
  #v(1.2cm)
  #text(10pt, weight: "bold", fill: rgb("#00A0E9"))[BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH] \
  #text(8pt, fill: rgb("#00A0E9"))[BPS-STATISTICS OF MEMPAWAH REGENCY]
  
  #v(3.5cm)
  #block(
    fill: rgb("#FEF3C7"),
    inset: (x: 20pt, y: 25pt),
    radius: 4pt,
    width: 100%,
    stroke: 1.5pt + rgb("#D97706"),
    [
      #text(22pt, weight: "bold", fill: rgb("#B45309"))[KECAMATAN TOHO] \
      #v(6pt)
      #text(18pt, weight: "bold", fill: rgb("#B45309"))[DALAM ANGKA 2026] \
      #v(10pt)
      #text(13pt, style: "italic", fill: rgb("#92400E"))[Toho Subdistrict in Figures 2026]
    ]
  )
  
  #v(4.0cm)
  #rect(fill: rgb("#F3F4F6"), inset: 8pt, radius: 3pt)[
    #text(8.5pt)[Nomor Publikasi / Publication Number: *61040.26006*]
  ]
  
  #v(1.5cm)
  #text(10pt, weight: "bold", fill: rgb("#374151"))[BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH]
]

#pagebreak()

// ==========================================
// 2. HALAMAN KATALOG & HAK CIPTA (HALAMAN ii)
// ==========================================
#v(1cm)
#text(12pt, weight: "bold")[Kecamatan Toho Dalam Angka 2026] \
#text(10pt, style: "italic")[Toho Subdistrict in Figures 2026]

#v(12pt)
#line(length: 100%, stroke: 0.5pt + rgb("#D1D5DB"))
#v(6pt)
#grid(
  columns: (1.5fr, 3fr),
  row-gutter: 8pt,
  [*Nomor Publikasi*], [: 61040.26006],
  [*Katalog BPS*], [: -],
  [*Ukuran Buku*], [: 21 cm x 29,7 cm (A4)],
  [*Jumlah Halaman*], [: viii + 48 halaman],
  [*Naskah*], [: BPS Kabupaten Mempawah],
  [*Penyunting*], [: Tim IPDS BPS Kabupaten Mempawah],
  [*Desain Kover*], [: BPS Kabupaten Mempawah],
  [*Penerbit*], [: © BPS Kabupaten Mempawah]
)
#v(6pt)
#line(length: 100%, stroke: 0.5pt + rgb("#D1D5DB"))

#v(15pt)
#block(
  fill: rgb("#F9FAFB"),
  inset: 10pt,
  stroke: 0.5pt + rgb("#E5E7EB"),
  radius: 3pt,
  [
    #text(8pt)[
      *Dilarang mengumumkan, mendistribusikan, mengomunikasikan, dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari Badan Pusat Statistik.* \
      _Prohibited to announce, distribute, communicate, and/or copy part or all of this book for commercial purposes without written permission from BPS-Statistics Indonesia._
    ]
  ]
)

#pagebreak()

// ==========================================
// 3. TIM PENYUSUN & KONTRIBUTOR DATA (HALAMAN iii - Suppressed)
// ==========================================
#align(center)[
  #text(13pt, weight: "bold", fill: rgb("#B45309"))[TIM PENYUSUN / DRAFTING TEAM]
]
#v(15pt)

#table(
  columns: (1.8fr, 3fr),
  stroke: none,
  row-gutter: 10pt,
  [*Pengarah / Director*], [Munawir, S.E., M.M. (Kepala BPS Kabupaten Mempawah)],
  [*Penanggung Jawab / Person in Charge*], [Kurniawan, S.Si., M.E.],
  [*Koordinator Teknis / Technical Coordinator*], [Sukma Andini, S.Tr.Stat.],
  [*Penyusun Naskah / Author*], [Arini Faurizah, S.Tr.Stat.],
  [*Pengolah Data / Data Processor*], [Arini Faurizah, S.Tr.Stat.],
  [*Penata Letak / Layout Editor*], [Tim Otomasi Publikasi BPS Kabupaten Mempawah]
)

#v(25pt)
#align(center)[
  #text(13pt, weight: "bold", fill: rgb("#B45309"))[KONTRIBUTOR DATA / DATA CONTRIBUTORS]
]
#v(12pt)
#grid(
  columns: (1fr, 1fr),
  row-gutter: 8pt,
  [1. Kantor Camat Toho], [5. Dinas Pertanian, KP & P Kab. Mempawah],
  [2. Dinas Kependudukan & Capil], [6. Dinas Perindagnaker Kab. Mempawah],
  [3. Dinas Dikporapar Kab. Mempawah], [7. Dinas Kesehatan, PP & KB Kab. Mempawah],
  [4. Kantor Kementerian Agama], [8. Bagian Tata Pemerintahan Setda Mempawah]
)

#pagebreak()

// ==========================================
// 4. KATA PENGANTAR (HALAMAN v)
// ==========================================
#align(center)[
  #text(14pt, weight: "bold", fill: rgb("#B45309"))[KATA PENGANTAR / PREFACE]
]
#v(15pt)

#grid(
  columns: (1fr, 1fr),
  column-gutter: 18pt,
  [
    Puji syukur ke hadirat Tuhan Yang Maha Kuasa atas terbitnya publikasi *"Kecamatan Toho Dalam Angka 2026"*. Publikasi ini merupakan publikasi tahunan yang menyajikan beragam data statistik dasar dan sektoral mengenai kondisi geografis, pemerintahan, kependudukan, sosial, pertanian, serta perekonomian di tingkat desa/kelurahan se-Kecamatan Toho.

    Data yang disajikan dihimpun dari instansi pemerintah daerah, kantor camat, dan hasil sensus/survei Badan Pusat Statistik. Diharapkan publikasi ini dapat menjadi rujukan utama dalam perencanaan dan evaluasi pembangunan daerah berbasis bukti (*evidence-based policy*).

    Kami menyampaikan penghargaan dan terima kasih yang setinggi-tingginya kepada Camat Toho, kepala desa/lurah, serta seluruh pimpinan instansi atas kerja sama yang baik. Kritik dan saran konstruktif sangat kami harapkan guna penyempurnaan pada edisi mendatang.
  ],
  [
    #text(style: "italic")[
      Praise be to God Almighty for the publication of *"Toho Subdistrict in Figures 2026"*. This annual publication presents a wide range of basic and sectoral statistical data concerning geography, government, population, social, agriculture, and economic conditions across villages in Toho Subdistrict.

      The data compiled originates from regional government agencies, subdistrict offices, and BPS censuses/surveys. We hope this publication serves as a primary reference in planning and evaluating regional development based on empirical evidence.

      We express our highest appreciation and gratitude to the Head of Toho Subdistrict, village heads, and agency leaders for their valuable cooperation. Constructive feedback is welcomed for future editions.
    ]
  ]
)

#v(20pt)
#align(right)[
  #block(width: 55%)[
    Mempawah, September 2026 \
    *Kepala BPS Kabupaten Mempawah* \
    _Chief Statistician of Mempawah Regency_ \
    #v(1.8cm)
    *Munawir, S.E., M.M.* \
    NIP. 19740510 199803 1 003
  ]
]

#pagebreak()

// ==========================================
// 5. DAFTAR ISI (HALAMAN vii)
// ==========================================
#text(14pt, weight: "bold", fill: rgb("#B45309"))[DAFTAR ISI / CONTENTS]
#v(10pt)
#line(length: 100%, stroke: 0.5pt + rgb("#D97706"))
#v(8pt)

#grid(
  columns: (1fr, auto),
  row-gutter: 8pt,
  [*Halaman Judul / Title Page*], [i],
  [*Halaman Katalog & Hak Cipta / Catalog and Copyright*], [ii],
  [*Tim Penyusun & Kontributor / Drafting Team & Contributors*], [iii],
  [*Kata Pengantar / Preface*], [v],
  [*Daftar Isi / Table of Contents*], [vii],
  [*Bab 1: Geografi dan Iklim / Geography and Climate*], [1],
  [*Bab 2: Pemerintahan / Government*], [5],
  [*Bab 3: Kependudukan / Population*], [10],
  [*Bab 4: Sosial dan Kesejahteraan Rakyat / Social and Welfare*], [13],
  [*Bab 5: Pertanian / Agriculture*], [23],
  [*Bab 6: Pariwisata, Transportasi & Komunikasi / Tourism, Transport & Comm.*], [31],
  [*Bab 7: Perbankan, Koperasi & Perdagangan / Banking, Cooperative & Trade*], [35]
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
Kecamatan Toho secara astronomis dan geografis terletak di wilayah pesisir dan daratan Kabupaten Mempawah, Provinsi Kalimantan Barat dengan ibukota kecamatan berada di Toho. Wilayah ini terbagi ke dalam 8 desa/kelurahan dengan akses perhubungan darat dan air yang menghubungkan pusat-pusat kegiatan ekonomi lokal dengan ibukota kabupaten.
]

#v(8pt)

=== Tabel 1.1: Luas Daerah Menurut Desa/Kelurahan di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 1.1: Total Area by Village/Subdistrict in Toho Subdistrict, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.5fr, 1.3fr, 1.2fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
  [Sambora], [3.608], [14,58],
  [Benuang], [2.407], [9,73],
  [Pak Utan], [3.713], [15,00],
  [Sepang], [3.966], [16,03],
  [Pak Laheng], [2.699], [10,91],
  [Terap], [3.395], [13,72],
  [Kecurit], [2.080], [8,41],
  [Toho Ilir], [2.878], [11,63]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Dinas Kependudukan dan Pencatatan Sipil / BAPEDDA Kabupaten Mempawah]
#v(12pt)

#pagebreak()


=== Tabel 1.2: Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten Menurut Desa/Kelurahan di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 1.2: Distance to Subdistrict and Regency Capital by Village in Toho Subdistrict, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.5fr, 1.3fr, 1.3fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
  [Sambora], [...], [...],
  [Benuang], [...], [...],
  [Pak Utan], [...], [...],
  [Sepang], [...], [...],
  [Pak Laheng], [...], [...],
  [Terap], [...], [...],
  [Kecurit], [...], [...],
  [Toho Ilir], [...], [...]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Toho]
#v(12pt)

#v(10pt)

=== Tabel 1.3: Batas Administrasi Kecamatan Toho Menurut Arah Mata Angin, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 1.3: Administrative Borders of Toho Subdistrict by Cardinal Direction, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (0.6fr, 1.8fr, 3.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Toho / Bagian Tata Pemerintahan Setda Mempawah]
#v(12pt)

#pagebreak()


=== Tabel 1.4: Jarak Kantor Camat Toho dengan Kota dan Tempat Penting Lainnya, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 1.4: Distance from Toho Subdistrict Office to Other Important Places, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (0.6fr, 3.2fr, 1.2fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Toho]
#v(12pt)

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
Secara administratif, Kecamatan Toho terbagi menjadi 8 desa/kelurahan yang dipimpin oleh kepala desa dan lurah definitif, didukung oleh aparatur pemerintah desa, Badan Permusyawaratan Desa (BPD), serta kelembagaan RT dan RW sebagai garda terdepan pelayanan kemasyarakatan.
]

#v(8pt)

=== Tabel 2.1.1: Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 2.1.1: Number of Hamlets, RW, and RT by Village/Subdistrict in Toho Subdistrict, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
  [Sambora], [...], [...], [...],
  [Benuang], [...], [...], [...],
  [Pak Utan], [...], [...], [...],
  [Sepang], [...], [...], [...],
  [Pak Laheng], [...], [...], [...],
  [Terap], [...], [...], [...],
  [Kecurit], [...], [...], [...],
  [Toho Ilir], [...], [...], [...]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Toho]
#v(12pt)

#pagebreak()


=== Tabel 2.1.2: Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan Toho
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 2.1.2: Names of District Heads of Toho Subdistrict]
#v(3pt)
#align(center)[
#table(
  columns: (0.6fr, 2.8fr, 1.6fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Toho]
#v(12pt)

#v(10pt)

=== Tabel 2.1.3: Nama-Nama Kepala Desa/Lurah di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 2.1.3: Names of Village Heads in Toho Subdistrict, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (0.6fr, 2.2fr, 2.8fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*No*], [*Desa/Kelurahan
Village/Subdistrict*], [*Nama Kepala Desa / Lurah
Name of Village Head*], [(1)], [(2)], [(3)]),
  [1], [Sambora], [...],
  [2], [Benuang], [...],
  [3], [Pak Utan], [...],
  [4], [Sepang], [...],
  [5], [Pak Laheng], [...],
  [6], [Terap], [...],
  [7], [Kecurit], [...],
  [8], [Toho Ilir], [...]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Toho]
#v(12pt)

#pagebreak()


=== Tabel 2.1.6: Status Desa Berdasarkan Indeks Desa Membangun (IDM) di Kecamatan Toho, 2024/2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 2.1.6: Village Status Based on Developing Village Index (IDM) in Toho Subdistrict, 2024/2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.5fr, 1.2fr, 1.5fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
  [Sambora], [...], [...],
  [Benuang], [...], [...],
  [Pak Utan], [...], [...],
  [Sepang], [...], [...],
  [Pak Laheng], [...], [...],
  [Terap], [...], [...],
  [Kecurit], [...], [...],
  [Toho Ilir], [...], [...]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kementerian Desa, Pembangunan Daerah Tertinggal, dan Transmigrasi]
#v(12pt)

#v(10pt)

=== Tabel 2.2.1: Jumlah Pegawai Negeri Sipil Pemerintah Daerah Kecamatan Menurut Golongan di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 2.2.1: Number of Civil Servants in Toho Subdistrict Office by Rank/Class, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Toho]
#v(12pt)

#pagebreak()


=== Tabel 2.2.2: Jumlah Pegawai Negeri Sipil Pemerintah Daerah Kecamatan Menurut Tingkat Pendidikan di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 2.2.2: Number of Civil Servants in Toho Subdistrict Office by Education Level, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kantor Camat Toho]
#v(12pt)

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
Berdasarkan data registrasi semester II tahun 2025 dari Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah, jumlah penduduk Kecamatan Toho terdistribusi di 8 desa/kelurahan dengan struktur demografi yang produktif. Komposisi penduduk laki-laki dan perempuan relatif berimbang, mencerminkan kestabilan demografis wilayah.
]

#v(8pt)

=== Tabel 3.1: Penduduk, Distribusi Persentase, dan Kepadatan Penduduk Menurut Desa/Kelurahan di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 3.1: Population, Percentage Distribution, and Density by Village/Subdistrict in Toho Subdistrict, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.0fr, 1.0fr, 1.0fr, 1.1fr, 1.0fr, 1.2fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
  [Sambora], [1.851], [1.757], [3.608], [14,58], [200,67],
  [Benuang], [1.236], [1.171], [2.407], [9,73], [236,91],
  [Pak Utan], [1.944], [1.769], [3.713], [15,00], [178,00],
  [Sepang], [2.063], [1.903], [3.966], [16,03], [171,02],
  [Pak Laheng], [1.390], [1.309], [2.699], [10,91], [115,44],
  [Terap], [1.745], [1.650], [3.395], [13,72], [103,92],
  [Kecurit], [1.051], [1.029], [2.080], [8,41], [81,22],
  [Toho Ilir], [1.504], [1.374], [2.878], [11,63], [39,88]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah (Semester II 2025)]
#v(12pt)

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
Pembangunan bidang sosial kemasyarakatan di Kecamatan Toho ditopang oleh perluasan aksesibilitas sarana pendidikan dasar hingga menengah, peningkatan mutu fasilitas kesehatan masyarakat, ketersediaan energi penerangan rumah tangga, serta kesiapsiagaan dalam menghadapi potensi bencana lingkungan hidup.
]

#v(8pt)

=== Tabel 4.1.1: Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 4.1.1: Number of Villages Having Educational Facilities by Level in Toho Subdistrict, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.1fr, 1.1fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*SD / MI*], [*SMP / MTs*], [*SMA / SMK / MA*], [*Akademi / PT*], [(1)], [(2)], [(3)], [(4)], [(5)]),
  [Sambora], [...], [...], [...], [...],
  [Benuang], [...], [...], [...], [...],
  [Pak Utan], [...], [...], [...], [...],
  [Sepang], [...], [...], [...], [...],
  [Pak Laheng], [...], [...], [...], [...],
  [Terap], [...], [...], [...], [...],
  [Kecurit], [...], [...], [...], [...],
  [Toho Ilir], [...], [...], [...], [...]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(12pt)

#pagebreak()


=== Tabel 4.1.2: Jumlah Satuan Pendidikan Menurut Tingkat Pendidikan di Kecamatan Toho, 2024/2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 4.1.2: Number of Educational Units by Education Level in Toho Subdistrict, 2024/2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama]
#v(12pt)

#v(10pt)

=== Tabel 4.1.3: Jumlah Kepala Sekolah dan Guru Menurut Tingkat Pendidikan di Kecamatan Toho, 2024/2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 4.1.3: Number of Principals and Teachers by Education Level in Toho Subdistrict, 2024/2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama]
#v(12pt)

#pagebreak()


=== Tabel 4.1.4: Jumlah Peserta Didik Menurut Tingkat Pendidikan di Kecamatan Toho, 2024/2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 4.1.4: Number of Students by Education Level in Toho Subdistrict, 2024/2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama]
#v(12pt)

#v(10pt)

=== Tabel 4.2.1: Banyaknya Sarana Kesehatan Menurut Jenis Sarana di Kecamatan Toho, 2023–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 4.2.1: Number of Health Facilities by Type in Toho Subdistrict, 2023–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Dinas Kesehatan, Pengendalian Penduduk dan KB Kabupaten Mempawah / Podes 2025]
#v(12pt)

#pagebreak()


=== Tabel 4.3.1: Banyaknya Keluarga Menurut Sumber Penerangan Utama di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 4.3.1: Number of Families by Main Electricity Source in Toho Subdistrict, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Listrik PLN*], [*Listrik Non-PLN*], [*Bukan Listrik*], [(1)], [(2)], [(3)], [(4)]),
  [Sambora], [...], [...], [...],
  [Benuang], [...], [...], [...],
  [Pak Utan], [...], [...], [...],
  [Sepang], [...], [...], [...],
  [Pak Laheng], [...], [...], [...],
  [Terap], [...], [...], [...],
  [Kecurit], [...], [...], [...],
  [Toho Ilir], [...], [...], [...]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(12pt)

#v(10pt)

=== Tabel 4.4.1: Banyaknya Kejadian Bencana Alam Menurut Jenis Bencana di Kecamatan Toho, 2023–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 4.4.1: Number of Natural Disaster Events by Type in Toho Subdistrict, 2023–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Badan Penanggulangan Bencana Daerah (BPBD) Kabupaten Mempawah / Podes 2025]
#v(12pt)

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
Sektor pertanian merupakan salah satu pilar penopang perekonomian masyarakat di Kecamatan Toho. Komoditas sayuran semusim, tanaman biofarmaka, serta buah-buahan tahunan dibudidayakan secara intensif oleh rumah tangga petani guna memenuhi kebutuhan pasar domestik dan regional Kabupaten Mempawah.
]

#v(8pt)

=== Tabel 5.1: Luas Panen Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Toho, 2022–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 5.1: Harvested Area of Seasonal Vegetables and Fruits by Kind of Plants in Toho Subdistrict, 2022–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS)]
#v(12pt)

#pagebreak()


=== Tabel 5.2: Produksi Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Toho, 2022–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 5.2: Production of Seasonal Vegetables and Fruits by Kind of Plants in Toho Subdistrict, 2022–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS)]
#v(12pt)

#pagebreak()


=== Tabel 5.3: Luas Panen Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Toho, 2022–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 5.3: Harvested Area of Medicinal Plants by Kind of Plants in Toho Subdistrict, 2022–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF)]
#v(12pt)

#v(10pt)

=== Tabel 5.4: Produksi Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Toho, 2022–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 5.4: Production of Medicinal Plants by Kind of Plants in Toho Subdistrict, 2022–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF)]
#v(12pt)

#pagebreak()


=== Tabel 5.7: Produksi Buah-Buahan dan Sayuran Tahunan Menurut Jenis Tanaman di Kecamatan Toho, 2022–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 5.7: Production of Annual Fruits and Vegetables by Kind of Plants in Toho Subdistrict, 2022–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)]
#v(12pt)

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
Konektivitas wilayah di Kecamatan Toho terhubung oleh jaringan jalan darat antardesa yang dapat dilalui kendaraan roda empat sepanjang tahun. Selain itu, penetrasi infrastruktur telekomunikasi bergerak (seluler) dan jaringan internet berkecepatan tinggi terus meluas, mempercepat arus informasi dan transaksi digital masyarakat.
]

#v(8pt)

=== Tabel 6.1.1: Banyaknya Desa/Kelurahan Menurut Keberadaan Sarana Transportasi Antardesa di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 6.1.1: Number of Villages by Inter-Village Transportation Infrastructure in Toho Subdistrict, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.2fr, 1.1fr, 1.2fr, 1.1fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Jenis Lalu Lintas*], [*Jenis Permukaan Jalan*], [*Dapat Dilalui Roda 4+*], [(1)], [(2)], [(3)], [(4)]),
  [Sambora], [...], [...], [...],
  [Benuang], [...], [...], [...],
  [Pak Utan], [...], [...], [...],
  [Sepang], [...], [...], [...],
  [Pak Laheng], [...], [...], [...],
  [Terap], [...], [...], [...],
  [Kecurit], [...], [...], [...],
  [Toho Ilir], [...], [...], [...]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(12pt)

#pagebreak()


=== Tabel 6.2.1: Banyaknya Desa/Kelurahan Menurut Keberadaan Kantor Pos dan Ekspedisi Swasta di Kecamatan Toho, 2023–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 6.2.1: Number of Villages by Availability of Post Office and Private Courier in Toho Subdistrict, 2023–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.8fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(12pt)

#v(10pt)

=== Tabel 6.3.1: Banyaknya Menara BTS dan Kekuatan Sinyal Internet Seluler Menurut Desa di Kecamatan Toho, 2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 6.3.1: Number of BTS Towers and Cellular Internet Signal Strength by Village in Toho Subdistrict, 2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.2fr, 1.0fr, 1.2fr, 1.2fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
  fill: (x, y) => if y <= 1 { rgb("#FEF3C7") }
                  else if calc.even(y) { rgb("#F9FAFB") }
                  else { white },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([*Desa/Kelurahan
Village/Subdistrict*], [*Jumlah Menara BTS*], [*Sinyal Telepon Seluler*], [*Sinyal Internet (4G/5G)*], [(1)], [(2)], [(3)], [(4)]),
  [Sambora], [...], [...], [...],
  [Benuang], [...], [...], [...],
  [Pak Utan], [...], [...], [...],
  [Sepang], [...], [...], [...],
  [Pak Laheng], [...], [...], [...],
  [Terap], [...], [...], [...],
  [Kecurit], [...], [...], [...],
  [Toho Ilir], [...], [...], [...]
)
]
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* BPS, Pendataan Potensi Desa (Podes) 2025]
#v(12pt)

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
Aktivitas perniagaan di Kecamatan Toho berkembang dinamis didukung oleh sarana perdagangan tradisional (pasar dan warung rakyat) serta jaringan minimarket modern. Keberadaan lembaga perbankan, koperasi, dan lembaga keuangan mikro memegang peranan krusial dalam memperluas inklusi keuangan serta akses permodalan bagi usaha mikro, kecil, dan menengah (UMKM).
]

#v(8pt)

=== Tabel 7.1: Banyaknya Sarana Perdagangan Menurut Jenis Sarana di Kecamatan Toho, 2023–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 7.1: Number of Trade Facilities by Type in Toho Subdistrict, 2023–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Dinas Perindagnaker Kab. Mempawah / Podes 2025]
#v(12pt)

#pagebreak()


=== Tabel 7.2: Banyaknya Koperasi Aktif Menurut Jenis Koperasi di Kecamatan Toho, 2023–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 7.2: Number of Active Cooperatives by Type in Toho Subdistrict, 2023–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Dinas Perindagnaker Kab. Mempawah / Podes 2025]
#v(12pt)

#v(10pt)

=== Tabel 7.3: Banyaknya Lembaga Keuangan Menurut Jenis Lembaga di Kecamatan Toho, 2023–2025
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table 7.3: Number of Financial Institutions by Type in Toho Subdistrict, 2023–2025]
#v(3pt)
#align(center)[
#table(
  columns: (2.8fr, 0.9fr, 0.9fr, 0.9fr),
  stroke: (x, y) => if y == 0 { (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }
                    else if y == 1 { (bottom: 1.2pt + rgb("#000000")) }
                    else { (bottom: 0.4pt + rgb("#E5E7EB")) },
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
#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* Otoritas Jasa Keuangan (OJK) / Podes 2025]
#v(12pt)

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
      #text(14pt, weight: "bold", fill: rgb("#B45309"))[KECAMATAN TOHO DALAM ANGKA 2026] \
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
