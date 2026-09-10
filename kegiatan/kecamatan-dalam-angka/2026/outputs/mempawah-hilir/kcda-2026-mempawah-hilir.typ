// Publikasi Resmi BPS Kabupaten Mempawah: Kecamatan Dalam Angka 2026 (Ukuran A5)

#let in_frontmatter = state("in_frontmatter", true)
#let active_chapter = state("active_chapter", "")
#let is_chapter_page = state("is_chapter_page", false)

#set page(
  paper: "a5",
  margin: (
    inside: 2.0cm,
    outside: 1.5cm,
    top: 2.0cm,
    bottom: 2.0cm,
  ),
  header: context {
    if not in_frontmatter.get() and not is_chapter_page.get() {
      let page_num = counter(page).get().first()
      let chapter_title = active_chapter.get()
      if calc.even(page_num) {
        align(left, text(6.5pt, font: ("Metropolis", "Liberation Sans", "Arial"), fill: rgb("#374151"), weight: "bold")[KECAMATAN MEMPAWAH HILIR DALAM ANGKA 2026])
      } else {
        let right_text = if chapter_title != "" { chapter_title } else { "BPS KABUPATEN MEMPAWAH" }
        align(right, text(6.5pt, font: ("Metropolis", "Liberation Sans", "Arial"), fill: rgb("#374151"), weight: "bold")[#right_text])
      }
    }
  },
  footer: context {
    let page_num = counter(page).get().first()
    if in_frontmatter.get() {
      // Sesuai Pedoman Publikasi BPS 2023 & Aturan KCDA 2026:
      // Halaman i (Judul Utama), ii (Katalog), iii (Tim Penyusun), iv (Kontributor) TIDAK dicantumkan nomor halamannya
      // Nomor halaman fisik baru mulai dicetak pada Kata Pengantar (halaman v)
      if page_num >= 5 {
        let display_val = counter(page).display("i")
        align(center, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#4B5563"), weight: "bold")[#display_val])
      }
    } else {
      let display_val = counter(page).display("1")
      if calc.even(page_num) {
        align(left, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#1F2937"), weight: "bold")[#display_val])
      } else {
        align(right, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#1F2937"), weight: "bold")[#display_val])
      }
    }
  }
)

#set text(font: ("Myriad Pro", "Liberation Sans", "Arial"), size: 7.5pt, lang: "id")
#set par(justify: true, leading: 0.5em)

// Matikan justify pada seluruh sel tabel agar spasi antar kata di header & data tabel tidak meregang
#show table.cell: set par(justify: false)

// Standarisasi Penulisan Judul Gambar BPS (Di Bawah Gambar tanpa prefix dobel)
#show figure.where(kind: image): set figure(supplement: none)
#show figure.where(kind: image): set figure.caption(separator: none)


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
      #text(weight: "bold")[1102001.6104050] \
      #text(style: "italic")[ISSN xxxx-xxxx]
    ]
  ]

  #v(0.8cm)

  // Judul Publikasi di Tengah Atas
  #align(center)[
    #text(16pt, weight: "bold", fill: white)[KECAMATAN MEMPAWAH HILIR] \
    #v(2pt)
    #text(15pt, weight: "bold", fill: white)[DALAM ANGKA] \
    #v(4pt)
    #text(11pt, style: "italic", fill: rgb("#F3F4F6"))[Mempawah Hilir District in Figures] \
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
// 2. HALAMAN JUDUL UTAMA / TITLE PAGE (HALAMAN i)
// ==========================================
// Kover depan tidak dihitung sebagai halaman buku.
// Perhitungan angka romawi resmi dimulai pada Halaman Judul Utama (halaman i).
#counter(page).update(1)

#align(right)[
  #text(7.5pt)[
    #text(style: "italic")[Katalog/Catalogue:] 1102001.6104050 \
    ISSN: 2477-6777
  ]
]

#v(1fr)

#text(16pt, weight: "bold")[KECAMATAN MEMPAWAH HILIR] \
#v(2pt)
#text(16pt, weight: "bold")[DALAM ANGKA] \
#v(4pt)
#text(11.5pt, style: "italic", fill: rgb("#F5A623"))[Mempawah Hilir District in Figures] \
#v(3pt)
#text(9pt, weight: "medium")[Volume 48, 2026]

#v(14pt)

#grid(
  columns: (auto, auto),
  column-gutter: 8pt,
  align: horizon,
  image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", height: 26pt),
  align(left)[
    #text(8pt, weight: "bold", fill: rgb("#00A0E9"))[BADAN PUSAT STATISTIK] \
    #text(8pt, weight: "bold", fill: rgb("#00A0E9"))[KABUPATEN MEMPAWAH] \
    #text(6.5pt, fill: rgb("#00A0E9"))[BPS-STATISTICS OF MEMPAWAH REGENCY]
  ]
)

#pagebreak()

// ==========================================
// 3. HALAMAN KATALOG & HAK CIPTA (HALAMAN ii)
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
#text(10.5pt, weight: "bold")[KECAMATAN MEMPAWAH HILIR DALAM ANGKA] \
#text(9.5pt, style: "italic")[Mempawah Hilir District in Figures] \
#text(9.5pt)[2026] \
#text(8pt, fill: luma(100))[Volume 48, 2026]

#let total_frontmatter_pages = context {
  let elems = query(<transisi_isi>)
  if elems.len() > 0 {
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("i", p)
  } else {
    "x"
  }
}
#let total_arabic_pages = context {
  let elems = query(<akhir_buku>)
  if elems.len() > 0 {
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("1", p)
  } else {
    "28"
  }
}

#v(8pt)
#grid(
  columns: (1fr, 1.2fr),
  row-gutter: 5pt,
  [*Katalog/_Catalogue_:*], [1102001.6104050],
  [*ISSN:*], [2477-6777],
  [*Nomor Publikasi/_Publication Number_:*], [61040.26012],
  [], [],
  [*Ukuran Buku/_Book Size_:*], [14,8 cm x 21 cm],
  [*Jumlah Halaman/_Number of Pages_:*], [#total_frontmatter_pages + #total_arabic_pages hal/pages],
  [], [],
  [*Penyusun Naskah/_Manuscript Drafter_:*], [BPS Kabupaten Mempawah \ _BPS-Statistics of Mempawah Regency_],
  [*Penyunting/_Editor_:*], [BPS Kabupaten Mempawah \ _BPS-Statistics of Mempawah Regency_],
  [*Pembuat Kover/_Cover Designer_:*], [BPS Kabupaten Mempawah \ _BPS-Statistics of Mempawah Regency_],
  [*Penerbit/_Publisher_:*], [© BPS Kabupaten Mempawah/_BPS-Statistics of Mempawah Regency_],
  [*Sumber Ilustrasi/_Illustration Source_:*], [-]
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
  #text(10.5pt, weight: "bold")[TIM PENYUSUN/_COMPILERS_] \
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan Mempawah Hilir Dalam Angka 2026] \
  #text(8pt, style: "italic")[Mempawah Hilir District in Figures 2026] \
  #text(7.5pt)[Volume xx, 2026]
  
  #v(16pt)
  #text(8.5pt, weight: "bold")[Pengarah/_Director_] \
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penanggung Jawab/_Persons in Charge_] \
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penyunting/_Editors_] \
  #text(8pt)[Kurniawan #sym.circle.filled.small Sukma Andini]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Pengolah Data dan Penulis Naskah/_Data Processor and Writers_] \
  #text(8pt)[Sukma Andini]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penata Letak/_Layouters_] \
  #text(8pt)[Tim IPDS BPS Kabupaten Mempawah]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penerjemah/_Translators_] \
  #text(8pt)[Tim IPDS BPS Kabupaten Mempawah]
]

#pagebreak()

// ==========================================
// 4. KONTRIBUTOR DATA (HALAMAN iv)
// ==========================================
#align(center)[
  #text(10.5pt, weight: "bold")[KONTRIBUTOR DATA/]#text(10.5pt, weight: "bold", style: "italic")[DATA CONTRIBUTORS]
]
#v(14pt)

#set enum(indent: 0pt, body-indent: 7pt, spacing: 9.5pt)
#text(8pt)[
+ Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]
+ Kementerian Agama/#text(style: "italic")[Ministry of Religious Affairs]
+ Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi/#text(style: "italic")[Ministry of Education, Culture, Research, and Technology]
+ Badan Pusat Statistik/#text(style: "italic")[BPS-Statistics Indonesia]
+ Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency]
+ Dinas Pendidikan, Pemuda, Olahraga dan Pariwisata Kabupaten Mempawah/#text(style: "italic")[Education, Youth, Sports, and Tourism Office of Mempawah Regency]
+ Dinas Pertanian, Ketahanan Pangan dan Perikanan Kabupaten Mempawah/#text(style: "italic")[Agriculture, Food Security, and Fisheries Office of Mempawah Regency]
+ Dinas Kesehatan, Pengendalian Penduduk dan Keluarga Berencana Kabupaten Mempawah/#text(style: "italic")[Health, Population Control, and Family Planning Office of Mempawah Regency]
+ Dinas Perindustrian, Perdagangan dan Tenaga Kerja Kabupaten Mempawah/#text(style: "italic")[Industry, Trade, and Manpower Office of Mempawah Regency]
+ Bagian Tata Pemerintahan Sekretariat Daerah Kabupaten Mempawah/#text(style: "italic")[Governance Division of Regional Secretariat of Mempawah Regency]
+ Pemerintah Desa/Kelurahan se-Kecamatan Mempawah Hilir/#text(style: "italic")[Village/Subdistrict Administrations throughout Mempawah Hilir District]
]

