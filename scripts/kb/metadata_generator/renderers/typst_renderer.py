"""Typst Renderer for Metadata Generator Engine.

Pure DTO-to-Typst markup builder with zero-width space wrapping for code variable names, font size optimization to prevent cell overflow, and dynamic section indexing.
"""

from ..schemas import DesaMetadataDTO


def render_metadata_typst(dto: DesaMetadataDTO) -> str:
    """Renders DesaMetadataDTO into a clean Typst markup document."""
    lines = []
    lines.append(f"""#set page(
  paper: "a4",
  margin: (x: 1.5cm, y: 2cm),
  header: align(right)[
    #text(8pt, fill: luma(120))[Satu Data Indonesia - Portal Metadata {dto.admin_type} Cantik 2026]
  ],
  footer: [
    #align(center)[
      #text(9pt)[#context counter(page).display()]
    ]
  ]
)

#set text(
  font: "Arial",
  size: 9.5pt,
  lang: "id"
)

#let wrap-var(name) = {{
  let clean = name.split("_").join("_\\u{{200b}}").split("(").join("(\\u{{200b}}").split(")").join(")\\u{{200b}}").split("/").join("/\\u{{200b}}")
  text(font: "Courier New", size: 7pt)[#clean]
}}
""")

    lines.append(f"""#align(center)[
  #text(16pt, weight: "bold", fill: rgb("#064e3b"))[METADATA STATISTIK SEKTORAL] \\
  #v(2mm)
  #text(12pt, weight: "bold")[Standar Satu Data Indonesia (SDI)] \\
  #v(1mm)
  #text(11pt, style: "italic")[{dto.admin_type} {dto.desa_title}, Kabupaten Mempawah]
]

#v(6mm)

== I. METADATA KEGIATAN (MS-KEGIATAN)

#table(
  columns: (2.5cm, 4.5cm, 11cm),
  fill: (col, row) => if row == 0 {{ rgb("#064e3b") }} else if calc.even(row) {{ rgb("#f0fdf4") }} else {{ none }},
  stroke: 0.4pt + rgb("#cbd5e1"),
  align: (col, row) => if row == 0 {{ center + horizon }} else {{ left + horizon }},
  
  // Headers
  text(fill: white, weight: "bold", size: 8.5pt)[No],
  text(fill: white, weight: "bold", size: 8.5pt)[Elemen Metadata],
  text(fill: white, weight: "bold", size: 8.5pt)[Keterangan / Nilai],
""")

    for k in dto.kegiatan:
        lines.append(f'  text(size: 8pt)[{k.no}], text(size: 8pt, weight: "bold")[{k.elemen}], text(size: 8pt)[{k.keterangan}],')

    lines.append(")\n\n#v(5mm)\n\n== II. METADATA VARIABEL (MS-VARIABEL)\n")

    sec_char = ord('A')

    if dto.variabel.rt_variables:
        letter = chr(sec_char)
        lines.append(f"=== {letter}. Tabel Variabel Tingkat Rukun Tetangga (Daftar_RT)\n")
        lines.append(r"""#table(
  columns: (0.6cm, 4.5cm, 2.0cm, 5.5cm, 1.4cm, 1.2cm, 2.8cm),
  fill: (col, row) => if row == 0 { rgb("#047857") } else if calc.even(row) { rgb("#f0fdf4") } else { none },
  stroke: 0.3pt + rgb("#cbd5e1"),
  align: (col, row) => if row == 0 { center + horizon } else { left + horizon },
  
  // Headers
  text(fill: white, weight: "bold", size: 7.5pt)[No],
  text(fill: white, weight: "bold", size: 7.5pt)[Nama Variabel],
  text(fill: white, weight: "bold", size: 7.5pt)[Konsep],
  text(fill: white, weight: "bold", size: 7.5pt)[Definisi],
  text(fill: white, weight: "bold", size: 7.5pt)[Satuan],
  text(fill: white, weight: "bold", size: 7.5pt)[Tipe],
  text(fill: white, weight: "bold", size: 7.5pt)[Rentang / Isian],
""")
        for v in dto.variabel.rt_variables:
            lines.append(f'  text(size: 7.5pt)[{v.no}], wrap-var("{v.nama_variabel}"), text(size: 7.5pt)[{v.konsep}], text(size: 7.5pt)[{v.definisi}], text(size: 7.5pt)[{v.satuan}], text(size: 7.5pt)[{v.tipe_data}], text(size: 7.5pt)[{v.pilihan_isian}],')
        lines.append(")\n\n#pagebreak()\n\n")
        sec_char += 1

    if dto.variabel.fasilitas_variables:
        letter = chr(sec_char)
        lines.append(f"=== {letter}. Tabel Variabel Tingkat Sarana Prasarana (Fasilitas)\n")
        lines.append(r"""#table(
  columns: (0.6cm, 4.5cm, 2.0cm, 5.5cm, 1.4cm, 1.2cm, 2.8cm),
  fill: (col, row) => if row == 0 { rgb("#059669") } else if calc.even(row) { rgb("#f0fdf4") } else { none },
  stroke: 0.3pt + rgb("#cbd5e1"),
  align: (col, row) => if row == 0 { center + horizon } else { left + horizon },
  
  // Headers
  text(fill: white, weight: "bold", size: 7.5pt)[No],
  text(fill: white, weight: "bold", size: 7.5pt)[Nama Variabel],
  text(fill: white, weight: "bold", size: 7.5pt)[Konsep],
  text(fill: white, weight: "bold", size: 7.5pt)[Definisi],
  text(fill: white, weight: "bold", size: 7.5pt)[Satuan],
  text(fill: white, weight: "bold", size: 7.5pt)[Tipe],
  text(fill: white, weight: "bold", size: 7.5pt)[Rentang / Isian],
""")
        for v in dto.variabel.fasilitas_variables:
            lines.append(f'  text(size: 7.5pt)[{v.no}], wrap-var("{v.nama_variabel}"), text(size: 7.5pt)[{v.konsep}], text(size: 7.5pt)[{v.definisi}], text(size: 7.5pt)[{v.satuan}], text(size: 7.5pt)[{v.tipe_data}], text(size: 7.5pt)[{v.pilihan_isian}],')
        lines.append(")\n\n")
        sec_char += 1

    if dto.variabel.capi_micro_variables:
        letter = chr(sec_char)
        lines.append(f"#pagebreak()\n\n=== {letter}. Tabel Variabel Data Mikro Bangunan Tempat Tinggal Biasa & Rumah Tangga CAPI\n")
        lines.append(r"""#table(
  columns: (0.6cm, 4.5cm, 2.0cm, 5.5cm, 1.4cm, 1.2cm, 2.8cm),
  fill: (col, row) => if row == 0 { rgb("#0d9488") } else if calc.even(row) { rgb("#f0fdf4") } else { none },
  stroke: 0.3pt + rgb("#cbd5e1"),
  align: (col, row) => if row == 0 { center + horizon } else { left + horizon },
  
  // Headers
  text(fill: white, weight: "bold", size: 7.5pt)[No],
  text(fill: white, weight: "bold", size: 7.5pt)[Nama Variabel],
  text(fill: white, weight: "bold", size: 7.5pt)[Konsep],
  text(fill: white, weight: "bold", size: 7.5pt)[Definisi],
  text(fill: white, weight: "bold", size: 7.5pt)[Satuan],
  text(fill: white, weight: "bold", size: 7.5pt)[Tipe],
  text(fill: white, weight: "bold", size: 7.5pt)[Rentang / Isian],
""")
        for v in dto.variabel.capi_micro_variables:
            lines.append(f'  text(size: 7.5pt)[{v.no}], wrap-var("{v.nama_variabel}"), text(size: 7.5pt)[{v.konsep}], text(size: 7.5pt)[{v.definisi}], text(size: 7.5pt)[{v.satuan}], text(size: 7.5pt)[{v.tipe_data}], text(size: 7.5pt)[{v.pilihan_isian}],')
        lines.append(")\n\n")
        sec_char += 1

    lines.append("#pagebreak()\n\n== III. METADATA INDIKATOR (MS-INDIKATOR)\n")
    lines.append(r"""#table(
  columns: (0.6cm, 3.4cm, 5.2cm, 4.5cm, 1.8cm, 2.5cm),
  fill: (col, row) => if row == 0 { rgb("#064e3b") } else if calc.even(row) { rgb("#f0fdf4") } else { none },
  stroke: 0.3pt + rgb("#cbd5e1"),
  align: (col, row) => if row == 0 { center + horizon } else { left + horizon },
  
  // Headers
  text(fill: white, weight: "bold", size: 8pt)[No],
  text(fill: white, weight: "bold", size: 8pt)[Nama Indikator],
  text(fill: white, weight: "bold", size: 8pt)[Definisi],
  text(fill: white, weight: "bold", size: 8pt)[Rumus Kalkulasi],
  text(fill: white, weight: "bold", size: 8pt)[Satuan],
  text(fill: white, weight: "bold", size: 8pt)[Klasifikasi],
""")

    for ind in dto.indikator:
        rumus_typst = f"[$ {ind.rumus} $]" if ind.rumus else "[-]"
        lines.append(f'  text(size: 7.5pt)[{ind.no}], text(size: 7.5pt, weight: "bold")[{ind.nama_indikator}], text(size: 7.5pt)[{ind.definisi}], {rumus_typst}, text(size: 7.5pt)[{ind.satuan}], text(size: 7.5pt)[{ind.klasifikasi}],')

    lines.append(")\n")
    return "\n".join(lines)
