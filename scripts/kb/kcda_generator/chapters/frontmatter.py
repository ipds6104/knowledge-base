"""Frontmatter generator for KCDA 2026 strictly following BPS Pusat DOCX template and layout."""

from typing import Dict, Any

def render_frontmatter(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    no_pub = cfg["no_publikasi"]
    no_katalog = cfg["no_katalog"]
    pic_polos = cfg["pic_nama_polos"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "").strip()
    issn = cfg.get("issn", "2477-6777")
    volume = cfg.get("volume", "Volume 48, 2026")

    return f"""
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
      #text(style: "italic")[Katalog/Catalogue:] \\
      #text(weight: "bold")[{no_katalog}] \\
      #text(style: "italic")[ISSN xxxx-xxxx]
    ]
  ]

  #v(0.8cm)

  // Judul Publikasi di Tengah Atas
  #align(center)[
    #text(16pt, weight: "bold", fill: white)[KECAMATAN {nama_singkat.upper()}] \\
    #v(2pt)
    #text(15pt, weight: "bold", fill: white)[DALAM ANGKA] \\
    #v(4pt)
    #text(11pt, style: "italic", fill: rgb("#F3F4F6"))[{nama_en} District in Figures] \\
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
        #text(28pt)[📷] \\
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
        #text(8pt, weight: "bold", fill: white)[BADAN PUSAT STATISTIK] \\
        #text(8pt, weight: "bold", fill: white)[KABUPATEN MEMPAWAH] \\
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
    #text(style: "italic")[Katalog/Catalogue:] {no_katalog} \\
    ISSN: {issn}
  ]
]

#v(1fr)

#text(16pt, weight: "bold")[KECAMATAN {nama_singkat.upper()}] \\
#v(2pt)
#text(16pt, weight: "bold")[DALAM ANGKA] \\
#v(4pt)
#text(11.5pt, style: "italic", fill: rgb("#F5A623"))[{nama_en} District in Figures] \\
#v(3pt)
#text(9pt, weight: "medium")[{volume}]

#v(14pt)

#grid(
  columns: (auto, auto),
  column-gutter: 8pt,
  align: horizon,
  image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", height: 26pt),
  align(left)[
    #text(8pt, weight: "bold", fill: rgb("#00A0E9"))[BADAN PUSAT STATISTIK] \\
    #text(8pt, weight: "bold", fill: rgb("#00A0E9"))[KABUPATEN MEMPAWAH] \\
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
    #text(8pt, weight: "bold", fill: rgb("#00A0E9"))[BADAN PUSAT STATISTIK] \\
    #text(8pt, weight: "bold", fill: rgb("#00A0E9"))[KABUPATEN MEMPAWAH] \\
    #text(6.5pt, fill: rgb("#00A0E9"))[BPS-STATISTICS OF MEMPAWAH REGENCY]
  ]
)

#v(2pt)
#line(length: 100%, stroke: 0.5pt + rgb("#D1D5DB"))

#v(8pt)
#text(10.5pt, weight: "bold")[KECAMATAN {nama_singkat.upper()} DALAM ANGKA] \\
#text(9.5pt, style: "italic")[{nama_en} District in Figures] \\
#text(9.5pt)[2026] \\
#text(8pt, fill: luma(100))[{volume}]

#let total_frontmatter_pages = context {{
  let elems = query(<transisi_isi>)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("i", p)
  }} else {{
    "x"
  }}
}}
#let total_arabic_pages = context {{
  let elems = query(<akhir_buku>)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("1", p)
  }} else {{
    "28"
  }}
}}

#v(8pt)
#grid(
  columns: (1fr, 1.2fr),
  row-gutter: 5pt,
  [*Katalog/_Catalogue_:*], [{no_katalog}],
  [*ISSN:*], [{issn}],
  [*Nomor Publikasi/_Publication Number_:*], [{no_pub}],
  [], [],
  [*Ukuran Buku/_Book Size_:*], [14,8 cm x 21 cm],
  [*Jumlah Halaman/_Number of Pages_:*], [#total_frontmatter_pages + #total_arabic_pages hal/pages],
  [], [],
  [*Penyusun Naskah/_Manuscript Drafter_:*], [BPS Kabupaten Mempawah \\ _BPS-Statistics of Mempawah Regency_],
  [*Penyunting/_Editor_:*], [BPS Kabupaten Mempawah \\ _BPS-Statistics of Mempawah Regency_],
  [*Pembuat Kover/_Cover Designer_:*], [BPS Kabupaten Mempawah \\ _BPS-Statistics of Mempawah Regency_],
  [*Penerbit/_Publisher_:*], [© BPS Kabupaten Mempawah/_BPS-Statistics of Mempawah Regency_],
  [*Sumber Ilustrasi/_Illustration Source_:*], [-]
)

#v(10pt)
#text(6.5pt)[
  *Dilarang mereproduksi dan/atau menggandakan sebagian atau seluruh isi buku ini untuk tujuan komersial tanpa izin tertulis dari Badan Pusat Statistik Kabupaten Mempawah.* \\
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
  #text(10.5pt, weight: "bold")[TIM PENYUSUN/_COMPILERS_] \\
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan {nama_singkat} Dalam Angka 2026] \\
  #text(8pt, style: "italic")[{nama_en} District in Figures 2026] \\
  #text(7.5pt)[Volume xx, 2026]
  
  #v(16pt)
  #text(8.5pt, weight: "bold")[Pengarah/_Director_] \\
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penanggung Jawab/_Persons in Charge_] \\
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penyunting/_Editors_] \\
  #text(8pt)[Kurniawan #sym.circle.filled.small Sukma Andini]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Pengolah Data dan Penulis Naskah/_Data Processor and Writers_] \\
  #text(8pt)[{pic_polos}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penata Letak/_Layouters_] \\
  #text(8pt)[Tim IPDS BPS Kabupaten Mempawah]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penerjemah/_Translators_] \\
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
+ Kantor Camat {nama_singkat}/#text(style: "italic")[{nama_singkat} District Office]
+ Kementerian Agama/#text(style: "italic")[Ministry of Religious Affairs]
+ Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi/#text(style: "italic")[Ministry of Education, Culture, Research, and Technology]
+ Badan Pusat Statistik/#text(style: "italic")[BPS-Statistics Indonesia]
+ Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah/#text(style: "italic")[Population and Civil Registration Service of Mempawah Regency]
+ Dinas Pendidikan, Pemuda, Olahraga dan Pariwisata Kabupaten Mempawah/#text(style: "italic")[Education, Youth, Sports, and Tourism Office of Mempawah Regency]
+ Dinas Pertanian, Ketahanan Pangan dan Perikanan Kabupaten Mempawah/#text(style: "italic")[Agriculture, Food Security, and Fisheries Office of Mempawah Regency]
+ Dinas Kesehatan, Pengendalian Penduduk dan Keluarga Berencana Kabupaten Mempawah/#text(style: "italic")[Health, Population Control, and Family Planning Office of Mempawah Regency]
+ Dinas Perindustrian, Perdagangan dan Tenaga Kerja Kabupaten Mempawah/#text(style: "italic")[Industry, Trade, and Manpower Office of Mempawah Regency]
+ Bagian Tata Pemerintahan Sekretariat Daerah Kabupaten Mempawah/#text(style: "italic")[Governance Division of Regional Secretariat of Mempawah Regency]
+ Pemerintah Desa/Kelurahan se-Kecamatan {nama_singkat}/#text(style: "italic")[Village/Subdistrict Administrations throughout {nama_singkat} District]
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
  Publikasi *Kecamatan {nama_singkat} Dalam Angka 2026* merupakan seri publikasi tahunan BPS Kabupaten Mempawah yang menyajikan beragam data statistik sektoral bersumber dari instansi pemerintah daerah, kantor camat, desa/kelurahan, serta survei dan sensus BPS. Publikasi ini memuat gambaran umum mengenai geografi, pemerintahan, serta perkembangan kondisi sosial-demografi dan perekonomian di wilayah Kecamatan {nama_singkat}.

  #v(5pt)
  Data yang disajikan diharapkan dapat menjadi rujukan empiris dan indikator penting dalam mendukung perencanaan, pemantauan, serta evaluasi kebijakan pembangunan daerah demi terwujudnya Satu Data Indonesia.

  #v(5pt)
  Ucapan terima kasih dan penghargaan setinggi-tingginya disampaikan kepada Camat {nama_singkat}, para Kepala Desa/Lurah se-Kecamatan {nama_singkat}, serta pimpinan instansi dinas/lembaga atas koordinasi dan kontribusi data yang diberikan dalam penyusunan buku ini.

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
        Mempawah, September 2026 \\
        Kepala BPS Kabupaten Mempawah \\
        #v(4pt)
        #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 38pt) \\
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
  *{nama_en} District in Figures 2026* is an annual publication series issued by BPS-Statistics of Mempawah Regency, presenting various sectoral statistical data sourced from regional government institutions, the subdistrict office, village administrations, as well as surveys and censuses conducted by BPS. This publication provides a comprehensive overview of geography, governance, and the socio-demographic and economic development in {nama_en} District.

  #v(5pt)
  The statistical indicators presented are expected to serve as essential empirical references to support evidence-based regional development planning, monitoring, and evaluation within the framework of Satu Data Indonesia (One Data Indonesia).

  #v(5pt)
  We would like to express our highest gratitude and appreciation to the Head of {nama_en} District, Village Heads throughout {nama_en} District, and all collaborating regional agencies for their valuable data contributions and seamless cooperation.

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
        Mempawah, September 2026 \\
        Chief Statistician of Mempawah Regency \\
        #v(4pt)
        #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 38pt) \\
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

#let get_page_roman(lbl, default: "-") = context {{
  let elems = query(lbl)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("i", p)
  }} else {{
    default
  }}
}}

#let get_page_arabic(lbl, default: "-") = context {{
  let elems = query(lbl)
  if elems.len() > 0 {{
    let loc = elems.first().location()
    let p = counter(page).at(loc).first()
    numbering("1", p)
  }} else {{
    default
  }}
}}

// Helper functions for Dot Leaders
#let toc_chapter(no, id_title, en_title, page_val) = {{
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
}}

#let toc_section(title_markup, page_val) = {{
  grid(
    columns: (1fr, auto),
    column-gutter: 6pt,
    align: (bottom + left, bottom + right),
    [#title_markup #box(width: 1fr, repeat[ . ])],
    [#page_val]
  )
}}

#let toc_entry_item(no, id_title, en_title, page_val) = {{
  grid(
    columns: (24pt, 1fr, auto),
    column-gutter: (4pt, 6pt),
    align: (top + left, top + left, bottom + right),
    [#no],
    [
      #id_title \\
      #text(style: "italic")[#en_title] #box(width: 1fr, repeat[ . ])
    ],
    [#page_val]
  )
}}

#align(right)[#text(7pt)[ISSN: {issn}]]
#v(4pt)

#align(center)[
  #text(10pt, weight: "bold")[DAFTAR ISI/CONTENTS] \\
  #v(2pt)
  #text(9pt, weight: "bold")[Kecamatan {nama_singkat} Dalam Angka 2026] \\
  #text(8.5pt, style: "italic")[{nama_en} District in Figures 2026] \\
  #v(1pt)
  #text(7.5pt)[{volume}]
]

#v(8pt)
#align(right)[
  #text(7.5pt)[Halaman] \\
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
  [*Tabel*\\ _Table_], [], [*Halaman*\\ _Page_]
)
#v(6pt)

#toc_entry_item("1.1", "Luas Daerah Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Total Area by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<tab_1_1>))
#v(5pt)
#toc_entry_item("1.2", "Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Distance to Subdistrict and Regency Capital by Village in {nama_en} District, 2025", get_page_arabic(<tab_1_2>))
#v(5pt)
#toc_entry_item("1.3", "Batas Administrasi Kecamatan {nama_singkat} Menurut Arah Mata Angin, 2025", "Administrative Borders of {nama_en} District by Cardinal Direction, 2025", get_page_arabic(<tab_1_3>))
#v(5pt)
#toc_entry_item("1.4", "Jarak Kantor Camat {nama_singkat} dengan Kota dan Tempat Penting Lainnya, 2025", "Distance from {nama_singkat} Subdistrict Office to Other Important Places, 2025", get_page_arabic(<tab_1_4>))
#v(5pt)
#toc_entry_item("2.1.1", "Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Number of Hamlets, RW, and RT by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<tab_2_1_1>))
#v(5pt)
#toc_entry_item("2.1.2", "Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan {nama_singkat}", "Names of District Heads of {nama_en} District", get_page_arabic(<tab_2_1_2>))
#v(5pt)
#toc_entry_item("2.1.3", "Nama-Nama Kepala Desa di Kecamatan {nama_singkat}, 2025", "Names of Village Heads in {nama_en} District, 2025", get_page_arabic(<tab_2_1_3>))
#v(5pt)
#toc_entry_item("3.1", "Penduduk, Distribusi Persentase, Kepadatan, dan Rasio Jenis Kelamin Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Population, Percentage Distribution, Density, and Sex Ratio by Village in {nama_en} District, 2025", get_page_arabic(<tab_3_1>))
#v(5pt)
#toc_entry_item("4.1.1", "Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan {nama_singkat}, 2023–2025", "Number of Villages Having Educational Facilities by Level in {nama_en} District, 2023–2025", get_page_arabic(<tab_4_1_1>))
#v(5pt)
#toc_entry_item("4.2.1", "Banyaknya Sarana Kesehatan Menurut Jenis Sarana di Kecamatan {nama_singkat}, 2023–2025", "Number of Health Facilities by Type in {nama_en} District, 2023–2025", get_page_arabic(<tab_4_2_1>))
#v(5pt)
#toc_entry_item("5.1", "Luas Panen Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis di Kecamatan {nama_singkat} (ha), 2022–2025", "Harvested Area of Vegetables and Seasonal Fruits by Type in {nama_en} District (ha), 2022–2025", get_page_arabic(<tab_5_1>))
#v(5pt)
#toc_entry_item("6.1.1", "Keberadaan Sarana Akomodasi Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Accommodation Facilities by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<tab_6_1_1>))
#v(5pt)
#toc_entry_item("7.1", "Keberadaan Lembaga Keuangan Bank Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Banking Financial Institutions by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<tab_7_1>))

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
  [*Gambar*\\ _Figure_], [], [*Halaman*\\ _Page_]
)
#v(6pt)

#toc_entry_item("1.1", "Jarak dari Desa/Kelurahan ke Ibukota Kecamatan di Kecamatan {nama_singkat}, 2025", "Distance from Village/Subdistrict to District Capital in {nama_en} District, 2025", get_page_arabic(<fig_1_1>))
#v(5pt)
#toc_entry_item("1.2", "Luas Wilayah Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Total Area by Village/Subdistrict in {nama_en} District, 2025", get_page_arabic(<fig_1_2>))
#v(5pt)
#toc_entry_item("2.1", "Jumlah Rukun Tetangga (RT) Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Number of RT by Village in {nama_en} District, 2025", get_page_arabic(<fig_2_1>))
#v(5pt)
#toc_entry_item("3.1", "Jumlah Penduduk Menurut Jenis Kelamin di Kecamatan {nama_singkat}, 2025", "Population by Sex in {nama_en} District, 2025", get_page_arabic(<fig_3_1>))
#v(5pt)
#toc_entry_item("4.1", "Banyaknya Fasilitas Sekolah Menurut Tingkat Pendidikan di Kecamatan {nama_singkat}, 2025", "Number of School Facilities by Level in {nama_en} District, 2025", get_page_arabic(<fig_4_1>))
#v(5pt)
#toc_entry_item("5.1", "Produksi Tanaman Hortikultura Unggulan di Kecamatan {nama_singkat}, 2025", "Production of Leading Horticulture Crops in {nama_en} District, 2025", get_page_arabic(<fig_5_1>))
#v(5pt)
#toc_entry_item("6.1", "Prasarana dan Sarana Komunikasi Menurut Desa/Kelurahan di Kecamatan {nama_singkat}, 2025", "Communication Infrastructure by Village in {nama_en} District, 2025", get_page_arabic(<fig_6_1>))
#v(5pt)
#toc_entry_item("7.1", "Keberadaan Sarana Perdagangan dan Koperasi Aktif di Kecamatan {nama_singkat}, 2025", "Trading Facilities and Active Cooperatives in {nama_en} District, 2025", get_page_arabic(<fig_7_1>))

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
Tanda-tanda khusus, singkatan, serta kesepakatan penulisan yang digunakan dalam publikasi ini adalah sebagai berikut: \\
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
Catatan Pembulatan: Karena adanya pembulatan, angka-angka dalam penjumlahan baris/kolom mungkin tidak selalu sama persis dengan total penjumlahan. \\
_Rounding Note: Due to rounding, figures in line/column totals may not strictly equal the sum of constituent elements._
]
"""
