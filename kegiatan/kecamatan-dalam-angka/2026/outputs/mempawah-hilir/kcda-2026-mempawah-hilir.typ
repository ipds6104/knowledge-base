// Publikasi Resmi BPS Kabupaten Mempawah: Kecamatan Dalam Angka 2026 (Ukuran A5)

#let in_frontmatter = state("in_frontmatter", true)
#let active_chapter = state("active_chapter", "")
#let active_chapter_en = state("active_chapter_en", "")
#let is_chapter_page = state("is_chapter_page", false)

// Warna Utama & Warna Running Title Resmi BPS (Pedoman KCDA 2026 Bagian B)
#let main_theme_color = cmyk(0%, 20%, 90%, 0%)
#let running_title_color = cmyk(0%, 35%, 95%, 0%)

// Badge pill numbering resmi BPS Pusat (Aturan KCDA 2026: main_theme_color, 49.2pt x 21pt)
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

#set page(
  paper: "a5",
  margin: (
    inside: 2.0cm,
    outside: 1.5cm,
    top: 2.0cm,
    bottom: 2.0cm,
  ),
  header-ascent: 40%,
  footer-descent: 20%,
  header: context {
    let p = here().page()
    let has_c = query(selector(<page_marker>)).any(m => {
      let pos = m.location().position()
      pos.page == p and pos.y > 1.4cm and pos.y < 19.4cm
    })
    let is_ch = query(selector(<chapter_page>)).any(m => m.location().page() == p)
    if has_c and not in_frontmatter.get() and not is_ch {
      let page_num = counter(page).get().first()
      let titles = query(selector(<chapter_title>)).filter(m => m.location().page() <= p)
      let chapter_title = if titles.len() > 0 { titles.last().value } else { "" }
      if calc.even(page_num) {
        // Halaman Genap (Verso/Kiri): Judul Publikasi Bahasa Indonesia (Metropolis, 8pt, running_title_color, bold)
        align(left, text(8pt, font: ("Metropolis", "Liberation Sans", "Arial"), fill: running_title_color, weight: "bold")[KECAMATAN MEMPAWAH HILIR DALAM ANGKA 2026])
      } else {
        // Halaman Ganjil (Rekto/Kanan): Judul Bab Bahasa Indonesia (Metropolis, 8pt, running_title_color, bold)
        let right_text = if chapter_title != "" { chapter_title } else { "BPS KABUPATEN MEMPAWAH" }
        align(right, text(8pt, font: ("Metropolis", "Liberation Sans", "Arial"), fill: running_title_color, weight: "bold")[#right_text])
      }
    }
  },
  footer: context {
    let p = here().page()
    let has_c = query(selector(<page_marker>)).any(m => {
      let pos = m.location().position()
      pos.page == p and pos.y > 1.4cm and pos.y < 19.4cm
    })
    let is_ch = query(selector(<chapter_page>)).any(m => m.location().page() == p)
    if not has_c or is_ch {
      // Sesuai Pedoman Publikasi BPS 2023 Subbab 4.1.3 Poin 9 & Subbab 4.4.1 (Hal. 47, 88):
      // Lembar pembatas bab dihitung sebagai halaman arab tetapi TANPA running title dan TANPA nomor halaman fisik.
      // Halaman kosong sisipan juga TANPA running title dan nomor halaman fisik.
      none
    } else if in_frontmatter.get() {
      let page_num = counter(page).get().first()
      // Sesuai Pedoman Publikasi BPS 2023 Subbab 4.1.3 Poin 1 & 2 (Hal. 46) serta Subbab 4.3 (Hal. 75):
      // - Halaman i (Judul Utama), ii (Katalog), iii (Tim Penyusun), iv (Kontributor) TIDAK dicetak nomornya.
      // - Nomor fisik baru mulai dicetak pada Kata Pengantar (halaman v ke atas).
      // - Mengikuti prinsip Rekto-Verso baku: Kiri untuk Genap (Verso) dan Kanan untuk Ganjil (Rekto).
      if page_num >= 5 {
        let display_val = counter(page).display("i")
        if calc.even(page_num) {
          align(left + top, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#4B5563"), weight: "bold")[#v(3pt) #display_val])
        } else {
          align(right + top, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#4B5563"), weight: "bold")[#v(3pt) #display_val])
        }
      }
    } else {
      let page_num = counter(page).get().first()
      let display_val = counter(page).display("1")
      let titles_en = query(selector(<chapter_title_en>)).filter(m => m.location().page() <= p)
      let chapter_en = if titles_en.len() > 0 { titles_en.last().value } else { "" }
      if calc.even(page_num) {
        // Halaman Genap (Verso/Kiri): Badge No Halaman di kiri + Judul Publikasi Bahasa Inggris (Metropolis, 8pt, running_title_color, italic)
        grid(
          columns: (auto, auto),
          align: horizon,
          column-gutter: 8pt,
          page_badge(display_val),
          text(8pt, font: ("Metropolis", "Liberation Sans", "Arial"), style: "italic", fill: running_title_color)[MEMPAWAH HILIR DISTRICT IN FIGURES 2026]
        )
      } else {
        // Halaman Ganjil (Rekto/Kanan): Judul Bab Bahasa Inggris + Badge No Halaman di kanan (Metropolis, 8pt, running_title_color, italic)
        let right_en_text = if chapter_en != "" { upper(chapter_en) } else { "MEMPAWAH HILIR DISTRICT IN FIGURES 2026" }
        grid(
          columns: (1fr, auto),
          align: horizon,
          column-gutter: 8pt,
          align(right, text(8pt, font: ("Metropolis", "Liberation Sans", "Arial"), style: "italic", fill: running_title_color)[#right_en_text]),
          page_badge(display_val)
        )
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
// 1. KOVER DEPAN (FRONT COVER) - DESAIN RESMI TERBARU
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/depan/Mempawah Hilir1.jpg", width: 100%, height: 100%)
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
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/depan/Mempawah Hilir2.jpg", width: 100%, height: 100%)
]

// ==========================================
// 3. HALAMAN KATALOG & HAK CIPTA (HALAMAN ii)
// ==========================================

// Judul Publikasi Langsung di Bagian Atas (Hitam)
#text(10.5pt, weight: "bold", fill: black)[KECAMATAN MEMPAWAH HILIR DALAM ANGKA 2026] \
#v(1pt)
#text(9pt, style: "italic", fill: black)[MEMPAWAH HILIR DISTRICT IN FIGURES 2026] \
#v(2pt)
#text(7.5pt, fill: black)[Volume 48, 2026]

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
  #text(weight: "bold")[Katalog/Catalogue:] 1102001.6104050
  #v(2pt)
  #text(weight: "bold")[Nomor Publikasi/Publication Number:] 61040.26012
]

#v(7pt)
#text(7.5pt)[
  #text(weight: "bold")[Ukuran Buku/Book Size:] 14,8 cm x 21,0 cm \
  #v(2pt)
  #text(weight: "bold")[Jumlah Halaman/Number of Pages:] #total_frontmatter_pages+#total_arabic_pages Halaman/Pages
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
  magnific.com, unsplash.com, BPS Kabupaten Mempawah
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
#v(0.6cm)

#align(center)[
  #text(10.5pt, weight: "bold")[TIM PENYUSUN/_COMPILERS_] \
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan Mempawah Hilir Dalam Angka 2026] \
  #text(8pt, style: "italic")[Mempawah Hilir District in Figures 2026] \
  #text(7.5pt)[Volume 48, 2026]
  
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
// 5. KONTRIBUTOR DATA (HALAMAN iv)
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
// 6. KATA PENGANTAR (HALAMAN v - INDONESIA)
// ==========================================
// ------------------------------------------
// KATA PENGANTAR (kata_pengantar)
// ------------------------------------------
#metadata("kata_pengantar") <kata_pengantar>

#block(width: 100%)[
  #text(11pt, weight: "bold", fill: rgb("#1F2937"))[KATA PENGANTAR]
  #v(3pt)
  #line(length: 4.5cm, stroke: 1.5pt + rgb("#FFA50C"))
]
#v(6pt)

#import "@preview/meander:0.2.2"

#let profile = (0.000, 0.000, 0.000, 0.541, 0.582, 0.602, 0.626, 0.639, 0.644, 0.644, 0.655, 0.651, 0.644, 0.624, 0.614, 0.626, 0.699, 0.781, 0.827, 0.842, 0.852, 0.861, 0.870, 0.879, 0.888, 0.897, 0.906, 0.915, 0.925, 0.927, 0.886, 0.882, 0.876, 0.861, 0.809, 0.800, 0.803, 0.808, 0.815, 0.819, 0.821, 0.822, 0.823, 0.823, 0.823, 0.823, 0.823, 0.823, 0.823, 0.823)

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
        image("/kegiatan/kecamatan-dalam-angka/2026/assets/kepala_bps.png", width: 100%, height: 100%)
      )
    )

    container()
    content[
      
        #text(fill: rgb("#EA580C"), weight: "bold")[Publikasi Kecamatan Mempawah Hilir Dalam Angka 2026] merupakan seri publikasi tahunan BPS Kabupaten Mempawah yang menyajikan beragam data statistik sektoral bersumber dari instansi pemerintah daerah, kantor camat, desa/kelurahan, serta survei dan sensus BPS. Publikasi ini memuat gambaran umum mengenai geografi, pemerintahan, serta perkembangan kondisi sosial-demografi dan perekonomian di wilayah Kecamatan Mempawah Hilir secara menyeluruh.

        #v(3.5pt)
        Data yang disajikan diharapkan dapat menjadi rujukan empiris dan indikator penting dalam mendukung perencanaan, pemantauan, serta evaluasi kebijakan pembangunan daerah demi terwujudnya Satu Data Indonesia. Seiring dinamika pembangunan dan kebutuhan data berkualitas, publikasi ini terus disempurnakan baik sistematika penyajian maupun visualisasinya.

        #v(3.5pt)
        Ucapan terima kasih dan penghargaan setinggi-tingginya kami sampaikan kepada Camat Mempawah Hilir, para Kepala Desa dan Lurah se-Kecamatan Mempawah Hilir, serta pimpinan Organisasi Perangkat Daerah atas koordinasi dan kontribusi data yang diberikan sehingga penyusunan publikasi ini selesai tepat waktu.

        #v(3.5pt)
        Kami menyadari publikasi ini masih memiliki ruang penyempurnaan. Oleh karena itu, saran dan masukan konstruktif sangat kami harapkan guna perbaikan edisi mendatang. Semoga publikasi ini memberikan manfaat nyata bagi seluruh pemangku kepentingan.

        #v(6pt)
        #align(right)[
          #block(width: 4.8cm)[
            #set align(left)
            Mempawah, September 2026 \
            Kepala BPS Kabupaten Mempawah \
            #v(3pt)
            #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 26pt) \
            #v(2pt)
            *MUNAWIR*
          ]
        ]
      
      #metadata("p") <page_marker>
    ]
  })
]