#pagebreak()

// ==========================================
// 5. KATA PENGANTAR (HALAMAN v - INDONESIA)
// ==========================================
#metadata("kata_pengantar") <kata_pengantar>
#align(center)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", height: 28pt)
  #v(8pt)
  #text(11pt, weight: "bold")[KATA PENGANTAR]
]
#v(12pt)

#set par(justify: true, leading: 0.65em, first-line-indent: 0pt)
#text(8pt)[
  Publikasi *Kecamatan Mempawah Hilir Dalam Angka 2026* merupakan seri publikasi tahunan BPS Kabupaten Mempawah yang menyajikan beragam data statistik sektoral bersumber dari instansi pemerintah daerah, kantor camat, desa/kelurahan, serta survei dan sensus BPS. Publikasi ini memuat gambaran umum mengenai geografi, pemerintahan, serta perkembangan kondisi sosial-demografi dan perekonomian di wilayah Kecamatan Mempawah Hilir.

  #v(5pt)
  Data yang disajikan diharapkan dapat menjadi rujukan empiris dan indikator penting dalam mendukung perencanaan, pemantauan, serta evaluasi kebijakan pembangunan daerah demi terwujudnya Satu Data Indonesia.

  #v(5pt)
  Ucapan terima kasih dan penghargaan setinggi-tingginya disampaikan kepada Camat Mempawah Hilir, para Kepala Desa/Lurah se-Kecamatan Mempawah Hilir, serta pimpinan instansi dinas/lembaga atas koordinasi dan kontribusi data yang diberikan dalam penyusunan buku ini.

  #v(5pt)
  Kami menyadari masih terdapat ruang penyempurnaan dalam penyajian publikasi ini. Oleh karena itu, masukan dan saran yang membangun sangat kami harapkan guna penyempurnaan edisi di masa mendatang. Semoga publikasi ini memberikan manfaat bagi segenap pemangku kepentingan, perencana kebijakan, akademisi, dan masyarakat luas.
]

#v(1fr)

#grid(
  columns: (46%, 54%),
  column-gutter: 10pt,
  align: (left + bottom, left + bottom),
  [
    #image("/kegiatan/kecamatan-dalam-angka/2026/assets/kepala_bps.png", width: 96%)
  ],
  [
    #block(inset: (bottom: 1.1cm))[
      #text(8pt)[
        Mempawah, September 2026 \
        Kepala BPS Kabupaten Mempawah \
        #v(4pt)
        #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 38pt) \
        #v(4pt)
        *MUNAWIR*
      ]
    ]
  ]
)

#pagebreak()

// ==========================================
// 6. PREFACE (HALAMAN vi - ENGLISH)
// ==========================================
#metadata("preface") <preface>
#align(center)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", height: 28pt)
  #v(8pt)
  #text(11pt, weight: "bold", style: "italic")[PREFACE]
]
#v(12pt)

#set par(justify: true, leading: 0.65em, first-line-indent: 0pt)
#text(8pt, style: "italic")[
  *Mempawah Hilir District in Figures 2026* is an annual publication series issued by BPS-Statistics of Mempawah Regency, presenting various sectoral statistical data sourced from regional government institutions, the subdistrict office, village administrations, as well as surveys and censuses conducted by BPS. This publication provides a comprehensive overview of geography, governance, and the socio-demographic and economic development in Mempawah Hilir District.

  #v(5pt)
  The statistical indicators presented are expected to serve as essential empirical references to support evidence-based regional development planning, monitoring, and evaluation within the framework of Satu Data Indonesia (One Data Indonesia).

  #v(5pt)
  We would like to express our highest gratitude and appreciation to the Head of Mempawah Hilir District, Village Heads throughout Mempawah Hilir District, and all collaborating regional agencies for their valuable data contributions and seamless cooperation.

  #v(5pt)
  We realize that there is still room for improvement in this publication. Therefore, constructive suggestions and feedback are warmly welcomed to enhance future editions. It is our hope that this publication will be beneficial for policy makers, researchers, academicians, and the general public.
]

#v(1fr)

#grid(
  columns: (46%, 54%),
  column-gutter: 10pt,
  align: (left + bottom, left + bottom),
  [
    #image("/kegiatan/kecamatan-dalam-angka/2026/assets/kepala_bps.png", width: 96%)
  ],
  [
    #block(inset: (bottom: 1.1cm))[
      #text(8pt, style: "italic")[
        Mempawah, September 2026 \
        Chief Statistician of Mempawah Regency \
        #v(4pt)
        #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 38pt) \
        #v(4pt)
        #text(weight: "bold", style: "normal")[MUNAWIR]
      ]
    ]
  ]
)

#pagebreak()

// ==========================================
// 6. DAFTAR ISI / CONTENTS
// ==========================================
#metadata("daftar_isi") <daftar_isi>

#let get_page_roman(lbl, default: "-") = context {
  let elems = query(lbl)
  if elems.len() > 0 {
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("i", p)
  } else {
    default
  }
}

#let get_page_arabic(lbl, default: "-") = context {
  let elems = query(lbl)
  if elems.len() > 0 {
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("1", p)
  } else {
    default
  }
}

// Helper functions for Dot Leaders
#let toc_chapter(no, id_title, en_title, page_val) = {
  grid(
    columns: (16pt, 1fr, auto),
    column-gutter: (4pt, 6pt),
    align: (top + left, top + left, bottom + right),
    [#no],
    [
      #id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
    [#page_val]
  )
}

#let toc_section(title_markup, page_val) = {
  grid(
    columns: (1fr, auto),
    column-gutter: 6pt,
    align: (bottom + left, bottom + right),
    [#title_markup #box(width: 1fr, repeat[ . ])],
    [#page_val]
  )
}

#let toc_entry_item(no, id_title, en_title, page_val) = {
  grid(
    columns: (24pt, 1fr, auto),
    column-gutter: (4pt, 6pt),
    align: (top + left, top + left, bottom + right),
    [#no],
    [
      #id_title \
      #text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
    [#page_val]
  )
}

#align(right)[#text(7pt)[ISSN: 2477-6777]]
#v(4pt)

#align(center)[
  #text(10pt, weight: "bold")[DAFTAR ISI/CONTENTS] \
  #v(2pt)
  #text(9pt, weight: "bold")[Kecamatan Mempawah Hilir Dalam Angka 2026] \
  #text(8.5pt, style: "italic")[Mempawah Hilir District in Figures 2026] \
  #v(1pt)
  #text(7.5pt)[Volume 48, 2026]
]

#v(8pt)
#align(right)[
  #text(7.5pt)[Halaman] \
  #text(7pt, style: "italic")[Page]
]
#v(4pt)

#toc_section([Kata Pengantar], get_page_roman(<kata_pengantar>))
#v(4pt)
#toc_section([_Preface_], get_page_roman(<preface>))
#v(4pt)
#toc_section([Daftar Isi/_Contents_], get_page_roman(<daftar_isi>))
#v(4pt)
#toc_section([Daftar Tabel/_List of Tables_], get_page_roman(<daftar_tabel>))
#v(4pt)
#toc_section([Daftar Gambar/_List of Figures_], get_page_roman(<daftar_gambar>))
#v(4pt)
#toc_section([Penjelasan Umum/_Explanatory Notes_], get_page_roman(<penjelasan_umum>))
#v(6pt)

#toc_chapter("1.", "Geografi dan Iklim", "Geography and Climate", get_page_arabic(<bab1>))
#v(4pt)
#toc_chapter("2.", "Pemerintahan", "Government", get_page_arabic(<bab2>))
#v(4pt)
#toc_chapter("3.", "Penduduk", "Population", get_page_arabic(<bab3>))
#v(4pt)
#toc_chapter("4.", "Sosial dan Kesejahteraan Rakyat", "Social and Welfare", get_page_arabic(<bab4>))
#v(4pt)
#toc_chapter("5.", "Pertanian, Kehutanan, Perikanan, dan Peternakan", "Agriculture, Forestry, Livestock, & Fishery", get_page_arabic(<bab5>))
#v(4pt)
#toc_chapter("6.", "Pariwisata, Transportasi, dan Komunikasi", "Tourism, Transportation, and Communication", get_page_arabic(<bab6>))
#v(4pt)
#toc_chapter("7.", "Perbankan, Koperasi, dan Perdagangan", "Banking, Cooperative, and Trade", get_page_arabic(<bab7>))
#v(6pt)
#toc_section([Daftar Pustaka/_Bibliography_], get_page_arabic(<daftar_pustaka>))

#pagebreak()

// ==========================================
// 7. DAFTAR TABEL / LIST OF TABLES
// ==========================================
#metadata("daftar_tabel") <daftar_tabel>
#align(center)[
  #text(10pt, weight: "bold")[DAFTAR TABEL/]#text(10pt, weight: "bold", style: "italic")[LIST OF TABLES]
]

#v(10pt)
#grid(
  columns: (24pt, 1fr, auto),
  column-gutter: (4pt, 6pt),
  [*Tabel*\ _Table_], [], [*Halaman*\ _Page_]
)
#v(6pt)

#toc_entry_item("1.1", "Luas Daerah Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025", "Total Area by Village/Subdistrict in Mempawah Hilir District, 2025", get_page_arabic(<tab_1_1>))
#v(5pt)
#toc_entry_item("1.2", "Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025", "Distance to Subdistrict and Regency Capital by Village in Mempawah Hilir District, 2025", get_page_arabic(<tab_1_2>))
#v(5pt)
#toc_entry_item("1.3", "Batas Administrasi Kecamatan Mempawah Hilir Menurut Arah Mata Angin, 2025", "Administrative Borders of Mempawah Hilir District by Cardinal Direction, 2025", get_page_arabic(<tab_1_3>))
#v(5pt)
#toc_entry_item("1.4", "Jarak Kantor Camat Mempawah Hilir dengan Kota dan Tempat Penting Lainnya, 2025", "Distance from Mempawah Hilir Subdistrict Office to Other Important Places, 2025", get_page_arabic(<tab_1_4>))
#v(5pt)
#toc_entry_item("2.1.1", "Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025", "Number of Hamlets, RW, and RT by Village/Subdistrict in Mempawah Hilir District, 2025", get_page_arabic(<tab_2_1_1>))
#v(5pt)
#toc_entry_item("2.1.2", "Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan Mempawah Hilir", "Names of District Heads of Mempawah Hilir District", get_page_arabic(<tab_2_1_2>))
#v(5pt)
#toc_entry_item("2.1.3", "Nama-Nama Kepala Desa di Kecamatan Mempawah Hilir, 2025", "Names of Village Heads in Mempawah Hilir District, 2025", get_page_arabic(<tab_2_1_3>))
#v(5pt)
#toc_entry_item("3.1", "Penduduk, Distribusi Persentase, Kepadatan, dan Rasio Jenis Kelamin Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025", "Population, Percentage Distribution, Density, and Sex Ratio by Village in Mempawah Hilir District, 2025", get_page_arabic(<tab_3_1>))
#v(5pt)
#toc_entry_item("4.1.1", "Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2023–2025", "Number of Villages Having Educational Facilities by Level in Mempawah Hilir District, 2023–2025", get_page_arabic(<tab_4_1_1>))
#v(5pt)
#toc_entry_item("4.2.1", "Banyaknya Sarana Kesehatan Menurut Jenis Sarana di Kecamatan Mempawah Hilir, 2023–2025", "Number of Health Facilities by Type in Mempawah Hilir District, 2023–2025", get_page_arabic(<tab_4_2_1>))
#v(5pt)
#toc_entry_item("5.1", "Luas Panen Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis di Kecamatan Mempawah Hilir (ha), 2022–2025", "Harvested Area of Vegetables and Seasonal Fruits by Type in Mempawah Hilir District (ha), 2022–2025", get_page_arabic(<tab_5_1>))
#v(5pt)
#toc_entry_item("6.1.1", "Keberadaan Sarana Akomodasi Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025", "Accommodation Facilities by Village/Subdistrict in Mempawah Hilir District, 2025", get_page_arabic(<tab_6_1_1>))
#v(5pt)
#toc_entry_item("7.1", "Keberadaan Lembaga Keuangan Bank Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025", "Banking Financial Institutions by Village/Subdistrict in Mempawah Hilir District, 2025", get_page_arabic(<tab_7_1>))

#pagebreak()

// ==========================================
// 8. DAFTAR GAMBAR / LIST OF FIGURES
// ==========================================
#metadata("daftar_gambar") <daftar_gambar>
#align(center)[
  #text(10pt, weight: "bold")[DAFTAR GAMBAR/]#text(10pt, weight: "bold", style: "italic")[LIST OF FIGURES]
]

