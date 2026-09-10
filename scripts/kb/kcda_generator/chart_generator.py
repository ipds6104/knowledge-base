"""
Dynamic Vector Chart Generator for KCDA 2026 Typst Engine.
Menghasilkan grafik SVG vektor modern berstandar BPS secara otomatis
berdasarkan ketersediaan data aktual di Google Sheets hulu (raw_tables).
Kaidah:
1. Selalu mengurutkan data bar chart (descending) agar mudah dibaca & dianalisis.
2. Penamaan Gambar dwibahasa 2-kolom persis standar BPS:
   Gambar
   ────── 1.1  Judul Indonesia (Bold)
   Figures     Judul Inggris (Bold Italic)
3. Sumber dwibahasa persis standar BPS:
   Sumber/Source : Instansi ID/Instansi EN (italic)
"""

import os
import re
import math
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from .data_loader import get_kecamatan_tab_rows, clean_cell_value
from .table_renderer import format_bilingual_source

def parse_number(val: Any) -> Optional[float]:
    """Mengekstrak angka float dari string cell Google Sheets/tabel lokal."""
    if val is None:
        return None
    s = str(val).strip()
    if s in ["", "-", "...", "–", "null", "None"]:
        return None
    s_clean = s.replace(".", "").replace(",", ".").replace("%", "").strip()
    try:
        return float(s_clean)
    except ValueError:
        return None

def format_id_number(val: float, is_decimal: bool = False) -> str:
    """Format angka sesuai standar Indonesia (koma untuk desimal, titik untuk ribuan)."""
    if is_decimal or (val % 1 != 0):
        formatted = f"{val:,.2f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        formatted = f"{int(round(val)):,}"
        return formatted.replace(",", ".")

def format_figure_header(fig_no: str, title_id: str, title_en: str) -> str:
    """
    Menghasilkan blok penamaan Gambar dwibahasa 2-kolom berstandar resmi BPS:
    Gambar
    ────── [No]  [Judul ID (Bold)]
    Figures      [Judul EN (Bold Italic)]
    """
    clean_fig = fig_no.replace(".", "_")
    return f"""#metadata("fig_{clean_fig}") <fig_{clean_fig}>
#grid(
  columns: (auto, 1fr),
  column-gutter: 8pt,
  align: (top + left, top + left),
  [
    #grid(
      columns: (auto, auto),
      column-gutter: 4.5pt,
      align: (top + center, horizon),
      [
        #box(stroke: (bottom: 0.6pt + black), inset: (x: 2pt, bottom: 2.5pt))[
          #text(7.5pt, weight: "bold")[Gambar]
        ] \\
        #v(-3.5pt)
        #text(6.5pt, style: "italic")[Figures]
      ],
      [
        #text(8.5pt, weight: "bold")[{fig_no}]
      ]
    )
  ],
  [
    #text(7.5pt, weight: "bold")[{title_id}] \\
    #v(-2pt)
    #text(6.5pt, weight: "bold", style: "italic", fill: rgb("#1E293B"))[{title_en}]
  ]
)"""