#pagebreak()

// ==========================================
// 7. PREFACE (HALAMAN vi - ENGLISH)
// ==========================================
// ------------------------------------------
// PREFACE (preface)
// ------------------------------------------
#metadata("preface") <preface>

#block(width: 100%)[
  #text(11pt, weight: "bold", style: "italic", fill: rgb("#1F2937"))[PREFACE]
  #v(3pt)
  #line(length: 4.5cm, stroke: 1.5pt + rgb("#FFA50C"))
]
#v(6pt)

#import "@preview/meander:0.2.2"

#let profile = (0.000, 0.000, 0.000, 0.541, 0.582, 0.602, 0.626, 0.639, 0.644, 0.644, 0.655, 0.651, 0.644, 0.624, 0.614, 0.626, 0.699, 0.781, 0.827, 0.842, 0.852, 0.861, 0.870, 0.879, 0.888, 0.897, 0.906, 0.915, 0.925, 0.927, 0.886, 0.882, 0.876, 0.861, 0.809, 0.800, 0.803, 0.808, 0.815, 0.819, 0.821, 0.822, 0.823, 0.823, 0.823, 0.823, 0.823, 0.823, 0.823, 0.823)

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
        image("/kegiatan/kecamatan-dalam-angka/2026/assets/kepala_bps.png", width: 100%, height: 100%)
      )
    )

    container()
    content[
      #text(style: "italic")[
        #text(fill: rgb("#EA580C"), weight: "bold")[Mempawah Hilir District in Figures 2026] is an annual publication series issued by BPS-Statistics of Mempawah Regency, presenting various sectoral statistical data sourced from regional government institutions, the subdistrict office, village administrations, as well as surveys and censuses conducted by BPS. This publication provides a comprehensive overview of geography, governance, and socio-demographic and economic development in Mempawah Hilir District.

        #v(3.5pt)
        The statistical indicators presented are expected to serve as essential empirical references to support evidence-based regional development planning, monitoring, and evaluation within the framework of Satu Data Indonesia (One Data Indonesia). In line with the growing need for high-quality data, this publication continues to be refined.

        #v(3.5pt)
        We would like to express our highest gratitude and appreciation to the Head of Mempawah Hilir District, Village Heads throughout Mempawah Hilir District, and all collaborating regional agencies for their valuable data contributions and seamless cooperation.

        #v(3.5pt)
        We realize that there is still room for improvement in this publication. Therefore, constructive suggestions and feedback are warmly welcomed to enhance future editions. It is our hope that this publication will be beneficial for policy makers, researchers, and the public.

        #v(6pt)
        #align(right)[
          #block(width: 4.8cm)[
            #set align(left)
            Mempawah, September 2026 \
            Chief Statistician of Mempawah Regency \
            #v(3pt)
            #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 26pt) \
            #v(2pt)
            #text(weight: "bold", style: "normal")[MUNAWIR]
          ]
        ]
      ]
      #metadata("p") <page_marker>
    ]
  })
]

