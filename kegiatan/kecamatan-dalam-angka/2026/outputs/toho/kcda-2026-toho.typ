
#let in_frontmatter = state("in_frontmatter", true)
#let active_chapter = state("active_chapter", "")
#let active_chapter_en = state("active_chapter_en", "")
#let is_chapter_page = state("is_chapter_page", false)

// Warna Utama & Warna Running Title Resmi BPS (Pedoman KCDA)
#let main_theme_color = cmyk(0%, 20%, 90%, 0%)
#let running_title_color = cmyk(0%, 35%, 95%, 0%)

// Badge pill numbering resmi BPS Pusat (Aturan KCDA: main_theme_color, 49.2pt x 21pt)
#let page_badge(val) = box(
  fill: main_theme_color,
  radius: 10.5pt,
  width: 49.2pt,
  height: 21pt,
)[
  #align(center + horizon)[
    #text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", fill: white)[#val]
  ]
]

#show heading: it => [ #it #metadata("h") <page_marker> ]
#show table: it => [ #it #metadata("t") <page_marker> ]
#show grid: it => [ #it #metadata("g") <page_marker> ]
#show par: it => [ #it #metadata("p") <page_marker> ]
#show figure: it => [ #it #metadata("f") <page_marker> ]
#show image: it => [ #it #metadata("i") <page_marker> ]

#let normal_margins = (
  inside: 2.0cm,
  outside: 1.5cm,
  top: 2.0cm,
  bottom: 2.0cm,
)

#let page_header = context {
  let p = here().page()
  let has_c = query(selector(<page_marker>)).any(m => {
    let pos = m.location().position()
    pos.page == p and pos.y > 1.4cm and pos.y < 19.4cm
  })
  if has_c and not in_frontmatter.get() {
    let page_num = counter(page).get().first()
    let titles = query(selector(<chapter_title>)).filter(m => m.location().page() <= p)
    let chapter_title = if titles.len() > 0 { titles.last().value } else { "" }
    if calc.even(page_num) {
      // Halaman Genap (Verso/Kiri): Judul Publikasi Bahasa Indonesia
      align(left, text(8pt, font: ("Metropolis", "Liberation Sans"), fill: running_title_color, weight: "bold")[KECAMATAN TOHO DALAM ANGKA 2026])
    } else {
      // Halaman Ganjil (Rekto/Kanan): Judul Bab Bahasa Indonesia
      let right_text = if chapter_title != "" { chapter_title } else { "BPS KABUPATEN MEMPAWAH" }
      align(right, text(8pt, font: ("Metropolis", "Liberation Sans"), fill: running_title_color, weight: "bold")[#right_text])
    }
  }
}

#let page_footer = context {
  let p = here().page()
  let has_c = query(selector(<page_marker>)).any(m => {
    let pos = m.location().position()
    pos.page == p and pos.y > 1.4cm and pos.y < 19.4cm
  })
  if not has_c {
    none
  } else if in_frontmatter.get() {
    let page_num = counter(page).get().first()
    if page_num >= 5 {
      let display_val = counter(page).display("i")
      if calc.even(page_num) {
        align(left + top, text(7.5pt, font: ("Myriad Pro", "Liberation Sans"), fill: rgb("#4B5563"), weight: "bold")[#v(3pt) #display_val])
      } else {
        align(right + top, text(7.5pt, font: ("Myriad Pro", "Liberation Sans"), fill: rgb("#4B5563"), weight: "bold")[#v(3pt) #display_val])
      }
    }
  } else {
    let page_num = counter(page).get().first()
    let display_val = counter(page).display("1")
    let titles_en = query(selector(<chapter_title_en>)).filter(m => m.location().page() <= p)
    let chapter_en = if titles_en.len() > 0 { titles_en.last().value } else { "" }
    if calc.even(page_num) {
      grid(
        columns: (auto, auto),
        align: horizon,
        column-gutter: 8pt,
        page_badge(display_val),
        text(8pt, font: ("Metropolis", "Liberation Sans"), style: "italic", fill: running_title_color)[TOHO DISTRICT IN FIGURES 2026]
      )
    } else {
      let right_en_text = if chapter_en != "" { upper(chapter_en) } else { "TOHO DISTRICT IN FIGURES 2026" }
      grid(
        columns: (1fr, auto),
        align: horizon,
        column-gutter: 8pt,
        align(right, text(8pt, font: ("Metropolis", "Liberation Sans"), style: "italic", fill: running_title_color)[#right_en_text]),
        page_badge(display_val)
      )
    }
  }
}

#set page(
  paper: "a5",
  margin: normal_margins,
  header-ascent: 40%,
  footer-descent: 20%,
  header: page_header,
  footer: page_footer,
)

#set text(font: ("Myriad Pro", "Liberation Sans"), size: 7.5pt, lang: "id")
#set par(justify: true, leading: 0.5em)

#show table.cell: set par(justify: false)
#show figure.where(kind: image): set figure(supplement: none)
#show figure.where(kind: image): set figure.caption(separator: none)

// ==========================================
// 1. KOVER DEPAN (FRONT COVER) - DESAIN RESMI TERBARU
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/assets/covers/depan/Toho1.jpg", width: 100%, height: 100%)
]

// ==========================================
// HALAMAN KOSONG DI BALIK KOVER DEPAN (INSIDE COVER / FLYLEAF)
// Sesuai Pedoman Pembuatan Publikasi BPS 2023 Subbab 4.1.2 Poin 6 (Hal. 45) & Terbitan Statistik Indonesia BPS RI.
// Halaman setelah kover depan tidak dihitung sebagai halaman dan tidak diberi nomor halaman.
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[ ]

// ==========================================
// 2. HALAMAN JUDUL UTAMA / TITLE PAGE (HALAMAN i)
// Terletak pada halaman ganjil (rekto/kanan) sesuai Pedoman Publikasi BPS 2023 Subbab 4.3.1 (Hal. 75).
// Perhitungan angka romawi resmi dimulai pada Halaman Judul Utama (halaman i).
// ==========================================
#counter(page).update(1)

#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/assets/covers/depan/Toho2.jpg", width: 100%, height: 100%)
]

// ==========================================
// 3. HALAMAN KATALOG & HAK CIPTA (HALAMAN ii)
// ==========================================

// Judul Publikasi Langsung di Bagian Atas (Hitam)
#text(10.5pt, weight: "bold", fill: black)[KECAMATAN TOHO DALAM ANGKA 2026] \
#v(1pt)
#text(9pt, style: "italic", fill: black)[TOHO DISTRICT IN FIGURES 2026] \
#v(2pt)
#text(7.5pt, fill: black)[Volume 17, 2026]

#let total_frontmatter_pages = context {
  let elems = query(<transisi_isi>)
  if elems.len() > 0 {
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    let final_p = if calc.odd(p) { p + 1 } else { p }
    numbering("i", final_p)
  } else {
    "xii"
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

#v(9pt)
#text(7.5pt)[
  #text(weight: "bold")[Katalog/Catalogue:] 1102001.6104070 \
  #v(2pt)
  #text(weight: "bold")[ISSN:] 3064-5476 \
  #v(2pt)
  #text(weight: "bold")[Nomor Publikasi/Publication Number:] 61040.26006
]

#v(7pt)
#text(7.5pt)[
  #text(weight: "bold")[Ukuran Buku/Book Size:] 14,8 cm x 21,0 cm \
  #v(2pt)
  #text(weight: "bold")[Jumlah Halaman/Number of Pages:] #total_frontmatter_pages \+ #total_arabic_pages Halaman/Pages
]

#v(7pt)
#text(7.5pt)[
  #text(weight: "bold")[Penyusun Naskah/Manuscript Drafter:] \
  #text(weight: "bold")[BPS Kabupaten Mempawah] \
  #text(style: "italic")[BPS-Statistics of Mempawah Regency]
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Penyunting/Editor:] \
  #text(weight: "bold")[BPS Kabupaten Mempawah] \
  #text(style: "italic")[BPS-Statistics of Mempawah Regency]
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Pembuat Kover/Cover Designer:] \
  #text(weight: "bold")[BPS Kabupaten Mempawah] \
  #text(style: "italic")[BPS-Statistics of Mempawah Regency]
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Sumber Ilustrasi/Illustration Source:] \
  Canva.com
]

#v(5pt)
#text(7.5pt)[
  #text(weight: "bold")[Penerbit/Publisher:] \
  #text(weight: "bold")[© Badan Pusat Statistik Kabupaten Mempawah/]#text(style: "italic")[BPS-Statistics of Mempawah Regency]
]

#v(1fr)

#text(6.8pt)[
  #text(weight: "bold")[Dilarang mereproduksi dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari Badan Pusat Statistik] \
  #v(2pt)
  #text(style: "italic")[It is prohibited to reproduce and/or duplicate part or all of this book for commercial purpose without permission from BPS-Statistics Indonesia]
]

#pagebreak()

// ==========================================
// 4. TIM PENYUSUN / COMPILERS (HALAMAN iii)
// ==========================================
#align(right)[
  #text(8pt)[ISSN 3064-5476]
]
#v(0.6cm)

#align(center)[
  #text(10.5pt, weight: "bold")[TIM PENYUSUN/_COMPILERS_] \
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan Toho Dalam Angka 2026] \
  #text(8pt, style: "italic")[Toho District in Figures 2026] \
  #text(7.5pt)[Volume 17, 2026]
  
  #v(16pt)
  #text(8.5pt, weight: "bold")[Pengarah/_Director_] \
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penanggung Jawab/_Persons in Charge_] \
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penyunting/_Editors_] \
  #text(8pt)[Ihza Fikri Zaki Karunia]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Pengolah Data dan Penulis Naskah/_Data Processor and Writers_] \
  #text(8pt)[Sukma Andini]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penata Letak/_Layouters_] \
  #text(8pt)[Akma Batrisyia Jazima]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penerjemah/_Translators_] \
  #text(8pt)[Sukma Andini]
]

#pagebreak()

// ==========================================
// 5. KONTRIBUTOR DATA / DATA CONTRIBUTORS (HALAMAN iv)
// ==========================================
#v(0.6cm)
#align(center)[
  #text(10.5pt, weight: "bold")[KONTRIBUTOR DATA/_DATA CONTRIBUTORS_] \
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan Toho Dalam Angka 2026] \
  #text(8pt, style: "italic")[Toho District in Figures 2026] \
  #text(7.5pt)[Volume 17, 2026]
]
#v(16pt)

#align(center)[
  #block(width: 88%)[
    #set align(left)
    #set text(8pt)
    1. Kementerian Agama/#text(style: "italic")[Ministry of Religious Affair]
    #v(4pt)
    2. Kementerian Pendidikan dan Kebudayaan/#text(style: "italic")[Ministry of Education and Culture]
    #v(4pt)
    3. Badan Pusat Statistik/#text(style: "italic")[BPS–Statistics Indonesia]
    #v(4pt)
    4. Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency]
    #v(4pt)
    5. Badan Perencanaan Pembangunan, Riset dan Inovasi Daerah Kabupaten Mempawah/#text(style: "italic")[Regional Development, Research and Innovation Agency of Mempawah Regency]
    #v(4pt)
    6. Kantor Kecamatan Toho/#text(style: "italic")[Toho District Office]
  ]
]

// ------------------------------------------
// KATA PENGANTAR (kata_pengantar)
// ------------------------------------------
#pagebreak()
#metadata("kata_pengantar") <kata_pengantar>

#block(width: 100%)[
  #text(11pt, weight: "bold", fill: rgb("#1F2937"))[KATA PENGANTAR]
  #v(3pt)
  #line(length: 4.5cm, stroke: 1.5pt + rgb("#FFA50C"))
]
#v(6pt)

#import "@preview/meander:0.2.2"

#let profile = (0.000, 0.000, 0.000, 0.598, 0.625, 0.640, 0.649, 0.654, 0.655, 0.655, 0.665, 0.664, 0.661, 0.655, 0.637, 0.628, 0.637, 0.692, 0.762, 0.820, 0.841, 0.852, 0.861, 0.868, 0.876, 0.883, 0.889, 0.896, 0.904, 0.911, 0.917, 0.925, 0.934, 0.940, 0.941, 0.919, 0.895, 0.891, 0.886, 0.879, 0.840, 0.810, 0.813, 0.816, 0.820, 0.826, 0.829, 0.831, 0.831, 0.832)

#block[
  #set text(hyphenate: false, size: 8pt)
  #set par(leading: 0.65em)
  #meander.reflow({
    import meander: *

    // Kontur organik 50-slice resolusi tinggi menyerupai Adobe InDesign
    placed(
      bottom + left,
      dx: -3.2cm,
      boundary: contour.horiz(div: 50, frac => {
        let idx = calc.min(49, calc.max(0, calc.floor(frac * 50)))
        let bound = profile.at(idx)
        if bound == 0.0 {
          (0.0, 0.0)
        } else {
          (0.0, bound)
        }
      }),
      box(
        width: 10.68cm,
        height: 12.5cm,
        image("/assets/kepala_bps.png", width: 100%, height: 100%)
      )
    )

    container()
    content[
      #text(fill: rgb("#EA580C"), weight: "bold")[Publikasi Kecamatan Toho Dalam Angka 2026] merupakan seri publikasi tahunan BPS Kabupaten Mempawah yang menyajikan beragam data statistik sektoral bersumber dari instansi pemerintah daerah, kantor camat, desa/kelurahan, serta survei dan sensus BPS. Publikasi ini memuat gambaran umum mengenai geografi, pemerintahan, serta perkembangan kondisi sosial-demografi dan perekonomian di wilayah Kecamatan Toho secara menyeluruh.

      #v(3.5pt)
      Data yang disajikan diharapkan dapat menjadi rujukan empiris dan indikator penting dalam mendukung perencanaan, pemantauan, serta evaluasi kebijakan pembangunan daerah demi terwujudnya Satu Data Indonesia. Seiring dinamika pembangunan dan kebutuhan data berkualitas, publikasi ini terus disempurnakan baik sistematika penyajian maupun visualisasinya.

      #v(3.5pt)
      Ucapan terima kasih dan penghargaan setinggi-tingginya kami sampaikan kepada Camat Toho, para Kepala Desa dan Lurah se-Kecamatan Toho, serta pimpinan Organisasi Perangkat Daerah atas koordinasi dan kontribusi data yang diberikan sehingga penyusunan publikasi ini selesai tepat waktu.

      #v(3.5pt)
      Kami menyadari publikasi ini masih memiliki ruang penyempurnaan. Oleh karena itu, saran dan masukan konstruktif sangat kami harapkan guna perbaikan edisi mendatang. Semoga publikasi ini memberikan manfaat nyata bagi seluruh pemangku kepentingan.

      #v(6pt)
      #align(right)[
        #block(width: 4.8cm)[
          #set align(left)
          Mempawah, September 2026 \
          Kepala BPS Kabupaten Mempawah \
          #v(3pt)
          #image("/assets/ttd_kepala_bps.png", height: 26pt) \
          #v(2pt)
          *MUNAWIR*
        ]
      ]
      #metadata("p") <page_marker>
    ]
  })
]
// ------------------------------------------
// PREFACE (preface)
// ------------------------------------------
#pagebreak()
#metadata("preface") <preface>

#block(width: 100%)[
  #text(11pt, weight: "bold", style: "italic", fill: rgb("#1F2937"))[PREFACE]
  #v(3pt)
  #line(length: 4.5cm, stroke: 1.5pt + rgb("#FFA50C"))
]
#v(6pt)

#import "@preview/meander:0.2.2"

#let profile = (0.000, 0.000, 0.000, 0.598, 0.625, 0.640, 0.649, 0.654, 0.655, 0.655, 0.665, 0.664, 0.661, 0.655, 0.637, 0.628, 0.637, 0.692, 0.762, 0.820, 0.841, 0.852, 0.861, 0.868, 0.876, 0.883, 0.889, 0.896, 0.904, 0.911, 0.917, 0.925, 0.934, 0.940, 0.941, 0.919, 0.895, 0.891, 0.886, 0.879, 0.840, 0.810, 0.813, 0.816, 0.820, 0.826, 0.829, 0.831, 0.831, 0.832)

#block[
  #set text(hyphenate: false, size: 8pt)
  #set par(leading: 0.65em)
  #meander.reflow({
    import meander: *

    // Kontur organik 50-slice resolusi tinggi menyerupai Adobe InDesign
    placed(
      bottom + left,
      dx: -3.2cm,
      boundary: contour.horiz(div: 50, frac => {
        let idx = calc.min(49, calc.max(0, calc.floor(frac * 50)))
        let bound = profile.at(idx)
        if bound == 0.0 {
          (0.0, 0.0)
        } else {
          (0.0, bound)
        }
      }),
      box(
        width: 10.68cm,
        height: 12.5cm,
        image("/assets/kepala_bps.png", width: 100%, height: 100%)
      )
    )

    container()
    content[
#text(style: "italic")[
      #text(fill: rgb("#EA580C"), weight: "bold")[Toho Subdistrict in Figures 2026] is an annual publication series issued by BPS-Statistics of Mempawah Regency, presenting various sectoral statistical data sourced from regional government institutions, the subdistrict office, village administrations, as well as surveys and censuses conducted by BPS. This publication provides a comprehensive overview of geography, governance, and socio-demographic and economic development in Toho Subdistrict.

      #v(3.5pt)
      The statistical indicators presented are expected to serve as essential empirical references and benchmarks in supporting regional development planning, monitoring, and policy evaluation towards the realization of One Data Indonesia. Concurrently with regional development dynamics and the growing demand for quality statistics, continuous enhancements have been made in both presentation structure and data visualization.

      #v(3.5pt)
      We express our highest appreciation and gratitude to the Head of Toho Subdistrict (Camat), Village Heads across Toho Subdistrict, and the heads of regional government agencies for their invaluable cooperation and data contributions that enabled the timely completion of this publication.

      #v(3.5pt)
      We acknowledge that there remains room for refinement in this publication. Therefore, constructive feedback and suggestions are warmly welcomed for the improvement of future editions. May this publication provide meaningful benefits to all stakeholders and data users.

      #v(6pt)
      #align(right)[
        #block(width: 4.8cm)[
          #set align(left)
          Mempawah, September 2026 \
          Chief Statistician of Mempawah Regency \
          #v(3pt)
          #image("/assets/ttd_kepala_bps.png", height: 26pt) \
          #v(2pt)
          #text(weight: "bold", style: "normal")[MUNAWIR]
        ]
      ]

]      #metadata("p") <page_marker>
    ]
  })
]

// ==========================================
// 8. DAFTAR ISI / CONTENTS
// ==========================================
#pagebreak()
#metadata("daftar_isi") <daftar_isi>

#set text(font: "Liberation Sans", size: 7.4pt, fill: rgb("#1F2937"), hyphenate: false)
#set par(leading: 0.42em)

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

// Helper functions for Dot Leaders in DAFTAR ISI
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

