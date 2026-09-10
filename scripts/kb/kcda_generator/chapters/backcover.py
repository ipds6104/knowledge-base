"""Backcover generator for KCDA 2026."""

from typing import Dict, Any

def render_backcover(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]

    return f"""
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
      #text(14pt, weight: "bold", fill: rgb("#B45309"))[{nama_resmi.upper()} DALAM ANGKA 2026] \\
      #v(6pt)
      #text(10pt, fill: rgb("#92400E"))[Satu Data Statistik Sektoral Kecamatan Mempawah] \\
      #text(8.5pt, fill: rgb("#92400E"))[Mencerdaskan Bangsa Melalui Data Akurat dan Terpercaya]
    ]
  )
  
  #v(8cm)
  #rect(fill: rgb("#F9FAFB"), inset: 12pt, radius: 4pt, stroke: 0.5pt + rgb("#D1D5DB"))[
    #grid(
      columns: (1fr, 1fr, 1fr),
      align: center + horizon,
      [*SENSUS EKONOMI 2026* \\
      #text(7pt)[BPS Republik Indonesia]],
      [*Core Values ASN* \\
      #text(7pt)[BerAKHLAK]],
      [*Bangga Melayani Bangsa* \\
      #text(7pt)[KemenPAN-RB]]
    )
  ]
  
  #v(1cm)
  #text(9pt, weight: "bold", fill: rgb("#1F2937"))[BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH] \\
  #text(8pt, fill: rgb("#4B5563"))[Jl. Raden Kusno No. 1, Mempawah, Kalimantan Barat 79511] \\
  #text(8pt, fill: rgb("#4B5563"))[Pos-el: #link("mailto:bps6104@bps.go.id")[bps6104\\@bps.go.id] | Laman: #link("https://mempawahkab.bps.go.id")]
]
"""