#v(10pt)
#grid(
  columns: (24pt, 1fr, auto),
  column-gutter: (4pt, 6pt),
  [*Gambar*\ _Figure_], [], [*Halaman*\ _Page_]
)
#v(6pt)

#toc_entry_item("1.1", "Jarak dari Desa/Kelurahan ke Ibukota Kecamatan di Kecamatan Mempawah Hilir, 2025", "Distance from Village/Subdistrict to District Capital in Mempawah Hilir District, 2025", get_page_arabic(<fig_1_1>))
#v(5pt)
#toc_entry_item("1.2", "Luas Wilayah Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025", "Total Area by Village/Subdistrict in Mempawah Hilir District, 2025", get_page_arabic(<fig_1_2>))
#v(5pt)
#toc_entry_item("2.1", "Jumlah Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025", "Number of RT by Village in Mempawah Hilir District, 2025", get_page_arabic(<fig_2_1>))
#v(5pt)
#toc_entry_item("3.1", "Jumlah Penduduk Menurut Jenis Kelamin di Kecamatan Mempawah Hilir, 2025", "Population by Sex in Mempawah Hilir District, 2025", get_page_arabic(<fig_3_1>))
#v(5pt)
#toc_entry_item("4.1", "Banyaknya Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2025", "Number of School Facilities by Level in Mempawah Hilir District, 2025", get_page_arabic(<fig_4_1>))
#v(5pt)
#toc_entry_item("5.1", "Produksi Tanaman Hortikultura Unggulan di Kecamatan Mempawah Hilir, 2025", "Production of Leading Horticulture Crops in Mempawah Hilir District, 2025", get_page_arabic(<fig_5_1>))
#v(5pt)
#toc_entry_item("6.1", "Prasarana dan Sarana Komunikasi Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025", "Communication Infrastructure by Village in Mempawah Hilir District, 2025", get_page_arabic(<fig_6_1>))
#v(5pt)
#toc_entry_item("7.1", "Keberadaan Sarana Perdagangan dan Koperasi Aktif di Kecamatan Mempawah Hilir, 2025", "Trading Facilities and Active Cooperatives in Mempawah Hilir District, 2025", get_page_arabic(<fig_7_1>))

#pagebreak()

// ==========================================
// 9. PENJELASAN UMUM / EXPLANATORY NOTES
// ==========================================
#metadata("penjelasan_umum") <penjelasan_umum>
#align(center)[
  #text(10pt, weight: "bold")[PENJELASAN UMUM/]#text(10pt, weight: "bold", style: "italic")[EXPLANATORY NOTES]
]

#v(10pt)
#text(8pt)[
Tanda-tanda khusus, singkatan, serta kesepakatan penulisan yang digunakan dalam publikasi ini adalah sebagai berikut: \
_Special signs, abbreviations, and conventions used in this publication are as follows:_
]

#v(8pt)
#grid(
  columns: (32pt, 1fr),
  row-gutter: 6pt,
  [*...*], [Data belum tersedia / _Data not yet available_],
  [*–*], [Data tidak ada atau bernilai nol / _Data not available or zero value_],
  [*0 / 0,0*], [Angka lebih kecil dari 0,5 / _Figure less than 0.5_],
  [*x*], [Data dirahasiakan untuk menjaga kerahasiaan individu/unit usaha / _Confidential data_],
  [*ha*], [Hektar / _Hectare_],
  [*km*], [Kilometer / _Kilometer_],
  [*km²*], [Kilometer persegi / _Square kilometer_],
  [*RT/RW*], [Rukun Tetangga / Rukun Warga (_Neighborhood / Hamlet units_)]
)

#v(12pt)
#text(8pt)[
Catatan Pembulatan: Karena adanya pembulatan, angka-angka dalam penjumlahan baris/kolom mungkin tidak selalu sama persis dengan total penjumlahan. \
_Rounding Note: Due to rounding, figures in line/column totals may not strictly equal the sum of constituent elements._
]

// --- TRANSISI KE ARABIC NUMBERING ---
#metadata("transisi_isi") <transisi_isi>
#in_frontmatter.update(false)
#active_chapter.update("1. GEOGRAFI DAN IKLIM")
#is_chapter_page.update(true)
#pagebreak()
#counter(page).update(1)
#metadata("bab1") <bab1>

// ==========================================
// BAB 1: GEOGRAFI DAN IKLIM (HALAMAN PEMBATAS & INFOGRAFIS)
// ==========================================
#is_chapter_page.update(true)
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



#v(6pt)
#align(center)[
  #image("charts/gambar_1_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(4pt)
#metadata("fig_1_1") <fig_1_1>
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Gambar]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Figures]
      ],
      [
        #text(8.5pt, weight: "bold")[1.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jarak dari Desa/Kelurahan ke Ibukota Kecamatan di Mempawah Hilir, 2025 (km)] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Distance from Village/Subdistrict to District Capital in Mempawah Hilir Subdistrict, 2025 (km)]
  ]
)
#v(10pt)


#v(6pt)
#align(center)[
  #image("charts/gambar_1_2.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Dinas Kependudukan dan Pencatatan Sipil/BAPEDDA Kabupaten Mempawah/#text(style: "italic")[Population and Civil Registration Service/Regional Development Planning Agency of Mempawah Regency]]
#v(4pt)
#metadata("fig_1_2") <fig_1_2>
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Gambar]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Figures]
      ],
      [
        #text(8.5pt, weight: "bold")[1.2]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Luas Wilayah menurut Desa/Kelurahan di Mempawah Hilir, 2025 (km²)] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Total Area by Village/Subdistrict in Mempawah Hilir Subdistrict, 2025 (sq.km)]
  ]
)
#v(10pt)



