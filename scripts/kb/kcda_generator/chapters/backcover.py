"""Backcover generator for KCDA 2026."""

from typing import Dict, Any

def render_backcover(cfg: Dict[str, Any]) -> str:
    return """
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
        #text(size: 7.5pt, weight: "bold", style: "italic")[BADAN PUSAT STATISTIK\\ KABUPATEN MEMPAWAH]\\
        #v(2.5pt)
        #block[
          #set par(leading: 0.44em)
          #text(size: 5.5pt)[
            Jl. Raden Kusno No. 1, Mempawah 79511\\
            Telp (0561) 691030, Email : bps6104\\@bps.go.id\\
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
"""