#let toc_subchapter(no, id_title, en_title, page_val) = {
  grid(
    columns: (14pt, 24pt, 1fr, auto),
    column-gutter: (0pt, 4pt, 6pt),
    align: (top + left, top + left, top + left, bottom + right),
    [],
    [#no],
    [
      #id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
    [#page_val]
  )
}

#let toc_section(id_title, en_title, page_val) = {
  grid(
    columns: (1fr, auto),
    column-gutter: 6pt,
    align: (bottom + left, bottom + right),
    [#id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])],
    [#page_val]
  )
}

// Helper functions for Dot Leaders in DAFTAR TABEL
#let toc_table_chapter(no, id_title, en_title, page_val) = {
  grid(
    columns: (30pt, 1fr, auto),
    column-gutter: 6pt,
    align: (top + left, top + left, bottom + right),
    [#text(weight: "bold")[#no]],
    [#text(weight: "bold")[#upper(id_title)/#text(style: "italic")[#upper(en_title)]]],
    [#text(weight: "bold")[#page_val]]
  )
}

#let toc_table_subchapter(no, id_title, en_title, page_val) = {
  grid(
    columns: (30pt, 1fr, auto),
    column-gutter: 6pt,
    align: (top + left, top + left, bottom + right),
    [#text(weight: "bold")[#no]],
    [#text(weight: "bold")[#id_title/#text(style: "italic")[#en_title]]],
    [#text(weight: "bold")[#page_val]]
  )
}

#let toc_table_entry(no, id_title, en_title, page_val) = {
  grid(
    columns: (30pt, 1fr),
    column-gutter: 6pt,
    align: (top + left, top + left),
    [#no],
    [
      #grid(
        columns: (1fr, auto),
        column-gutter: 4pt,
        align: (bottom + left, bottom + right),
        [#id_title #box(width: 1fr, repeat[ . ])],
        [#page_val]
      )
      #v(2pt)
      #grid(
        columns: (1fr, auto),
        column-gutter: 4pt,
        align: (bottom + left, bottom + right),
        [#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])],
        [#text(style: "italic")[#page_val]]
      )
    ]
  )
}

// Helper functions for Dot Leaders in DAFTAR GAMBAR
#let toc_figure_entry(no, id_title, en_title, page_val) = {
  grid(
    columns: (26pt, 1fr),
    column-gutter: 6pt,
    align: (top + left, top + left),
    [#no],
    [
      #grid(
        columns: (1fr, auto),
        column-gutter: 4pt,
        align: (bottom + left, bottom + right),
        [#id_title #box(width: 1fr, repeat[ . ])],
        [#page_val]
      )
      #v(2pt)
      #grid(
        columns: (1fr, auto),
        column-gutter: 4pt,
        align: (bottom + left, bottom + right),
        [#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])],
        [#text(style: "italic")[#page_val]]
      )
    ]
  )
}

#align(right)[#text(8pt)[ISSN 3064-5476]]
#v(4pt)
#align(center)[
  #text(10pt, weight: "bold")[DAFTAR ISI/]#text(10pt, weight: "bold", style: "italic")[CONTENTS]

  #v(2pt)
  #text(9pt, weight: "bold")[Kecamatan Toho Dalam Angka 2026]

  #text(8.5pt, style: "italic")[Toho District in Figures 2026]

  #v(1pt)
  #text(7.5pt)[Volume 17, 2026]
]

#v(3pt)
#align(right)[
  #text(7.5pt)[halaman]   #text(7pt, style: "italic")[page]
]
#v(1.5pt)

#toc_section("Kata Pengantar", "Preface", get_page_roman(<kata_pengantar>))
#v(1.8pt)
#toc_section("Daftar Isi", "Contents", get_page_roman(<daftar_isi>))
#v(1.8pt)
#toc_section("Daftar Tabel", "List of Tables", get_page_roman(<daftar_tabel>))
#v(1.8pt)
#toc_section("Daftar Gambar", "List of Figures", get_page_roman(<daftar_gambar>))
#v(1.8pt)
#toc_section("Penjelasan Umum", "Explanatory Notes", get_page_roman(<penjelasan_umum>))

#v(4.5pt)
#toc_chapter("1", "Geografi", "Geography", get_page_arabic(<bab1>))

#v(4.5pt)
#toc_chapter("2", "Pemerintahan", "Government", get_page_arabic(<bab2>))
#v(1.5pt)
#toc_subchapter("2.1", "Wilayah Administratif", "Administrative Area", get_page_arabic(<tab_2_1_1>))
#v(1.5pt)
#toc_subchapter("2.2", "Sumber Daya Manusia", "Human Resources", get_page_arabic(<tab_2_2_1>))

#v(4.5pt)
#toc_chapter("3", "Penduduk", "Population", get_page_arabic(<bab3>))

#v(4.5pt)
#toc_chapter("4", "Sosial dan Kesejahteraan Rakyat", "Social And Welfare", get_page_arabic(<bab4>))
#v(1.5pt)
#toc_subchapter("4.1", "Pendidikan", "Education", get_page_arabic(<tab_4_1_1>))
#v(1.5pt)
#toc_subchapter("4.2", "Kesehatan", "Health", get_page_arabic(<tab_4_2_1>))
#v(1.5pt)
#toc_subchapter("4.3", "Perumahan dan Lingkungan", "Housing and Environment", get_page_arabic(<tab_4_3_1>))
#v(1.5pt)
#toc_subchapter("4.4", "Sosial Lainnya", "Religion and Other Social Affairs", get_page_arabic(<tab_4_4_1>))

#v(4.5pt)
#toc_chapter("5", "Pertanian", "Agriculture", get_page_arabic(<bab5>))

#v(4.5pt)
#toc_chapter("6", "Pariwisata, Transportasi, dan Komunikasi", "Tourism, Transportation, and Communication", get_page_arabic(<bab6>))
#v(1.5pt)
#toc_subchapter("6.1", "Pariwisata", "Tourism", get_page_arabic(<tab_6_1_1>))
#v(1.5pt)
#toc_subchapter("6.2", "Transportasi", "Transportation", get_page_arabic(<tab_6_2_1>))
#v(1.5pt)
#toc_subchapter("6.3", "Komunikasi", "Communication", get_page_arabic(<tab_6_3_1>))

#v(4.5pt)
#toc_chapter("7", "Perbankan, Koperasi, dan Perdagangan", "Banking, Cooperative, and Trade", get_page_arabic(<bab7>))

#v(4.5pt)
#toc_section("Daftar Pustaka", "Bibliography", get_page_arabic(<daftar_pustaka>))

#pagebreak()

// ==========================================
// 9. DAFTAR TABEL / LIST OF TABLES
// ==========================================
#metadata("daftar_tabel") <daftar_tabel>
#align(right)[#text(8pt)[ISSN 3064-5476]]
#v(4pt)
#align(center)[
  #text(10pt, weight: "bold")[DAFTAR TABEL/]#text(10pt, weight: "bold", style: "italic")[LIST OF TABLES]
]

#v(8pt)
#grid(
  columns: (30pt, 1fr, auto),
  column-gutter: 6pt,
  [Tabel \ #text(style: "italic")[Table]],
  [],
  [#align(right)[halaman \ #text(style: "italic")[page]]]
)
#v(6pt)

#toc_table_chapter("1", "Geografi", "Geography", get_page_arabic(<bab1>))
#v(5pt)
#toc_table_entry("1.1", "Luas Daerah Menurut Desa/Kelurahan di Kecamatan Toho, 2025", "Area by Villages/Subdistricts in Toho District, 2025", get_page_arabic(<tab_1_1>))
#v(5pt)
#toc_table_entry("1.2", "Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten/Kota Menurut Desa/Kelurahan di Kecamatan Toho (km), 2025", "Distance to District Capital and Regency Capital by Villages/Subdistricts in Toho District (km), 2025", get_page_arabic(<tab_1_2>))
#v(5pt)
#toc_table_entry("1.3", "Batas Administrasi Kecamatan Toho Menurut Arah Mata Angin, 2025", "Administrative Borders of Toho District by Cardinal Direction, 2025", get_page_arabic(<tab_1_3>))
#v(5pt)
#toc_table_entry("1.4", "Jarak Kantor Camat Toho dengan Kota dan Tempat Penting Lainnya, 2025", "Distance from Toho Subdistrict Office to Other Important Places, 2025", get_page_arabic(<tab_1_4>))

#v(7pt)
#toc_table_chapter("2", "Pemerintahan", "Government", get_page_arabic(<bab2>))
#v(4pt)
#toc_table_subchapter("2.1", "Wilayah Administratif", "Administrative Area", get_page_arabic(<tab_2_1_1>))
#v(4pt)
#toc_table_entry("2.1.1", "Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan Toho, 2025", "Number of Hamlets, Rukun Warga and Rukun Tetangga by Villages/Subdistricts in Toho District, 2025", get_page_arabic(<tab_2_1_1>))
#v(5pt)
#toc_table_entry("2.1.2", "Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan Toho, 2026", "Names of Last and Current Who Have/Still Served in Toho District, 2026", get_page_arabic(<tab_2_1_2>))
#v(5pt)
#toc_table_entry("2.1.3", "Nama-Nama Kepala Desa/Lurah di Kecamatan Toho, 2025", "Names of Village Heads in Toho District, 2025", get_page_arabic(<tab_2_1_3>))
#v(5pt)
#toc_table_entry("2.1.4", "Nama-Nama Kepala Dusun di Kecamatan Toho, 2025", "Names of Hamlet Heads in Toho District, 2025", get_page_arabic(<tab_2_1_4>))
#v(5pt)
#toc_table_entry("2.1.5", "Klasifikasi Desa/Kelurahan Perdesaan dan Perkotaan di Kecamatan Toho, 2024", "Urban and Rural Classification of Village/Subdistrict in Toho District, 2024", get_page_arabic(<tab_2_1_5>))
#v(5pt)
#toc_table_entry("2.1.6", "Status Desa Berdasarkan Indeks Desa Membangun (IDM) di Kecamatan Toho, 2024", "Village Status Based on Developing Village Index (IDM) in Toho District, 2024", get_page_arabic(<tab_2_1_6>))

#v(6pt)
#toc_table_subchapter("2.2", "Sumber Daya Manusia", "Human Resources", get_page_arabic(<tab_2_2_1>))
#v(4pt)
#toc_table_entry("2.2.1", "Jumlah Pegawai Negeri Sipil Menurut Pemerintah Daerah dan Jenis Kelamin di Kecamatan Toho, 2025", "Number of Government Employee by Local Government and Sex in Toho District, 2025", get_page_arabic(<tab_2_2_1>))
#v(5pt)
#toc_table_entry("2.2.2", "Jumlah Pegawai Negeri Sipil Pemerintah Kecamatan Toho Menurut Tingkat Pendidikan dan Jenis Kelamin, 2025", "Number of Government Employee of Toho District Government by Educational Level and Sex, 2025", get_page_arabic(<tab_2_2_2>))

#v(7pt)
#toc_table_chapter("3", "Penduduk", "Population", get_page_arabic(<bab3>))
#v(5pt)
#toc_table_entry("3.1", "Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Desa/Kelurahan di Kecamatan Toho, 2025", "Population, Percentage Distribution of Population, Population Density, and Population Sex Ratio by Villages/Subdistricts in Toho District, 2025", get_page_arabic(<tab_3_1>))

#v(7pt)
#toc_table_chapter("4", "Sosial dan Kesejahteraan Rakyat", "Social and Welfare", get_page_arabic(<bab4>))
#v(4pt)
#toc_table_subchapter("4.1", "Pendidikan", "Education", get_page_arabic(<tab_4_1_1>))
#v(4pt)
#toc_table_entry("4.1.1", "Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan Toho, 2023–2025", "Number of Villages/Subdistricts Having Educational Facilities by Educational Level in Toho District, 2023–2025", get_page_arabic(<tab_4_1_1>))
#v(5pt)
#toc_table_entry("4.1.2", "Jumlah Satuan Pendidikan Menurut Tingkat Pendidikan di Kecamatan Toho, 2024/2025 dan 2025/2026", "Number of Schools by Educational Level in Toho District, 2024/2025 and 2025/2026", get_page_arabic(<tab_4_1_2>))
#v(5pt)
#toc_table_entry("4.1.3", "Jumlah Kepala Sekolah dan Pendidik Menurut Tingkat Pendidikan di Kecamatan Toho, 2024/2025 dan 2025/2026", "Number of Headmasters and Teachers by Educational Level in Toho District, 2024/2025 and 2025/2026", get_page_arabic(<tab_4_1_3>))
#v(5pt)
#toc_table_entry("4.1.4", "Jumlah Peserta Didik Menurut Tingkat Pendidikan di Kecamatan Toho, 2024/2025 dan 2025/2026", "Number of Pupils by Educational Level in Toho District, 2024/2025 and 2025/2026", get_page_arabic(<tab_4_1_4>))

#v(6pt)
#toc_table_subchapter("4.2", "Kesehatan", "Health", get_page_arabic(<tab_4_2_1>))
#v(4pt)
#toc_table_entry("4.2.1", "Banyaknya Desa/Kelurahan yang Memiliki Sarana Kesehatan Menurut Jenis Sarana Kesehatan di Kecamatan Toho, 2023–2025", "Number of Villages/Subdistricts Health Facilities by Type of Health Facilities in Toho District, 2023–2025", get_page_arabic(<tab_4_2_1>))

#v(6pt)
#toc_table_subchapter("4.3", "Perumahan dan Lingkungan", "Housing and Environment", get_page_arabic(<tab_4_3_1>))
#v(4pt)
#toc_table_entry("4.3.1", "Banyaknya Desa/Kelurahan Menurut Sumber Penerangan Jalan Utama Desa/Kelurahan di Kecamatan Toho, 2023–2025", "Number of Villages/Subdistricts by Source of Main Street Illumination in Toho District, 2023–2025", get_page_arabic(<tab_4_3_1>))
#v(5pt)
#toc_table_entry("4.3.2", "Banyaknya Desa/Kelurahan Menurut Jenis Bahan Bakar untuk Memasak yang Digunakan Sebagian Besar Keluarga di Kecamatan Toho, 2025", "Number of Villages/Subdistricts by Type of Cooking Fuel Used by Majority Family in Toho District, 2025", get_page_arabic(<tab_4_3_2>))

#v(6pt)
#toc_table_subchapter("4.4", "Sosial Lainnya", "Religion and Other Social Affairs", get_page_arabic(<tab_4_4_1>))
#v(4pt)
#toc_table_entry("4.4.1", "Banyaknya Desa/Kelurahan yang Mengalami Kejadian Bencana Alam Menurut Jenis Bencana Alam di Kecamatan Toho, 2025", "Number of Villages/Subdistricts with Natural Disaster Events by Type of Natural Disaster in Toho District, 2025", get_page_arabic(<tab_4_4_1>))
#v(5pt)
#toc_table_entry("4.4.2", "Banyaknya Desa/Kelurahan dengan Keberadaan Fasilitas/Upaya Antisipasi/Mitigasi Bencana Alam Menurut Jenis Fasilitas/Upaya Antisipasi/Mitigasi di Kecamatan Toho, 2025", "Number of Villages/Subdistricts with Availability of Facilities/Efforts for Anticipation/Mitigation of Natural Disasters by Type of Facilities/Efforts for Anticipation/Mitigation in Toho District, 2025", get_page_arabic(<tab_4_4_2>))

#v(7pt)
#toc_table_chapter("5", "Pertanian", "Agriculture", get_page_arabic(<bab5>))
#v(5pt)
#toc_table_entry("5.1", "Luas Panen Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Toho (ha), 2022–2025", "Harvested Area of Temporary Vegetables and Fruit Crops by Type of Crops in Toho District (ha), 2022–2025", get_page_arabic(<tab_5_1>))
#v(5pt)
#toc_table_entry("5.2", "Produksi Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Toho (kuintal), 2022–2025", "Production of Temporary Vegetables and Fruit Crops by Type of Crops in Toho District (quintal), 2022–2025", get_page_arabic(<tab_5_2>))
#v(5pt)
#toc_table_entry("5.3", "Luas Panen Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Toho (m2), 2022–2025", "Harvested Area of Medicinal Crops by Type of Crops in Toho District (m2), 2022–2025", get_page_arabic(<tab_5_3>))
#v(5pt)
#toc_table_entry("5.4", "Produksi Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Toho (kg), 2022–2025", "Production of Medicinal Crops by Type of Crops in Toho District (kg), 2022–2025", get_page_arabic(<tab_5_4>))
#v(5pt)
#toc_table_entry("5.5", "Luas Panen Tanaman Hias Menurut Jenis Tanaman di Kecamatan Toho (m2), 2022–2025", "Harvested Area of Ornamental Crops by Type of Crops in Toho District (m2), 2022–2025", get_page_arabic(<tab_5_5>))
#v(5pt)
#toc_table_entry("5.6", "Produksi Tanaman Hias Menurut Jenis Tanaman di Kecamatan Toho (tangkai), 2022–2025", "Production of Ornamental Crops by Type of Crops in Toho District (stalks), 2022–2025", get_page_arabic(<tab_5_6>))
#v(5pt)
#toc_table_entry("5.7", "Produksi Buah-buahan dan Sayuran Tahunan Menurut Jenis Tanaman di Kecamatan Toho (kuintal), 2022–2025", "Production of Permanent Fruit and Vegetable by Type of Crops (quintal), 2022–2025", get_page_arabic(<tab_5_7>))

#v(7pt)
#toc_table_chapter("6", "Pariwisata, Transportasi, dan Komunikasi", "Tourism, Transportation, and Communication", get_page_arabic(<bab6>))
#v(4pt)
#toc_table_subchapter("6.1", "Pariwisata", "Tourism", get_page_arabic(<tab_6_1_1>))
#v(4pt)
#toc_table_entry("6.1.1", "Banyaknya Desa/Kelurahan dengan Keberadaan Sarana Akomodasi Menurut Jenis Akomodasi di Kecamatan Toho, 2025", "Number of Villages/Subdistricts with Availability of Accommodation Facilities by Type of Accommodation in Toho District, 2025", get_page_arabic(<tab_6_1_1>))
#v(6pt)
#toc_table_subchapter("6.2", "Transportasi", "Transportation", get_page_arabic(<tab_6_2_1>))
#v(4pt)
#toc_table_entry("6.2.1", "Banyaknya Desa/Kelurahan Menurut Prasarana dan Sarana Transportasi Antardesa/Kelurahan di Kecamatan Toho, 2025", "Number of Villages/Subdistricts by Inter-Village/ Subdistricts Transportation Infrastructure and Facilities in Toho District, 2025", get_page_arabic(<tab_6_2_1>))
#v(6pt)
#toc_table_subchapter("6.3", "Komunikasi", "Communication", get_page_arabic(<tab_6_3_1>))
#v(4pt)
#toc_table_entry("6.3.1", "Banyaknya Desa/Kelurahan Menurut Keberadaan Kantor Pos/Pos Pembantu/Rumah Pos, Pos Keliling, dan Perusahaan/Agen Jasa Ekspedisi Swasta di Kecamatan Toho, 2025", "Number of Villages/Subdistricts with Postal and Expedition Services in Toho District, 2025", get_page_arabic(<tab_6_3_1>))

#v(7pt)
#toc_table_chapter("7", "Perbankan, Koperasi, dan Perdagangan", "Banking, Cooperative, and Trade", get_page_arabic(<bab7>))
#v(5pt)
#toc_table_entry("7.1", "Banyaknya Desa/Kelurahan dengan Keberadaan Sarana Lembaga Keuangan Bank Menurut Jenis Bank di Kecamatan Toho, 2025", "Number of Villages/Subdistricts with Availability of Bank by Type of Bank in Toho District, 2025", get_page_arabic(<tab_7_1>))
#v(5pt)
#toc_table_entry("7.2", "Banyaknya Desa/Kelurahan dengan Keberadaan Koperasi Aktif Menurut Jenis Koperasi di Kecamatan Toho, 2025", "Number of Villages/Subdistricts with Availability of Cooperative by Type of Cooperative in Toho District, 2025", get_page_arabic(<tab_7_2>))
#v(5pt)
#toc_table_entry("7.3", "Banyaknya Desa/Kelurahan dengan Keberadaan Sarana Perdagangan Menurut Jenis Sarana Perdagangan di Kecamatan Toho, 2025", "Number of Villages/Subdistricts with Availability of Trade Facilities by Type of Trade Facilities in Toho District, 2025", get_page_arabic(<tab_7_3>))

#pagebreak()

// ==========================================
// 10. DAFTAR GAMBAR / LIST OF FIGURES
// ==========================================
#metadata("daftar_gambar") <daftar_gambar>
#align(right)[#text(8pt)[ISSN 3064-5476]]
#v(4pt)
#align(center)[
  #text(10pt, weight: "bold")[DAFTAR GAMBAR/]#text(10pt, weight: "bold", style: "italic")[LIST OF FIGURES]
]

#v(8pt)
#grid(
  columns: (26pt, 1fr, auto),
  column-gutter: 6pt,
  [Gambar \ #text(style: "italic")[Figure]],
  [],
  [#align(right)[halaman \ #text(style: "italic")[page]]]
)
#v(6pt)

#toc_figure_entry("1", "Peta Wilayah Kecamatan Toho, 2025", "Map of Toho District, 2025", get_page_arabic(<fig_1>))
#v(5pt)
#toc_figure_entry("2", "Jarak ke Ibukota Kecamatan Menurut Desa/Kelurahan di Kecamatan Toho (km), 2025", "Distance to District Capital by Village/Subdistrict in Toho District (km), 2025", get_page_arabic(<fig_2>))
#v(5pt)
#toc_figure_entry("3", "Jumlah Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan Toho, 2025", "Number of RT by Village in Toho District, 2025", get_page_arabic(<fig_3>))
#v(5pt)
#toc_figure_entry("4", "Jumlah Penduduk Menurut Jenis Kelamin di Kecamatan Toho, 2025", "Population by Sex in Toho District, 2025", get_page_arabic(<fig_4>))
#v(5pt)
#toc_figure_entry("5", "Produksi Tanaman Hortikultura Unggulan di Kecamatan Toho, 2025", "Production of Leading Horticulture Crops in Toho District, 2025", get_page_arabic(<fig_5>))

#pagebreak()

// ==========================================
// 11. PENJELASAN UMUM / EXPLANATORY NOTES
// ==========================================
#metadata("penjelasan_umum") <penjelasan_umum>
#align(right)[#text(8pt)[ISSN 3064-5476]]
#v(4pt)
#align(center)[
  #text(10pt, weight: "bold")[PENJELASAN UMUM/]#text(10pt, weight: "bold", style: "italic")[EXPLANATORY NOTES]
]

#v(8pt)
#text(8pt)[
Tanda-tanda, satuan-satuan, dan lain-lainnya yang digunakan dalam publikasi ini adalah sebagai berikut: \
#text(style: "italic")[Symbols, measurement units, and acronyms which are used in this publication, are as follows:]
]

#v(6pt)
#text(8.5pt, weight: "bold")[1. TANDA-TANDA/]#text(8.5pt, weight: "bold", style: "italic")[SYMBOLS]
#v(3pt)
#grid(
  columns: (34pt, auto, 1fr),
  row-gutter: 4.5pt,
  [*...*], [ : ], [Data tidak tersedia / #text(style: "italic")[Data not available]],
  [*–*], [ : ], [Tidak ada atau nol / #text(style: "italic")[Null or zero]],
  [*0*], [ : ], [Data dapat diabaikan / #text(style: "italic")[Data negligible]],
  [*,*], [ : ], [Tanda desimal / #text(style: "italic")[Decimal point]],
  [*NA*], [ : ], [Data tidak dapat ditampilkan / #text(style: "italic")[Not applicable]],
  [*e*], [ : ], [Angka perkiraan / #text(style: "italic")[Estimated figures]],
  [*x*], [ : ], [Angka sementara / #text(style: "italic")[Preliminary figures]],
  [*xx*], [ : ], [Angka sangat sementara / #text(style: "italic")[Very preliminary figures]],
  [*r*], [ : ], [Angka diperbaiki / #text(style: "italic")[Revised figures]]
)

#v(8pt)
#text(8.5pt, weight: "bold")[2. SATUAN/]#text(8.5pt, weight: "bold", style: "italic")[UNITS]
#v(3pt)
#text(7.5pt)[
barel / #text(style: "italic")[barrel] : 158,99 liter/litres = 1/6,2898 m³ \
hektar (ha) / #text(style: "italic")[hectare (ha)] : 10.000 m² \
kilometer (km) / #text(style: "italic")[kilometres (km)] : 1.000 meter/meters (m) \
knot / #text(style: "italic")[knot] : 1,8523 km/jam (km/hour) \
kuintal / #text(style: "italic")[quintal] : 100 kg \
KWh : 1.000 Watt hour \
MWh : 1.000 KWh \
liter (untuk beras) / #text(style: "italic")[litre (for rice)] : 0,80 kg \
ons / #text(style: "italic")[ounce] : 28,31 gram/grams \
ton : 1.000 kg \
#v(3pt)
Satuan lain: buah, dus, butir, helai/lembar, kaleng, batang, pulsa, ton kilometer (ton-km), jam, menit, persen (%). \
#text(style: "italic")[Other units: unit, pack, pieces, sheet, tin, pulse, ton-kilometres (ton-km), hour, minute, percent (%).] \
#v(3pt)
Perbedaan angka di belakang koma disebabkan oleh pembulatan angka. \
#text(style: "italic")[The difference in decimal numbers is caused by rounding.]
]


#metadata("transisi_isi") <transisi_isi>


// ==========================================
// BAB 1: GEOGRAFI (PEMBATAS, ULASAN & PENJELASAN TEKNIS)
// ==========================================

// ----------------------------------------------------
// BAB 1: GEOGRAFI (GEOGRAPHY)
// ----------------------------------------------------
#pagebreak()

#in_frontmatter.update(false)
#counter(page).update(1)
#set page(margin: 0pt, header: none, footer: none)
#metadata("bab1") <bab1>
#image("/assets/dividers/Bab_1.jpg", width: 100%, height: 100%)

#pagebreak()
#set page(
  margin: normal_margins,
  header: page_header,
  footer: page_footer,
)
#metadata("GEOGRAFI") <chapter_title>
#metadata("GEOGRAPHY") <chapter_title_en>

// --- HALAMAN PENJELASAN TEKNIS / TECHNICAL NOTES ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[PENJELASAN TEKNIS]]
    #v(10pt)
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Luas wilayah merujuk pada batas geografis suatu daerah yang mencakup daratan, perairan, dan ruang udara di atasnya. Luas wilayah merupakan ukuran area geografis yang mencakup semua aspek yang menjadi bagian dari suatu entitas administratif, dan penting dalam pengelolaan sumber daya serta perencanaan pembangunan di suatu daerah.],
      [2.], [Ibu kota merujuk pada kota yang menjadi pusat pemerintahan suatu negara atau daerah, di mana terdapat kantor pemerintahan, lembaga legislatif, dan institusi penting lainnya. Ibu kota berfungsi sebagai simbol kedaulatan dan identitas suatu daerah, serta pusat administrasi dan pengambilan keputusan.],
      [3.], [Batas administrasi merujuk pada garis atau daerah yang menentukan wilayah administratif suatu entitas, seperti desa, kecamatan, kabupaten, atau provinsi. Batas administrasi adalah batas wilayah yang memisahkan satu daerah otonom dengan daerah otonom lainnya.]
    )
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[TECHNICAL NOTES]]
    #v(10pt)
    #set text(style: "italic")
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [The area of the area refers to the geographical boundaries of an area that includes land, waters, and airspace on it. The area is a size of the geographical area that covers all aspects of an administrative entity, and is important in the management of resources and development planning in an area],
      [2.], [The capital refers to the city that is the center of government of a country or region, where there are government offices, legislative institutions, and other important institutions. The capital serves as a symbol of the sovereignty and identity of an area, as well as the administrative and decision–making centers.],
      [3.], [Administration Limits refer to the lines or areas that determine the administrative territory of an entity, such as villages, sub– districts, districts, or provinces. The administrative limit is the boundary of the region that separates one autonomous region from another autonomous region]
    )
  ]
)

#pagebreak()

// --- HALAMAN ULASAN / DESCRIPTION ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[ULASAN]]
    #v(10pt)
    #block[
  #text(8pt, weight: "bold")[1. #h(2pt) Letak Wilayah] \
  #v(2pt)
  Kecamatan Toho adalah salah satu kecamatan di Kabupaten Mempawah. Secara administratif, batas wilayah Kecamatan Toho adalah:\
Utara : Kec. Sadaniang\
Selatan : Kec. Anjongan\
Barat : Kec. Mempawah Timur\
Timur : Kab. Landak
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Luas Wilayah] \
  #v(2pt)
  Luas wilayah Kecamatan Toho mencapai 226,01 km². Kecamatan Toho terdiri dari 8 desa/kelurahan. Toho Ilir menjadi desa terluas di Kecamatan Toho dengan luas mencapai 72,16 km² atau sekitar 31,93 persen dari luas Kecamatan Toho. Sementara, Benuang menjadi desa dengan luas terkecil yaitu 10,16 km² atau sekitar 4,50 persen dari luas Kecamatan Toho.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[3. #h(2pt) Aksesibilitas Wilayah] \
  #v(2pt)
  Aksesibilitas antarwilayah desa ke pusat pemerintahan kecamatan cukup bervariasi. Desa dengan jarak terjauh ke ibukota kecamatan adalah Sambora dengan jarak sekitar 17,90 km, sedangkan desa terdekat adalah Pak Laheng (0,90 km). 
]
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[DESCRIPTION]]
    #v(10pt)
    #set text(style: "italic")
    #block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Area Location] \
  #v(2pt)
  Toho District is one of the districts in Mempawah Regency. Administratively, the boundaries of Toho District are:\
North : Kec. Sadaniang\
South : Kec. Anjongan\
West : Kec. Mempawah Timur\
East : Kab. Landak
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Total Area] \
  #v(2pt)
  The area of Toho District reaches 226,01 sq.km. Toho District consists of 8 villages. Toho Ilir became the largest village in Toho District with an area of 72,16 sq.km or about 31,93 percent of the area of Toho District. Meanwhile, Benuang became the smallest village with the smallest area of 10,16 sq.km or about 4,50 percent of the area of Toho District.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[3. #h(2pt) Regional Accessibility] \
  #v(2pt)
  Accessibility between villages and the district capital varies. The village with the farthest distance to the district capital is Sambora (17,90 km), while the nearest village is Pak Laheng (0,90 km). 
]
  ]
)

#pagebreak()


#metadata("fig_peta") <fig_peta>
#v(0.3cm)
#align(center)[
  #box(width: 95%, stroke: 0.5pt + rgb("#CBD5E1"), radius: 4pt)[
    #image("/assets/maps/toho.jpg", width: 100%)
  ]
]
#v(6pt)
#metadata("fig_1") <fig_1>
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
        #text(8.5pt, weight: "bold")[1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Peta Wilayah Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Map of Toho District, 2025]
  ]
)
#pagebreak()