#pagebreak()
#is_chapter_page.update(false)

// ==========================================
// ISI BAB 1: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Kecamatan Mempawah Hilir secara astronomis dan geografis terletak di wilayah pesisir dan daratan Kabupaten Mempawah, Provinsi Kalimantan Barat dengan ibukota kecamatan berada di Tanjung. Wilayah ini terbagi ke dalam 8 desa/kelurahan dengan akses perhubungan darat dan air yang menghubungkan pusat-pusat kegiatan ekonomi lokal dengan ibukota kabupaten.
]
#v(12pt)


#metadata("tab_1_1") <tab_1_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[1.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Luas Daerah Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Total Area by Village/Subdistrict in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.3fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Luas Daerah] \ #text(6pt, weight: "bold", style: "italic")[Total Area (km²)]], [#strong[Persentase] \ #text(6pt, weight: "bold", style: "italic")[Percentage (%)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]]),
  [Tanjung], [1.217], [2,62],
  [Kuala Secapah], [5.337], [11,50],
  [Tengah], [6.621], [14,26],
  [Terusan], [13.175], [28,38],
  [Pasir], [9.345], [20,13],
  [Penibung], [2.491], [5,37],
  [Sengkubang], [3.976], [8,56],
  [Malikian], [4.262], [9,18]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Dinas Kependudukan dan Pencatatan Sipil/BAPEDDA Kabupaten Mempawah / Population and Civil Registration Service/#text(style: "italic")[Regional Development Planning Agency of Mempawah Regency]]
#v(8pt)

#pagebreak()


#metadata("tab_1_2") <tab_1_2>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[1.2]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Distance to Subdistrict and Regency Capital by Village in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.3fr, 1.3fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Ke Ibukota Kec.] \ #text(6pt, weight: "bold", style: "italic")[To District Capital (km)]], [#strong[Ke Ibukota Kab.] \ #text(6pt, weight: "bold", style: "italic")[To Regency Capital (km)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]]),
  [Tanjung], [5,00], [5,50],
  [Kuala Secapah], [4,50], [3,00],
  [Tengah], [2,70], [0,35],
  [Terusan], [0,00], [2,70],
  [Pasir], [3,60], [5,40],
  [Penibung], [5,00], [7,60],
  [Sengkubang], [7,10], [10,00],
  [Malikian], [8,00], [12,00]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(8pt)

#v(10pt)

#metadata("tab_1_3") <tab_1_3>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[1.3]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Batas Administrasi Kecamatan Mempawah Hilir Menurut Arah Mata Angin, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Administrative Borders of Mempawah Hilir Subdistrict by Cardinal Direction, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 1.8fr, 3.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[No]], [#strong[Arah Mata Angin] \ #text(6pt, weight: "bold", style: "italic")[Wind Direction]], [#strong[Berbatasan Dengan] \ #text(6pt, weight: "bold", style: "italic")[Bordering With]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]]),
  [1], [Utara/North], [Kecamatan Sungai Kunyit/Sungai Kunyit District],
  [2], [Selatan/South], [Kecamatan Mempawah Timur/ Mempawah Timur District],
  [3], [Barat/West], [Selat Karimata/ Karimata Strait],
  [4], [Timur/East], [Kecamatan Sadaniang/ Sadaniang District]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/Bagian Tata Pemerintahan Setda Mempawah/#text(style: "italic")[Mempawah Hilir District Office/Regional Secretariat Governance Division of Mempawah Regency]]
#v(8pt)

#pagebreak()


#metadata("tab_1_4") <tab_1_4>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[1.4]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jarak Kantor Camat Mempawah Hilir dengan Kota dan Tempat Penting Lainnya, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Distance from Mempawah Hilir Subdistrict Office to Other Important Places, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 3.2fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[No]], [#strong[Nama Kota dan Tempat Penting] \ #text(6pt, weight: "bold", style: "italic")[Other Important Places]], [#strong[Jarak] \ #text(6pt, weight: "bold", style: "italic")[Distance (km)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]]),
  [1], [Ibukota Provinsi Kalimantan Barat (Kota Pontianak)], [63,00],
  [2], [Pusat Pemerintahan Kabupaten Mempawah (Mempawah Hilir)], [2,80],
  [3], [Makam Juang Mandor], [50,00]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(8pt)


#active_chapter.update("2. PEMERINTAHAN")
#is_chapter_page.update(true)
#pagebreak()
#metadata("bab2") <bab2>

// ==========================================
// BAB 2: PEMERINTAHAN (HALAMAN PEMBATAS & INFOGRAFIS)
// ==========================================
#is_chapter_page.update(true)
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



#v(6pt)
#align(center)[
  #image("charts/gambar_2_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(4pt)
#metadata("fig_2_1") <fig_2_1>
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Gambar]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Figures]
      ],
      [
        #text(8.5pt, weight: "bold")[2.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Rukun Tetangga (RT) menurut Desa/Kelurahan di Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Neighborhood Units (RT) by Village/Subdistrict in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(10pt)



#pagebreak()
#is_chapter_page.update(false)

// ==========================================
// ISI BAB 2: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Secara administratif, Kecamatan Mempawah Hilir terbagi menjadi 8 desa/kelurahan yang dipimpin oleh kepala desa dan lurah definitif, didukung oleh aparatur pemerintah desa, Badan Permusyawaratan Desa (BPD), serta kelembagaan RT dan RW sebagai garda terdepan pelayanan kemasyarakatan.
]
#v(12pt)


#metadata("tab_2_1_1") <tab_2_1_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[2.1.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Hamlets, RW, and RT by Village/Subdistrict in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Jumlah Dusun] \ #text(6pt, weight: "bold", style: "italic")[Hamlets]], [#strong[Rukun Warga] \ #text(6pt, weight: "bold", style: "italic")[(RW)]], [#strong[Rukun Tetangga] \ #text(6pt, weight: "bold", style: "italic")[(RT)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Tanjung], [–], [3], [6],
  [Kuala Secapah], [4], [8], [15],
  [Tengah], [–], [8], [24],
  [Terusan], [–], [17], [41],
  [Pasir], [7], [10], [34],
  [Penibung], [3], [8], [16],
  [Sengkubang], [4], [7], [16],
  [Malikian], [8], [10], [27]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(8pt)

#pagebreak()


#metadata("tab_2_1_2") <tab_2_1_2>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[2.1.2]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan Mempawah Hilir] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Names of District Heads of Mempawah Hilir Subdistrict]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 2.8fr, 1.6fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[No]], [#strong[Nama Camat] \ #text(6pt, weight: "bold", style: "italic")[Name of District Head]], [#strong[Periode Menjabat] \ #text(6pt, weight: "bold", style: "italic")[Period]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]]),
  [1], [Saidi Said], [1949 – 1953],
  [2], [T.A.A Samaun], [1953 – 1957],
  [3], [M. Yusuf Abdul Rahim], [1957 – 1961],
  [4], [Abdul Wahab H Jamaludin], [1961 – 1965],
  [5], [M Yusuf Abdul Rahim], [1965 – 1969],
  [6], [Abdul Jabar], [1969 – 1973],
  [7], [Gusti Amirudin Hamid], [1973 – 1977],
  [8], [Abdul Majid Rani], [1977 – 1981],
  [9], [Syarif Ismail Abdullah], [1981 – 1985],
  [10], [Drs. Daeng Syarifuddin], [1985 – 1989],
  [11], [Drs. A . Malik], [1989 – 1993],
  [12], [Drs. Suhardi Sakim], [1993 – 1998]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(8pt)

#v(10pt)

#metadata("tab_2_1_3") <tab_2_1_3>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[2.1.3]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Nama-Nama Kepala Desa/Lurah di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Names of Village Heads in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 2.2fr, 2.8fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[No]], [#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Nama Kepala Desa / Lurah] \ #text(6pt, weight: "bold", style: "italic")[Name of Village Head]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]]),
  [1], [Tanjung], [Syarif Hilman Noviardi, S.Kom],
  [2], [Kuala Secapah], [Mawardi],
  [3], [Tengah], [Friant Adhitya, S.IP, MAP],
  [4], [Terusan], [Hendi Permana, S.STP, M.A.B],
  [5], [Pasir], [–],
  [6], [Penibung], [Evi Junita, S.Pd.I],
  [7], [Sengkubang], [Alfian],
  [8], [Malikian], [Akhmad]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(8pt)

#pagebreak()


#metadata("tab_2_1_6") <tab_2_1_6>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[2.1.6]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Status Desa Berdasarkan Indeks Desa Membangun (IDM) di Kecamatan Mempawah Hilir, 2024/2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Village Status Based on Developing Village Index (IDM) in Mempawah Hilir Subdistrict, 2024/2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.2fr, 1.5fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Skor IDM] \ #text(6pt, weight: "bold", style: "italic")[IDM Score]], [#strong[Status IDM] \ #text(6pt, weight: "bold", style: "italic")[IDM Status]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]]),
  [Tanjung], [...], [...],
  [Kuala Secapah], [...], [...],
  [Tengah], [...], [...],
  [Terusan], [...], [...],
  [Pasir], [...], [...],
  [Penibung], [...], [...],
  [Sengkubang], [...], [...],
  [Malikian], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kementerian Desa, Pembangunan Daerah Tertinggal, dan Transmigrasi/#text(style: "italic")[Ministry of Villages, Disadvantaged Regions Development, and Transmigration]]