def generate_horizontal_bar_chart(
    labels: List[str],
    values: List[float],
    unit: str = "",
    color: str = "#0284C7",
    width: int = 340,
    sort_descending: bool = True
) -> str:
    """
    Menghasilkan SVG Horizontal Bar Chart modern beresolusi tajam.
    Secara default diurutkan (sort_descending=True) dari nilai tertinggi ke terendah.
    """
    n = len(labels)
    if n == 0:
        return ""

    if sort_descending and len(values) == n:
        pairs = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
        labels = [p[0] for p in pairs]
        values = [p[1] for p in pairs]

    row_height = 19
    top_margin = 14
    bottom_margin = 16
    left_margin = 85
    right_margin = 48
    plot_width = width - left_margin - right_margin
    height = top_margin + n * row_height + bottom_margin

    max_val = max(values) if values and max(values) > 0 else 1.0
    order = 10 ** math.floor(math.log10(max_val)) if max_val > 0 else 1
    ceil_val = math.ceil(max_val / order) * order
    if ceil_val < max_val * 1.15:
        ceil_val = math.ceil((max_val * 1.2) / order) * order

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" style="font-family: \'Liberation Sans\', Arial, sans-serif;">',
        f'<rect width="{width}" height="{height}" rx="4" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.8"/>'
    ]

    # Grid lines & ticks
    num_ticks = 4
    for i in range(num_ticks + 1):
        x = left_margin + (i / num_ticks) * plot_width
        val_tick = (i / num_ticks) * ceil_val
        val_str = f"{val_tick:.1f}".replace(".", ",") if ceil_val < 10 else f"{int(val_tick):,}".replace(",", ".")
        svg.append(f'<line x1="{x}" y1="{top_margin}" x2="{x}" y2="{height - bottom_margin}" stroke="#F1F5F9" stroke-width="0.8" stroke-dasharray="2,2"/>')
        svg.append(f'<text x="{x}" y="{height - 5}" font-size="5.5" fill="#94A3B8" text-anchor="middle">{val_str}</text>')

    # Axis line
    svg.append(f'<line x1="{left_margin}" y1="{top_margin}" x2="{left_margin}" y2="{height - bottom_margin}" stroke="#CBD5E1" stroke-width="1"/>')

    # Bars
    bar_h = 10.5
    for i, (label, val) in enumerate(zip(labels, values)):
        y = top_margin + i * row_height + (row_height - bar_h) / 2
        bar_w = (val / ceil_val) * plot_width if ceil_val > 0 else 0
        val_display = format_id_number(val, is_decimal=(val % 1 != 0))

        svg.append(f'<text x="{left_margin - 6}" y="{y + bar_h - 2.5}" font-size="6.5" fill="#334155" text-anchor="end">{label}</text>')
        svg.append(f'<rect x="{left_margin}" y="{y}" width="{bar_w}" height="{bar_h}" rx="2.5" fill="{color}"/>')
        svg.append(f'<text x="{left_margin + bar_w + 3.5}" y="{y + bar_h - 2.5}" font-size="6.5" font-weight="bold" fill="#0F172A">{val_display}</text>')

    svg.append("</svg>")
    return "\n".join(svg)

