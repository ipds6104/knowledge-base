"""Frontmatter generator for KCDA 2026 strictly following BPS Pusat DOCX template and layout."""

from typing import Dict, Any

def render_frontmatter(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    no_pub = cfg["no_publikasi"]
    no_katalog = cfg["no_katalog"]
    pic_polos = cfg["pic_nama_polos"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "").strip()

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
// 2. HALAMAN KATALOG & HAK CIPTA (HALAMAN ii)
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
#text(8pt, fill: luma(100))[Volume xx, 2026]

#v(8pt)
#grid(
  columns: (1fr, 1.2fr),
  row-gutter: 5pt,
  [*Katalog/Catalogue:*], [{no_katalog}],
  [*ISSN:*], [-],
  [*Nomor Publikasi/Publication Number:*], [{no_pub}],
  [], [],
  [*Ukuran Buku/Book Size:*], [14,8 cm x 21 cm],
  [*Jumlah Halaman/Number of Pages:*], [viii + 35 hal/pages],
  [], [],
  [*Penyusun Naskah/Manuscript Drafter:*], [BPS Kabupaten Mempawah \\ BPS-Statistics of Mempawah Regency],
  [*Penyunting/Editor:*], [BPS Kabupaten Mempawah \\ BPS-Statistics of Mempawah Regency],
  [*Pembuat Kover/Cover Designer:*], [BPS Kabupaten Mempawah \\ BPS-Statistics of Mempawah Regency],
  [*Penerbit/Publisher:*], [© BPS Kabupaten Mempawah/BPS-Statistics of Mempawah Regency],
  [*Sumber Ilustrasi/Illustration Source:*], [-]
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
  #text(10.5pt, weight: "bold")[TIM PENYUSUN/COMPILERS] \\
  #v(2pt)
  #text(8.5pt, weight: "bold")[Kecamatan {nama_singkat} Dalam Angka 2026] \\
  #text(8pt, style: "italic")[{nama_en} District in Figures 2026] \\
  #text(7.5pt)[Volume xx, 2026]
  
  #v(16pt)
  #text(8.5pt, weight: "bold")[Pengarah/Director] \\
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penanggung Jawab/Persons in Charge] \\
  #text(8pt)[Munawir]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penyunting/Editors] \\
  #text(8pt)[Kurniawan #sym.circle.filled.small Sukma Andini]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Pengolah Data dan Penulis Naskah/Data Processor and Writers] \\
  #text(8pt)[{pic_polos}]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penata Letak/Layouters] \\
  #text(8pt)[Tim IPDS BPS Kabupaten Mempawah]
  
  #v(11pt)
  #text(8.5pt, weight: "bold")[Penerjemah/Translators] \\
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
  [Kantor Camat {nama_singkat}],
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
      Publikasi *Kecamatan {nama_singkat} Dalam Angka 2026* merupakan seri tahunan BPS Kabupaten Mempawah yang menyajikan beragam data dari BPS, kecamatan, kelurahan/desa, serta instansi terkait. Publikasi ini memuat gambaran umum mengenai geografi, pemerintahan, serta kondisi sosial demografi dan perekonomian di Kecamatan {nama_singkat}.

      Data yang disajikan diharapkan dapat menjadi indikator penting dalam mendukung perencanaan dan pengambilan kebijakan pembangunan daerah berbasis data akurat.

      Ucapan terima kasih disampaikan kepada Camat {nama_singkat}, para Lurah/Kepala Desa se-Kecamatan {nama_singkat}, serta seluruh pihak yang telah membantu dalam penyusunan publikasi ini. Kritik dan saran membangun sangat kami harapkan demi penyempurnaan edisi berikutnya.
    ]
  ],
  [
    #text(7.5pt, style: "italic")[
      *"{nama_en} District in Figures 2026"* is an annual series issued by BPS-Statistics of Mempawah Regency, presenting various data collected from BPS, subdistrict offices, villages/urban villages, and related regional agencies. This publication provides a comprehensive overview of geography, governance, as well as social, demographic, and economic conditions across villages in {nama_en} District.

      The data presented are expected to serve as vital empirical indicators to support evidence-based regional development planning and policy-making.

      We express our sincere gratitude to the Head of {nama_en} District, village heads, and all collaborating institutions. Constructive feedback is warmly appreciated for continuous refinement.
    ]
  ]
)

#v(14pt)
#align(right)[
  #block(width: 60%)[
    #text(7.5pt)[
      Mempawah, September 2026 \\
      *Kepala BPS Kabupaten Mempawah* \\
      _Chief Statistician of Mempawah Regency_ \\
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
"""