#v(8pt)

#v(10pt)

#metadata("tab_2_2_1") <tab_2_2_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[2.2.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Pegawai Negeri Sipil Pemerintah Daerah Kecamatan Menurut Golongan di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Civil Servants in Mempawah Hilir Subdistrict Office by Rank/Class, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Golongan] \ #text(6pt, weight: "bold", style: "italic")[Rank / Class]], [#strong[Laki-laki] \ #text(6pt, weight: "bold", style: "italic")[Male]], [#strong[Perempuan] \ #text(6pt, weight: "bold", style: "italic")[Female]], [#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Golongan I], [...], [...], [...],
  [Golongan II], [...], [...], [...],
  [Golongan III], [...], [...], [...],
  [Golongan IV], [...], [...], [...],
  [Jumlah/_Total_], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(8pt)

#pagebreak()


#metadata("tab_2_2_2") <tab_2_2_2>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[2.2.2]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Pegawai Negeri Sipil Pemerintah Daerah Kecamatan Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Civil Servants in Mempawah Hilir Subdistrict Office by Education Level, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Education Level]], [#strong[Laki-laki] \ #text(6pt, weight: "bold", style: "italic")[Male]], [#strong[Perempuan] \ #text(6pt, weight: "bold", style: "italic")[Female]], [#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [≤ SMP/Junior High], [...], [...], [...],
  [SMA/Senior High], [...], [...], [...],
  [Diploma I/II/III], [...], [...], [...],
  [S1/D-IV (Bachelor)], [...], [...], [...],
  [S2/Master], [...], [...], [...],
  [Jumlah/_Total_], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(8pt)


#active_chapter.update("3. KEPENDUDUKAN")
#is_chapter_page.update(true)
#pagebreak()
#metadata("bab3") <bab3>

// ==========================================
// BAB 3: KEPENDUDUKAN (HALAMAN PEMBATAS & INFOGRAFIS)
// ==========================================
#is_chapter_page.update(true)
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



#v(6pt)
#align(center)[
  #image("charts/gambar_3_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah (Semester II 2025)/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency (Semester II 2025)]]
#v(4pt)
#metadata("fig_3_1") <fig_3_1>
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Gambar]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Figures]
      ],
      [
        #text(8.5pt, weight: "bold")[3.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Penduduk menurut Jenis Kelamin dan Desa/Kelurahan di Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Population by Sex and Village/Subdistrict in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(10pt)



#pagebreak()
#is_chapter_page.update(false)

// ==========================================
// ISI BAB 3: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Berdasdasarkan data registrasi semester II tahun 2025 dari Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah, jumlah penduduk Kecamatan Mempawah Hilir terdistribusi di 8 desa/kelurahan dengan struktur demografi yang produktif. Komposisi penduduk laki-laki dan perempuan relatif berimbang, mencerminkan kestabilan demografis wilayah.
]
#v(12pt)


#metadata("tab_3_1") <tab_3_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[3.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Penduduk, Distribusi Persentase, dan Kepadatan Penduduk Menurut Desa/Kelurahan di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Population, Percentage Distribution, and Density by Village/Subdistrict in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.0fr, 1.0fr, 1.0fr, 1.1fr, 1.0fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Laki-laki] \ #text(6pt, weight: "bold", style: "italic")[Male]], [#strong[Perempuan] \ #text(6pt, weight: "bold", style: "italic")[Female]], [#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], [#strong[Persentase] \ #text(6pt, weight: "bold", style: "italic")[Percentage (%)]], [#strong[Kepadatan] \ #text(6pt, weight: "bold", style: "italic")[Density (jiwa/km²)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]], [#strong[(6)]]),
  [Tanjung], [615], [602], [1.217], [2,62], [124,69],
  [Kuala Secapah], [2.728], [2.609], [5.337], [11,50], [549,64],
  [Tengah], [3.364], [3.257], [6.621], [14,26], [793,88],
  [Terusan], [6.558], [6.617], [13.175], [28,38], [2.688,78],
  [Pasir], [4.768], [4.577], [9.345], [20,13], [170,19],
  [Penibung], [1.280], [1.211], [2.491], [5,37], [212,00],
  [Sengkubang], [1.996], [1.980], [3.976], [8,56], [160,65],
  [Malikian], [2.151], [2.111], [4.262], [9,18], [139,24]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah (Semester II 2025)/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency (Semester II 2025)]]
#v(8pt)


#active_chapter.update("4. SOSIAL DAN KESEJAHTERAAN RAKYAT")
#is_chapter_page.update(true)
#pagebreak()
#metadata("bab4") <bab4>

// ==========================================
// BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT (HALAMAN PEMBATAS & INFOGRAFIS)
// ==========================================
#is_chapter_page.update(true)
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


#v(1.5cm)
#align(center)[
  #rect(width: 95%, height: 11cm, fill: rgb("#FFFBEB"), stroke: (paint: rgb("#F59E0B"), thickness: 1.5pt, dash: "dashed"), radius: 6pt)[
    #align(center + horizon)[
      #text(12pt, weight: "bold", fill: rgb("#B45309"))[INFOGRAFIS SOSIAL & KESEJAHTERAAN RAKYAT]      #v(6pt)
      #text(8.5pt, fill: rgb("#92400E"), style: "italic")[Kecamatan Mempawah Hilir]
    ]
  ]
]


#pagebreak()
#is_chapter_page.update(false)

// ==========================================
// ISI BAB 4: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Pembangunan bidang sosial kemasyarakatan di Kecamatan Mempawah Hilir ditopang oleh perluasan aksesibilitas sarana pendidikan dasar hingga menengah, peningkatan mutu fasilitas kesehatan masyarakat, ketersediaan energi penerangan rumah tangga, serta kesiapsiagaan dalam menghadapi potensi bencana lingkungan hidup.
]
#v(12pt)


#metadata("tab_4_1_1") <tab_4_1_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[4.1.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2023–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Villages Having Educational Facilities by Educational Level in Mempawah Hilir Subdistrict, 2023–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], [#strong[2023]], [#strong[2024]], [#strong[2025]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Taman Kanak-Kanak (TK)], [...], [...], [...],
  [Raudatul Athfal (RA)], [...], [...], [...],
  [Sekolah Dasar (SD)], [...], [...], [...],
  [Madrasah Ibtidaiyah (MI)], [...], [...], [...],
  [Sekolah Menengah Pertama (SMP)], [...], [...], [...],
  [Madrasah Tsanawiyah (MTs)], [...], [...], [...],
  [Sekolah Menengah Atas (SMA)], [...], [...], [...],
  [Sekolah Menengah Kejuruan (SMK)], [...], [...], [...],
  [Madrasah Aliyah (MA)], [...], [...], [...],
  [Akademi/Perguruan Tinggi], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS-Statistics Indonesia, Village Potential Census (Podes)]]
#v(8pt)

#pagebreak()


#metadata("tab_4_1_2") <tab_4_1_2>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[4.1.2]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Satuan Pendidikan Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2024/2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Educational Units by Education Level in Mempawah Hilir Subdistrict, 2024/2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], [#strong[Negeri] \ #text(6pt, weight: "bold", style: "italic")[Public]], [#strong[Swasta] \ #text(6pt, weight: "bold", style: "italic")[Private]], [#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Taman Kanak-Kanak (TK)], [...], [...], [...],
  [Raudatul Athfal (RA)], [...], [...], [...],
  [Sekolah Dasar (SD)], [...], [...], [...],
  [Madrasah Ibtidaiyah (MI)], [...], [...], [...],
  [Sekolah Menengah Pertama (SMP)], [...], [...], [...],
  [Madrasah Tsanawiyah (MTs)], [...], [...], [...],
  [Sekolah Menengah Atas (SMA)], [...], [...], [...],
  [Sekolah Menengah Kejuruan (SMK)], [...], [...], [...],
  [Madrasah Aliyah (MA)], [...], [...], [...],
  [Jumlah/_Total_], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama/#text(style: "italic")[Ministry of Education, Culture, Research, and Technology & Ministry of Religious Affairs]]
#v(8pt)

#v(10pt)

#metadata("tab_4_1_3") <tab_4_1_3>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[4.1.3]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Kepala Sekolah dan Guru Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2024/2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Principals and Teachers by Education Level in Mempawah Hilir Subdistrict, 2024/2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], [#strong[Negeri] \ #text(6pt, weight: "bold", style: "italic")[Public]], [#strong[Swasta] \ #text(6pt, weight: "bold", style: "italic")[Private]], [#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Taman Kanak-Kanak (TK)], [...], [...], [...],
  [Raudatul Athfal (RA)], [...], [...], [...],
  [Sekolah Dasar (SD)], [...], [...], [...],
  [Madrasah Ibtidaiyah (MI)], [...], [...], [...],
  [Sekolah Menengah Pertama (SMP)], [...], [...], [...],
  [Madrasah Tsanawiyah (MTs)], [...], [...], [...],
  [Sekolah Menengah Atas (SMA)], [...], [...], [...],
  [Sekolah Menengah Kejuruan (SMK)], [...], [...], [...],
  [Madrasah Aliyah (MA)], [...], [...], [...],
  [Jumlah/_Total_], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama/#text(style: "italic")[Ministry of Education, Culture, Research, and Technology & Ministry of Religious Affairs]]
