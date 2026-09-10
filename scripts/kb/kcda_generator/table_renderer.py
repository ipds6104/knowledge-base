"""Table renderer helper for KCDA 2026 Typst documents following BPS standards."""

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
    """Merender tabel berstandar BPS (Booktabs, bilingual title, column numbers, zebra fill, source)."""
    num_cols = len(headers)
    if col_widths and len(col_widths) == num_cols:
        col_spec = "(" + ", ".join(col_widths) + ")"
    else:
        # Default: kolom pertama lebih lebar (nama wilayah/indikator)
        widths = ["2.2fr"] + ["1.1fr"] * (num_cols - 1)
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
    note_str = f"#v(-3pt)\n#text(7pt, fill: luma(100))[{note}]\n" if note else ""

    markup = f"""
=== Tabel {table_no}: {title_id}
#text(8pt, style: "italic", fill: rgb("#92400E"))[Table {table_no}: {title_en}]
#v(3pt)
#align(center)[
#table(
  columns: {col_spec},
  stroke: (x, y) => if y == 0 {{ (top: 1.5pt + rgb("#000000"), bottom: 0.5pt + rgb("#000000")) }}
                    else if y == 1 {{ (bottom: 1.2pt + rgb("#000000")) }}
                    else {{ (bottom: 0.4pt + rgb("#E5E7EB")) }},
  fill: (x, y) => if y <= 1 {{ rgb("#FEF3C7") }}
                  else if calc.even(y) {{ rgb("#F9FAFB") }}
                  else {{ white }},
  align: (col, row) => if row <= 1 {{ center + horizon }}
                       else if col == 0 {{ left + horizon }}
                       else {{ right + horizon }},
  table.header({header_cells}, {col_num_cells}),
  {rows_str}
)
]
{note_str}#v(-4pt)
#text(7.5pt, fill: luma(80))[*Sumber / Source:* {source}]
#v(12pt)
"""
    return markup