#v(6pt)
#align(center)[
  #image("charts/gambar_2.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Toho/#text(style: "italic")[Toho District Office]]
#v(4pt)
#metadata("fig_2") <fig_2>
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
        #text(8.5pt, weight: "bold")[2]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jarak ke Ibukota Kecamatan Menurut Desa/Kelurahan di Kecamatan Toho (km), 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Distance to District Capital by Village/Subdistrict in Toho District (km), 2025]
  ]
)
#v(10pt)

#pagebreak()

// ==========================================
// TABEL DATA BAB 1 (1 HALAMAN 1 TABEL)
// ==========================================


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[1.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Luas Daerah Menurut Desa/Kelurahan di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Area by Village/Subdistrict in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (1.9fr, 1.1fr, 1.8fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], table.cell(align: center + horizon)[#strong[Luas Daerah] \ #text(6pt, weight: "bold", style: "italic")[Area (km²)]], table.cell(align: center + horizon)[#strong[Persentase terhadap Luas Kecamatan] \ #text(6pt, weight: "bold", style: "italic")[Percentage to District Area]], table.cell(align: center + horizon)[#strong[Status Batas] \ #text(6pt, weight: "bold", style: "italic")[Boundary Status]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: left + horizon)[Sambora], table.cell(align: center + horizon)[17,98], table.cell(align: center + horizon)[7,96], table.cell(align: center + horizon)[Indikatif],
  table.cell(align: left + horizon)[Benuang], table.cell(align: center + horizon)[10,16], table.cell(align: center + horizon)[4,50], table.cell(align: center + horizon)[Indikatif],
  table.cell(align: left + horizon)[Pak Utan], table.cell(align: center + horizon)[20,86], table.cell(align: center + horizon)[9,23], table.cell(align: center + horizon)[Indikatif],
  table.cell(align: left + horizon)[Sepang], table.cell(align: center + horizon)[23,19], table.cell(align: center + horizon)[10,26], table.cell(align: center + horizon)[Indikatif],
  table.cell(align: left + horizon)[Pak Laheng], table.cell(align: center + horizon)[23,38], table.cell(align: center + horizon)[10,34], table.cell(align: center + horizon)[Indikatif],
  table.cell(align: left + horizon)[Terap], table.cell(align: center + horizon)[32,67], table.cell(align: center + horizon)[14,46], table.cell(align: center + horizon)[Indikatif],
  table.cell(align: left + horizon)[Kecurit], table.cell(align: center + horizon)[25,61], table.cell(align: center + horizon)[11,33], table.cell(align: center + horizon)[Indikatif],
  table.cell(align: left + horizon)[Toho Ilir], table.cell(align: center + horizon)[72,16], table.cell(align: center + horizon)[31,93], table.cell(align: center + horizon)[Indikatif],
  table.cell(align: left + horizon)[Kecamatan Toho], table.cell(align: center + horizon)[226,01], table.cell(align: center + horizon)[100,00], table.cell(align: center + horizon)[]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[Untuk desa/kelurahan dengan status Indikatif masih perlu dilakukan pelacakan ke lapangan dan kesepakatan batas antarwilayah yang berbatasan./#text(style: "italic")[For villages/subdistricts with Indicative status, field tracking and boundary agreements between adjacent areas are still required.]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Perencanaan Pembangunan, Riset dan Inovasi Daerah Kabupaten Mempawah/#text(style: "italic")[Regional Development, Research and Innovation Agency of Mempawah Regency]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[1.2]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten/Kota Menurut Desa/Kelurahan di Kecamatan Toho (km), 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Distance to District Capital and Regency Capital by Village in Toho District (km), 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (1.8fr, 1.7fr, 1.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], table.cell(align: center + horizon)[#strong[Jarak ke Ibukota Kecamatan] \ #text(6pt, weight: "bold", style: "italic")[Distance to District Capital]], table.cell(align: center + horizon)[#strong[Jarak ke Ibukota Kabupaten/Kota] \ #text(6pt, weight: "bold", style: "italic")[Distance to Regency/Municipal Capital]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]]),
  table.cell(align: left + horizon)[Sambora], table.cell(align: center + horizon)[17,90], table.cell(align: center + horizon)[51,70],
  table.cell(align: left + horizon)[Benuang], table.cell(align: center + horizon)[15,20], table.cell(align: center + horizon)[50,10],
  table.cell(align: left + horizon)[Pak Utan], table.cell(align: center + horizon)[7,40], table.cell(align: center + horizon)[44,90],
  table.cell(align: left + horizon)[Sepang], table.cell(align: center + horizon)[7,10], table.cell(align: center + horizon)[44,50],
  table.cell(align: left + horizon)[Pak Laheng], table.cell(align: center + horizon)[0,90], table.cell(align: center + horizon)[38,80],
  table.cell(align: left + horizon)[Terap], table.cell(align: center + horizon)[4,70], table.cell(align: center + horizon)[36,70],
  table.cell(align: left + horizon)[Kecurit], table.cell(align: center + horizon)[8,10], table.cell(align: center + horizon)[33,40],
  table.cell(align: left + horizon)[Toho Ilir], table.cell(align: center + horizon)[1,90], table.cell(align: center + horizon)[39,30]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Kantor Camat Toho/#text(style: "italic")[Toho District Office]]]
)
#v(8pt)

#pagebreak()



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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[1.3]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Batas Administrasi Kecamatan Toho Menurut Arah Mata Angin, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Administrative Borders of Toho District by Cardinal Direction, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 1.8fr, 3.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[No]], table.cell(align: center + horizon)[#strong[Arah Mata Angin] \ #text(6pt, weight: "bold", style: "italic")[Wind Direction]], table.cell(align: center + horizon)[#strong[Berbatasan Dengan] \ #text(6pt, weight: "bold", style: "italic")[Bordering With]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]]),
  table.cell(align: center + horizon)[1], table.cell(align: left + horizon)[Utara/#text(style: "italic")[North]], table.cell(align: left + horizon)[Kec. Sadaniang],
  table.cell(align: center + horizon)[2], table.cell(align: left + horizon)[Selatan/#text(style: "italic")[South]], table.cell(align: left + horizon)[Kec. Anjongan],
  table.cell(align: center + horizon)[3], table.cell(align: left + horizon)[Barat/#text(style: "italic")[West]], table.cell(align: left + horizon)[Kec. Mempawah Timur],
  table.cell(align: center + horizon)[4], table.cell(align: left + horizon)[Timur/#text(style: "italic")[East]], table.cell(align: left + horizon)[Kab. Landak]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Kantor Camat Toho/#text(style: "italic")[Toho District Office]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[1.4]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Jarak Kantor Camat Toho dengan Kota dan Tempat Penting Lainnya, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Distance from Toho Subdistrict Office to Other Important Places, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 3.2fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[No]], table.cell(align: center + horizon)[#strong[Nama Kota dan Tempat Penting] \ #text(6pt, weight: "bold", style: "italic")[Other Important Places]], table.cell(align: center + horizon)[#strong[Jarak] \ #text(6pt, weight: "bold", style: "italic")[Distance (km)]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]]),
  table.cell(align: center + horizon)[1], table.cell(align: left + horizon)[Ibukota Provinsi Kalimantan Barat/#text(style: "italic")[(Kota Pontianak)]], table.cell(align: center + horizon)[82,60],
  table.cell(align: center + horizon)[2], table.cell(align: left + horizon)[Pusat Pemerintahan Kabupaten/#text(style: "italic")[Mempawah (Mempawah Hilir)]], table.cell(align: center + horizon)[35,50]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Kantor Camat Toho/#text(style: "italic")[Toho District Office]]]
)
#v(8pt)



// ==========================================
// BAB 2: PEMERINTAHAN (PEMBATAS, ULASAN & PENJELASAN TEKNIS)
// ==========================================

// ----------------------------------------------------
// BAB 2: PEMERINTAHAN (GOVERNMENT)
// ----------------------------------------------------
#pagebreak()
#set page(margin: 0pt, header: none, footer: none)
#metadata("bab2") <bab2>
#image("/assets/dividers/Bab_2.jpg", width: 100%, height: 100%)

#pagebreak()
#set page(
  margin: normal_margins,
  header: page_header,
  footer: page_footer,
)
#metadata("PEMERINTAHAN") <chapter_title>
#metadata("GOVERNMENT") <chapter_title_en>

// --- HALAMAN PENJELASAN TEKNIS / TECHNICAL NOTES ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[PENJELASAN TEKNIS]]
    #v(10pt)
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Kecamatan adalah bagian wilayah dari daerah kabupaten/kota yang dipimpin oleh Camat. Kecamatan diatur sesuai dengan ketentuan Undang-Undang Nomor 23 Tahun 2014 tentang Pemerintahan Daerah.],
      [2.], [Desa/Kelurahan adalah wilayah yang dipimpin oleh kepala desa/kepala kelurahan (lurah) yang berada di bawah koordinasi camat.],
      [3.], [Rukun Tetangga (RT) dan Rukun Warga (RW) digunakan untuk mengidentifikasi satuan lingkungan setempat. RT dan RW merupakan organisasi yang dibentuk melalui musyawarah oleh masyarakat setempat serta diakui dan dibina oleh Pemerintah untuk menjadi mitra dalam pemberdayaan masyarakat. Pembentukan RT dan RW sejalan dengan besaran jumlah penduduk di suatu wilayah.],
      [4.], [Klasifikasi Wilayah adalah golongan suatu wilayah administrasi setingkat desa/kelurahan yang ditentukan berdasarkan standar atau ciri wilayah perkotaan dan perdesaan.],
      [5.], [Indeks Desa Membangun (IDM) merupakan indeks komposit yang dibentuk dari tiga indeks, yaitu Indeks Ketahanan Sosial (IKS), Indeks Ketahanan Ekonomi (IKE), dan Indeks Ketahanan Ekologi/Lingkungan (IKL). Nilai IDM yang semakin tinggi menunjukkan kondisi desa yang semakin baik dari segi sosial, ekonomi, dan ekologi. IDM dapat menentukan status desa menjadi Desa Mandiri, Maju, Berkembang, Tertinggal, dan Sangat Tertinggal berdasarkan nilai dari indeks-indeks tersebut.],
      [6.], [Pegawai Negeri Sipil (PNS) adalah setiap warga negara Republik Indonesia yang telah memenuhi syarat yang ditentukan, diangkat oleh pejabat yang berwenang dan diserahi tugas dalam jabatan negeri, atau diserahi tugas negara lainnya, dan digaji berdasarkan peraturan perundang-undangan yang berlaku. PNS terdiri dari PNS pusat dan PNS daerah.]
    )
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[TECHNICAL NOTES]]
    #v(10pt)
    #set text(style: "italic")
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [District is part of the region of the district / city led by Camat. District is regulated in accordance with the provisions of Law No. 23 of 2014 on Regional Government.],
      [2.], [Village/Subdistrict is a region led by the village head/subdistrict head (lurah) who is under the coordination of district head.],
      [3.], [RT and RW are used to identify local environmental units. RT and RW are organisations formed through deliberation by local communities and recognized and built by the Government to become partners in community empowerment. The formation of RT and RW is in line with the size of the population in a region.],
      [4.], [Regional Classification is a group of administrative regions as high as village/subdistrict specified based on standards or characteristics of urban and rural areas.],
      [5.], [Index of Developing Village is a composite index formed from three indices, namely Social Resilience Index, Economic Resilience Index, and Ecological/Environmental.Resilience Index. The higher Index of Developing Village values indicate the better of the village in terms of social, economic, and ecological terms. Index of Developing Village can determine the status of the village to be \"Mandiri\", \"Maju\", \"Berkembang\", \"Tertinggal\" and \"Sangat Tertinggal\" Village based on the value of these indexes.],
      [6.], [Civil Service (PNS) is any citizen of the Republic of Indonesia who has qualified as specified, appointed by the authorized officials and assigned duties in state office, or assigned to other state duties, and paid under applicable legislation. The PNS consists of the central PNS and the local PNS.]
    )
  ]
)

#pagebreak()

// --- HALAMAN ULASAN / DESCRIPTION ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[ULASAN]]
    #v(10pt)
    #block[
  #text(8pt, weight: "bold")[1. #h(2pt) Kepala Daerah] \
  #v(2pt)
  Sejak awal berdirinya, Kecamatan Toho sudah banyak mengalami pergantian pemimpin. Jabatan Camat Toho pertama dijabat oleh A. Syahdansyah (1946–1950). Dalam perkembangannya, kepemimpinan kecamatan terus berlanjut hingga saat ini dijabat oleh Bennidiktus, S.IP., M.AP (Oktober 2025 - saat ini).
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Pemerintah Desa] \
  #v(2pt)
  Kecamatan Toho pada tahun 2025 terdiri dari 8 desa/kelurahan yang terbagi menjadi 21 dusun, 25 RW, dan 89 RT. Berdasarkan klasifikasi perdesaan dan perkotaan, 3 desa/kelurahan yaitu Sepang, Pak Laheng, Toho Ilir merupakan wilayah perkotaan, sedangkan 5 desa lainnya merupakan wilayah perdesaan.\