#v(8pt)

#pagebreak()


#metadata("tab_4_1_4") <tab_4_1_4>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[4.1.4]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Peserta Didik Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2024/2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Students by Education Level in Mempawah Hilir Subdistrict, 2024/2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], [#strong[Negeri] \ #text(6pt, weight: "bold", style: "italic")[Public]], [#strong[Swasta] \ #text(6pt, weight: "bold", style: "italic")[Private]], [#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Taman Kanak-Kanak (TK)], [...], [...], [...],
  [Raudatul Athfal (RA)], [...], [...], [...],
  [Sekolah Dasar (SD)], [...], [...], [...],
  [Madrasah Ibtidaiyah (MI)], [...], [...], [...],
  [Sekolah Menengah Pertama (SMP)], [...], [...], [...],
  [Madrasah Tsanawiyah (MTs)], [...], [...], [...],
  [Sekolah Menengah Atas (SMA)], [...], [...], [...],
  [Sekolah Menengah Kejuruan (SMK)], [...], [...], [...],
  [Madrasah Aliyah (MA)], [...], [...], [...],
  [Jumlah/_Total_], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama/#text(style: "italic")[Ministry of Education, Culture, Research, and Technology & Ministry of Religious Affairs]]
#v(8pt)

#v(10pt)

#metadata("tab_4_2_1") <tab_4_2_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[4.2.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Sarana Kesehatan Menurut Jenis Sarana di Kecamatan Mempawah Hilir, 2023–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Health Facilities by Type in Mempawah Hilir Subdistrict, 2023–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Sarana Kesehatan] \ #text(6pt, weight: "bold", style: "italic")[Type of Health Facility]], [#strong[2023]], [#strong[2024]], [#strong[2025]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Rumah Sakit/_Hospital_], [...], [...], [...],
  [Puskesmas Rawat Inap/_Inpatient PHC_], [...], [...], [...],
  [Puskesmas Tanpa Rawat Inap/_Outpatient PHC_], [...], [...], [...],
  [Puskesmas Pembantu (Pustu)], [...], [...], [...],
  [Poliklinik/Balai Pengobatan], [...], [...], [...],
  [Apotek/_Pharmacy_], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Dinas Kesehatan, Pengendalian Penduduk dan KB Kabupaten Mempawah/Podes 2025/#text(style: "italic")[Health, Population Control, and Family Planning Service of Mempawah Regency/Podes 2025]]
#v(8pt)

#pagebreak()


#metadata("tab_4_3_1") <tab_4_3_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[4.3.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Keluarga Menurut Sumber Penerangan Utama di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Families by Main Electricity Source in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.2fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Listrik PLN] \ #text(6pt, weight: "bold", style: "italic")[PLN Electricity]], [#strong[Listrik Non-PLN] \ #text(6pt, weight: "bold", style: "italic")[Non-PLN Electricity]], [#strong[Bukan Listrik] \ #text(6pt, weight: "bold", style: "italic")[Non-Electricity]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Tanjung], [...], [...], [...],
  [Kuala Secapah], [...], [...], [...],
  [Tengah], [...], [...], [...],
  [Terusan], [...], [...], [...],
  [Pasir], [...], [...], [...],
  [Penibung], [...], [...], [...],
  [Sengkubang], [...], [...], [...],
  [Malikian], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS, Pendataan Potensi Desa (Podes) 2025/#text(style: "italic")[BPS-Statistics Indonesia, Village Potential Census (Podes) 2025]]
#v(8pt)

#v(10pt)

#metadata("tab_4_4_1") <tab_4_4_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[4.4.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Kejadian Bencana Alam Menurut Jenis Bencana di Kecamatan Mempawah Hilir, 2023–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Natural Disaster Events by Type in Mempawah Hilir Subdistrict, 2023–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Bencana Alam] \ #text(6pt, weight: "bold", style: "italic")[Type of Disaster]], [#strong[2023]], [#strong[2024]], [#strong[2025]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Tanah Longsor/_Landslide_], [...], [...], [...],
  [Banjir/_Flood_], [...], [...], [...],
  [Banjir Bandang/_Flash Flood_], [...], [...], [...],
  [Gempa Bumi/_Earthquake_], [...], [...], [...],
  [Gelombang Pasang Laut/_Tidal Wave_], [...], [...], [...],
  [Angin Puyuh/Puting Beliung], [...], [...], [...],
  [Kebakaran Hutan dan Lahan/_Forest Fire_], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Badan Penanggulangan Bencana Daerah (BPBD) Kabupaten Mempawah/Podes 2025/#text(style: "italic")[Regional Disaster Management Agency (BPBD) of Mempawah Regency/Podes 2025]]
#v(8pt)


#active_chapter.update("5. PERTANIAN")
#is_chapter_page.update(true)
#pagebreak()
#metadata("bab5") <bab5>

// ==========================================
// BAB 5: PERTANIAN (HALAMAN PEMBATAS & INFOGRAFIS)
// ==========================================
#is_chapter_page.update(true)
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


#v(1.5cm)
#align(center)[
  #rect(width: 95%, height: 11cm, fill: rgb("#FFFBEB"), stroke: (paint: rgb("#F59E0B"), thickness: 1.5pt, dash: "dashed"), radius: 6pt)[
    #align(center + horizon)[
      #text(12pt, weight: "bold", fill: rgb("#B45309"))[INFOGRAFIS PERTANIAN]      #v(6pt)
      #text(8.5pt, fill: rgb("#92400E"), style: "italic")[Kecamatan Mempawah Hilir]
    ]
  ]
]


#pagebreak()
#is_chapter_page.update(false)

// ==========================================
// ISI BAB 5: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Sektor pertanian merupakan salah satu pilar penopang perekonomian masyarakat di Kecamatan Mempawah Hilir. Komoditas sayuran semusim, tanaman biofarmaka, serta buah-buahan tahunan dibudidayakan secara intensif oleh rumah tangga petani guna memenuhi kebutuhan pasar domestik dan regional Kabupaten Mempawah.
]
#v(12pt)


#metadata("tab_5_1") <tab_5_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[5.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Luas Panen Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Mempawah Hilir, 2022–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Harvested Area of Seasonal Vegetables and Fruits by Kind of Plants in Mempawah Hilir Subdistrict, 2022–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (ha)]], [#strong[2023 (ha)]], [#strong[2024 (ha)]], [#strong[2025 (ha)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Bawang Merah/_Shallots_], [...], [...], [...], [...],
  [Cabai Besar/_Big Chili_], [...], [...], [...], [...],
  [Cabai Rawit/_Cayenne Pepper_], [...], [...], [...], [...],
  [Tomat/_Tomato_], [...], [...], [...], [...],
  [Terung/_Eggplant_], [...], [...], [...], [...],
  [Kacang Panjang/_Long Beans_], [...], [...], [...], [...],
  [Ketimun/_Cucumber_], [...], [...], [...], [...],
  [Kangkung/_Water Spinach_], [...], [...], [...], [...],
  [Bayam/_Spinach_], [...], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS)/#text(style: "italic")[BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-SBS)]]
#v(8pt)

#pagebreak()


#metadata("tab_5_2") <tab_5_2>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[5.2]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Produksi Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Mempawah Hilir, 2022–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Production of Seasonal Vegetables and Fruits by Kind of Plants in Mempawah Hilir Subdistrict, 2022–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (ku)]], [#strong[2023 (ku)]], [#strong[2024 (ku)]], [#strong[2025 (ku)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Bawang Merah/_Shallots_], [...], [...], [...], [...],
  [Cabai Besar/_Big Chili_], [...], [...], [...], [...],
  [Cabai Rawit/_Cayenne Pepper_], [...], [...], [...], [...],
  [Tomat/_Tomato_], [...], [...], [...], [...],
  [Terung/_Eggplant_], [...], [...], [...], [...],
  [Kacang Panjang/_Long Beans_], [...], [...], [...], [...],
  [Ketimun/_Cucumber_], [...], [...], [...], [...],
  [Kangkung/_Water Spinach_], [...], [...], [...], [...],
  [Bayam/_Spinach_], [...], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS)/#text(style: "italic")[BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-SBS)]]
#v(8pt)

#pagebreak()


#metadata("tab_5_3") <tab_5_3>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[5.3]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Luas Panen Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Mempawah Hilir, 2022–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Harvested Area of Medicinal Plants by Kind of Plants in Mempawah Hilir Subdistrict, 2022–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (m²)]], [#strong[2023 (m²)]], [#strong[2024 (m²)]], [#strong[2025 (m²)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Jahe/_Ginger_], [...], [...], [...], [...],
  [Lengkuas/_Galangal_], [...], [...], [...], [...],
  [Kencur/_East Indian Galangal_], [...], [...], [...], [...],
  [Kunyit/_Turmeric_], [...], [...], [...], [...],
  [Lempuyang], [...], [...], [...], [...],
  [Temulawak/_Java Turmeric_], [...], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF)/#text(style: "italic")[BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-TBF)]]
#v(8pt)

#v(10pt)