#pagebreak()

// ==========================================
// 8. DAFTAR ISI / CONTENTS
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

#let toc_subchapter(no, id_title, en_title, page_val) = {
  grid(
    columns: (24pt, 1fr, auto),
    column-gutter: (4pt, 6pt),
    align: (top + left, top + left, bottom + right),
    [#no],
    [
      #id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
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
      #id_title/#text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
    [#page_val]
  )
}

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
// 9. DAFTAR TABEL / LIST OF TABLES
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
// 10. DAFTAR GAMBAR / LIST OF FIGURES
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
// 11. PENJELASAN UMUM / EXPLANATORY NOTES
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

#metadata("transisi_isi") <transisi_isi>
// --- TRANSISI KE ARABIC NUMBERING ---
#pagebreak(to: "odd")
#in_frontmatter.update(false)
#counter(page).update(1)

// ==========================================
// LEMBAR PEMBATAS BAB 1 (FULL-BLEED A5)
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/pembatas/Bab 1.jpg", width: 100%, height: 100%)
] <chapter_page>

#metadata("1. GEOGRAFI DAN IKLIM") <chapter_title>
#metadata("Geography and Climate") <chapter_title_en>
#metadata("bab1") <bab1>

// ==========================================
// BAB 1: GEOGRAFI DAN IKLIM (INFOGRAFIS & NARASI)
// ==========================================


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
  columns: (2.2fr, 1.1fr, 1.0fr, 1.3fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Luas Daerah] \ #text(6pt, weight: "bold", style: "italic")[Total Area (km²)]], [#strong[Persentase] \ #text(6pt, weight: "bold", style: "italic")[Percentage (%)]], [#strong[Status Batas] \ #text(6pt, weight: "bold", style: "italic")[Boundary Status]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Tanjung], [8,37], [5,43], [Indikatif],
  [Kuala Secapah], [10,42], [6,76], [Indikatif],
  [Tengah], [7,04], [4,57], [Indikatif],
  [Terusan], [6,74], [4,37], [Indikatif],
  [Pasir], [54,84], [35,58], [Indikatif],
  [Penibung], [11,59], [7,52], [Indikatif],
  [Sengkubang], [24,62], [15,98], [Indikatif],
  [Malikian], [30,50], [19,79], [Indikatif],
  [Kecamatan Mempawah Hilir/_Total_], [154,13], [100,00], []
)
#v(-2pt)
#text(6pt, fill: luma(60))[Catatan/#text(style: "italic")[Note] : Untuk desa/kelurahan dengan status Indikatif masih perlu dilakukan pelacakan ke lapangan dan kesepakatan batas antarwilayah yang berbatasan. / For villages/subdistricts with Indicative status, field tracking and boundary agreements between adjacent areas are still required.]
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[No]], [#strong[Nama Kota dan Tempat Penting] \ #text(6pt, weight: "bold", style: "italic")[Other Important Places]], [#strong[Jarak] \ #text(6pt, weight: "bold", style: "italic")[Distance (km)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]]),
  [1], [Ibukota Provinsi Kalimantan Barat 
(Kota Pontianak)], [63,00],
  [2], [Pusat Pemerintahan Kabupaten 
Mempawah (Mempawah Hilir)], [2,80],
  [3], [Makam Juang Mandor], [...]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kantor Camat Mempawah Hilir/#text(style: "italic")[Mempawah Hilir District Office]]
#v(8pt)


#pagebreak(to: "odd")

// ==========================================
// LEMBAR PEMBATAS BAB 2 (FULL-BLEED A5)
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/pembatas/Bab 2.jpg", width: 100%, height: 100%)
] <chapter_page>

