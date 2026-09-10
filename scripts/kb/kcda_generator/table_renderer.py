"""Table renderer helper for KCDA 2026 Typst documents following BPS standards (A5 Paper)."""

from typing import List, Optional

def render_typst_table(
    table_no: str,
    title_id: str,
    title_en: str,
    headers: List[str],
    col_numbers: List[str],
    rows: List[List[str]],
    col_widths: Optional[List[str]] = None,
    source: str = "BPS Kabupaten Mempawah",
    note: Optional[str] = None
) -> str:
    """Merender tabel berstandar BPS untuk buku ukuran A5 dengan format judul dua kolom (hanging indent) ala DDA."""
    num_cols = len(headers)
    if col_widths and len(col_widths) == num_cols:
        col_spec = "(" + ", ".join(col_widths) + ")"
    else:
        widths = ["2.2fr"] + ["1.0fr"] * (num_cols - 1)
        col_spec = "(" + ", ".join(widths) + ")"

    header_cells = ", ".join([f"[*{h}*]" for h in headers])
    col_num_cells = ", ".join([f"[{cn}]" for cn in col_numbers])

    rendered_rows = []
    for r in rows:
        cells = []
        for c in r:
            cells.append(f"[{c}]")
        rendered_rows.append(", ".join(cells))

    rows_str = ",\n  ".join(rendered_rows)
    note_str = f"#v(-2pt)\n#text(6pt, fill: luma(100))[{note}]\n" if note else ""

    markup = f"""
#v(6pt)
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #text(7.5pt, weight: "bold")[Tabel {table_no}] \\
    #text(6.5pt, style: "italic", fill: rgb("#475569"))[Table {table_no}]
  ],
  [
    #text(7.5pt, weight: "bold")[{title_id}] \\
    #text(6.5pt, style: "italic", fill: rgb("#475569"))[{title_en}]
  ]
)
#v(3pt)
#table(
  columns: {col_spec},
  inset: (x: 2.5pt, y: 3.5pt),
  stroke: (x, y) => if y == 0 {{ (top: 1.2pt + rgb("#000000"), bottom: 0.4pt + rgb("#000000")) }}
                    else if y == 1 {{ (bottom: 0.8pt + rgb("#000000")) }}
                    else {{ (bottom: 0.3pt + rgb("#E5E7EB")) }},
  fill: (x, y) => if y <= 1 {{ rgb("#FEF3C7") }}
                  else if calc.even(y) {{ rgb("#F9FAFB") }}
                  else {{ white }},
  align: (col, row) => if row <= 1 {{ center + horizon }}
                       else if col == 0 {{ left + horizon }}
                       else {{ right + horizon }},
  table.header({header_cells}, {col_num_cells}),
  {rows_str}
)
{note_str}#v(-3pt)
#text(6.5pt, fill: luma(80))[*Sumber / Source:* {source}]
#v(8pt)
"""
    return markup