#metadata("tab_5_4") <tab_5_4>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[5.4]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Produksi Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Mempawah Hilir, 2022–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Production of Medicinal Plants by Kind of Plants in Mempawah Hilir Subdistrict, 2022–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (kg)]], [#strong[2023 (kg)]], [#strong[2024 (kg)]], [#strong[2025 (kg)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Jahe/_Ginger_], [...], [...], [...], [...],
  [Lengkuas/_Galangal_], [...], [...], [...], [...],
  [Kencur/_East Indian Galangal_], [...], [...], [...], [...],
  [Kunyit/_Turmeric_], [...], [...], [...], [...],
  [Lempuyang], [...], [...], [...], [...],
  [Temulawak/_Java Turmeric_], [...], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF)/#text(style: "italic")[BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-TBF)]]
#v(8pt)

#pagebreak()


#metadata("tab_5_7") <tab_5_7>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[5.7]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Produksi Buah-Buahan dan Sayuran Tahunan Menurut Jenis Tanaman di Kecamatan Mempawah Hilir, 2022–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Production of Annual Fruits and Vegetables by Kind of Plants in Mempawah Hilir Subdistrict, 2022–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (ku)]], [#strong[2023 (ku)]], [#strong[2024 (ku)]], [#strong[2025 (ku)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Durian/_Durian_], [...], [...], [...], [...],
  [Mangga/_Mango_], [...], [...], [...], [...],
  [Jeruk Siam/_Siamese Orange_], [...], [...], [...], [...],
  [Pisang/_Banana_], [...], [...], [...], [...],
  [Pepaya/_Papaya_], [...], [...], [...], [...],
  [Nanas/_Pineapple_], [...], [...], [...], [...],
  [Rambutan/_Rambutan_], [...], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)/#text(style: "italic")[BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-BST)]]
#v(8pt)


#active_chapter.update("6. PARIWISATA, TRANSPORTASI, DAN KOMUNIKASI")
#is_chapter_page.update(true)
#pagebreak()
#metadata("bab6") <bab6>

// ==========================================
// BAB 6: PARIWISATA, TRANSPORTASI & KOMUNIKASI (HALAMAN PEMBATAS & INFOGRAFIS)
// ==========================================
#is_chapter_page.update(true)
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


#v(1.5cm)
#align(center)[
  #rect(width: 95%, height: 11cm, fill: rgb("#FFFBEB"), stroke: (paint: rgb("#F59E0B"), thickness: 1.5pt, dash: "dashed"), radius: 6pt)[
    #align(center + horizon)[
      #text(12pt, weight: "bold", fill: rgb("#B45309"))[INFOGRAFIS PARIWISATA, TRANSPORTASI & KOMUNIKASI]      #v(6pt)
      #text(8.5pt, fill: rgb("#92400E"), style: "italic")[Kecamatan Mempawah Hilir]
    ]
  ]
]


#pagebreak()
#is_chapter_page.update(false)

// ==========================================
// ISI BAB 6: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Konektivitas wilayah di Kecamatan Mempawah Hilir terhubung oleh jaringan jalan darat antardesa yang dapat dilalui kendaraan roda empat sepanjang tahun. Selain itu, penetrasi infrastruktur telekomunikasi bergerak (seluler) dan jaringan internet berkecepatan tinggi terus meluas, mempercepat arus informasi dan transaksi digital masyarakat.
]
#v(12pt)


#metadata("tab_6_1_1") <tab_6_1_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[6.1.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Desa/Kelurahan Menurut Keberadaan Sarana Transportasi Antardesa di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Villages by Inter-Village Transportation Infrastructure in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.2fr, 1.1fr, 1.2fr, 1.1fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Jenis Lalu Lintas] \ #text(6pt, weight: "bold", style: "italic")[Type of Traffic]], [#strong[Jenis Permukaan Jalan] \ #text(6pt, weight: "bold", style: "italic")[Type of Road Surface]], [#strong[Dapat Dilalui Roda 4+] \ #text(6pt, weight: "bold", style: "italic")[Passable by 4+ Wheels]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Tanjung], [...], [...], [...],
  [Kuala Secapah], [...], [...], [...],
  [Tengah], [...], [...], [...],
  [Terusan], [...], [...], [...],
  [Pasir], [...], [...], [...],
  [Penibung], [...], [...], [...],
  [Sengkubang], [...], [...], [...],
  [Malikian], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS, Pendataan Potensi Desa (Podes) 2025/#text(style: "italic")[BPS-Statistics Indonesia, Village Potential Census (Podes) 2025]]
#v(8pt)

#pagebreak()


#metadata("tab_6_2_1") <tab_6_2_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[6.2.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Desa/Kelurahan Menurut Keberadaan Kantor Pos dan Ekspedisi Swasta di Kecamatan Mempawah Hilir, 2023–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Villages by Availability of Post Office and Private Courier in Mempawah Hilir Subdistrict, 2023–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.8fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Fasilitas Pos/Logistik] \ #text(6pt, weight: "bold", style: "italic")[Type of Postal/Courier Facility]], [#strong[2023]], [#strong[2024]], [#strong[2025]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Kantor Pos/Pos Pembantu/Rumah Pos], [...], [...], [...],
  [Perusahaan/Agen Jasa Ekspedisi Swasta], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS, Pendataan Potensi Desa (Podes) 2025/#text(style: "italic")[BPS-Statistics Indonesia, Village Potential Census (Podes) 2025]]
#v(8pt)

#v(10pt)

#metadata("tab_6_3_1") <tab_6_3_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[6.3.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Menara BTS dan Kekuatan Sinyal Internet Seluler Menurut Desa di Kecamatan Mempawah Hilir, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of BTS Towers and Cellular Internet Signal Strength by Village in Mempawah Hilir Subdistrict, 2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.2fr, 1.0fr, 1.2fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Jumlah Menara BTS] \ #text(6pt, weight: "bold", style: "italic")[Number of BTS Towers]], [#strong[Sinyal Telepon Seluler] \ #text(6pt, weight: "bold", style: "italic")[Cellular Signal]], [#strong[Sinyal Internet (4G/5G)] \ #text(6pt, weight: "bold", style: "italic")[Internet Signal (4G/5G)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Tanjung], [...], [...], [...],
  [Kuala Secapah], [...], [...], [...],
  [Tengah], [...], [...], [...],
  [Terusan], [...], [...], [...],
  [Pasir], [...], [...], [...],
  [Penibung], [...], [...], [...],
  [Sengkubang], [...], [...], [...],
  [Malikian], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS, Pendataan Potensi Desa (Podes) 2025/#text(style: "italic")[BPS-Statistics Indonesia, Village Potential Census (Podes) 2025]]
#v(8pt)


#active_chapter.update("7. PERBANKAN, KOPERASI, DAN PERDAGANGAN")
#is_chapter_page.update(true)
#pagebreak()
#metadata("bab7") <bab7>

// ==========================================
// BAB 7: PERBANKAN, KOPERASI & PERDAGANGAN (HALAMAN PEMBATAS & INFOGRAFIS)
// ==========================================
#is_chapter_page.update(true)
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


#v(1.5cm)
#align(center)[
  #rect(width: 95%, height: 11cm, fill: rgb("#FFFBEB"), stroke: (paint: rgb("#F59E0B"), thickness: 1.5pt, dash: "dashed"), radius: 6pt)[
    #align(center + horizon)[
      #text(12pt, weight: "bold", fill: rgb("#B45309"))[INFOGRAFIS PERBANKAN, KOPERASI & PERDAGANGAN]      #v(6pt)
      #text(8.5pt, fill: rgb("#92400E"), style: "italic")[Kecamatan Mempawah Hilir]
    ]
  ]
]


#pagebreak()
#is_chapter_page.update(false)

// ==========================================
// ISI BAB 7: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Aktivitas perniagaan di Kecamatan Mempawah Hilir berkembang dinamis didukung oleh sarana perdagangan tradisional (pasar dan warung rakyat) serta jaringan minimarket modern. Keberadaan lembaga perbankan, koperasi, dan lembaga keuangan mikro memegang peranan krusial dalam memperluas inklusi keuangan serta akses permodalan bagi usaha mikro, kecil, dan menengah (UMKM).
]
#v(12pt)


#metadata("tab_7_1") <tab_7_1>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[7.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Sarana Perdagangan Menurut Jenis Sarana di Kecamatan Mempawah Hilir, 2023–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Trade Facilities by Type in Mempawah Hilir Subdistrict, 2023–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Sarana Perdagangan] \ #text(6pt, weight: "bold", style: "italic")[Type of Trade Facility]], [#strong[2023]], [#strong[2024]], [#strong[2025]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Pasar dengan Bangunan Permanen], [...], [...], [...],
  [Pasar dengan Bangunan Semi Permanen], [...], [...], [...],
  [Pasar Tanpa Bangunan], [...], [...], [...],
  [Kelompok Pertokoan/Ruko], [...], [...], [...],
  [Minimarket/Supermarket], [...], [...], [...],
  [Restoran/Rumah Makan / Warung Makan], [...], [...], [...],
  [Hotel/Penginapan / Losmen], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Dinas Perindagnaker Kab. Mempawah/Podes 2025/#text(style: "italic")[Industry, Trade, and Manpower Service of Mempawah Regency/Podes 2025]]
#v(8pt)

#pagebreak()