#metadata("2. PEMERINTAHAN") <chapter_title>
#metadata("Government") <chapter_title_en>
#metadata("bab2") <bab2>

// ==========================================
// BAB 2: PEMERINTAHAN (INFOGRAFIS & NARASI)
// ==========================================


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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Jumlah Dusun] \ #text(6pt, weight: "bold", style: "italic")[Hamlets]], [#strong[Rukun Warga] \ #text(6pt, weight: "bold", style: "italic")[(RW)]], [#strong[Rukun Tetangga] \ #text(6pt, weight: "bold", style: "italic")[(RT)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Tanjung], [0], [3], [6],
  [Kuala Secapah], [4], [8], [15],
  [Tengah], [0], [8], [24],
  [Terusan], [0], [17], [41],
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
          #text(7.5pt, weight: "bold")[Tabel]
        ] \
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Tables]
      ],
      [
        #text(8.5pt, weight: "bold")[2.1.5]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Klasifikasi Desa/Kelurahan Perdesaan dan Perkotaan di Kecamatan Mempawah Hilir, 2024] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Urban and Rural Classification of Village/Subdistrict in Mempawah Hilir Subdistrict, 2024]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 2.2fr, 1.6fr, 1.6fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[No]], [#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Wilayah Administratif] \ #text(6pt, weight: "bold", style: "italic")[Administrative Area]], [#strong[Klasifikasi Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Urban/Rural Classification]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [1], [Tanjung], [Kelurahan], [Perdesaan],
  [2], [Kuala Secapah], [Desa], [Perkotaan],
  [3], [Tengah], [Kelurahan], [Perkotaan],
  [4], [Terusan], [Kelurahan], [Perkotaan],
  [5], [Pasir], [Desa], [Perkotaan],
  [6], [Penibung], [Desa], [Perdesaan],
  [7], [Sengkubang], [Desa], [Perdesaan],
  [8], [Malikian], [Desa], [Perdesaan]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Peraturan Kepala BPS No. 120 Tahun 2020 / Chief of BPS Regulation No. 120 of 2020/#text(style: "italic")[Peraturan Kepala BPS No. 120 Tahun 2020 / Chief of BPS Regulation No. 120 of 2020]]
#v(8pt)

#v(10pt)

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
    #text(7.5pt, weight: "bold")[Status Desa Berdasarkan Indeks Desa Membangun (IDM) di Kecamatan Mempawah Hilir, 2024] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Village Status Based on Developing Village Index (IDM) in Mempawah Hilir Subdistrict, 2024]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (0.6fr, 2.5fr, 2.5fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[No]], [#strong[Desa/Kelurahan] \ #text(6pt, weight: "bold", style: "italic")[Village/Subdistrict]], [#strong[Status Indeks Desa Membangun] \ #text(6pt, weight: "bold", style: "italic")[Developing Village Index Status]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]]),
  [1], [Tanjung], [–],
  [2], [Kuala Secapah], [Mandiri],
  [3], [Tengah], [–],
  [4], [Terusan], [–],
  [5], [Pasir], [Mandiri],
  [6], [Penibung], [Mandiri],
  [7], [Sengkubang], [Mandiri],
  [8], [Malikian], [Mandiri]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : Kementerian Desa, Pembangunan Daerah Tertinggal, dan Transmigrasi/#text(style: "italic")[Ministry of Villages, Disadvantaged Regions Development, and Transmigration]]
#v(8pt)

#pagebreak()


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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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

#v(10pt)

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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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


#pagebreak(to: "odd")

// ==========================================
// LEMBAR PEMBATAS BAB 3 (FULL-BLEED A5)
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/pembatas/Bab 3.jpg", width: 100%, height: 100%)
] <chapter_page>

