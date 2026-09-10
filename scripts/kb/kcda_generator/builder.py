"""KCDA 2026 Typst Document Builder Engine (Orchestrator)."""

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

def build_kcda_typst(slug: str) -> str:
    """Menyusun kode dokumen Typst lengkap untuk satu kecamatan sesuai Pedoman Resmi KCDA 2026."""
    cfg = KCDA_KECAMATAN_CONFIG.get(slug)
    if not cfg:
        raise ValueError(f"Kecamatan slug '{slug}' tidak ditemukan di KCDA_KECAMATAN_CONFIG.")

    nama_resmi = cfg["nama_resmi"]

    # Header & Footer Logic Typst
    header_logic = f"""
#set page(
  paper: "a4",
  margin: (
    inside: 2.5cm,
    outside: 1.5cm,
    top: 2.0cm,
    bottom: 2.0cm,
  ),
  header: context {{
    let page_num = counter(page).get().first()
    // Running header hanya muncul pada halaman Arab bab isi (setelah frontmatter)
    if page_num >= 7 {{
      if calc.even(page_num) {{
        align(left, text(8pt, fill: rgb("#D97706"), weight: "bold")[{nama_resmi.upper()} DALAM ANGKA 2026])
      }} else {{
        align(right, text(8pt, fill: rgb("#D97706"), weight: "bold")[BPS KABUPATEN MEMPAWAH])
      }}
    }}
  }},
  footer: context {{
    let page_num = counter(page).get().first()
    if page_num > 1 and page_num < 7 {{
      // Halaman iii suppressed sesuai pedoman KCDA 2026
      if page_num != 3 {{
        align(center, text(9pt)[#counter(page).display("i")])
      }}
    }} else if page_num >= 7 {{
      if calc.even(page_num) {{
        align(left, text(9pt, weight: "medium")[#counter(page).display("1")])
      }} else {{
        align(right, text(9pt, weight: "medium")[#counter(page).display("1")])
      }}
    }}
  }}
)

#set text(font: ("Liberation Sans", "Arial"), size: 8.5pt, lang: "id")
#set par(justify: true, leading: 0.55em)
"""

    parts = [
        "// Publikasi Resmi BPS Kabupaten Mempawah: Kecamatan Dalam Angka 2026",
        header_logic,
        render_frontmatter(cfg),
        render_chapter1(cfg),
        render_chapter2(cfg),
        render_chapter3(cfg),
        render_chapter4(cfg),
        render_chapter5(cfg),
        render_chapter6(cfg),
        render_chapter7(cfg),
        render_backcover(cfg)
    ]

    return "\n".join(parts)