#metadata("tab_7_2") <tab_7_2>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[7.2]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Koperasi Aktif Menurut Jenis Koperasi di Kecamatan Mempawah Hilir, 2023–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Active Cooperatives by Type in Mempawah Hilir Subdistrict, 2023–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Koperasi] \ #text(6pt, weight: "bold", style: "italic")[Type of Cooperative]], [#strong[2023]], [#strong[2024]], [#strong[2025]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Koperasi Unit Desa (KUD)], [...], [...], [...],
  [Koperasi Simpan Pinjam (KSP)], [...], [...], [...],
  [Koperasi Lainnya (Non-KUD)], [...], [...], [...],
  [Jumlah/_Total_], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Dinas Perindagnaker Kab. Mempawah/Podes 2025/#text(style: "italic")[Industry, Trade, and Manpower Service of Mempawah Regency/Podes 2025]]
#v(8pt)

#v(10pt)

#metadata("tab_7_3") <tab_7_3>
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[7.3]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Banyaknya Lembaga Keuangan Menurut Jenis Lembaga di Kecamatan Mempawah Hilir, 2023–2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Financial Institutions by Type in Mempawah Hilir Subdistrict, 2023–2025]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.8fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { rgb("#FFC934") }
                      else if row == 1 { rgb("#FFDC8A") }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Lembaga Keuangan] \ #text(6pt, weight: "bold", style: "italic")[Type of Financial Institution]], [#strong[2023]], [#strong[2024]], [#strong[2025]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Bank Umum Pemerintah (BRI, Mandiri, BNI, BTN, dll.)], [...], [...], [...],
  [Bank Umum Swasta], [...], [...], [...],
  [Bank Perekonomian Rakyat (BPR)], [...], [...], [...],
  [Kantor Pegadaian], [...], [...], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Otoritas Jasa Keuangan (OJK)/Podes 2025/#text(style: "italic")[Financial Services Authority (OJK)/Podes 2025]]
#v(8pt)


#active_chapter.update("DAFTAR PUSTAKA")
#pagebreak()

// ==========================================
// DAFTAR PUSTAKA / BIBLIOGRAPHY
// ==========================================
#metadata("daftar_pustaka") <daftar_pustaka>
#v(0.8cm)
#align(center)[
  #text(11pt, weight: "bold")[DAFTAR PUSTAKA/]#text(11pt, weight: "bold", style: "italic")[BIBLIOGRAPHY]
]
#v(16pt)

#set par(justify: true, first-line-indent: -1.5em, hanging-indent: 1.5em, leading: 0.65em)
#text(8pt)[
  Badan Pusat Statistik. 2022. _Buku 3: Konsep dan Definisi Podes 2022_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Direktorat Statistik Ketahanan Sosial. 2024. _Buku 3: Pedoman Konsep dan Definisi Podes 2024_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Kementerian Pertanian & Badan Pusat Statistik. 2023. _Pedoman Statistik Pertanian Hortikultura (SPH)_. Jakarta: Kementerian Pertanian.
]

#metadata("akhir_buku") <akhir_buku>

// ==========================================
// KOVER BELAKANG (BACK COVER) - GENERATED NATIVELY VIA TYPST
// ==========================================
#page(
  paper: "a5",
  margin: (top: 0cm, bottom: 0cm, left: 0cm, right: 0cm),
  header: none,
  footer: none,
  fill: gradient.linear(angle: 145deg, rgb("#440815"), rgb("#2E040C"), rgb("#180206")),
)[
  // 1. Pita Dekoratif Melengkung Khas Publikasi (Typst Bezier Curves)
  #place(top + left)[
    #let ribbon_left(dx, dy, alpha, thick) = {
      curve(
        stroke: (paint: rgb(220, 130, 125, alpha), thickness: thick),
        curve.move((dx + -30pt, dy + 320pt)),
        curve.cubic(
          (dx + 90pt, dy + 250pt),
          (dx + 180pt, dy + 130pt),
          (dx + 220pt, dy + -30pt),
        ),
      )
    }
    #ribbon_left(-55pt, 60pt, 5%, 3.5pt)
    #ribbon_left(-40pt, 75pt, 8%, 3.5pt)
    #ribbon_left(-25pt, 90pt, 12%, 3.5pt)
    #ribbon_left(-10pt, 105pt, 16%, 3.5pt)
    #ribbon_left(5pt, 120pt, 14%, 3.5pt)
    #ribbon_left(20pt, 135pt, 9%, 3.5pt)
    #ribbon_left(35pt, 150pt, 5%, 3.5pt)
  ]

  #place(bottom + right)[
    #let ribbon_right(dx, dy, alpha, thick) = {
      curve(
        stroke: (paint: rgb(220, 130, 125, alpha), thickness: thick),
        curve.move((dx + 40pt, dy + 40pt)),
        curve.cubic(
          (dx - 70pt, dy - 140pt),
          (dx - 140pt, dy - 290pt),
          (dx - 160pt, dy - 440pt),
        ),
      )
    }
    #ribbon_right(-15pt, 15pt, 5%, 4pt)
    #ribbon_right(0pt, 0pt, 8%, 4pt)
    #ribbon_right(15pt, -15pt, 12%, 4pt)
    #ribbon_right(30pt, -30pt, 17%, 4pt)
    #ribbon_right(45pt, -45pt, 14%, 4pt)
    #ribbon_right(60pt, -60pt, 9%, 4pt)
    #ribbon_right(75pt, -75pt, 5%, 4pt)
  ]

  // 2. Logo Resmi Nasional Kanan Atas (SE 2026, BerAKHLAK, Bangga Melayani Bangsa)
  #place(top + right, dx: -1.2cm, dy: 1.2cm)[
    #image("/kegiatan/kecamatan-dalam-angka/2026/assets/backcover_top_logos.png", width: 3.35cm)
  ]

  // 3. Tipografi Utama di Tengah: SEJAJAR DAN SAMA PANJANG DENGAN PRESISI
  // Lebar blok utama: 11.0cm (ujung kiri dan kanan sejajar vertikal)
  #let block_w = 11.0cm

  #place(center + horizon)[
    #align(center)[
      #box(width: block_w)[
        #stack(
          dir: ttb,
          spacing: 11pt,

          // Baris 1: DATA - Huruf D di paling kiri, huruf A di paling kanan
          grid(
            columns: (auto, 1fr, auto, 1fr, auto, 1fr, auto),
            align: (left + bottom, horizon, center + bottom, horizon, center + bottom, horizon, right + bottom),
            text(font: ("Metropolis", "Liberation Sans", "Arial"), size: 78pt, weight: "black", fill: white)[D],
            [],
            text(font: ("Metropolis", "Liberation Sans", "Arial"), size: 78pt, weight: "black", fill: white)[A],
            [],
            text(font: ("Metropolis", "Liberation Sans", "Arial"), size: 78pt, weight: "black", fill: white)[T],
            [],
            text(font: ("Metropolis", "Liberation Sans", "Arial"), size: 78pt, weight: "black", fill: white)[A],
          ),

          // Baris 2: MENCERDASKAN BANGSA - Lebar tepat sama 11.0cm (rata kiri ke kanan)
          text(
            font: ("Liberation Sans", "Arial"),
            stretch: 80%,
            size: 16.5pt,
            weight: "bold",
            fill: white,
            tracking: 0.32em,
          )[MENCERDASKAN#box(width: 0.8em)[]BANGSA],

          v(2pt),

          // Baris 3: Enlighten The Nation - Garis kiri dan kanan membentang pas sampai batas tepi 11.0cm
          grid(
            columns: (1fr, auto, 1fr),
            gutter: 10pt,
            align: horizon,
            line(length: 100%, stroke: 0.9pt + white),
            text(
              font: ("Liberation Serif", "Times New Roman"),
              size: 13pt,
              style: "italic",
              fill: white,
            )[Enlighten The Nation],
            line(length: 100%, stroke: 0.9pt + white),
          ),
        )
      ]
    ]
  ]

  // 4. Identitas Resmi BPS Kabupaten Mempawah (Kiri Bawah)
  #place(bottom + left, dx: 0.9cm, dy: -1.0cm)[
    #grid(
      columns: (auto, auto),
      gutter: 10pt,
      align: horizon,
      image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", width: 1.55cm),
      [
        #set text(font: ("Metropolis", "Liberation Sans", "Arial"), fill: white)
        #text(size: 7.5pt, weight: "bold", style: "italic")[BADAN PUSAT STATISTIK\ KABUPATEN MEMPAWAH]\
        #v(2.5pt)
        #block[
          #set par(leading: 0.44em)
          #text(size: 5.5pt)[
            Jl. Raden Kusno No. 1, Mempawah 79511\
            Telp (0561) 691030, Email : bps6104\@bps.go.id\
            Homepage : https://mempawahkab.bps.go.id
          ]
        ]
      ]
    )
  ]

  // 5. Barcode & Kotak ISSN Resmi (Kanan Bawah)
  #place(bottom + right, dx: -0.9cm, dy: -1.0cm)[
    #rect(
      fill: white,
      radius: 1.5pt,
      inset: (x: 8pt, top: 6pt, bottom: 5pt),
      stroke: none,
    )[
      #align(center)[
        #text(font: ("Liberation Sans", "Arial"), size: 5.8pt, weight: "bold", fill: black)[ISSN 2477-6777]
        #v(3pt)
        #image("/kegiatan/kecamatan-dalam-angka/2026/assets/backcover_barcode_clean.png", width: 1.95cm)
      ]
    ]
  ]
]