#metadata("3. KEPENDUDUKAN") <chapter_title>
#metadata("Population") <chapter_title_en>
#metadata("bab3") <bab3>

// ==========================================
// BAB 3: KEPENDUDUKAN (INFOGRAFIS & NARASI)
// ==========================================


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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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


#pagebreak(to: "odd")

// ==========================================
// LEMBAR PEMBATAS BAB 4 (FULL-BLEED A5)
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/pembatas/Bab 4.jpg", width: 100%, height: 100%)
] <chapter_page>

#metadata("4. SOSIAL DAN KESEJAHTERAAN RAKYAT") <chapter_title>
#metadata("Social and Welfare") <chapter_title_en>
#metadata("bab4") <bab4>

// ==========================================
// BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT (INFOGRAFIS & NARASI)
// ==========================================

#v(8pt)

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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], [#strong[2023]], [#strong[2024]], [#strong[2025]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Taman Kanak-Kanak (TK)], [6], [6], [...],
  [Raudatul Athfal (RA)], [2], [0], [...],
  [Sekolah Dasar (SD)], [8], [8], [...],
  [Madrasah Ibtidaiyah (MI)], [7], [0], [...],
  [Sekolah Menengah Pertama (SMP)], [5], [7], [...],
  [Madrasah Tsanawiyah (MTs)], [6], [0], [...],
  [Sekolah Menengah Atas (SMA)], [2], [5], [...],
  [Sekolah Menengah Kejuruan (SMK)], [3], [3], [...],
  [Madrasah Aliyah (MA)], [3], [0], [...],
  [Akademi/Perguruan Tinggi], [1], [1], [...]
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
    #text(7.5pt, weight: "bold")[Jumlah Satuan Pendidikan Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2024/2025–2025/2026] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Educational Units by Education Level in Mempawah Hilir Subdistrict, 2024/2025–2025/2026]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], [#strong[Negeri] \ #text(6pt, weight: "bold", style: "italic")[Public]], [#strong[Swasta] \ #text(6pt, weight: "bold", style: "italic")[Private]], [#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Taman Kanak-Kanak (TK)1/Kindergarten1], [3], [5], [8],
  [Raudatul Athfal (RA)2], [0], [3], [3],
  [Sekolah Dasar (SD)1], [24], [2], [26],
  [Madrasah Ibtidaiyah], [0], [12], [12],
  [Sekolah Menengah Pertama (SMP)1], [4], [3], [7],
  [Madrasah Tsanawiyah (MTs)2], [1], [11], [12],
  [Sekolah Menengah Atas (SMA)1], [2], [0], [2],
  [Sekolah Menengah Kejuruan (SMK)1], [1], [3], [4],
  [Madrasah Aliyah (MA)2], [0], [7], [7]
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
    #text(7.5pt, weight: "bold")[Jumlah Kepala Sekolah dan Pendidik Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2024/2025–2025/2026] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Principals and Teachers by Education Level in Mempawah Hilir Subdistrict, 2024/2025–2025/2026]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], [#strong[Negeri] \ #text(6pt, weight: "bold", style: "italic")[Public]], [#strong[Swasta] \ #text(6pt, weight: "bold", style: "italic")[Private]], [#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Taman Kanak-Kanak], [16], [27], [43],
  [Raudatul Athfal (RA)2], [0], [13], [13],
  [Sekolah Dasar (SD)1,3], [237], [28], [265],
  [Madrasah Ibtidaiyah], [0], [139], [139],
  [Sekolah Menengah], [92], [20], [112],
  [Madrasah], [33], [126], [159],
  [Sekolah Menengah], [72], [0], [72],
  [Sekolah Menengah], [65], [26], [91],
  [Madrasah Aliyah (MA)2], [0], [96], [96]
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
    #text(7.5pt, weight: "bold")[Jumlah Peserta Didik Menurut Tingkat Pendidikan di Kecamatan Mempawah Hilir, 2024/2025–2025/2026] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Number of Students by Education Level in Mempawah Hilir Subdistrict, 2024/2025–2025/2026]
  ]
)
#v(3pt)
#show table.cell: set par(justify: false)
#table(
  columns: (2.5fr, 1.0fr, 1.0fr, 1.0fr),
  inset: (x: 3.5pt, y: 4.5pt),
  stroke: none,
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Tingkat Pendidikan] \ #text(6pt, weight: "bold", style: "italic")[Educational Level]], [#strong[Negeri] \ #text(6pt, weight: "bold", style: "italic")[Public]], [#strong[Swasta] \ #text(6pt, weight: "bold", style: "italic")[Private]], [#strong[Jumlah] \ #text(6pt, weight: "bold", style: "italic")[Total]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]]),
  [Taman Kanak-Kanak], [145], [270], [415],
  [Raudatul Athfal (RA)2], [0], [130], [130],
  [Sekolah Dasar (SD)1], [2.626], [429], [3.055],
  [Madrasah Ibtidaiyah], [0], [1828], [1828],
  [Sekolah Menengah], [1.331], [138], [1.469],
  [Madrasah], [614], [1397], [2011],
  [Sekolah Menengah], [1.369], [0], [1.369],
  [Sekolah Menengah], [1.016], [164], [1.180],
  [Madrasah Aliyah], [0], [1048], [1048]
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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


