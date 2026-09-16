"""
Frontmatter: Cover & Title Page for KCDA 2026.
Menangani Kover Depan dan Halaman Judul Utama (Halaman i).
"""

from typing import Dict, Any

def render_cover_and_title_page(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    no_katalog = cfg["no_katalog"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "").strip()
    issn = cfg.get("issn")
    volume = cfg.get("volume", "Volume 48, 2026")

    issn_front = f" \\\\\n      #text(style: \"italic\")[ISSN {issn}]" if issn else ""
    issn_title = f" \\\\\n    ISSN: {issn}" if issn else ""

    return f"""// ==========================================
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
      #text(weight: "bold")[{no_katalog}]{issn_front}
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
    #text(8.5pt, fill: rgb("#E5E7EB"))[{volume}]
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
      width: 100%,
      height: 7.5cm,
      fill: rgb(255, 255, 255, 12%),
      radius: 4pt,
      stroke: 0.5pt + rgb(255, 255, 255, 30%),
    )[
      #align(center + horizon)[
        #image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", height: 48pt) \\
        #v(8pt)
        #text(9pt, weight: "bold", fill: rgb("#E5E7EB"))[COVER DEPAN] \\
        #text(7pt, fill: rgb("#D1D5DB"))[Kecamatan {nama_singkat} Dalam Angka 2026]
      ]
    ]
  ]

  #v(1fr)

  // Logo & Identitas Resmi BPS di Kiri Bawah
  #align(left)[
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

// ==========================================
// HALAMAN KOSONG DI BALIK KOVER DEPAN (INSIDE COVER / FLYLEAF)
// Sesuai Pedoman Pembuatan Publikasi BPS 2023 Subbab 4.1.2 Poin 6 (Hal. 45) & Terbitan Statistik Indonesia BPS RI.
// Halaman setelah kover depan tidak dihitung sebagai halaman dan tidak diberi nomor halaman.
// ==========================================
#page(header: none, footer: none)[ ]

// ==========================================
// 2. HALAMAN JUDUL UTAMA / TITLE PAGE (HALAMAN i)
// Terletak pada halaman ganjil (rekto/kanan) sesuai Pedoman Publikasi BPS 2023 Subbab 4.3.1 (Hal. 75).
// Perhitungan angka romawi resmi dimulai pada Halaman Judul Utama (halaman i).
// ==========================================
#counter(page).update(1)

#align(right)[
  #text(7.5pt)[
    #text(style: "italic")[Katalog/Catalogue:] {no_katalog}{issn_title}
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
"""