def generate_grouped_horizontal_bar_chart(
    labels: List[str],
    series_data: List[Dict[str, Any]],
    width: int = 340,
    sort_descending: bool = True
) -> str:
    """
    Menghasilkan SVG Grouped Horizontal Bar Chart dwibahasa untuk perbandingan multi-seri (misal Laki-laki vs Perempuan).
    Secara default diurutkan berdasarkan total agregat nilai per baris secara descending.
    """
    n = len(labels)
    num_series = len(series_data)
    if n == 0 or num_series == 0:
        return ""

    if sort_descending:
        totals = [sum(s["values"][i] for s in series_data) for i in range(n)]
        indices = sorted(range(n), key=lambda i: totals[i], reverse=True)
        labels = [labels[i] for i in indices]
        for s in series_data:
            s["values"] = [s["values"][i] for i in indices]

    bar_h = 7.0
    group_gap = 5.5
    row_height = num_series * bar_h + group_gap + 3
    top_margin = 26  # untuk legend
    bottom_margin = 15
    left_margin = 85
    right_margin = 52
    plot_width = width - left_margin - right_margin
    height = top_margin + n * row_height + bottom_margin

    all_vals = []
    for s in series_data:
        all_vals.extend(s["values"])
    max_val = max(all_vals) if all_vals and max(all_vals) > 0 else 1.0

    order = 10 ** math.floor(math.log10(max_val)) if max_val > 0 else 1
    ceil_val = math.ceil(max_val / order) * order
    if ceil_val < max_val * 1.15:
        ceil_val = math.ceil((max_val * 1.2) / order) * order

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" style="font-family: \'Liberation Sans\', Arial, sans-serif;">',
        f'<rect width="{width}" height="{height}" rx="4" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.8"/>'
    ]

    # Legend at top dwibahasa: Nama ID / Nama EN (italic)
    leg_x = left_margin
    for s in series_data:
        raw_name = s["name"]
        if "/" in raw_name:
            p = raw_name.split("/", 1)
            legend_html = f'{p[0].strip()}/<tspan font-style="italic">{p[1].strip()}</tspan>'
        else:
            legend_html = raw_name

        svg.append(f'<rect x="{leg_x}" y="8" width="11" height="7" rx="2" fill="{s["color"]}"/>')
        svg.append(f'<text x="{leg_x + 15}" y="14" font-size="6" font-weight="bold" fill="#334155">{legend_html}</text>')
        leg_x += len(raw_name) * 4.4 + 25

    # Grid lines
    num_ticks = 4
    for i in range(num_ticks + 1):
        x = left_margin + (i / num_ticks) * plot_width
        val_tick = (i / num_ticks) * ceil_val
        val_str = f"{int(val_tick):,}".replace(",", ".")
        svg.append(f'<line x1="{x}" y1="{top_margin}" x2="{x}" y2="{height - bottom_margin}" stroke="#F1F5F9" stroke-width="0.8" stroke-dasharray="2,2"/>')
        svg.append(f'<text x="{x}" y="{height - 4}" font-size="5.5" fill="#94A3B8" text-anchor="middle">{val_str}</text>')

    svg.append(f'<line x1="{left_margin}" y1="{top_margin}" x2="{left_margin}" y2="{height - bottom_margin}" stroke="#CBD5E1" stroke-width="1"/>')

    for i, label in enumerate(labels):
        group_top = top_margin + i * row_height + 3
        label_y = group_top + (num_series * bar_h) / 2 + 1.5
        svg.append(f'<text x="{left_margin - 6}" y="{label_y}" font-size="6.5" fill="#334155" text-anchor="end">{label}</text>')

        for s_idx, s in enumerate(series_data):
            y = group_top + s_idx * bar_h
            val = s["values"][i]
            bar_w = (val / ceil_val) * plot_width if ceil_val > 0 else 0
            val_display = format_id_number(val, is_decimal=False)
            svg.append(f'<rect x="{left_margin}" y="{y}" width="{bar_w}" height="{bar_h - 1.5}" rx="1.5" fill="{s["color"]}"/>')
            svg.append(f'<text x="{left_margin + bar_w + 3}" y="{y + bar_h - 2.5}" font-size="5.5" fill="#475569">{val_display}</text>')

    svg.append("</svg>")
    return "\n".join(svg)


# ==============================================================================
# HIGH-LEVEL DYNAMIC EXTRACTORS PER CHAPTER (SORTED & STANDARDIZED)
# ==============================================================================

