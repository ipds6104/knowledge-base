"""KCDA 2026 Typst Document Builder Engine (Orchestrator - A5 Template Pusat)."""

from typing import Dict, Any
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
    nama_singkat = nama_resmi.replace("Kecamatan ", "").strip()

    # Header & Footer Logic Typst untuk A5 (Sesuai Pedoman Publikasi BPS 2023 & Template KCDA 2026)
    header_logic = f"""
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
  header: context {{
    if not in_frontmatter.get() and not is_chapter_page.get() {{
      let page_num = counter(page).get().first()
      let chapter_title = active_chapter.get()
      if calc.even(page_num) {{
        align(left, text(6.5pt, font: ("Metropolis", "Liberation Sans", "Arial"), fill: rgb("#374151"), weight: "bold")[KECAMATAN {nama_singkat.upper()} DALAM ANGKA 2026])
      }} else {{
        let right_text = if chapter_title != "" {{ chapter_title }} else {{ "BPS KABUPATEN MEMPAWAH" }}
        align(right, text(6.5pt, font: ("Metropolis", "Liberation Sans", "Arial"), fill: rgb("#374151"), weight: "bold")[#right_text])
      }}
    }}
  }},
  footer: context {{
    let page_num = counter(page).get().first()
    if in_frontmatter.get() {{
      // Sesuai Pedoman Publikasi BPS 2023 & Aturan KCDA 2026:
      // Halaman i (Judul Utama), ii (Katalog), iii (Tim Penyusun), iv (Kontributor) TIDAK dicantumkan nomor halamannya
      // Nomor halaman fisik baru mulai dicetak pada Kata Pengantar (halaman v)
      if page_num >= 5 {{
        let display_val = counter(page).display("i")
        align(center, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#4B5563"), weight: "bold")[#display_val])
      }}
    }} else {{
      let display_val = counter(page).display("1")
      if calc.even(page_num) {{
        align(left, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#1F2937"), weight: "bold")[#display_val])
      }} else {{
        align(right, text(7.5pt, font: ("Myriad Pro", "Liberation Sans", "Arial"), fill: rgb("#1F2937"), weight: "bold")[#display_val])
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
"""

    parts = [
        "// Publikasi Resmi BPS Kabupaten Mempawah: Kecamatan Dalam Angka 2026 (Ukuran A5)",
        header_logic,
        render_frontmatter(cfg),
        "// --- TRANSISI KE ARABIC NUMBERING ---",
        '#metadata("transisi_isi") <transisi_isi>',
        '#in_frontmatter.update(false)',
        '#active_chapter.update("1. GEOGRAFI DAN IKLIM")',
        '#is_chapter_page.update(true)',
        '#pagebreak()',
        "#counter(page).update(1)",
        '#metadata("bab1") <bab1>',
        render_chapter1(cfg, out_dir),
        '#active_chapter.update("2. PEMERINTAHAN")',
        '#is_chapter_page.update(true)',
        '#pagebreak()',
        '#metadata("bab2") <bab2>',
        render_chapter2(cfg, out_dir),
        '#active_chapter.update("3. KEPENDUDUKAN")',
        '#is_chapter_page.update(true)',
        '#pagebreak()',
        '#metadata("bab3") <bab3>',
        render_chapter3(cfg, out_dir),
        '#active_chapter.update("4. SOSIAL DAN KESEJAHTERAAN RAKYAT")',
        '#is_chapter_page.update(true)',
        '#pagebreak()',
        '#metadata("bab4") <bab4>',
        render_chapter4(cfg, out_dir),
        '#active_chapter.update("5. PERTANIAN")',
        '#is_chapter_page.update(true)',
        '#pagebreak()',
        '#metadata("bab5") <bab5>',
        render_chapter5(cfg, out_dir),
        '#active_chapter.update("6. PARIWISATA, TRANSPORTASI, DAN KOMUNIKASI")',
        '#is_chapter_page.update(true)',
        '#pagebreak()',
        '#metadata("bab6") <bab6>',
        render_chapter6(cfg),
        '#active_chapter.update("7. PERBANKAN, KOPERASI, DAN PERDAGANGAN")',
        '#is_chapter_page.update(true)',
        '#pagebreak()',
        '#metadata("bab7") <bab7>',
        render_chapter7(cfg),
        '#active_chapter.update("DAFTAR PUSTAKA")',
        '#pagebreak()',
        daftar_pustaka_markup,
        '#metadata("akhir_buku") <akhir_buku>',
        render_backcover(cfg)
    ]

    return "\n".join(parts)
