"""KCDA 2026 Typst Document Builder Engine (Orchestrator - A5 Template Pusat)."""

from typing import Dict, Any
from pathlib import Path
from .config import KCDA_KECAMATAN_CONFIG
from .chapters.frontmatter import render_frontmatter
from .chapters.chapter1 import render_chapter1
from .chapters.chapter2 import render_chapter2
from .chapters.chapter3 import render_chapter3
from .chapters.chapter4 import render_chapter4
from .chapters.chapter5 import render_chapter5
from .chapters.chapter6 import render_chapter6
from .chapters.chapter7 import render_chapter7
from .chapters.backcover import render_backcover

def build_kcda_typst(slug: str, out_dir: Any = None) -> str:
    """Menyusun kode dokumen Typst lengkap ukuran A5 sesuai Template Resmi KCDA 2026 BPS Pusat."""
    cfg = KCDA_KECAMATAN_CONFIG.get(slug)
    if not cfg:
        raise ValueError(f"Kecamatan slug '{slug}' tidak ditemukan di KCDA_KECAMATAN_CONFIG.")

    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"].replace(" Subdistrict", "")
    nama_singkat = nama_resmi.replace("Kecamatan ", "").strip()

    # Header & Footer Logic Typst untuk A5 (Sesuai Pedoman Publikasi BPS 2023 & Template Resmi KCDA 2026)
    header_logic = f"""
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
  header: context {{
    let p = here().page()
    let has_c = query(selector(<page_marker>)).any(m => {{
      let pos = m.location().position()
      pos.page == p and pos.y > 1.4cm and pos.y < 19.4cm
    }})
    let is_ch = query(selector(<chapter_page>)).any(m => m.location().page() == p)
    if has_c and not in_frontmatter.get() and not is_ch {{
      let page_num = counter(page).get().first()
      let titles = query(selector(<chapter_title>)).filter(m => m.location().page() <= p)
      let chapter_title = if titles.len() > 0 {{ titles.last().value }} else {{ "" }}
      if calc.even(page_num) {{
        // Halaman Genap (Verso/Kiri): Judul Publikasi Bahasa Indonesia (Metropolis, 8pt, running_title_color, bold)
        align(left, text(8pt, font: ("Metropolis", "Liberation Sans", "Arial"), fill: running_title_color, weight: "bold")[KECAMATAN {nama_singkat.upper()} DALAM ANGKA 2026])
      }} else {{
        // Halaman Ganjil (Rekto/Kanan): Judul Bab Bahasa Indonesia (Metropolis, 8pt, running_title_color, bold)
        let right_text = if chapter_title != "" {{ chapter_title }} else {{ "BPS KABUPATEN MEMPAWAH" }}
        align(right, text(8pt, font: ("Metropolis", "Liberation Sans", "Arial"), fill: running_title_color, weight: "bold")[#right_text])
      }}
    }}
  }},
  footer: context {{
    let p = here().page()
    let has_c = query(selector(<page_marker>)).any(m => {{
      let pos = m.location().position()
      pos.page == p and pos.y > 1.4cm and pos.y < 19.4cm
    }})
    let is_ch = query(selector(<chapter_page>)).any(m => m.location().page() == p)
    if not has_c or is_ch {{
      // Sesuai Pedoman Publikasi BPS 2023 Subbab 4.1.3 Poin 9 & Subbab 4.4.1 (Hal. 47, 88):
      // Lembar pembatas bab dihitung sebagai halaman arab tetapi TANPA running title dan TANPA nomor halaman fisik.
      // Halaman kosong sisipan juga TANPA running title dan nomor halaman fisik.
      none
    }} else if in_frontmatter.get() {{
      let page_num = counter(page).get().first()
      // Sesuai Pedoman Publikasi BPS 2023 Subbab 4.1.3 Poin 1 & 2 (Hal. 46) serta Subbab 4.3 (Hal. 75):
      // - Halaman i (Judul Utama), ii (Katalog), iii (Tim Penyusun), iv (Kontributor) TIDAK dicetak nomornya.
      // - Nomor fisik baru mulai dicetak pada Kata Pengantar (halaman v ke atas).
      // - Mengikuti prinsip Rekto-Verso baku: Kiri untuk Genap (Verso) dan Kanan untuk Ganjil (Rekto).
      if page_num >= 5 {{
        let display_val = counter(page).display("i")
        if calc.even(page_num) {{
          align(left + top, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#4B5563"), weight: "bold")[#v(3pt) #display_val])
        }} else {{
          align(right + top, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#4B5563"), weight: "bold")[#v(3pt) #display_val])
        }}
      }}
    }} else {{
      let page_num = counter(page).get().first()
      let display_val = counter(page).display("1")
      let titles_en = query(selector(<chapter_title_en>)).filter(m => m.location().page() <= p)
      let chapter_en = if titles_en.len() > 0 {{ titles_en.last().value }} else {{ "" }}
      if calc.even(page_num) {{
        // Halaman Genap (Verso/Kiri): Badge No Halaman di kiri + Judul Publikasi Bahasa Inggris (Metropolis, 8pt, running_title_color, italic)
        grid(
          columns: (auto, auto),
          align: horizon,
          column-gutter: 8pt,
          page_badge(display_val),
          text(8pt, font: ("Metropolis", "Liberation Sans", "Arial"), style: "italic", fill: running_title_color)[{nama_en.upper()} DISTRICT IN FIGURES 2026]
        )
      }} else {{
        // Halaman Ganjil (Rekto/Kanan): Judul Bab Bahasa Inggris + Badge No Halaman di kanan (Metropolis, 8pt, running_title_color, italic)
        let right_en_text = if chapter_en != "" {{ upper(chapter_en) }} else {{ "{nama_en.upper()} DISTRICT IN FIGURES 2026" }}
        grid(
          columns: (1fr, auto),
          align: horizon,
          column-gutter: 8pt,
          align(right, text(8pt, font: ("Metropolis", "Liberation Sans", "Arial"), style: "italic", fill: running_title_color)[#right_en_text]),
          page_badge(display_val)
        )
      }}
    }}
  }}
)

#set text(font: ("Myriad Pro", "Liberation Sans", "Arial"), size: 7.5pt, lang: "id")
#set par(justify: true, leading: 0.5em)

// Matikan justify pada seluruh sel tabel agar spasi antar kata di header & data tabel tidak meregang
#show table.cell: set par(justify: false)

// Standarisasi Penulisan Judul Gambar BPS (Di Bawah Gambar tanpa prefix dobel)
#show figure.where(kind: image): set figure(supplement: none)
#show figure.where(kind: image): set figure.caption(separator: none)
"""

    daftar_pustaka_markup = f"""
// ==========================================
// DAFTAR PUSTAKA (BIBLIOGRAPHY)
// ==========================================
#v(0.5cm)
#block[
  #text(12pt, weight: "bold")[DAFTAR PUSTAKA] \\
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
"""

    parts = [
        "// Publikasi Resmi BPS Kabupaten Mempawah: Kecamatan Dalam Angka 2026 (Ukuran A5)",
        header_logic,
        render_frontmatter(cfg),
        '#metadata("transisi_isi") <transisi_isi>',
        "// --- TRANSISI KE ARABIC NUMBERING ---",
        '#pagebreak(to: "odd")',
        '#in_frontmatter.update(false)',
        '#metadata("1. GEOGRAFI DAN IKLIM") <chapter_title>',
        '#metadata("Geography and Climate") <chapter_title_en>',
        "#counter(page).update(1)",
        '#metadata("bab1") <bab1>',
        render_chapter1(cfg, out_dir),
        '#pagebreak(to: "odd")',
        '#metadata("2. PEMERINTAHAN") <chapter_title>',
        '#metadata("Government") <chapter_title_en>',
        '#metadata("bab2") <bab2>',
        render_chapter2(cfg, out_dir),
        '#pagebreak(to: "odd")',
        '#metadata("3. KEPENDUDUKAN") <chapter_title>',
        '#metadata("Population") <chapter_title_en>',
        '#metadata("bab3") <bab3>',
        render_chapter3(cfg, out_dir),
        '#pagebreak(to: "odd")',
        '#metadata("4. SOSIAL DAN KESEJAHTERAAN RAKYAT") <chapter_title>',
        '#metadata("Social and Welfare") <chapter_title_en>',
        '#metadata("bab4") <bab4>',
        render_chapter4(cfg, out_dir),
        '#pagebreak(to: "odd")',
        '#metadata("5. PERTANIAN") <chapter_title>',
        '#metadata("Agriculture") <chapter_title_en>',
        '#metadata("bab5") <bab5>',
        render_chapter5(cfg, out_dir),
        '#pagebreak(to: "odd")',
        '#metadata("6. PARIWISATA, TRANSPORTASI, DAN KOMUNIKASI") <chapter_title>',
        '#metadata("Tourism, Transportation, and Communication") <chapter_title_en>',
        '#metadata("bab6") <bab6>',
        render_chapter6(cfg),
        '#pagebreak(to: "odd")',
        '#metadata("7. PERBANKAN, KOPERASI, DAN PERDAGANGAN") <chapter_title>',
        '#metadata("Banking, Cooperative, and Trade") <chapter_title_en>',
        '#metadata("bab7") <bab7>',
        render_chapter7(cfg),
        '#pagebreak(to: "odd")',
        '#metadata("DAFTAR PUSTAKA") <chapter_title>',
        '#metadata("Bibliography") <chapter_title_en>',
        daftar_pustaka_markup,
        '#metadata("akhir_buku") <akhir_buku>',
        '#pagebreak(to: "even")',
        render_backcover(cfg)
    ]

    return "\n".join(parts)