\
Berdasarkan status Indeks Desa Membangun (IDM), capaian kemandirian desa mencakup 7 desa berstatus Mandiri, 1 desa Berkembang.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[3. #h(2pt) Pegawai Negeri Sipil] \
  #v(2pt)
  Aparatur sipil negara di lingkungan Pemerintah Daerah Kecamatan Toho menjalankan fungsi pelayanan publik, koordinasi administrasi perizinan, dan fasilitasi pembangunan antardesa.
]
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[DESCRIPTION]]
    #v(10pt)
    #set text(style: "italic")
    #block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Regional Head] \
  #v(2pt)
  Since its inception, Toho District has experienced many changes in leadership. The first position of Head of Toho District was held by A. Syahdansyah (1946–1950). Over time, district leadership has continued through to the present term held by Bennidiktus, S.IP., M.AP (Oktober 2025 - saat ini).
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Village Government] \
  #v(2pt)
  Toho District in 2025 consists of 8 villages/subdistricts divided into 21 dusun, 25 RW, and 89 RT. Based on the classification of rural and urban areas, 3 village(s) (Sepang, Pak Laheng, Toho Ilir) are urban areas, while 5 other villages are rural areas.\
\
Based on the Developing Village Index (IDM), village autonomy achievements include 7 Independent Village(s), 1 Developing Village(s).
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[3. #h(2pt) Civil Service] \
  #v(2pt)
  Civil servants within the Toho District Government perform public service functions, administrative coordination, and development facilitation among villages.
]
  ]
)

#pagebreak()



#v(6pt)
#align(center)[
  #image("charts/gambar_3.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Toho/#text(style: "italic")[Toho District Office]]
#v(4pt)
#metadata("fig_3") <fig_3>
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
        #text(8.5pt, weight: "bold")[3]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of RT by Village/Subdistrict in Toho District, 2025]
  ]
)
#v(10pt)

#pagebreak()

// ==========================================
// TABEL DATA BAB 2 (1 HALAMAN 1 TABEL)
// ==========================================

#v(0.2cm)
#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold")[2.1 WILAYAH ADMINISTRATIF/]#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", style: "italic")[ADMINISTRATIVE AREA]
#v(6pt)


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[2.1.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Hamlets, Rukun Warga and Rukun Tetangga by Villages/Subdistricts in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.2fr, 0.9fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], table.cell(align: center + horizon)[#strong[Dusun] \ #text(6pt, weight: "bold", style: "italic")[Hamlet]], table.cell(align: center + horizon)[#strong[Rukun Warga] \ #text(6pt, weight: "bold", style: "italic")[(RW)]], table.cell(align: center + horizon)[#strong[Rukun Tetangga] \ #text(6pt, weight: "bold", style: "italic")[(RT)]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: left + horizon)[Sambora], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[4], table.cell(align: center + horizon)[15],
  table.cell(align: left + horizon)[Benuang], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[9],
  table.cell(align: left + horizon)[Pak Utan], table.cell(align: center + horizon)[4], table.cell(align: center + horizon)[4], table.cell(align: center + horizon)[12],
  table.cell(align: left + horizon)[Sepang], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[14],
  table.cell(align: left + horizon)[Pak Laheng], table.cell(align: center + horizon)[3], table.cell(align: center + horizon)[3], table.cell(align: center + horizon)[9],
  table.cell(align: left + horizon)[Terap], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[4], table.cell(align: center + horizon)[11],
  table.cell(align: left + horizon)[Kecurit], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[6],
  table.cell(align: left + horizon)[Toho Ilir], table.cell(align: center + horizon)[4], table.cell(align: center + horizon)[4], table.cell(align: center + horizon)[13],
  table.cell(align: left + horizon)[Kecamatan Toho], table.cell(align: center + horizon)[21], table.cell(align: center + horizon)[25], table.cell(align: center + horizon)[89]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Master SLS Badan Pusat Statistik/#text(style: "italic")[Master SLS BPS-Statistics Indonesia]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[2.1.2]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan Toho, 2026] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Names of Last and Current Who Have/Still Served in Toho District, 2026]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#set text(size: 6.8pt)
#table(
  columns: (0.6fr, 2.8fr, 1.6fr),
  inset: (x: 3.5pt, y: 2.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[No]], table.cell(align: center + horizon)[#strong[Nama Camat] \ #text(6pt, weight: "bold", style: "italic")[Name of District Head]], table.cell(align: center + horizon)[#strong[Periode Menjabat] \ #text(6pt, weight: "bold", style: "italic")[Period]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]]),
  table.cell(align: center + horizon)[1], table.cell(align: left + horizon)[A. Syahdansyah], table.cell(align: center + horizon)[1946–1950],
  table.cell(align: center + horizon)[2], table.cell(align: left + horizon)[P. Amin], table.cell(align: center + horizon)[1950–1955],
  table.cell(align: center + horizon)[3], table.cell(align: left + horizon)[Jafar A. Rahim], table.cell(align: center + horizon)[1955–1959],
  table.cell(align: center + horizon)[4], table.cell(align: left + horizon)[A. Majid Rani], table.cell(align: center + horizon)[1959–1963],
  table.cell(align: center + horizon)[5], table.cell(align: left + horizon)[P. Syahdan Sahudin], table.cell(align: center + horizon)[1963–1972],
  table.cell(align: center + horizon)[6], table.cell(align: left + horizon)[RM. Ibrani], table.cell(align: center + horizon)[1972–1979],
  table.cell(align: center + horizon)[7], table.cell(align: left + horizon)[Muas Mustafa, BA], table.cell(align: center + horizon)[1979–1983],
  table.cell(align: center + horizon)[8], table.cell(align: left + horizon)[A.Y. Leopold Dajalain], table.cell(align: center + horizon)[1983–1984],
  table.cell(align: center + horizon)[9], table.cell(align: left + horizon)[A. Habib Salim], table.cell(align: center + horizon)[1984–1987],
  table.cell(align: center + horizon)[10], table.cell(align: left + horizon)[Drs. Hermance Somah], table.cell(align: center + horizon)[1987–1989],
  table.cell(align: center + horizon)[11], table.cell(align: left + horizon)[Drs. Titus Sinyor], table.cell(align: center + horizon)[1989–1992],
  table.cell(align: center + horizon)[12], table.cell(align: left + horizon)[Drs. Hendrikus Ngadan], table.cell(align: center + horizon)[1992–1998],
  table.cell(align: center + horizon)[13], table.cell(align: left + horizon)[Marcos Lahiran, S.Sos.], table.cell(align: center + horizon)[1998–2000],
  table.cell(align: center + horizon)[14], table.cell(align: left + horizon)[Th. C. Leydianto, S.Sos.], table.cell(align: center + horizon)[2000–2006],
  table.cell(align: center + horizon)[15], table.cell(align: left + horizon)[H. Tommy As. S.H.], table.cell(align: center + horizon)[2006–2008],
  table.cell(align: center + horizon)[16], table.cell(align: left + horizon)[JH. Lumban Gaol], table.cell(align: center + horizon)[2008–2009],
  table.cell(align: center + horizon)[17], table.cell(align: left + horizon)[H. Tommy As. S.H.], table.cell(align: center + horizon)[2009–2010],
  table.cell(align: center + horizon)[18], table.cell(align: left + horizon)[JH. Lumban Gaol], table.cell(align: center + horizon)[2010–2019],
  table.cell(align: center + horizon)[19], table.cell(align: left + horizon)[H. Tommy As. S.H.], table.cell(align: center + horizon)[2019–April 2025],
  table.cell(align: center + horizon)[20], table.cell(align: left + horizon)[Bennidiktus, S.IP., M.AP], table.cell(align: center + horizon)[Oktober 2025 - saat ini]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Kantor Camat Toho/#text(style: "italic")[Toho District Office]]]
)
#v(8pt)

#pagebreak()



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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[2.1.3]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Nama-Nama Kepala Desa/Lurah di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Names of Village Heads in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 2.2fr, 2.8fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[No]], table.cell(align: center + horizon)[#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], table.cell(align: center + horizon)[#strong[Nama Kepala Desa / Lurah] \ #text(6pt, weight: "bold", style: "italic")[Name of Village Head]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]]),
  table.cell(align: center + horizon)[1], table.cell(align: left + horizon)[Sambora], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[2], table.cell(align: left + horizon)[Benuang], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[3], table.cell(align: left + horizon)[Pak Utan], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[4], table.cell(align: left + horizon)[Sepang], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[5], table.cell(align: left + horizon)[Pak Laheng], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[6], table.cell(align: left + horizon)[Terap], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[7], table.cell(align: left + horizon)[Kecurit], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[8], table.cell(align: left + horizon)[Toho Ilir], table.cell(align: center + horizon)[...]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Kantor Camat Toho/#text(style: "italic")[Toho District Office]]]
)
#v(8pt)

#pagebreak()



#metadata("tab_2_1_4") <tab_2_1_4>
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[2.1.4]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Nama-Nama Kepala Dusun di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Names of Hamlet Heads in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#set text(size: 6.8pt)
#table(
  columns: (0.6fr, 1.8fr, 1.6fr, 2.0fr),
  inset: (x: 3.5pt, y: 2.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[No]], table.cell(align: center + horizon)[#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], table.cell(align: center + horizon)[#strong[Nama Dusun] \ #text(6pt, weight: "bold", style: "italic")[Name of Hamlet]], table.cell(align: center + horizon)[#strong[Nama Kepala Dusun] \ #text(6pt, weight: "bold", style: "italic")[Name of Hamlet Head]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: center + horizon)[1], table.cell(align: left + horizon)[Sambora], table.cell(align: left + horizon)[Mekar Jaya], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[2], table.cell(align: left + horizon)[Sambora], table.cell(align: left + horizon)[Tunas Jaya], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[3], table.cell(align: left + horizon)[Benuang], table.cell(align: left + horizon)[Benuang], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[4], table.cell(align: left + horizon)[Benuang], table.cell(align: left + horizon)[Bobor], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[5], table.cell(align: left + horizon)[Pak Utan], table.cell(align: left + horizon)[I], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[6], table.cell(align: left + horizon)[Pak Utan], table.cell(align: left + horizon)[II], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[7], table.cell(align: left + horizon)[Pak Utan], table.cell(align: left + horizon)[III], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[8], table.cell(align: left + horizon)[Pak Utan], table.cell(align: left + horizon)[IV], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[9], table.cell(align: left + horizon)[Sepang], table.cell(align: left + horizon)[Sepang], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[10], table.cell(align: left + horizon)[Sepang], table.cell(align: left + horizon)[Kumpang], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[11], table.cell(align: left + horizon)[Pak Laheng], table.cell(align: left + horizon)[Pak Ona], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[12], table.cell(align: left + horizon)[Pak Laheng], table.cell(align: left + horizon)[Pak Laheng], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[13], table.cell(align: left + horizon)[Pak Laheng], table.cell(align: left + horizon)[Sekek], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[14], table.cell(align: left + horizon)[Terap], table.cell(align: left + horizon)[Terap], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[15], table.cell(align: left + horizon)[Terap], table.cell(align: left + horizon)[Balah], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[16], table.cell(align: left + horizon)[Kecurit], table.cell(align: left + horizon)[Pinang], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[17], table.cell(align: left + horizon)[Kecurit], table.cell(align: left + horizon)[Dandang], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[18], table.cell(align: left + horizon)[Toho Ilir], table.cell(align: left + horizon)[Toho Ilir], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[19], table.cell(align: left + horizon)[Toho Ilir], table.cell(align: left + horizon)[Kuala Toho], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[20], table.cell(align: left + horizon)[Toho Ilir], table.cell(align: left + horizon)[Bonsoran], table.cell(align: center + horizon)[...],
  table.cell(align: center + horizon)[21], table.cell(align: left + horizon)[Toho Ilir], table.cell(align: left + horizon)[Prompong], table.cell(align: center + horizon)[...]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Kantor Camat Toho/#text(style: "italic")[Toho District Office]]]
)
#v(8pt)

#pagebreak()


#metadata("tab_2_1_5") <tab_2_1_5>
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[2.1.5]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Klasifikasi Desa/Kelurahan Perdesaan dan Perkotaan di Kecamatan Toho, 2024] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Urban and Rural Classification of Village/Subdistrict in Toho District, 2024]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 2.2fr, 1.6fr, 1.6fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[No]], table.cell(align: center + horizon)[#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], table.cell(align: center + horizon)[#strong[Wilayah Administratif] \ #text(6pt, weight: "bold", style: "italic")[Administrative Area]], table.cell(align: center + horizon)[#strong[Klasifikasi Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Urban/Rural Classification]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: center + horizon)[1], table.cell(align: left + horizon)[Sambora], table.cell(align: center + horizon)[Desa], table.cell(align: left + horizon)[Perdesaan],
  table.cell(align: center + horizon)[2], table.cell(align: left + horizon)[Benuang], table.cell(align: center + horizon)[Desa], table.cell(align: left + horizon)[Perdesaan],
  table.cell(align: center + horizon)[3], table.cell(align: left + horizon)[Pak Utan], table.cell(align: center + horizon)[Desa], table.cell(align: left + horizon)[Perdesaan],
  table.cell(align: center + horizon)[4], table.cell(align: left + horizon)[Sepang], table.cell(align: center + horizon)[Desa], table.cell(align: left + horizon)[Perkotaan],
  table.cell(align: center + horizon)[5], table.cell(align: left + horizon)[Pak Laheng], table.cell(align: center + horizon)[Desa], table.cell(align: left + horizon)[Perkotaan],
  table.cell(align: center + horizon)[6], table.cell(align: left + horizon)[Terap], table.cell(align: center + horizon)[Desa], table.cell(align: left + horizon)[Perdesaan],
  table.cell(align: center + horizon)[7], table.cell(align: left + horizon)[Kecurit], table.cell(align: center + horizon)[Desa], table.cell(align: left + horizon)[Perdesaan],
  table.cell(align: center + horizon)[8], table.cell(align: left + horizon)[Toho Ilir], table.cell(align: center + horizon)[Desa], table.cell(align: left + horizon)[Perkotaan]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Peraturan Kepala Badan Pusat Statistik Nomor 120 Tahun 2020 Tentang Klasifikasi Desa Perkotaan dan Perdesaan di Indonesia Tahun 2020/#text(style: "italic")[Regulation of the Chief Statistician Number 120 of 2020 Concerning the Classification of Urban and Rural Villages in Indonesia in 2020]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[2.1.6]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Status Desa berdasarkan Indeks Desa Membangun di Kecamatan Toho, 2024] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Village Status Based on Developing Village Index in Toho District, 2024]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 2.5fr, 2.5fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[No]], table.cell(align: center + horizon)[#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], table.cell(align: center + horizon)[#strong[Status Indeks Desa Membangun] \ #text(6pt, weight: "bold", style: "italic")[Developing Village Index Status]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]]),
  table.cell(align: center + horizon)[1], table.cell(align: left + horizon)[Sambora], table.cell(align: center + horizon)[Mandiri],
  table.cell(align: center + horizon)[2], table.cell(align: left + horizon)[Benuang], table.cell(align: center + horizon)[Mandiri],
  table.cell(align: center + horizon)[3], table.cell(align: left + horizon)[Pak Utan], table.cell(align: center + horizon)[Berkembang],
  table.cell(align: center + horizon)[4], table.cell(align: left + horizon)[Sepang], table.cell(align: center + horizon)[Mandiri],
  table.cell(align: center + horizon)[5], table.cell(align: left + horizon)[Pak Laheng], table.cell(align: center + horizon)[Mandiri],
  table.cell(align: center + horizon)[6], table.cell(align: left + horizon)[Terap], table.cell(align: center + horizon)[Mandiri],
  table.cell(align: center + horizon)[7], table.cell(align: left + horizon)[Kecurit], table.cell(align: center + horizon)[Mandiri],
  table.cell(align: center + horizon)[8], table.cell(align: left + horizon)[Toho Ilir], table.cell(align: center + horizon)[Mandiri]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Indeks Desa Membangun (IDM) Tahun 2024 per Desa, Kementerian Desa, PDT dan Transmigrasi/#text(style: "italic")[Index of Developing Village 2024 for each Village, Ministry of Villages, Development of Disadvantaged Regions, and Transmigration]]]
)
#v(8pt)

#pagebreak()


#v(0.2cm)
#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold")[2.2 SUMBER DAYA MANUSIA/]#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", style: "italic")[HUMAN RESOURCES]
#v(6pt)


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[2.2.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Jumlah Pegawai Negeri Sipil Menurut Pemerintah Daerah dan Jenis Kelamin di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Government Employee by Local Government and Sex in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Pemerintah Daerah] \ #text(6pt, weight: "bold", style: "italic")[Local Government]], table.cell(align: center + horizon)[#strong[Laki-laki] \ #text(6pt, weight: "bold", style: "italic")[Male]], table.cell(align: center + horizon)[#strong[Perempuan] \ #text(6pt, weight: "bold", style: "italic")[Female]], table.cell(align: center + horizon)[#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: left + horizon)[Pemerintah Daerah Kecamatan Toho/#text(style: "italic")[Toho District Government]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Kantor Camat Toho/#text(style: "italic")[Toho District Office]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[2.2.2]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Jumlah Pegawai Negeri Sipil Pemerintah Daerah Kecamatan Toho Menurut Tingkat Pendidikan dan Jenis Kelamin, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Government Employee of Toho District Local Government by Educational Level and Sex, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], table.cell(align: center + horizon)[#strong[Laki-laki] \ #text(6pt, weight: "bold", style: "italic")[Male]], table.cell(align: center + horizon)[#strong[Perempuan] \ #text(6pt, weight: "bold", style: "italic")[Female]], table.cell(align: center + horizon)[#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: left + horizon)[Sekolah Dasar (SD)/#text(style: "italic")[Primary School]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[SMP/#text(style: "italic")[Sederajat Junior High School]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[SMA/#text(style: "italic")[Sederajat Senior High School]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[Diploma I/Akta I Diploma I/#text(style: "italic")[Akta I]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[Diploma II/Akta II Diploma II/#text(style: "italic")[Akta II]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[Diploma III/Akta III Diploma III/#text(style: "italic")[Akta III]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[Diploma IV/Akta IV Diploma IV/#text(style: "italic")[Akta IV]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[S1/Sarjana Under Graduate/#text(style: "italic")[Bachelor]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[S2/#text(style: "italic")[Pasca Sarjana Graduate]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[S3/Doktor/#text(style: "italic")[Ph.D Post Graduate]], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...],
  table.cell(align: left + horizon)[Jumlah], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...], table.cell(align: center + horizon)[...]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Kantor Camat Toho/#text(style: "italic")[Toho District Office]]]
)
#v(8pt)



// ==========================================
// BAB 3: PENDUDUK (PEMBATAS, ULASAN & PENJELASAN TEKNIS)
// ==========================================

// ----------------------------------------------------
// BAB 3: PENDUDUK (POPULATION)
// ----------------------------------------------------
#pagebreak()
#set page(margin: 0pt, header: none, footer: none)
#metadata("bab3") <bab3>
#image("/assets/dividers/Bab_3.jpg", width: 100%, height: 100%)

#pagebreak()
#set page(
  margin: normal_margins,
  header: page_header,
  footer: page_footer,
)
#metadata("PENDUDUK") <chapter_title>
#metadata("POPULATION") <chapter_title_en>