def get_chapter1_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 1 (Geografi & Iklim):
    Gambar 1.1: Jarak dari Desa/Kelurahan ke Ibukota Kecamatan (km) [Tabel 1.2 - Terurut Menurun]
    Gambar 1.2: Luas Wilayah menurut Desa/Kelurahan (km²) [Tabel 1.1 - Terurut Menurun]
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    figures = []

    # 1. Gambar 1.1: Jarak ke Ibukota Kecamatan (Tabel 1.2) - Terurut Menurun
    rows_1_2 = get_kecamatan_tab_rows("1.2.", nama_singkat)
    labels = []
    values = []
    for r in rows_1_2[3:]:
        if len(r) > 1 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]):
            num = parse_number(r[1])
            if num is not None and num > 0:
                labels.append(r[0].strip())
                values.append(num)

    if len(values) >= 2:
        svg_code = generate_horizontal_bar_chart(labels, values, unit="km", color="#F5A623", sort_descending=True)
        chart_path = charts_dir / "gambar_1_1.svg"
        chart_path.write_text(svg_code, encoding="utf-8")

        src_fmt = format_bilingual_source(f"Kantor Camat {nama_singkat} / {nama_singkat} District Office")
        fig_header = format_figure_header(
            "1.1",
            f"Jarak dari Desa/Kelurahan ke Ibukota Kecamatan di {nama_singkat}, 2025 (km)",
            f"Distance from Village/Subdistrict to District Capital in {nama_en}, 2025 (km)"
        )
        fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_1_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
        figures.append(fig_typst)

    # 2. Gambar 1.2: Luas Wilayah (Tabel 1.1 - jika ada data luas) - Terurut Menurun & Tanpa Baris Total
    rows_1_1 = get_kecamatan_tab_rows("1.1.", nama_singkat)
    luas_labels = []
    luas_values = []
    for r in rows_1_1[3:]:
        if len(r) > 7 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]):
            if any(r[0].strip().lower() == l.lower() for l in luas_labels):
                break
            num = parse_number(r[7])
            if num is not None and num > 0:
                luas_labels.append(r[0].strip())
                luas_values.append(num)

    if len(luas_values) >= 2:
        svg_code_luas = generate_horizontal_bar_chart(luas_labels, luas_values, unit="km²", color="#0284C7", sort_descending=True)
        chart_path_luas = charts_dir / "gambar_1_2.svg"
        chart_path_luas.write_text(svg_code_luas, encoding="utf-8")

        src_fmt_luas = format_bilingual_source("Dinas Kependudukan dan Pencatatan Sipil / BAPEDDA Kabupaten Mempawah")
        fig_header_luas = format_figure_header(
            "1.2",
            f"Luas Wilayah menurut Desa/Kelurahan di {nama_singkat}, 2025 (km²)",
            f"Total Area by Village/Subdistrict in {nama_en}, 2025 (sq.km)"
        )
        fig_luas = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_1_2.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt_luas}]