#pagebreak(to: "odd")

// ==========================================
// LEMBAR PEMBATAS BAB 5 (FULL-BLEED A5)
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/pembatas/Bab 5.jpg", width: 100%, height: 100%)
] <chapter_page>

#metadata("5. PERTANIAN") <chapter_title>
#metadata("Agriculture") <chapter_title_en>
#metadata("bab5") <bab5>

// ==========================================
// BAB 5: PERTANIAN (INFOGRAFIS & NARASI)
// ==========================================


#v(6pt)
#align(center)[
  #image("charts/gambar_5_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)/#text(style: "italic")[BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-BST)]]
#v(4pt)
#metadata("fig_5_1") <fig_5_1>
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
        #text(8.5pt, weight: "bold")[5.1]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[Produksi Buah-buahan Utama di Mempawah Hilir, 2025 (Kuintal)] \
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[Production of Major Fruits in Mempawah Hilir Subdistrict, 2025 (Quintal)]
  ]
)
#v(10pt)

#pagebreak()

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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (ha)]], [#strong[2023 (ha)]], [#strong[2024 (ha)]], [#strong[2025 (ha)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Bawang Merah/Shallots], [...], [...], [...], [...],
  [Cabai Besar/TW/Teropong Chili/Big Chili], [1], [1], [...], [...],
  [Cabai Keriting Curly Chili], [...], [...], [...], [...],
  [Cabai Rawit Chili/Cayenne Pepper], [2], [6], [5], [3],
  [Kentang/Potato], [...], [...], [...], [...],
  [Kubis/Cabbage], [...], [...], [...], [...],
  [Tomat/Tomato], [1], [1], [...], [...],
  [Bawang Putih/Garlic], [...], [...], [...], [...],
  [Bawang Daun/ Scallion], [3], [3], [2], [3],
  [Kacang Panjang/ Long Beans], [3], [3], [2], [2],
  [Ketimun/ Cucumber], [3], [2], [3], [1],
  [Petsai/Sawi/ Chinese Cabbage/mustard green], [13], [15], [11], [11],
  [Semangka/ Water Melon], [...], [3], [...], [1]
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (ku)]], [#strong[2023 (ku)]], [#strong[2024 (ku)]], [#strong[2025 (ku)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Bawang Merah/Shallots], [...], [...], [...], [...],
  [Cabai Besar/TW/Teropong Chili/Big Chili], [41], [67], [...], [...],
  [Cabai Keriting Curly Chili], [...], [...], [...], [...],
  [Cabai Rawit Chili/Cayenne Pepper], [78], [230], [66], [87],
  [Kentang/Potato], [...], [...], [...], [...],
  [Kubis/Cabbage], [...], [...], [...], [...],
  [Tomat/Tomato], [62], [45], [...], [...],
  [Bawang Putih/Garlic], [...], [...], [...], [...],
  [Bawang Daun/ Scallion], [144], [140], [87], [72],
  [Kacang Panjang/ Long Beans], [167], [183], [126], [112],
  [Ketimun/ Cucumber], [282], [161], [135], [128],
  [Petsai/Sawi/ Chinese Cabbage/mustard green], [290], [330], [328], [241],
  [Semangka/ Water Melon], [...], [550], [...], [150]
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (m²)]], [#strong[2023 (m²)]], [#strong[2024 (m²)]], [#strong[2025 (m²)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Jahe/Ginger], [14.000], [11.000], [12.000], [5.000],
  [Laos/Lengkuas/Galanga], [40], [10], [25], [12],
  [Kencur/East Indian Galangal], [20], [10], [7], [3],
  [Kunyit/Turmeric], [30], [10], [12], [...]
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (kg)]], [#strong[2023 (kg)]], [#strong[2024 (kg)]], [#strong[2025 (kg)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Jahe/Ginger], [30.500], [32.400], [36.000], [30.000],
  [Laos/Lengkuas/Galanga], [128], [28], [69], [39],
  [Kencur/East Indian Galangal], [20], [20], [19], [5],
  [Kunyit/Turmeric], [30], [10], [20], [...]
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
                      else if calc.even(row) { rgb("#FFF8E7") }
                      else { rgb("#FFF4D4") },
  align: (col, row) => if row <= 1 { center + horizon }
                       else if col == 0 { left + horizon }
                       else { right + horizon },
  table.header([#strong[Jenis Tanaman] \ #text(6pt, weight: "bold", style: "italic")[Kind of Plants]], [#strong[2022 (ku)]], [#strong[2023 (ku)]], [#strong[2024 (ku)]], [#strong[2025 (ku)]], [#strong[(1)]], [#strong[(2)]], [#strong[(3)]], [#strong[(4)]], [#strong[(5)]]),
  [Mangga/Mango], [1.650], [2.180], [...], [1250],
  [Durian/Durian], [1.570], [3.550], [525], [2620],
  [Jeruk Siam/Keprok/Orange/Tangerine], [5.260], [5.200], [3.900], [3.300],
  [Pisang/Banana], [233.579], [123.855], [60.307], [69.601],
  [Pepaya/Papaya], [308], [62], [106], [...],
  [Salak/Snakefruit], [30], [80], [3], [...],
  [Sawo/ Sapodilla/Sawo], [1.618], [1.478], [375], [525],
  [Rambutan/ Rambutan], [1.250], [893], [400], [875],
  [Jeruk Besar/ Pomelo], [453], [980], [15], [...],
  [Nangka/Cempedak/ Jackfruit], [455], [580], [100], [112],
  [Nenas/ Pineapple], [118.612], [77.670], [70.130], [86.682],
  [Lengkeng/ Dimocarpus Longan], [496], [560], [11], [...],
  [Sukun/ Breadfruit], [220], [630], [160], [...],
  [Jengkol/Jengkol], [420], [120], [118], [106],
  [Melinjo/ Gnetum/Melinjo], [575], [850], [443], [76],
  [Petai/ Twisted Cluster Bean], [400], [155], [145], [90]
)
#v(-3pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)/#text(style: "italic")[BPS-Statistics Indonesia - Ministry of Agriculture, Horticultural Agricultural Survey (SPH-BST)]]
#v(8pt)


#pagebreak(to: "odd")

// ==========================================
// LEMBAR PEMBATAS BAB 6 (FULL-BLEED A5)
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/pembatas/Bab 6.jpg", width: 100%, height: 100%)
] <chapter_page>

#metadata("6. PARIWISATA, TRANSPORTASI, DAN KOMUNIKASI") <chapter_title>
#metadata("Tourism, Transportation, and Communication") <chapter_title_en>
#metadata("bab6") <bab6>

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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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


#pagebreak(to: "odd")

// ==========================================
// LEMBAR PEMBATAS BAB 7 (FULL-BLEED A5)
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/pembatas/Bab 7.jpg", width: 100%, height: 100%)
] <chapter_page>

#metadata("7. PERBANKAN, KOPERASI, DAN PERDAGANGAN") <chapter_title>
#metadata("Banking, Cooperative, and Trade") <chapter_title_en>
#metadata("bab7") <bab7>

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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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
  fill: (col, row) => if row == 0 { cmyk(0%, 20%, 90%, 0%) }
                      else if row == 1 { cmyk(0%, 10%, 45%, 0%) }
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


#pagebreak(to: "odd")
#metadata("DAFTAR PUSTAKA") <chapter_title>
#metadata("Bibliography") <chapter_title_en>

// ==========================================
// DAFTAR PUSTAKA (BIBLIOGRAPHY)
// ==========================================
#v(0.5cm)
#block[
  #text(12pt, weight: "bold")[DAFTAR PUSTAKA] \
  #text(9pt, style: "italic", fill: rgb("#4B5563"))[BIBLIOGRAPHY]
] <chapter_page>
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
#pagebreak(to: "even")
// ==========================================
// KOVER BELAKANG (BACK COVER) - DESAIN VISUAL RESMI
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/belakang/Mempawah hilir.jpg", width: 100%, height: 100%)
]