// --- HALAMAN PENJELASAN TEKNIS / TECHNICAL NOTES ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[PENJELASAN TEKNIS]]
    #v(10pt)
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Kepadatan penduduk adalah angka yang menyatakan banyaknya penduduk per kilometer persegi, dihitung dengan perbandingan antara banyaknya penduduk terhadap luas wilayah.],
      [2.], [Rasio jenis kelamin adalah perbandingan antara jumlah penduduk laki-laki dan jumlah penduduk perempuan pada suatu daerah dan waktu tertentu, yang biasanya dinyatakan dalam banyaknya penduduk laki-laki perseratus penduduk perempuan.]
    )
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[TECHNICAL NOTES]]
    #v(10pt)
    #set text(style: "italic")
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [The population density is a figure that states the number of residents per square kilometer, calculated by comparison between the population of the area.],
      [2.], [Sex ratio is a comparison between the number of male population and the number of female population at a given area and time, which is usually expressed in the number of male population per hundred female population.]
    )
  ]
)

#pagebreak()

// --- HALAMAN ULASAN / DESCRIPTION ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[ULASAN]]
    #v(10pt)
    #block[
  #text(8pt, weight: "bold")[1. #h(2pt) Perkembangan Penduduk dan Rasio Jenis Kelamin] \
  #v(2pt)
  Penduduk Kecamatan Toho pada tahun 2025 tercatat sebanyak 24.189 jiwa, terdiri atas 12.527 jiwa laki-laki dan 11.662 jiwa perempuan. Komposisi ini menghasilkan rasio jenis kelamin sebesar 107,42, yang mengindikasikan terdapat sekitar 107 penduduk laki-laki untuk setiap 100 penduduk perempuan di wilayah ini.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Distribusi dan Kepadatan Penduduk] \
  #v(2pt)
  Kepadatan penduduk di Kecamatan Toho mencapai rata-rata sekitar 107,03 jiwa per kilometer persegi. Penyebaran penduduk belum merata antardesa, di mana Desa Benuang memiliki kepadatan tertinggi mencapai 235,33 jiwa/km², sedangkan Desa Toho Ilir mencatat kepadatan terendah sebesar 39,88 jiwa/km².\
\
Dari sisi konsentrasi penduduk, Sepang merupakan desa dengan proporsi penduduk terbesar (15,68 persen), sementara proporsi penduduk terkecil berada di Kecurit (8,18 persen).
]
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[DESCRIPTION]]
    #v(10pt)
    #set text(style: "italic")
    #block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Population Growth and Sex Ratio] \
  #v(2pt)
  The population of Toho District in 2025 was recorded at 24.189 people, comprising 12.527 males and 11.662 females. This composition yields a sex ratio of 107,42, indicating approximately 107 males for every 100 females in this district.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Population Distribution and Density] \
  #v(2pt)
  The average population density in Toho District reaches approximately 107,03 people per square kilometer. Population distribution is not evenly distributed across villages; Benuang village has the highest density at 235,33 people/sq.km, while Toho Ilir village records the lowest at 39,88 people/sq.km.\
\
In terms of population concentration, Sepang has the largest share (15,68 percent), whereas the smallest share is found in Kecurit (8,18 percent).
]
  ]
)

#pagebreak()



#v(6pt)
#align(center)[
  #image("charts/gambar_4.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah (Semester II 2025)/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency (Semester II 2025)]]
#v(4pt)
#metadata("fig_4") <fig_4>
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
        #text(8.5pt, weight: "bold")[4]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Jumlah Penduduk Menurut Jenis Kelamin dan Desa/Kelurahan di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Population by Sex and Village/Subdistrict in Toho District, 2025]
  ]
)
#v(10pt)

#pagebreak()

// ==========================================
// TABEL DATA BAB 3 (FORMAT 2 HALAMAN)
// ==========================================


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[3.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Desa/Kelurahan di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Population, Percentage Distribution of Population, Population Density, and Population Sex Ratio by Villages/Subdistricts in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 1.1fr, 1.1fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], table.cell(align: center + horizon)[#strong[Laki-laki] \ #text(6pt, weight: "bold", style: "italic")[Male]], table.cell(align: center + horizon)[#strong[Perempuan] \ #text(6pt, weight: "bold", style: "italic")[Female]], table.cell(align: center + horizon)[#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: left + horizon)[Sambora], table.cell(align: center + horizon)[1.851], table.cell(align: center + horizon)[1.743], table.cell(align: center + horizon)[3.594],
  table.cell(align: left + horizon)[Benuang], table.cell(align: center + horizon)[1.227], table.cell(align: center + horizon)[1.164], table.cell(align: center + horizon)[2.391],
  table.cell(align: left + horizon)[Pak Utan], table.cell(align: center + horizon)[1.883], table.cell(align: center + horizon)[1.703], table.cell(align: center + horizon)[3.586],
  table.cell(align: left + horizon)[Sepang], table.cell(align: center + horizon)[1.988], table.cell(align: center + horizon)[1.806], table.cell(align: center + horizon)[3.794],
  table.cell(align: left + horizon)[Pak Laheng], table.cell(align: center + horizon)[1.358], table.cell(align: center + horizon)[1.289], table.cell(align: center + horizon)[2.647],
  table.cell(align: left + horizon)[Terap], table.cell(align: center + horizon)[1.715], table.cell(align: center + horizon)[1.606], table.cell(align: center + horizon)[3.321],
  table.cell(align: left + horizon)[Kecurit], table.cell(align: center + horizon)[1.006], table.cell(align: center + horizon)[972], table.cell(align: center + horizon)[1.978],
  table.cell(align: left + horizon)[Toho Ilir], table.cell(align: center + horizon)[1.499], table.cell(align: center + horizon)[1.379], table.cell(align: center + horizon)[2.878],
  table.cell(align: left + horizon)[Kecamatan Toho], table.cell(align: center + horizon)[12.527], table.cell(align: center + horizon)[11.662], table.cell(align: center + horizon)[24.189]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency]]]
)
#v(8pt)

#pagebreak()



#metadata("tab_3_1_Lanjutan") <tab_3_1_Lanjutan>
#v(6pt)
#text(10pt, weight: "bold")[Lanjutan Tabel 3.1 / #text(style: "italic")[Continued Table 3.1]]
#v(4pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.4fr, 1.2fr, 1.2fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], table.cell(align: center + horizon)[#strong[Distribusi Penduduk] \ #text(6pt, weight: "bold", style: "italic")[Population Distribution (%)]], table.cell(align: center + horizon)[#strong[Kepadatan Penduduk (per km²)] \ #text(6pt, weight: "bold", style: "italic")[Population Density per sq.km]], table.cell(align: center + horizon)[#strong[Rasio Jenis Kelamin Penduduk] \ #text(6pt, weight: "bold", style: "italic")[Population Sex Ratio]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: left + horizon)[Sambora], table.cell(align: center + horizon)[14,86], table.cell(align: center + horizon)[199,89], table.cell(align: center + horizon)[106,20],
  table.cell(align: left + horizon)[Benuang], table.cell(align: center + horizon)[9,88], table.cell(align: center + horizon)[235,33], table.cell(align: center + horizon)[105,41],
  table.cell(align: left + horizon)[Pak Utan], table.cell(align: center + horizon)[14,82], table.cell(align: center + horizon)[171,91], table.cell(align: center + horizon)[110,57],
  table.cell(align: left + horizon)[Sepang], table.cell(align: center + horizon)[15,68], table.cell(align: center + horizon)[163,61], table.cell(align: center + horizon)[110,08],
  table.cell(align: left + horizon)[Pak Laheng], table.cell(align: center + horizon)[10,94], table.cell(align: center + horizon)[113,22], table.cell(align: center + horizon)[105,35],
  table.cell(align: left + horizon)[Terap], table.cell(align: center + horizon)[13,73], table.cell(align: center + horizon)[101,65], table.cell(align: center + horizon)[106,79],
  table.cell(align: left + horizon)[Kecurit], table.cell(align: center + horizon)[8,18], table.cell(align: center + horizon)[77,24], table.cell(align: center + horizon)[103,50],
  table.cell(align: left + horizon)[Toho Ilir], table.cell(align: center + horizon)[11,90], table.cell(align: center + horizon)[39,88], table.cell(align: center + horizon)[108,70],
  table.cell(align: left + horizon)[Kecamatan Toho], table.cell(align: center + horizon)[100,00], table.cell(align: center + horizon)[107,03], table.cell(align: center + horizon)[107,42]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency]]]
)
#v(8pt)



// ==========================================
// BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT
// ==========================================

// ----------------------------------------------------
// BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT (SOCIAL AND WELFARE)
// ----------------------------------------------------
#pagebreak()
#set page(margin: 0pt, header: none, footer: none)
#metadata("bab4") <bab4>
#image("/assets/dividers/Bab_4.jpg", width: 100%, height: 100%)

#pagebreak()
#set page(
  margin: normal_margins,
  header: page_header,
  footer: page_footer,
)
#metadata("SOSIAL DAN KESEJAHTERAAN RAKYAT") <chapter_title>
#metadata("SOCIAL AND WELFARE") <chapter_title_en>

// --- HALAMAN PENJELASAN TEKNIS / TECHNICAL NOTES ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[PENJELASAN TEKNIS]]
    #v(10pt)
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Jenjang Pendidikan Formal terdiri atas pendidikan dasar, pendidikan menengah, dan pendidikan tinggi. Jenis pendidikan yang diajarkan mencakup pendidikan umum, kejuruan, akademik, profesi, vokasi, keagamaan, dan khusus.

a. Pendidikan Dasar berbentuk Sekolah Dasar (SD) dan Madrasah Ibtidaiyah (MI) atau bentuk lain yang sederajat serta Sekolah Menengah Pertama (SMP) dan Madrasah Tsanawiyah (MTs) atau bentuk lain yang sederajat.

b. Pendidikan Menengah berbentuk Sekolah Menengah Atas (SMA), Madrasah Aliyah (MA), Sekolah Menengah Kejuruan (SMK), dan Madrasah Aliyah Kejuruan (MAK), atau bentuk lain yang sederajat.

c. Pendidikan Tinggi merupakan jenjang Pendidikan setelah pendidikan menengah yang mencakup program pendidikan diploma, sarjana, magister, spesialis, dan doktor yang diselenggarakan oleh perguruan tinggi. Perguruan tinggi dapat berbentuk akademi, politeknik, sekolah tinggi, atau institut.],
      [2.], [Rumah Sakit adalah tempat pemeriksaan dan perawatan kesehatan, biasanya berada di bawah pengawasan dokter/tenaga medis, yang melayani penderita yang sakit untuk berobat rawat jalan atau rawat inap. Undang-undang RI No. 44 Tahun 2009 tentang rumah sakit mengelompokkan rumah sakit berdasarkan jenis pelayanan yang diberikan menjadi:

Rumah Sakit Umum adalah rumah sakit yang memberikan pelayanan kesehatan pada semua bidang dan jenis penyakit.

Rumah Sakit khusus adalah rumah sakit yang memberikan pelayanan utama pada satu bidang atau satu jenis penyakit tertentu berdasarkan disiplin ilmu, golongan umur, organ, jenis penyakit, atau kekhususan lainnya.],
      [3.], [Pusat Kesehatan Masyarakat (Puskesmas) adalah unit pelaksana teknis dinas kesehatan kabupaten/kota yang mempunyai fungsi utama sebagai penyelenggara pelayanan kesehatan tingkat pertama. Wilayah kerja puskesmas maksimal adalah satu kecamatan. Untuk dapat menjangkau wilayah kerjanya, puskesmas mempunyai jaringan pelayanan yang meliputi unit Puskesmas Pembantu (Pustu), unit Puskesmas Keliling (Puskel), dan unit bidan desa/komunitas (Peraturan Menteri Kesehatan RI No. 75 Tahun 2014 tentang Pusat Kesehatan Masyarakat).]
    )
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[TECHNICAL NOTES]]
    #v(10pt)
    #set text(style: "italic")
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [The Formal Education Level consists of primary education, secondary education, and high education. The kind of education that taught consists of general education, vocational, academic, professional, religious, and specific education.

a. The Primary Education consists of Elementary School and Islamic Elementary School or other equivalent forms and Junior High School and MTs or other equivalent forms.

b. The Secondary Education consists of the senior high school, Madrasah Aliyah, Vocational School, and Vocational Madrasah Aliyah, or other equivalent forms.

c. The Tertiary Education consists of the education level after the secondary education that consists of diplomas, bachelor, master, specialist, and doctoral degrees that are held by the college. The universities can be academy, polytechnic, college, or institute.],
      [2.], [Hospital is a place for health check, usually controlled/supervised by doctors/medical personnel to serve the ill patients to get outpatient or inpatient treatment services. The law of the Republic of Indonesia Number 44 year 2009 concerning about hospital have been grouping hospital based on the type of service being given into:

General Hospital is a hospital that provides health services in all areas and types of diseases.

Special Hospital is a hospital that provides primary care in one area or one particular type of disease base on dicipline, age group, organ, type of disease, or other specificity.],
      [3.], [Public Health Center is technical implementation unit of regency health department that have the primary function as a first-level health care providers. The working area standard of public health center is one district and to reach their working areas, public health centers have a service network covering subsidiary of public health center, mobile public health center units, and midwife units (Regulation of the Minister of Health of Indonesia Number 75 Year 2014 about Public Health Center).]
    )
  ]
)

#pagebreak()

// --- HALAMAN ULASAN / DESCRIPTION ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[ULASAN]]
    #v(10pt)
    #block[
  #text(8pt, weight: "bold")[1. #h(2pt) Pendidikan] \
  #v(2pt)
  Ketersediaan fasilitas pendidikan merupakan fondasi utama dalam meningkatkan mutu sumber daya manusia. Pada tahun ajaran 2025/2026, jenjang pendidikan dasar di Kecamatan Toho didukung oleh 18 Sekolah Dasar (SD) serta 2 Madrasah Ibtidaiyah (MI). Untuk jenjang pendidikan menengah pertama, tercatat keberadaan 6 Sekolah Menengah Pertama (SMP) serta 1 Madrasah Tsanawiyah (MTs). Sementara pada jenjang pendidikan menengah atas dan kejuruan, terdapat 1 SMA guna menampung kelanjutan studi peserta didik.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Kesehatan] \
  #v(2pt)
  Ketersediaan sarana pelayanan kesehatan yang memadai merupakan kebutuhan vital masyarakat. Pada tahun 2025, fasilitas kesehatan di Kecamatan Toho mencakup 2 unit Puskesmas tanpa rawat inap. Akses masyarakat terhadap obat-obatan dan perbekalan medis juga ditunjang oleh 2 desa/kelurahan yang memiliki sarana apotek/toko obat. Keberadaan sarana ini berperan strategis dalam memelihara dan meningkatkan derajat kesehatan masyarakat di seluruh wilayah kecamatan.
]
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[DESCRIPTION]]
    #v(10pt)
    #set text(style: "italic")
    #block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Education] \
  #v(2pt)
  The availability of educational facilities is an essential foundation for enhancing human resource quality. In the 2025/2026 academic year, basic education in Toho District was supported by 18 primary schools (SD) and 2 Madrasah Ibtidaiyah (MI). At the junior secondary level, there were 6 junior high schools (SMP) and 1 Madrasah Tsanawiyah (MTs). Meanwhile, at the senior secondary and vocational level, there were 1 senior high school(s) (SMA) to accommodate continuing students.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Health] \
  #v(2pt)
  The availability of adequate health service facilities is a vital necessity for the community. In 2025, health facilities in Toho District included 2 outpatient Public Health Center(s). Public access to medicines and medical supplies is also supported by 2 village(s) with pharmacies/drugstores. These facilities play a strategic role in maintaining and enhancing public health across the district.
]
  ]
)

#pagebreak()


// ==========================================
// TABEL DATA BAB 4 (1 HALAMAN 1 TABEL)
// ==========================================