#v(4pt)
{fig_header_luas}
#v(10pt)
"""
        figures.append(fig_luas)

    return "\n".join(figures)


def get_chapter2_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 2 (Pemerintahan):
    Gambar 2.1: Jumlah Rukun Tetangga (RT) menurut Desa/Kelurahan [Tabel 2.1.1 - Terurut Menurun]
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    rows_2_1_1 = get_kecamatan_tab_rows("2.1.1", nama_singkat)
    labels = []
    values = []
    for r in rows_2_1_1[3:]:
        if len(r) > 3 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]):
            num = parse_number(r[3])
            if num is not None and num > 0:
                labels.append(r[0].strip())
                values.append(num)

    if len(values) < 2:
        return ""

    svg_code = generate_horizontal_bar_chart(labels, values, unit="RT", color="#0284C7", sort_descending=True)
    chart_path = charts_dir / "gambar_2_1.svg"
    chart_path.write_text(svg_code, encoding="utf-8")

    src_fmt = format_bilingual_source(f"Kantor Camat {nama_singkat} / {nama_singkat} District Office")
    fig_header = format_figure_header(
        "2.1",
        f"Jumlah Rukun Tetangga (RT) menurut Desa/Kelurahan di {nama_singkat}, 2025",
        f"Number of Neighborhood Units (RT) by Village/Subdistrict in {nama_en}, 2025"
    )
    fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_2_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
    return fig_typst


def get_chapter3_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 3 (Kependudukan):
    Gambar 3.1: Jumlah Penduduk menurut Jenis Kelamin dan Desa/Kelurahan [Tabel 3.1 - Terurut Menurun]
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    rows_3_1 = get_kecamatan_tab_rows("3.1", nama_singkat)
    labels = []
    male_vals = []
    female_vals = []

    for r in rows_3_1[3:]:
        if len(r) > 2 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "kecamatan"]):
            if any(r[0].strip().lower() == l.lower() for l in labels):
                break
            m = parse_number(r[1])
            f = parse_number(r[2])
            if m is not None and f is not None and (m > 0 or f > 0):
                labels.append(r[0].strip())
                male_vals.append(m)
                female_vals.append(f)

    if len(labels) < 2:
        return ""

    series = [
        {"name": "Laki-laki / Male", "color": "#0284C7", "values": male_vals},
        {"name": "Perempuan / Female", "color": "#F5A623", "values": female_vals}
    ]

    svg_code = generate_grouped_horizontal_bar_chart(labels, series, sort_descending=True)
    chart_path = charts_dir / "gambar_3_1.svg"
    chart_path.write_text(svg_code, encoding="utf-8")

    src_fmt = format_bilingual_source("Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah (Semester II 2025)")
    fig_header = format_figure_header(
        "3.1",
        f"Jumlah Penduduk menurut Jenis Kelamin dan Desa/Kelurahan di {nama_singkat}, 2025",
        f"Population by Sex and Village/Subdistrict in {nama_en}, 2025"
    )
    fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_3_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
    return fig_typst


def get_chapter4_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 4 (Sosial & Pendidikan):
    Gambar 4.1: Fasilitas Pendidikan (jika data terisi di Google Sheets).
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    rows_4_1_1 = get_kecamatan_tab_rows("4.1.1", nama_singkat)
    for r in rows_4_1_1:
        if len(r) > 4 and "sekolah dasar" in r[0].lower():
            vals = [parse_number(x) for x in r[1:5]]
            valid_vals = [v for v in vals if v is not None and v > 0]
            if len(valid_vals) >= 2:
                years = ["2022", "2023", "2024", "2025"]
                filtered_years = []
                filtered_nums = []
                for y, v in zip(years, vals):
                    if v is not None:
                        filtered_years.append(y)
                        filtered_nums.append(v)

                svg_code = generate_horizontal_bar_chart(filtered_years, filtered_nums, unit="Unit", color="#10B981", sort_descending=False)
                chart_path = charts_dir / "gambar_4_1.svg"
                chart_path.write_text(svg_code, encoding="utf-8")

                src_fmt = format_bilingual_source("BPS, Pendataan Potensi Desa (Podes) 2025")
                fig_header = format_figure_header(
                    "4.1",
                    f"Perkembangan Jumlah Sekolah Dasar (SD) di {nama_singkat}, 2022–2025",
                    f"Number of Primary Schools (SD) in {nama_en}, 2022–2025"
                )
                fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_4_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
                return fig_typst

    return ""


def get_chapter5_charts(slug: str, nama_singkat: str, nama_en: str, out_dir: Optional[Path]) -> str:
    """
    Menghasilkan visualisasi Bab 5 (Pertanian):
    Gambar 5.1: Produksi Tanaman Sayuran / Buah-buahan (jika data terisi di Google Sheets).
    """
    if not out_dir:
        return ""

    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    rows_5_7 = get_kecamatan_tab_rows("5.7", nama_singkat)
    labels = []
    values = []
    for r in rows_5_7[3:]:
        if len(r) > 4 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ["jumlah", "total", "sumber", "catatan", "buah"]):
            num = parse_number(r[4])
            if num is not None and num > 0:
                name = r[0].split("/")[0].strip()
                labels.append(name)
                values.append(num)

    if len(values) >= 2:
        svg_code = generate_horizontal_bar_chart(labels[:8], values[:8], unit="Kuintal", color="#F5A623", sort_descending=True)
        chart_path = charts_dir / "gambar_5_1.svg"
        chart_path.write_text(svg_code, encoding="utf-8")

        src_fmt = format_bilingual_source("BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)")
        fig_header = format_figure_header(
            "5.1",
            f"Produksi Buah-buahan Utama di {nama_singkat}, 2025 (Kuintal)",
            f"Production of Major Fruits in {nama_en}, 2025 (Quintal)"
        )
        fig_typst = f"""
#v(6pt)
#align(center)[
  #image("charts/gambar_5_1.svg", width: 100%)
]
#v(-2pt)
#text(6.5pt, fill: luma(60))[Sumber/#text(style: "italic")[Source] : {src_fmt}]
#v(4pt)
{fig_header}
#v(10pt)
"""
        return fig_typst

    return ""