#v(0.2cm)
#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold")[4.1 PENDIDIKAN/]#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", style: "italic")[EDUCATION]
#v(6pt)


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[4.1.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan Toho, 2023–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts Having Educational Facilities by Educational Level in Toho District, 2023–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], table.cell(align: center + horizon)[#strong[2023#super[2]]], table.cell(align: center + horizon)[#strong[2024#super[3]]], table.cell(align: center + horizon)[#strong[2025#super[3]]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: left + horizon)[Taman Kanak-Kanak (TK)/Raudatul Athfal (RA)/#text(style: "italic")[Bustanul Athfal (BA) Kindergarten]], table.cell(align: center + horizon)[…], table.cell(align: center + horizon)[3], table.cell(align: center + horizon)[3],
  table.cell(align: left + horizon)[Sekolah Dasar (SD)/#text(style: "italic")[Madrasah Ibtidaiyah (MI) Primary School]], table.cell(align: center + horizon)[…], table.cell(align: center + horizon)[8], table.cell(align: center + horizon)[8],
  table.cell(align: left + horizon)[Sekolah Menengah Pertama (SMP)/#text(style: "italic")[Madrasah Tsanawiyah (MTs) Junior High School]], table.cell(align: center + horizon)[…], table.cell(align: center + horizon)[7], table.cell(align: center + horizon)[7],
  table.cell(align: left + horizon)[Sekolah Menengah Atas (SMA)/#text(style: "italic")[Madrasah Aliyah (MA) Senior High School]], table.cell(align: center + horizon)[…], table.cell(align: center + horizon)[1], table.cell(align: center + horizon)[1],
  table.cell(align: left + horizon)[Sekolah Menengah Kejuruan (SMK)/#text(style: "italic")[Vocational High School]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Akademi/Perguruan Tinggi Academy/#text(style: "italic")[University]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1] Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[#super[2] Kantor Camat Toho/#text(style: "italic")[Toho District Office] \ 
#super[3] Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS-Statistics Indonesia, Village Potential Data Collecting]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[4.1.2]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Jumlah Satuan Pendidikan Menurut Tingkat Pendidikan di Kecamatan Toho, 2024/2025 dan 2025/2026] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Schools by Educational Level in Toho District, 2024/2025 and 2025/2026]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (1.9fr, 1.0fr, 1.0fr, 1.0fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 2 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 2 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(rowspan: 2, align: center + horizon)[#strong[Tingkat Pendidikan] \ #text(6pt, style: "italic", weight: "bold")[Educational Level]],
    table.cell(colspan: 2, align: center + horizon, stroke: (bottom: 0.6pt + black))[#strong[Negeri]/#text(style: "italic", weight: "bold")[Public]],
    table.cell(colspan: 2, align: center + horizon, stroke: (bottom: 0.6pt + black))[#strong[Swasta]/#text(style: "italic", weight: "bold")[Private]],
    table.cell(colspan: 2, align: center + horizon, stroke: (bottom: 0.6pt + black))[#strong[Jumlah]/#text(style: "italic", weight: "bold")[Total]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2024/2025]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2025/2026]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2024/2025]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2025/2026]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2024/2025]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2025/2026]],
    table.cell(align: center + horizon)[#strong[(1)]],
    table.cell(align: center + horizon)[#strong[(2)]],
    table.cell(align: center + horizon)[#strong[(3)]],
    table.cell(align: center + horizon)[#strong[(4)]],
    table.cell(align: center + horizon)[#strong[(5)]],
    table.cell(align: center + horizon)[#strong[(6)]],
    table.cell(align: center + horizon)[#strong[(7)]]),
  table.cell(align: left + horizon)[Taman Kanak-Kanak (TK)#super[1]/#text(style: "italic")[Kindergarten#super[1]]], table.cell(align: center + horizon)[3], table.cell(align: center + horizon)[3], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[5], table.cell(align: center + horizon)[5],
  table.cell(align: left + horizon)[Raudatul Athfal (RA)#super[2]/#text(style: "italic")[Raudatul Athfal (RA)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Sekolah Dasar (SD)#super[1]/#text(style: "italic")[Primary School#super[1]]], table.cell(align: center + horizon)[18], table.cell(align: center + horizon)[18], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[18], table.cell(align: center + horizon)[18],
  table.cell(align: left + horizon)[Madrasah Ibtidaiyah (MI)#super[2]/#text(style: "italic")[Madrasah Ibtidaiyah (MI)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2],
  table.cell(align: left + horizon)[Sekolah Menengah Pertama (SMP)#super[1]/#text(style: "italic")[Junior High School#super[1]]], table.cell(align: center + horizon)[6], table.cell(align: center + horizon)[6], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[6], table.cell(align: center + horizon)[6],
  table.cell(align: left + horizon)[Madrasah Tsanawiyah (MTs)#super[2]/#text(style: "italic")[Madrasah Tsanawiyah (MTs)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[1], table.cell(align: center + horizon)[1], table.cell(align: center + horizon)[1], table.cell(align: center + horizon)[1],
  table.cell(align: left + horizon)[Sekolah Menengah Atas (SMA)#super[1]/#text(style: "italic")[Senior High School#super[1]]], table.cell(align: center + horizon)[1], table.cell(align: center + horizon)[1], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[1], table.cell(align: center + horizon)[1],
  table.cell(align: left + horizon)[Sekolah Menengah Kejuruan (SMK)#super[1]/#text(style: "italic")[Vocational High School#super[1]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Madrasah Aliyah (MA)#super[2]/#text(style: "italic")[Madrasah Aliyah (MA)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[#super[1] Kementerian Pendidikan Dasar dan Menengah; Sistem Data Pokok Pendidikan; data semester ganjil laporan sampai dengan 30 November/#text(style: "italic")[Ministry of Primary and Secondary Education; Sistem Data Pokok Pendidikan; odd semester report data up to 30 November] \ 
#super[2] Kementerian Agama; EMIS; data semester genap laporan sampai dengan 30 Juni/#text(style: "italic")[Ministry of Religious Affairs; EMIS; even semester report data up to 30 June]]]
)
#v(8pt)

#pagebreak()



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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[4.1.3]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Jumlah Kepala Sekolah dan Pendidik Menurut Tingkat Pendidikan di Kecamatan Toho, 2024/2025 dan 2025/2026] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Headmasters and Teachers by Educational Level in Toho District, 2024/2025 and 2025/2026]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (1.9fr, 1.0fr, 1.0fr, 1.0fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 2 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 2 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(rowspan: 2, align: center + horizon)[#strong[Tingkat Pendidikan] \ #text(6pt, style: "italic", weight: "bold")[Educational Level]],
    table.cell(colspan: 2, align: center + horizon, stroke: (bottom: 0.6pt + black))[#strong[Negeri]/#text(style: "italic", weight: "bold")[Public]],
    table.cell(colspan: 2, align: center + horizon, stroke: (bottom: 0.6pt + black))[#strong[Swasta]/#text(style: "italic", weight: "bold")[Private]],
    table.cell(colspan: 2, align: center + horizon, stroke: (bottom: 0.6pt + black))[#strong[Jumlah]/#text(style: "italic", weight: "bold")[Total]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2024/2025]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2025/2026]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2024/2025]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2025/2026]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2024/2025]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2025/2026]],
    table.cell(align: center + horizon)[#strong[(1)]],
    table.cell(align: center + horizon)[#strong[(2)]],
    table.cell(align: center + horizon)[#strong[(3)]],
    table.cell(align: center + horizon)[#strong[(4)]],
    table.cell(align: center + horizon)[#strong[(5)]],
    table.cell(align: center + horizon)[#strong[(6)]],
    table.cell(align: center + horizon)[#strong[(7)]]),
  table.cell(align: left + horizon)[Taman Kanak-Kanak (TK)#super[1]/#text(style: "italic")[Kindergarten#super[1]]], table.cell(align: center + horizon)[16], table.cell(align: center + horizon)[11], table.cell(align: center + horizon)[5], table.cell(align: center + horizon)[5], table.cell(align: center + horizon)[21], table.cell(align: center + horizon)[16],
  table.cell(align: left + horizon)[Raudatul Athfal (RA)#super[2]/#text(style: "italic")[Raudatul Athfal (RA)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Sekolah Dasar (SD)#super[1]/#text(style: "italic")[Primary School#super[1]]], table.cell(align: center + horizon)[185], table.cell(align: center + horizon)[183], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[185], table.cell(align: center + horizon)[183],
  table.cell(align: left + horizon)[Madrasah Ibtidaiyah (MI)#super[2]/#text(style: "italic")[Madrasah Ibtidaiyah (MI)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[32], table.cell(align: center + horizon)[29], table.cell(align: center + horizon)[32], table.cell(align: center + horizon)[29],
  table.cell(align: left + horizon)[Sekolah Menengah Pertama (SMP)#super[1]/#text(style: "italic")[Junior High School#super[1]]], table.cell(align: center + horizon)[82], table.cell(align: center + horizon)[80], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[82], table.cell(align: center + horizon)[80],
  table.cell(align: left + horizon)[Madrasah Tsanawiyah (MTs)#super[2]/#text(style: "italic")[Madrasah Tsanawiyah (MTs)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[13], table.cell(align: center + horizon)[14], table.cell(align: center + horizon)[13], table.cell(align: center + horizon)[14],
  table.cell(align: left + horizon)[Sekolah Menengah Atas (SMA)#super[1]/#text(style: "italic")[Senior High School#super[1]]], table.cell(align: center + horizon)[48], table.cell(align: center + horizon)[51], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[48], table.cell(align: center + horizon)[51],
  table.cell(align: left + horizon)[Sekolah Menengah Kejuruan (SMK)#super[1]/#text(style: "italic")[Vocational High School#super[1]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Madrasah Aliyah (MA)#super[2]/#text(style: "italic")[Madrasah Aliyah (MA)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[#super[1] Kementerian Pendidikan Dasar dan Menengah; Sistem Data Pokok Pendidikan; data semester ganjil laporan sampai dengan 30 November/#text(style: "italic")[Ministry of Primary and Secondary Education; Sistem Data Pokok Pendidikan; odd semester report data up to 30 November] \ 
#super[2] Kementerian Agama; EMIS; data semester genap laporan sampai dengan 30 Juni/#text(style: "italic")[Ministry of Religious Affairs; EMIS; even semester report data up to 30 June]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[4.1.4]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Jumlah Peserta Didik Menurut Tingkat Pendidikan di Kecamatan Toho, 2024/2025 dan 2025/2026] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Pupils by Educational Level in Toho District, 2024/2025 and 2025/2026]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (1.9fr, 1.0fr, 1.0fr, 1.0fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 2 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 2 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(rowspan: 2, align: center + horizon)[#strong[Tingkat Pendidikan] \ #text(6pt, style: "italic", weight: "bold")[Educational Level]],
    table.cell(colspan: 2, align: center + horizon, stroke: (bottom: 0.6pt + black))[#strong[Negeri]/#text(style: "italic", weight: "bold")[Public]],
    table.cell(colspan: 2, align: center + horizon, stroke: (bottom: 0.6pt + black))[#strong[Swasta]/#text(style: "italic", weight: "bold")[Private]],
    table.cell(colspan: 2, align: center + horizon, stroke: (bottom: 0.6pt + black))[#strong[Jumlah]/#text(style: "italic", weight: "bold")[Total]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2024/2025]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2025/2026]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2024/2025]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2025/2026]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2024/2025]],
    table.cell(align: center + horizon)[#text(5.5pt, weight: "bold")[2025/2026]],
    table.cell(align: center + horizon)[#strong[(1)]],
    table.cell(align: center + horizon)[#strong[(2)]],
    table.cell(align: center + horizon)[#strong[(3)]],
    table.cell(align: center + horizon)[#strong[(4)]],
    table.cell(align: center + horizon)[#strong[(5)]],
    table.cell(align: center + horizon)[#strong[(6)]],
    table.cell(align: center + horizon)[#strong[(7)]]),
  table.cell(align: left + horizon)[Taman Kanak-Kanak (TK)#super[1]/#text(style: "italic")[Kindergarten#super[1]]], table.cell(align: center + horizon)[151], table.cell(align: center + horizon)[121], table.cell(align: center + horizon)[48], table.cell(align: center + horizon)[44], table.cell(align: center + horizon)[199], table.cell(align: center + horizon)[165],
  table.cell(align: left + horizon)[Raudatul Athfal (RA)#super[2]/#text(style: "italic")[Raudatul Athfal (RA)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Sekolah Dasar (SD)#super[1]/#text(style: "italic")[Primary School#super[1]]], table.cell(align: center + horizon)[2.176], table.cell(align: center + horizon)[2.148], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[2.176], table.cell(align: center + horizon)[2.148],
  table.cell(align: left + horizon)[Madrasah Ibtidaiyah (MI)#super[2]/#text(style: "italic")[Madrasah Ibtidaiyah (MI)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[261], table.cell(align: center + horizon)[266], table.cell(align: center + horizon)[261], table.cell(align: center + horizon)[266],
  table.cell(align: left + horizon)[Sekolah Menengah Pertama (SMP)#super[1]/#text(style: "italic")[Junior High School#super[1]]], table.cell(align: center + horizon)[1.028], table.cell(align: center + horizon)[1.050], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[1.028], table.cell(align: center + horizon)[1.050],
  table.cell(align: left + horizon)[Madrasah Tsanawiyah (MTs)#super[2]/#text(style: "italic")[Madrasah Tsanawiyah (MTs)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[75], table.cell(align: center + horizon)[94], table.cell(align: center + horizon)[75], table.cell(align: center + horizon)[94],
  table.cell(align: left + horizon)[Sekolah Menengah Atas (SMA)#super[1]/#text(style: "italic")[Senior High School#super[1]]], table.cell(align: center + horizon)[703], table.cell(align: center + horizon)[704], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[703], table.cell(align: center + horizon)[704],
  table.cell(align: left + horizon)[Sekolah Menengah Kejuruan (SMK)#super[1]/#text(style: "italic")[Vocational High School#super[1]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Madrasah Aliyah (MA)#super[2]/#text(style: "italic")[Madrasah Aliyah (MA)#super[2]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[#super[1] Kementerian Pendidikan Dasar dan Menengah; Sistem Data Pokok Pendidikan; data semester ganjil laporan sampai dengan 30 November/#text(style: "italic")[Ministry of Primary and Secondary Education; Sistem Data Pokok Pendidikan; odd semester report data up to 30 November] \ 
#super[2] Kementerian Agama; EMIS; data semester genap laporan sampai dengan 30 Juni/#text(style: "italic")[Ministry of Religious Affairs; EMIS; even semester report data up to 30 June]]]
)
#v(8pt)

#pagebreak()


#v(0.2cm)
#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold")[4.2 KESEHATAN/]#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", style: "italic")[HEALTH]
#v(6pt)


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[4.2.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan yang Memiliki Sarana Kesehatan Menurut Jenis Sarana Kesehatan di Kecamatan Toho, 2023–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts Having Health Facilities by Type of Health Facilities in Toho District, 2023–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Sarana Kesehatan] \ #text(6pt, weight: "bold", style: "italic")[Type of Health Facilities]], table.cell(align: center + horizon)[#strong[2023#super[2]]], table.cell(align: center + horizon)[#strong[2024#super[3]]], table.cell(align: center + horizon)[#strong[2025#super[3]]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: left + horizon)[Rumah Sakit/#text(style: "italic")[Hospital]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Puskesmas Rawat Inap/#text(style: "italic")[Public Health Center with Inpatient Care]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Puskesmas Tanpa Rawat Inap/#text(style: "italic")[Public Health Center without Inpatient Care]], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2],
  table.cell(align: left + horizon)[Apotek/#text(style: "italic")[Pharmacy]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[2]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1] Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[#super[2] Kantor Camat Toho/#text(style: "italic")[Toho District Office] \ 
#super[3] Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS–Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)

#pagebreak()


#v(0.2cm)
#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold")[4.3 PERUMAHAN DAN LINGKUNGAN/]#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", style: "italic")[HOUSING AND ENVIRONMENT]
#v(6pt)


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[4.3.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan Menurut Sumber Penerangan Jalan Utama Desa/Kelurahan di Kecamatan Toho, 2023–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts by Source of Main Street Illumination in Toho District, 2023–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Sumber Penerangan Jalan Utama] \ #text(6pt, weight: "bold", style: "italic")[Source of Main Street Illumination]], table.cell(align: center + horizon)[#strong[2023#super[2]]], table.cell(align: center + horizon)[#strong[2024#super[3]]], table.cell(align: center + horizon)[#strong[2025#super[3]]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]]),
  table.cell(align: left + horizon)[Listrik Pemerintah/#text(style: "italic")[State Electricity]], table.cell(align: center + horizon)[…], table.cell(align: center + horizon)[2], table.cell(align: center + horizon)[7],
  table.cell(align: left + horizon)[Listrik Non-Pemerintah/#text(style: "italic")[Non-State Electricity]], table.cell(align: center + horizon)[…], table.cell(align: center + horizon)[6], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Non Listrik/#text(style: "italic")[Non-Electric]], table.cell(align: center + horizon)[…], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1] Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[#super[2] Kantor Camat Toho/#text(style: "italic")[Toho District Office] \ 
#super[3] Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS–Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)

#pagebreak()



#metadata("tab_4_3_2") <tab_4_3_2>
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[4.3.2]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan Menurut Jenis Bahan Bakar untuk Memasak yang Digunakan Sebagian Besar Keluarga di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts by Type of Cooking Fuel Used by Majority Family in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (3.4fr, 1.4fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Bahan Bakar Memasak] \ #text(6pt, weight: "bold", style: "italic")[Type of Cooking Fuel]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]]),
  table.cell(align: left + horizon)[Listrik/#text(style: "italic")[Electric]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Elpiji 5,5 kg/#text(style: "italic")[5.5 kg-LPG]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Elpiji 12 kg/#text(style: "italic")[12 kg-LPG]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Elpiji 3 kg/#text(style: "italic")[3 kg-LPG]], table.cell(align: center + horizon)[8],
  table.cell(align: left + horizon)[Gas Kota/#text(style: "italic")[City Gas]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Biogas/#text(style: "italic")[Biogas]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Minyak Tanah/#text(style: "italic")[Kerosene]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Briket/#text(style: "italic")[Briquettes]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Arang/#text(style: "italic")[Charcoal]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Kayu Bakar/#text(style: "italic")[Firewood]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Lainnya/#text(style: "italic")[Others]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Jumlah/#text(style: "italic")[Total]], table.cell(align: center + horizon)[8]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1] Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS–Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)

#pagebreak()


#v(0.2cm)
#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold")[4.4 SOSIAL LAINNYA/]#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", style: "italic")[RELIGION AND OTHER SOCIAL AFFAIRS]
#v(6pt)


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[4.4.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan yang Mengalami Kejadian Bencana Alam Menurut Jenis Bencana Alam di Kecamatan Toho, 2025#super[2]] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts with Natural Disaster Events by Type of Natural Disaster in Toho District, 2025#super[2]]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (3.4fr, 1.4fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Bencana Alam] \ #text(6pt, weight: "bold", style: "italic")[Type of Natural Disaster]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]]),
  table.cell(align: left + horizon)[Gempa Bumi/#text(style: "italic")[Earthquake]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Tsunami], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Gunung Meletus/#text(style: "italic")[Volcanic Eruption]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Tanah Longsor/#text(style: "italic")[Landslide]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Banjir/#text(style: "italic")[Floods]], table.cell(align: center + horizon)[5],
  table.cell(align: left + horizon)[Banjir Bandang/#text(style: "italic")[Flash Floods]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Kekeringan/#text(style: "italic")[Drought]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Kebakaran Hutan dan Lahan/#text(style: "italic")[Forest and Land Fires]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Angin Puyuh/Puting Beliung/Topan/#text(style: "italic")[Tornado/Typhoon]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Gelombang Pasang/#text(style: "italic")[Tidal Wave]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Abrasi/#text(style: "italic")[Abrasion]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Tidak Ada Bencana Alam/No Natural Disaster], table.cell(align: center + horizon)[3]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1] Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries] \ 
#super[2] Periode Januari–Mei 2025/#text(style: "italic")[During January–May 2025]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS-Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)

#pagebreak()



#metadata("tab_4_4_2") <tab_4_4_2>
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[4.4.2]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Fasilitas/Upaya Antisipasi/Mitigasi Bencana Alam Menurut Jenis Fasilitas/Upaya Antisipasi/Mitigasi di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts with Availability of Facilities/Efforts for Anticipation/Mitigation of Natural Disasters by Type of Facilities/Efforts for Anticipation/Mitigation in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (3.4fr, 1.4fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Fasilitas/Upaya Antisipasi/Mitigasi] \ #text(6pt, weight: "bold", style: "italic")[Type of Facilities/Efforts for Anticipation/Mitigation]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]]),
  table.cell(align: left + horizon)[Sistem peringatan dini bencana alam/#text(style: "italic")[Natural disaster early warning system]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Sistem peringatan dini khusus tsunami/#text(style: "italic")[Tsunami early warning system]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Perlengkapan keselamatan/#text(style: "italic")[Safety equipment]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Rambu‐Rambu dan jalur evakuasi bencana/#text(style: "italic")[Sign and evacuation route]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Pembuatan, perawatan, atau normalisasi sungai, kanal, tanggul, dll/#text(style: "italic")[Manufacture, maintenance, or normalization of rivers, canals, etc]], table.cell(align: center + horizon)[7]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1] Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS-Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)



// ==========================================
// BAB 5: PERTANIAN (PENJELASAN TEKNIS & GAMBAR)
// ==========================================

// ----------------------------------------------------
// BAB 5: PERTANIAN (AGRICULTURE)
// ----------------------------------------------------
#pagebreak()
#set page(margin: 0pt, header: none, footer: none)
#metadata("bab5") <bab5>
#image("/assets/dividers/Bab_5.jpg", width: 100%, height: 100%)

#pagebreak()
#set page(
  margin: normal_margins,
  header: page_header,
  footer: page_footer,
)
#metadata("PERTANIAN") <chapter_title>
#metadata("AGRICULTURE") <chapter_title_en>

// --- HALAMAN PENJELASAN TEKNIS / TECHNICAL NOTES ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[PENJELASAN TEKNIS]]
    #v(10pt)
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Tanaman sayuran dan buah-buahan semusim

a. Tanaman sayuran semusim adalah tanaman yang bermanfaat sebagai sayur, sebagai sumber vitamin, mineral, dan lain-lain yang berumur kurang dari satu tahun. Pada umumnya bagian yang digunakan sebagai sayur berupa daun, bunga, buah, dan umbi.

b. Tanaman buah-buahan semusim adalah tanaman yang menghasilkan buah segar sebagai sumber vitamin, mineral, dan lain-lain yang berumur kurang dari satu tahun dan berbatang lunak. Pada umumnya buah yang dihasilkan dapat dikonsumsi tanpa dimasak terlebih dahulu.],
      [2.], [Tanaman buah-buahan dan sayuran tahunan

a. Tanaman buah-buahan tahunan adalah tanaman yang menghasilkan buah segar sebagai sumber vitamin, mineral, dan lain-lain yang berumur satu tahun atau lebih dan berbatang keras. Pada umumnya buah yang dihasilkan dapat dikonsumsi tanpa dimasak terlebih dahulu.

b. Tanaman sayuran tahunan adalah tanaman yang bermanfaat sebagai sayur, sebagai sumber vitamin, mineral, dan lain-lain yang berumur satu tahun atau lebih. Pada umumnya bagian yang digunakan sebagai sayur berupa daun, bunga, buah, dan umbi.],
      [3.], [Tanaman biofarmaka adalah tanaman yang bermanfaat untuk obat-obatan, kosmetik, dan kesehatan yang dikonsumsi atau digunakan dari bagian-bagian tanaman, seperti daun, batang, buah, umbi (rimpang) ataupun akar.],
      [4.], [Tanaman hias adalah tanaman yang mempunyai nilai keindahan baik bentuk, warna daun, tajuk maupun bunganya, sering digunakan untuk penghias pekarangan dan lain sebagainya.],
      [5.], [Luas panen untuk tanaman sayuran: luas tanaman yang dipanen sekaligus/habis/dibongkar dan luas tanaman yang dipanen berkali-kali (lebih dari satu kali)/belum habis.

a. Tanaman yang dipanen sekaligus/habis/dibongkar adalah tanaman yang sehabis panen langsung dibongkar/dicabut, terdiri dari bawang merah, bawang putih, bawang daun, kentang, kol/kubis, kembang kol, petsai/sawi, wortel, lobak, dan kacang merah.

b. Tanaman yang dipanen berkali-kali (lebih dari satu kali)/belum habis adalah tanaman yang pemanenannya lebih dari satu kali dan biasanya dibongkar apabila panenan terakhir sudah tidak memadai lagi, terdiri dari: kacang panjang, cabai besar, cabai rawit, jamur, tomat, terung, buncis, ketimun, labu siam, kangkung, bayam, melon, semangka, dan blewah.],
      [6.], [Produksi adalah hasil menurut bentuk produk dari setiap tanaman sayuran, buah-buahan, biofarmaka, dan tanaman hias yang diambil berdasarkan luas yang dipanen/tanaman yang menghasilkan pada bulan/triwulan laporan.]
    )
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[TECHNICAL NOTES]]
    #v(10pt)
    #set text(style: "italic")
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Seasonal vegetable and fruit plants

a. Seasonal vegetable plants are used/consumed as vegetables, which are the sources of vitamin, mineral, etc that are aged less than 1 year. In general, parts that consumed are in the form of leaves, flower, fruits, and tubers.

b. Seasonal fruit plants are plants that produce fresh fruit as a sources of vitamin, mineral, etc that aged less than 1 year and soft trunked. Generally, the fruit produced can be consumed without being cooked first.],
      [2.], [Annual fruit and vegetable plants

a. Annual fruit plants are plants that produce fresh fruit as sources of vitamin, mineral, etc that are aged more than 1 year and hard trunked. Generally, the fruit produced can be consumed without being cooked first.

b. Annual vegetable plants are plants used as vegetables as sources of vitamin, mineral, etc that is aged more than 1 year. In general, the parts that consumed are in the form of leaves, flower, fruits, and tubers.],
      [3.], [Medicinal plants are plants that are beneficial for medicines, cosmetics, and health which are consumed or used from parts of plants, such as leaves, stems, fruits, tubers (rhizomes) or roots.],
      [4.], [Ornamental plants are plants which have an aesthetic value, either in shape, leaf colour, canopy or flower, and are often used as yard decorators.],
      [5.], [Harvested area of vegetables: area of entirely harvested/demolished plant and plant that is harvested several times/undemolished.

a. Entirely harvested/demolished plants are plants usually harvested once and demolished to be substituted by other plants, consisting of: shallots, garlic, welsh onion, potato, cabbage, cauliflower, chinese cabbage, carrots, radish, and red beans.

b. Plants that are harvested several times/undemolished are plants usually harvested more than once and demolished in the case that the last harvest was economically not profitable. They consist of: yard long beans, chili, small chili, mushroom, tomatoes, eggplant, green beans, cucumber, chayote, water spinach, spinach, melon, watermelon, and cantaloupe.],
      [6.], [Production is the standard production quantity form of vegetable, fruit, medicinal and ornamental plant based on harvested area/the number of production plants reported monthly/quarterly.]
    )
  ]
)

#pagebreak()

// --- HALAMAN ULASAN / DESCRIPTION ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[ULASAN]]
    #v(10pt)
    #block[
  #text(8pt, weight: "bold")[Hortikultura] \
  #v(2pt)
  Sektor pertanian memegang peranan penting dalam perekonomian masyarakat Kecamatan Toho, khususnya budidaya aneka tanaman hortikultura semusim dan tahunan. Pada tahun 2025, produksi tanaman sayuran semusim terbesar dicatat oleh komoditas Ketimun dengan produksi mencapai 6290 kuintal; produksi tanaman biofarmaka didominasi oleh Serai sebesar 3650 kg; produksi buah-buahan tahunan tertinggi diraih oleh komoditas Pepaya sebanyak 782 kuintal. Hasil panen komoditas ini menjadi pasokan pangan penting bagi konsumsi masyarakat lokal maupun dipasarkan ke luar wilayah kecamatan.
]
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[DESCRIPTION]]
    #v(10pt)
    #set text(style: "italic")
    #block[
  #text(8pt, weight: "bold", style: "italic")[Horticulture] \
  #v(2pt)
  The agricultural sector plays a crucial role in the economy of Toho District, particularly the cultivation of seasonal and annual horticultural crops. In 2025, the largest seasonal vegetable crop production was recorded by Cucumber reaching 6290 quintals; medicinal plants production was dominated by Lemongrass amounting to 3650 kg; the highest annual fruit crop production was achieved by Papaya with 782 quintals. These harvest yields serve as important food supplies for local consumption and are traded to surrounding markets.
]
  ]
)

#pagebreak()



#v(6pt)
#align(center)[
  #image("charts/gambar_5.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)/#text(style: "italic")[BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-BST)]]
#v(4pt)
#metadata("fig_5") <fig_5>
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
        #text(8.5pt, weight: "bold")[5]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Produksi Buah-buahan Utama di Kecamatan Toho, 2025 (Kuintal)] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Production of Major Fruits in Toho District, 2025 (Quintal)]
  ]
)
#v(10pt)

#pagebreak()

// ==========================================
// TABEL DATA BAB 5 (1 HALAMAN 1 TABEL)
// ==========================================


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[5.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Luas Panen Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Toho (ha), 2022–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Harvested Area of Temporary Vegetables and Fruit Crops by Type of Crops in Toho District (ha), 2022–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], table.cell(align: center + horizon)[#strong[2022]], table.cell(align: center + horizon)[#strong[2023]], table.cell(align: center + horizon)[#strong[2024]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]], table.cell(align: center + horizon)[#strong[(5)]]),
  table.cell(colspan: 5, align: left + horizon)[#strong[Sayuran] / #text(weight: "bold", style: "italic")[Vegetables:]],
  table.cell(align: left + horizon)[Bawang Merah/#text(style: "italic")[Shallots]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Cabai Besar/TW/Teropong Chili/#text(style: "italic")[Big Chili]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Cabai keriting/#text(style: "italic")[Curly Chili]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Cabai Rawit Chili/#text(style: "italic")[Cayenne Pepper]], table.cell(align: center + horizon)[3], table.cell(align: center + horizon)[12], table.cell(align: center + horizon)[7], table.cell(align: center + horizon)[19],
  table.cell(align: left + horizon)[Kentang/#text(style: "italic")[Potato]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Kubis/#text(style: "italic")[Cabbage]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Tomat/#text(style: "italic")[Tomato]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Bawang Putih/#text(style: "italic")[Garlic]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Kacang Panjang/#text(style: "italic")[Long Beans]], table.cell(align: center + horizon)[12], table.cell(align: center + horizon)[12], table.cell(align: center + horizon)[28], table.cell(align: center + horizon)[14],
  table.cell(align: left + horizon)[Ketimun/#text(style: "italic")[Cucumber]], table.cell(align: center + horizon)[18], table.cell(align: center + horizon)[43], table.cell(align: center + horizon)[80], table.cell(align: center + horizon)[35],
  table.cell(align: left + horizon)[Terung/#text(style: "italic")[Eggplant]], table.cell(align: center + horizon)[7], table.cell(align: center + horizon)[13], table.cell(align: center + horizon)[28], table.cell(align: center + horizon)[20]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik-Kementerian Pertanian (Direktorat Jenderal Hortikultura)/#text(style: "italic")[BPS-Statistics Indonesia-Ministry of Agriculture (Directorate General of Horticulture)]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[5.2]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Produksi Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di Kecamatan Toho (kuintal), 2022–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Production of Temporary Vegetables and Fruit Crops by Type of Crops in Toho District (quintal), 2022–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], table.cell(align: center + horizon)[#strong[2022]], table.cell(align: center + horizon)[#strong[2023]], table.cell(align: center + horizon)[#strong[2024]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]], table.cell(align: center + horizon)[#strong[(5)]]),
  table.cell(colspan: 5, align: left + horizon)[#strong[Sayuran] / #text(weight: "bold", style: "italic")[Vegetables:]],
  table.cell(align: left + horizon)[Bawang Merah/#text(style: "italic")[Shallots]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Cabai Besar/TW/Teropong Chili/#text(style: "italic")[Big Chili]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Cabai keriting/#text(style: "italic")[Curly Chili]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Cabai Rawit Chili/#text(style: "italic")[Cayenne Pepper]], table.cell(align: center + horizon)[52], table.cell(align: center + horizon)[348], table.cell(align: center + horizon)[751], table.cell(align: center + horizon)[479],
  table.cell(align: left + horizon)[Kentang/#text(style: "italic")[Potato]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Kubis/#text(style: "italic")[Cabbage]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Tomat/#text(style: "italic")[Tomato]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Bawang Putih/#text(style: "italic")[Garlic]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Kacang Panjang/#text(style: "italic")[Long Beans]], table.cell(align: center + horizon)[301], table.cell(align: center + horizon)[244], table.cell(align: center + horizon)[3.289], table.cell(align: center + horizon)[281],
  table.cell(align: left + horizon)[Ketimun/#text(style: "italic")[Cucumber]], table.cell(align: center + horizon)[478], table.cell(align: center + horizon)[2.950], table.cell(align: center + horizon)[7.599], table.cell(align: center + horizon)[6.290],
  table.cell(align: left + horizon)[Terung/#text(style: "italic")[Eggplant]], table.cell(align: center + horizon)[341], table.cell(align: center + horizon)[442], table.cell(align: center + horizon)[4.216], table.cell(align: center + horizon)[2024]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik-Kementerian Pertanian (Direktorat Jenderal Hortikultura)/#text(style: "italic")[BPS-Statistics Indonesia-Ministry of Agriculture (Directorate General of Horticulture)]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[5.3]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Luas Panen Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Toho (m2), 2022–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Harvested Area of Medicinal Crops by Type of Crops in Toho District (m2), 2022–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], table.cell(align: center + horizon)[#strong[2022]], table.cell(align: center + horizon)[#strong[2023]], table.cell(align: center + horizon)[#strong[2024]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]], table.cell(align: center + horizon)[#strong[(5)]]),
  table.cell(align: left + horizon)[Jahe/#text(style: "italic")[Ginger]], table.cell(align: center + horizon)[500], table.cell(align: center + horizon)[900], table.cell(align: center + horizon)[700], table.cell(align: center + horizon)[325],
  table.cell(align: left + horizon)[Laos/Lengkuas/#text(style: "italic")[Galanga]], table.cell(align: center + horizon)[400], table.cell(align: center + horizon)[350], table.cell(align: center + horizon)[250], table.cell(align: center + horizon)[238],
  table.cell(align: left + horizon)[Kencur/#text(style: "italic")[East Indian Galangal]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Kunyit/#text(style: "italic")[Turmeric]], table.cell(align: center + horizon)[250], table.cell(align: center + horizon)[450], table.cell(align: center + horizon)[400], table.cell(align: center + horizon)[285],
  table.cell(align: left + horizon)[Serai/#text(style: "italic")[Lemongrass]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[500], table.cell(align: center + horizon)[1.050], table.cell(align: center + horizon)[675]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik-Kementerian Pertanian (Direktorat Jenderal Hortikultura)/#text(style: "italic")[BPS-Statistics Indonesia-Ministry of Agriculture (Directorate General of Horticulture)]]]
)
#v(8pt)

#pagebreak()



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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[5.4]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Produksi Tanaman Biofarmaka Menurut Jenis Tanaman di Kecamatan Toho (kg), 2022–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Production of Medicinal Crops by Type of Crops in Toho District (kg), 2022–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], table.cell(align: center + horizon)[#strong[2022]], table.cell(align: center + horizon)[#strong[2023]], table.cell(align: center + horizon)[#strong[2024]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]], table.cell(align: center + horizon)[#strong[(5)]]),
  table.cell(align: left + horizon)[Jahe/#text(style: "italic")[Ginger]], table.cell(align: center + horizon)[1.250], table.cell(align: center + horizon)[4.200], table.cell(align: center + horizon)[3.460], table.cell(align: center + horizon)[725],
  table.cell(align: left + horizon)[Laos/Lengkuas/#text(style: "italic")[Galanga]], table.cell(align: center + horizon)[900], table.cell(align: center + horizon)[1.650], table.cell(align: center + horizon)[743], table.cell(align: center + horizon)[599],
  table.cell(align: left + horizon)[Kencur/#text(style: "italic")[East Indian Galangal]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Kunyit/#text(style: "italic")[Turmeric]], table.cell(align: center + horizon)[875], table.cell(align: center + horizon)[1.400], table.cell(align: center + horizon)[773], table.cell(align: center + horizon)[865],
  table.cell(align: left + horizon)[Serai/#text(style: "italic")[Lemongrass]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[3.500], table.cell(align: center + horizon)[7.850], table.cell(align: center + horizon)[3.650]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik-Kementerian Pertanian (Direktorat Jenderal Hortikultura)/#text(style: "italic")[BPS-Statistics Indonesia-Ministry of Agriculture (Directorate General of Horticulture)]]]
)
#v(8pt)

#pagebreak()



#metadata("tab_5_5") <tab_5_5>
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[5.5]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Luas Panen Tanaman Hias Menurut Jenis Tanaman di Kecamatan Toho (m2), 2022–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Harvested Area of Ornamental Crops by Type of Crops in Toho District (m2), 2022–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], table.cell(align: center + horizon)[#strong[2022]], table.cell(align: center + horizon)[#strong[2023]], table.cell(align: center + horizon)[#strong[2024]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]], table.cell(align: center + horizon)[#strong[(5)]]),
  table.cell(align: left + horizon)[Anggrek Pot#super[1]/#text(style: "italic")[Pot Orchid#super[1]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Anggrek Potong/#text(style: "italic")[Cut Orchid]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Krisan/#text(style: "italic")[Chrysantemum]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Mawar/#text(style: "italic")[Rose]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Sedap Malam/#text(style: "italic")[Tuberose]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik-Kementerian Pertanian (Direktorat Jenderal Hortikultura)/#text(style: "italic")[BPS-Statistics Indonesia-Ministry of Agriculture (Directorate General of Horticulture)]]]
)
#v(8pt)

#pagebreak()



#metadata("tab_5_6") <tab_5_6>
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[5.6]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Produksi Tanaman Hias Menurut Jenis Tanaman di Kecamatan Toho (tangkai), 2022–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Production of Ornamental Crops by Type of Crops in Toho District (stalks), 2022–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], table.cell(align: center + horizon)[#strong[2022]], table.cell(align: center + horizon)[#strong[2023]], table.cell(align: center + horizon)[#strong[2024]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]], table.cell(align: center + horizon)[#strong[(5)]]),
  table.cell(align: left + horizon)[Anggrek Pot#super[1]/#text(style: "italic")[Pot Orchid#super[1]]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Anggrek Potong/#text(style: "italic")[Cut Orchid]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Krisan/#text(style: "italic")[Chrysantemum]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Mawar/#text(style: "italic")[Rose]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Sedap Malam/#text(style: "italic")[Tuberose]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[–]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1] Satuan produksi dalam pohon/#text(style: "italic")[The unit of production is tree]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik-Kementerian Pertanian (Direktorat Jenderal Hortikultura)/#text(style: "italic")[BPS-Statistics Indonesia-Ministry of Agriculture (Directorate General of Horticulture)]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[5.7]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Produksi Buah-buahan dan Sayuran Tahunan Menurut Jenis Tanaman di Kecamatan Toho (kuintal), 2022–2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Production of Permanent Fruit and Vegetable by Type of Crops (quintal), 2022–2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#set text(size: 6.8pt)
#table(
  columns: (2.6fr, 0.9fr, 0.9fr, 0.9fr, 0.9fr),
  inset: (x: 3.5pt, y: 2.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], table.cell(align: center + horizon)[#strong[2022]], table.cell(align: center + horizon)[#strong[2023]], table.cell(align: center + horizon)[#strong[2024]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]], table.cell(align: center + horizon)[#strong[(3)]], table.cell(align: center + horizon)[#strong[(4)]], table.cell(align: center + horizon)[#strong[(5)]]),
  table.cell(colspan: 5, align: left + horizon)[#strong[Buah–Buahan] / #text(weight: "bold", style: "italic")[Fruits:]],
  table.cell(align: left + horizon)[Mangga/#text(style: "italic")[Mango]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[18], table.cell(align: center + horizon)[168], table.cell(align: center + horizon)[257],
  table.cell(align: left + horizon)[Durian/#text(style: "italic")[Durian]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[800], table.cell(align: center + horizon)[1.883], table.cell(align: center + horizon)[656],
  table.cell(align: left + horizon)[Pisang/#text(style: "italic")[Banana]], table.cell(align: center + horizon)[2.360], table.cell(align: center + horizon)[280], table.cell(align: center + horizon)[571], table.cell(align: center + horizon)[551],
  table.cell(align: left + horizon)[Pepaya/#text(style: "italic")[Papaya]], table.cell(align: center + horizon)[2.637], table.cell(align: center + horizon)[2.000], table.cell(align: center + horizon)[1.133], table.cell(align: center + horizon)[782],
  table.cell(align: left + horizon)[Sawo/Sapodilla/#text(style: "italic")[Sawo]], table.cell(align: center + horizon)[20], table.cell(align: center + horizon)[65], table.cell(align: center + horizon)[72], table.cell(align: center + horizon)[51],
  table.cell(align: left + horizon)[Rambutan/#text(style: "italic")[Rambutan]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[280], table.cell(align: center + horizon)[599], table.cell(align: center + horizon)[470],
  table.cell(align: left + horizon)[Nangka/Cempedak/#text(style: "italic")[Jackfruit]], table.cell(align: center + horizon)[59], table.cell(align: center + horizon)[688], table.cell(align: center + horizon)[1.052], table.cell(align: center + horizon)[517],
  table.cell(align: left + horizon)[Lengkeng/Dimocarpus/#text(style: "italic")[Longan]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[4], table.cell(align: center + horizon)[21], table.cell(align: center + horizon)[41],
  table.cell(align: left + horizon)[Sukun/#text(style: "italic")[Breadfruit]], table.cell(align: center + horizon)[38], table.cell(align: center + horizon)[50], table.cell(align: center + horizon)[100], table.cell(align: center + horizon)[128],
  table.cell(align: left + horizon)[Belimbing/#text(style: "italic")[Starfruit]], table.cell(align: center + horizon)[30], table.cell(align: center + horizon)[12], table.cell(align: center + horizon)[84], table.cell(align: center + horizon)[63],
  table.cell(align: left + horizon)[Duku/Langsat/#text(style: "italic")[Duku]], table.cell(align: center + horizon)[8], table.cell(align: center + horizon)[320], table.cell(align: center + horizon)[632], table.cell(align: center + horizon)[667],
  table.cell(align: left + horizon)[Jambu Air/#text(style: "italic")[Water Apple]], table.cell(align: center + horizon)[20], table.cell(align: center + horizon)[70], table.cell(align: center + horizon)[177], table.cell(align: center + horizon)[144],
  table.cell(align: left + horizon)[Jambu Biji/#text(style: "italic")[Guava]], table.cell(align: center + horizon)[58], table.cell(align: center + horizon)[81], table.cell(align: center + horizon)[92], table.cell(align: center + horizon)[107],
  table.cell(align: left + horizon)[Alpukat/#text(style: "italic")[Avocado]], table.cell(align: center + horizon)[–], table.cell(align: center + horizon)[3], table.cell(align: center + horizon)[27], table.cell(align: center + horizon)[765],
  table.cell(colspan: 5, align: left + horizon)[#strong[Sayuran] / #text(weight: "bold", style: "italic")[Vegetables:]],
  table.cell(align: left + horizon)[Jengkol/#text(style: "italic")[Jengkol]], table.cell(align: center + horizon)[820], table.cell(align: center + horizon)[1916], table.cell(align: center + horizon)[776], table.cell(align: center + horizon)[331],
  table.cell(align: left + horizon)[Petai/#text(style: "italic")[Petai]], table.cell(align: center + horizon)[318], table.cell(align: center + horizon)[410], table.cell(align: center + horizon)[153], table.cell(align: center + horizon)[362]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik-Kementerian Pertanian (Direktorat Jenderal Hortikultura)/#text(style: "italic")[BPS-Statistics Indonesia-Ministry of Agriculture (Directorate General of Horticulture)]]]
)
#v(8pt)



// ==========================================
// ISI BAB 6: ULASAN NARASI & TABEL DATA
// ==========================================

// ----------------------------------------------------
// BAB 6: PARIWISATA, TRANSPORTASI, DAN KOMUNIKASI (TOURISM, TRANSPORTATION, AND COMMUNICATION)
// ----------------------------------------------------
#pagebreak()
#set page(margin: 0pt, header: none, footer: none)
#metadata("bab6") <bab6>
#image("/assets/dividers/Bab_6.jpg", width: 100%, height: 100%)

#pagebreak()
#set page(
  margin: normal_margins,
  header: page_header,
  footer: page_footer,
)
#metadata("PARIWISATA, TRANSPORTASI, DAN KOMUNIKASI") <chapter_title>
#metadata("TOURISM, TRANSPORTATION, AND COMMUNICATION") <chapter_title_en>

// --- HALAMAN PENJELASAN TEKNIS / TECHNICAL NOTES ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[PENJELASAN TEKNIS]]
    #v(10pt)
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Hotel adalah jenis akomodasi yang mempergunakan sebagian atau keseluruhan bangunan untuk jasa pelayanan penginapan, penyedia makanan dan minuman serta jasa lainnya (seperti restoran, binatu, d.l.l) bagi masyarakat umum yang dikelola secara komersial dengan izin usaha sebagai hotel.],
      [2.], [Penginapan (Hostel/Motel/Losmen/Wisma) adalah jenis akomodasi yang mempergunakan sebagian atau keseluruhan bangunan untuk jasa pelayanan penginapan bagi umum, biasanya tanpa fasilitas pelayanan makan minum yang dikelola secara komersial dengan izin usaha bukan hotel.],
      [3.], [Prasarana Transportasi adalah sarana penunjang lalu lintas pemindahan orang dan atau barang, yang terdiri atas jalan, jembatan, dermaga, pelabuhan, dan lain-lain yang digunakan oleh warga desa untuk mobilitas dari dan ke desa terdekat.],
      [4.], [Kantor Pos adalah tempat pemberi pelayanan komunikasi tertulis dan atau surat elektronik, layanan paket, layanan logistik, layanan transaksi keuangan, dan layanan keagenan pos untuk kepentingan umum. Rumah pos berfungsi sama seperti kantor pos dan kantor pos pembantu, bedanya rumah pos biasanya terletak di daerah terpencil.],
      [5.], [Pos Keliling adalah pelayanan pos (menjual, mengirim, dan menerima benda pos) keliling dengan menggunakan mobil atau sarana angkutan yang berfungsi sama seperti kantor pos atau kantor pos pembantu.],
      [6.], [Perusahaan Jasa Agen Ekspedisi Swasta adalah pelayanan pengiriman paket maupun dokumen yang dikelola oleh pihak swasta, misalnya Tiki, JNE, ESL, d.l.l.]
    )
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[TECHNICAL NOTES]]
    #v(10pt)
    #set text(style: "italic")
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Hotel is the kind of accommodation that use part or the whole building for lodging services, food and beverage and other services (such as restaurants, laundry, etc.) for the public which is commercially managed with a business license of hotel.],
      [2.], [Inn is a type of accommodation that use part or the whole building for lodging services to the public, usually without eating and drinking facilities which is commercially managed with a business license of non-hotel.],
      [3.], [Transportation Infrastructure is a facility of supporting the transfer of people and or goods, which consists of roads, bridges, docks, harbors, etc used by villagers for mobility to and from the nearest village.],
      [4.], [Post Office is a service provider place of written communication and or electronic mail, parcel service, logistics services, financial transaction services, postal and agency services to the public. Postal house has the same function as the post office and subsidiary of post office, the difference is that postal house usually located in remote areas.],
      [5.], [Mobile Postal Service is nomadic postal service (to sell, send, and receive postal stationery) by car or transportation facility that the functions are the same as the post office or subsidiary of post office.],
      [6.], [Private Expedition Service Company is packages and documents delivery service managed by privates, for example Tiki, JNE, ESL, etc.]
    )
  ]
)

#pagebreak()

// --- HALAMAN ULASAN / DESCRIPTION ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[ULASAN]]
    #v(10pt)
    #block[
  #text(8pt, weight: "bold")[1. #h(2pt) Pariwisata dan Akomodasi] \
  #v(2pt)
  Ketersediaan sarana akomodasi pariwisata di Kecamatan Toho tercatat sebanyak 2 penginapan/losmen guna menunjang mobilitas wisatawan dan perjalanan dinas.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Transportasi Antardesa] \
  #v(2pt)
  Seluruh desa/kelurahan di Kecamatan Toho (8 desa/kelurahan) telah terhubung dan dapat diakses dengan mudah melalui prasarana dan sarana transportasi darat.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[3. #h(2pt) Komunikasi dan Pos] \
  #v(2pt)
  Layanan komunikasi dan pengiriman logistik kian berkembang dengan 2 desa memiliki kantor pos/pos pembantu serta 1 desa dilayani agen ekspedisi swasta yang mempermudah sirkulasi barang dan perniagaan masyarakat.
]
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[DESCRIPTION]]
    #v(10pt)
    #set text(style: "italic")
    #block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Tourism and Accommodation] \
  #v(2pt)
  The availability of tourism accommodation facilities in Toho District was recorded at 2 inn(s) to support visitor mobility and business travel.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Inter-Village Transportation] \
  #v(2pt)
  All villages in Toho District (8 village(s)) are connected and readily accessible through land transportation infrastructure and facilities.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[3. #h(2pt) Communication and Postal Services] \
  #v(2pt)
  Communication and courier logistics services continue to expand with 2 village(s) had post office facilities and 1 village(s) served by private courier agencies, facilitating the flow of goods and local commerce.
]
  ]
)

#pagebreak()

// ==========================================
// 6.1 PARIWISATA
// ==========================================

#v(0.2cm)
#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold")[6.1 PARIWISATA/]#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", style: "italic")[TOURISM]
#v(6pt)



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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[6.1.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Sarana Akomodasi Menurut Jenis Akomodasi di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts with Availability of Accommodation Facilities by Type of Accommodation in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (3.6fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Akomodasi] \ #text(6pt, weight: "bold", style: "italic")[Type of Accommodation]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]]),
  table.cell(align: left + horizon)[Hotel], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Penginapan/#text(style: "italic")[Inn]], table.cell(align: center + horizon)[2]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1]Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS–Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)

#pagebreak()

// ==========================================
// 6.2 TRANSPORTASI
// ==========================================

#v(0.2cm)
#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold")[6.2 TRANSPORTASI/]#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", style: "italic")[TRANSPORTATION]
#v(6pt)



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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[6.2.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan Menurut Prasarana dan Sarana Transportasi Antardesa/Kelurahan di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts by Inter-Village/ Subdistricts Transportation Infrastructure and Facilities in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (3.6fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Prasarana dan Sarana Transportasi Antardesa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Transportation Infrastructure and Facilities Between Villages/Subdistricts]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]]),
  table.cell(align: left + horizon)[Darat/#text(style: "italic")[Land]], table.cell(align: center + horizon)[8],
  table.cell(align: left + horizon)[Air/#text(style: "italic")[Water]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Darat dan air/#text(style: "italic")[Land and water]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Udara/#text(style: "italic")[Air]], table.cell(align: center + horizon)[–]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1]Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS–Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)

#pagebreak()

// ==========================================
// 6.3 KOMUNIKASI
// ==========================================

#v(0.2cm)
#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold")[6.3 KOMUNIKASI/]#text(9pt, font: ("Metropolis", "Liberation Sans", "Arial"), weight: "bold", style: "italic")[COMMUNICATION]
#v(6pt)



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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[6.3.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan Menurut Keberadaan Kantor Pos/Pos Pembantu/Rumah Pos, Pos Keliling, dan Perusahaan/Agen Jasa Ekspedisi Swasta di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts by Post Office/Subsidiary of Post Office, Mobile Postal Service, Private Expedition Service Company in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (3.6fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Fasilitas Pos dan Ekspedisi] \ #text(6pt, weight: "bold", style: "italic")[Post and Expedition Facilities]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]]),
  table.cell(align: left + horizon)[Kantor Pos/Pos Pembantu/Rumah Pos Post Office/#text(style: "italic")[Subsidiary of Post Office]], table.cell(align: center + horizon)[2],
  table.cell(align: left + horizon)[Pos Keliling/#text(style: "italic")[Mobile Portal Service]], table.cell(align: center + horizon)[1],
  table.cell(align: left + horizon)[Perusahaan/#text(style: "italic")[Agen Jasa Ekspedisi Swasta Private Expedition Service Company]], table.cell(align: center + horizon)[1]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1]Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS–Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)



// ==========================================
// ISI BAB 7: ULASAN NARASI & TABEL DATA
// ==========================================

// ----------------------------------------------------
// BAB 7: PERBANKAN, KOPERASI, DAN PERDAGANGAN (BANKING, COOPERATIVE, AND TRADE)
// ----------------------------------------------------
#pagebreak()
#set page(margin: 0pt, header: none, footer: none)
#metadata("bab7") <bab7>
#image("/assets/dividers/Bab_7.jpg", width: 100%, height: 100%)

#pagebreak()
#set page(
  margin: normal_margins,
  header: page_header,
  footer: page_footer,
)
#metadata("PERBANKAN, KOPERASI, DAN PERDAGANGAN") <chapter_title>
#metadata("BANKING, COOPERATIVE, AND TRADE") <chapter_title_en>

// --- HALAMAN PENJELASAN TEKNIS / TECHNICAL NOTES ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[PENJELASAN TEKNIS]]
    #v(10pt)
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Bank adalah badan usaha yang menghimpun dana dari masyarakat dalam bentuk simpanan, dan menyalurkannya kepada masyarakat dalam rangka meningkatkan taraf hidup rakyat banyak.],
      [2.], [Bank Umum adalah bank yang dapat memberikan jasa dalam lalu lintas pembayaran (Undang-Undang Nomor 7 Tahun 1992 Tentang Perbankan).],
      [3.], [Bank Perkreditan Rakyat adalah bank yang menerima simpanan hanya dalam bentuk deposito berjangka, tabungan, dan/atau bentuk lainnya yang dipersamakan dengan itu.],
      [4.], [Koperasi adalah badan usaha yang beranggotakan orang-seorang atau badan hukum koperasi dengan melandaskan kegiatannya berdasarkan prinsip:

a. Keanggotaannya sukarela dan terbuka;

b. Pengelolaannya dilakukan secara demokratis;

c. Pembagian sisa hasil usahanya dilakukan secara adil, sebanding dengan besarnya jasa usaha masing-masing anggota;

d. Pemberian balas jasa yang terbatas terhadap modal; dan

e. Kemandirian, serta sekaligus sebagai gerakan ekonomi rakyat yang berdasarkan atas asas kekeluargaan.],
      [5.], [Kelompok Pertokoan adalah sejumlah toko yang terdiri dari minimal sepuluh toko dan mengelompok. Dalam satu kelompok pertokoan, jumlah bangunan fisiknya bisa lebih dari satu.],
      [6.], [Pasar dengan Bangunan Permanen/Semi Permanen adalah pasar yang menggunakan bangunan tetap dan memiliki lantai, atap, baik berdinding maupun tidak.],
      [7.], [Pasar Tanpa Bangunan adalah pasar yang tidak berada dalam bangunan, termasuk pasar terapung.],
      [8.], [Mini Market adalah tempat usaha yang menjual berbagai jenis barang secara eceran dengan sistem pelayanan mandiri dan semua barang memiliki label harga, dengan luas bangunan kurang dari 400 m².],
      [9.], [Restoran adalah tempat usaha yang mempergunakan seluruh bangunan secara permanen untuk menyediakan jasa pangan yang pengolahannya dan penyajiannya secara langsung di tempat sesuai dengan keinginan para pengguna jasa.]
    )
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[TECHNICAL NOTES]]
    #v(10pt)
    #set text(style: "italic")
    #grid(
      columns: (12pt, 1fr),
      column-gutter: 3pt,
      row-gutter: 12pt,
      [1.], [Bank is business entity that raise funds from the public in deposits and distribute it to the public in order to improve the living standard of the people.],
      [2.], [Commercial Bank is a bank that can provide services in payment transfer (Law Number 7 Year 1992 About Banking).],
      [3.], [Rural bank is a bank that accepts saving in time deposits, savings, or others.],
      [4.], [Cooperative is a business entity consisting of people or cooperative legal entities which activities are based on the principles:

a. Membership is voluntary and open;

b. Management is conducted democratically;

c. Benefits are distributed proportionally according to the member’s share;

d. Remuneration is limited to the capital; and

e. Independence, as well as the people’s economic movement based on the principle of kinship.],
      [5.], [Shopping Complex is a group of shops consisting at least ten stores and clumped. In one shopping complex, number of physical buildings can be more than one.],
      [6.], [Market in the Permanent/Semi Permanent Building is a market that uses the permanent building and have floor, roof, whether it walled or not.],
      [7.], [Market Without Building is a market that is not located within the building, including the floating market.],
      [8.], [Mini Market is a place of business which sell various kinds of goods at retail by self-service system and everything has a price tag, with a building area of less than 400 m².],
      [9.], [Restaurant is a place of business that use the entire building permanently to provide food processing services and presented directly in place in accordance with the wishes of service users.]
    )
  ]
)

#pagebreak()

// --- HALAMAN ULASAN / DESCRIPTION ---
#set text(font: "Liberation Sans", size: 8.5pt)
#set par(justify: true, leading: 0.9em)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 14pt,
  [
    #align(center)[#text(9pt, weight: "bold")[ULASAN]]
    #v(10pt)
    #block[
  #text(8pt, weight: "bold")[1. #h(2pt) Perbankan dan Koperasi] \
  #v(2pt)
  Lembaga keuangan perbankan dan koperasi memegang peranan krusial dalam mendukung likuiditas permodalan dan pertumbuhan ekonomi wilayah. Aktivitas perbankan masyarakat ditunjang oleh agen layanan perbankan tanpa kantor serta jaringan bank di kecamatan sekitar. Di sektor perkoperasian, terdapat Koperasi Simpan Pinjam di 1 desa yang berperan aktif memperkuat permodalan usaha warga.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold")[2. #h(2pt) Sarana Perdagangan] \
  #v(2pt)
  Aktivitas perdagangan dan distribusi barang konsumsi di Kecamatan Toho berkembang dengan ketersediaan pasar permanen/semi permanen di 1 desa/kelurahan, kelompok pertokoan di 2 desa/kelurahan, minimarket/swalayan di 2 desa/kelurahan. Keberadaan sarana perniagaan ini memastikan kelancaran rantai pasok kebutuhan pokok bagi masyarakat.
]
  ],
  [
    #align(center)[#text(9pt, weight: "bold", style: "italic")[DESCRIPTION]]
    #v(10pt)
    #set text(style: "italic")
    #block[
  #text(8pt, weight: "bold", style: "italic")[1. #h(2pt) Banking and Cooperatives] \
  #v(2pt)
  Banking institutions and cooperatives play a vital role in supporting capital liquidity and regional economic growth. Community banking activities are supported by branchless banking agents and banking networks in neighboring districts. In the cooperative sector, there were Savings and Loan Cooperatives in 1 village(s) actively strengthening capital for local businesses.
]
#v(6pt)
#block[
  #text(8pt, weight: "bold", style: "italic")[2. #h(2pt) Trade Facilities] \
  #v(2pt)
  Trade and consumer goods distribution activities in Toho District thrive with the availability of permanent/semi-permanent markets in 1 village(s), shopping complexes in 2 village(s), minimarkets/supermarkets in 2 village(s). These commercial amenities ensure smooth supply chains of basic necessities for the community.
]
  ]
)

#pagebreak()

// ==========================================
// TABEL DATA BAB 7 (1 HALAMAN 1 TABEL)
// ==========================================


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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[7.1]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Sarana Lembaga Keuangan Bank Menurut Jenis Bank di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts with Availability of Bank by Type of Bank in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (3.6fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Bank] \ #text(6pt, weight: "bold", style: "italic")[Type of Bank]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]]),
  table.cell(align: left + horizon)[Bank Umum Pemerintah/#text(style: "italic")[Government Bank]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Bank Umum Swasta/#text(style: "italic")[Private Bank]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Bank Perkreditan Rakyat (BPR)/#text(style: "italic")[Rural Bank]], table.cell(align: center + horizon)[–]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1]Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS–Statistics Indonesia, Village Potential Data Collecting]]]
)
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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[7.2]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Koperasi Aktif Menurut Jenis Koperasi di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts with Availability of Cooperative by Type of Cooperative in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (3.6fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Koperasi] \ #text(6pt, weight: "bold", style: "italic")[Type of Cooperative]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]]),
  table.cell(align: left + horizon)[Koperasi Unit Desa (KUD)/#text(style: "italic")[Village Cooperative Unit]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Koperasi industri kecil dan kerajinan rakyat (Kopinkra)/#text(style: "italic")[Small industry and citizen handicraft cooperative]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Koperasi simpan pinjam (kospin)/#text(style: "italic")[Savings and loan cooperative]], table.cell(align: center + horizon)[1],
  table.cell(align: left + horizon)[Koperasi lainnya/#text(style: "italic")[Other cooperative]], table.cell(align: center + horizon)[–]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1]Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS–Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)

#pagebreak()



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
          #text(10pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(8pt, style: "italic")[Table]
      ],
      [
        #text(10pt, weight: "bold")[7.3]
      ]
    )
  ],
  [
    #text(10pt, weight: "bold")[Banyaknya Desa#super[1]/Kelurahan dengan Keberadaan Sarana Perdagangan Menurut Jenis Sarana Perdagangan di Kecamatan Toho, 2025] \
    #v(-2pt)
    #text(10pt, weight: "bold", style: "italic", fill: black)[Number of Villages#super[1]/Subdistricts with Availability of Trade Facilities by Type of Trade Facilities in Toho District, 2025]
  ]
)
#v(3pt)

#show table.cell: set par(justify: false)
#table(
  columns: (3.6fr, 1.2fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row < 1 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  table.header(table.cell(align: center + horizon)[#strong[Jenis Sarana Perdagangan] \ #text(6pt, weight: "bold", style: "italic")[Type of Trade Facilities]], table.cell(align: center + horizon)[#strong[2025]], table.cell(align: center + horizon)[#strong[(1)]], table.cell(align: center + horizon)[#strong[(2)]]),
  table.cell(align: left + horizon)[Kelompok pertokoan/#text(style: "italic")[Shopping complexs]], table.cell(align: center + horizon)[2],
  table.cell(align: left + horizon)[Pasar dengan bangunan permanen/#text(style: "italic")[Markets in permanent building]], table.cell(align: center + horizon)[1],
  table.cell(align: left + horizon)[Pasar dengan bangunan semi permanen/#text(style: "italic")[Market in semi permanent buildin]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Pasar tanpa bangunan/#text(style: "italic")[Market without permanent building]], table.cell(align: center + horizon)[–],
  table.cell(align: left + horizon)[Mini market/swalayan/#text(style: "italic")[supermarket]], table.cell(align: center + horizon)[2],
  table.cell(align: left + horizon)[Restoran/rumah makan Restaurant/#text(style: "italic")[food stall]], table.cell(align: center + horizon)[–]
)
#v(-2pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Catatan/#text(style: "italic")[Note] :]],
  [#text(6.5pt, fill: black)[#super[1]Desa pada tabel ini termasuk Unit Permukiman Transmigrasi (UPT) yang masih dibina oleh kementerian terkait/#text(style: "italic")[Villages in this table include Transmigration Settlement Unit which is still fostered by the relevant ministries]]]
)
#v(-3pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 4pt,
  align: (top + left, top + left),
  [#text(6.5pt, fill: black)[Sumber/#text(style: "italic")[Source] :]],
  [#text(6.5pt, fill: black)[Badan Pusat Statistik, Pendataan Potensi Desa (Podes)/#text(style: "italic")[BPS–Statistics Indonesia, Village Potential Data Collecting]]]
)
#v(8pt)



// ==========================================
// DAFTAR PUSTAKA (BIBLIOGRAPHY)
// ==========================================
#pagebreak()
#metadata("DAFTAR PUSTAKA") <chapter_title>
#metadata("BIBLIOGRAPHY") <chapter_title_en>
#metadata("daftar_pustaka") <daftar_pustaka>
#v(0.5cm)
#align(center)[#block[
  #text(12pt, weight: "bold")[DAFTAR PUSTAKA] \
  #text(9pt, style: "italic", fill: rgb("#4B5563"))[BIBLIOGRAPHY]
]]
#v(10pt)

#text(8pt)[
  Badan Pusat Statistik Kabupaten Mempawah. 2025. _Kabupaten Mempawah Dalam Angka 2025_. Mempawah: BPS Kabupaten Mempawah.

  #v(8pt)
  Badan Pusat Statistik. 2024. _Indikator Pertanian 2023/2024_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Badan Pusat Statistik. 2023. _Statistik Indonesia 2023_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Badan Pusat Statistik. 2022. _Buku 3: Konsep dan Definisi Podes 2022_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Direktorat Statistik Ketahanan Sosial. 2024. _Buku 3: Pedoman Konsep dan Definisi Podes 2024_. Jakarta: Badan Pusat Statistik.

  #v(8pt)
  Kementerian Pertanian & Badan Pusat Statistik. 2023. _Pedoman Statistik Pertanian Hortikultura (SPH)_. Jakarta: Kementerian Pertanian.
]
#metadata("akhir_buku") <akhir_buku>

// ==========================================
// KOVER BELAKANG (BACK COVER) - DESAIN VISUAL RESMI
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/assets/covers/belakang/Toho.jpg", width: 100%, height: 100%)
]
