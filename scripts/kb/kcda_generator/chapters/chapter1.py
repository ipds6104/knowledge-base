"""Chapter 1: Geografi dan Iklim Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table
from ..chart_generator import get_chapter1_charts

def render_chapter1(cfg: Dict[str, Any], out_dir: Optional[Any] = None) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")
    ibukota = cfg["ibukota_kecamatan"]
    desa_list = cfg["desa_list"]
    slug = cfg.get("slug", "")

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter1_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else "\n#v(8pt)\n"

    # --- 1.1 Luas Daerah ---
    rows_1_1_raw = get_kecamatan_tab_rows("1.1.", nama_singkat)
    luas_map = {}
    for r in rows_1_1_raw[3:]:
        if len(r) > 1 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['jumlah', 'total', 'sumber']):
            luas_val = clean_cell_value(r[3] if len(r) > 3 else r[1])
            pct_val = clean_cell_value(r[4] if len(r) > 4 else "...")
            luas_map[r[0].strip().lower()] = [luas_val, pct_val]

    t1_1_rows = []
    for d in desa_list:
        v = luas_map.get(d.lower(), ["...", "..."])
        t1_1_rows.append([d, v[0], v[1]])

    t1_1_markup = render_typst_table(
        table_no="1.1",
        title_id=f"Luas Daerah Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Total Area by Village/Subdistrict in {nama_en}, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Luas Daerah\nTotal Area (km²)", "Persentase\nPercentage (%)"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_1_rows,
        col_widths=["2.5fr", "1.3fr", "1.2fr"],
        source="Dinas Kependudukan dan Pencatatan Sipil/BAPEDDA Kabupaten Mempawah / Population and Civil Registration Service/Regional Development Planning Agency of Mempawah Regency"
    )

    # --- 1.2 Jarak ke Ibukota Kecamatan & Kabupaten ---
    rows_1_2_raw = get_kecamatan_tab_rows("1.2.", nama_singkat)
    jarak_map = {}
    for r in rows_1_2_raw[3:]:
        if len(r) > 1 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['jumlah', 'total', 'sumber']):
            j_kec = clean_cell_value(r[1] if len(r) > 1 else "...")
            j_kab = clean_cell_value(r[2] if len(r) > 2 else "...")
            jarak_map[r[0].strip().lower()] = [j_kec, j_kab]

    t1_2_rows = []
    for d in desa_list:
        v = jarak_map.get(d.lower(), ["...", "..."])
        t1_2_rows.append([d, v[0], v[1]])

    t1_2_markup = render_typst_table(
        table_no="1.2",
        title_id=f"Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Distance to Subdistrict and Regency Capital by Village in {nama_en}, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Ke Ibukota Kec.\nTo District Capital (km)", "Ke Ibukota Kab.\nTo Regency Capital (km)"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_2_rows,
        col_widths=["2.5fr", "1.3fr", "1.3fr"],
        source=f"Kantor Camat {nama_singkat}"
    )

    # --- 1.3 Batas Administrasi ---
    rows_1_3_raw = get_kecamatan_tab_rows("1.3.", nama_singkat)
    t1_3_rows = []
    for r in rows_1_3_raw[3:]:
        if len(r) > 2 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan']):
            arah = clean_cell_value(r[1])
            batas = clean_cell_value(r[2])
            no_idx = clean_cell_value(r[0])
            t1_3_rows.append([no_idx, arah, batas])
    if not t1_3_rows:
        t1_3_rows = [
            ["1", "Utara/North", "..."],
            ["2", "Selatan/South", "..."],
            ["3", "Barat/West", "..."],
            ["4", "Timur/East", "..."]
        ]

    t1_3_markup = render_typst_table(
        table_no="1.3",
        title_id=f"Batas Administrasi {nama_resmi} Menurut Arah Mata Angin, 2025",
        title_en=f"Administrative Borders of {nama_en} by Cardinal Direction, 2025",
        headers=["No", "Arah Mata Angin\nWind Direction", "Berbatasan Dengan\nBordering With"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_3_rows,
        col_widths=["0.6fr", "1.8fr", "3.0fr"],
        source=f"Kantor Camat {nama_singkat} / Bagian Tata Pemerintahan Setda Mempawah"
    )

    # --- 1.4 Jarak Kantor Camat ke Tempat Penting ---
    rows_1_4_raw = get_kecamatan_tab_rows("1.4.", nama_singkat)
    t1_4_rows = []
    for r in rows_1_4_raw[3:]:
        if len(r) > 1 and r[1].strip() and not any(r[1].lower().startswith(x) for x in ['sumber', 'catatan']):
            tempat = clean_cell_value(r[1])
            jarak = clean_cell_value(r[2] if len(r) > 2 else "...")
            no_idx = clean_cell_value(r[0])
            t1_4_rows.append([no_idx, tempat, jarak])
    if not t1_4_rows:
        t1_4_rows = [
            ["1", "Ibukota Provinsi (Kota Pontianak)", "..."],
            ["2", "Ibukota Kabupaten (Kota Mempawah)", "..."],
            ["3", "Bandara Internasional Supadio", "..."],
            ["4", "Pelabuhan Internasional Kijing", "..."]
        ]

    t1_4_markup = render_typst_table(
        table_no="1.4",
        title_id=f"Jarak Kantor Camat {nama_singkat} dengan Kota dan Tempat Penting Lainnya, 2025",
        title_en=f"Distance from {nama_singkat} Subdistrict Office to Other Important Places, 2025",
        headers=["No", "Nama Kota dan Tempat Penting\nOther Important Places", "Jarak\nDistance (km)"],
        col_numbers=["(1)", "(2)", "(3)"],
        rows=t1_4_rows,
        col_widths=["0.6fr", "3.2fr", "1.2fr"],
        source=f"Kantor Camat {nama_singkat}"
    )

    # Infografis Halaman Bab 1
    infografis_markup = f"\n{charts_markup}\n" if charts_markup.strip() else """
#v(1.5cm)
#align(center)[
  #rect(width: 95%, height: 11cm, fill: rgb("#FFFBEB"), stroke: (paint: rgb("#F59E0B"), thickness: 1.5pt, dash: "dashed"), radius: 6pt)[
    #align(center + horizon)[
      #text(12pt, weight: "bold", fill: rgb("#B45309"))[INFOGRAFIS GEOGRAFI & IKLIM]\
      #v(6pt)
      #text(8.5pt, fill: rgb("#92400E"), style: "italic")[Kecamatan """ + nama_singkat + """]
    ]
  ]
]
"""

    return f"""
// ==========================================
// BAB 1: GEOGRAFI DAN IKLIM (HALAMAN PEMBATAS & INFOGRAFIS)
// ==========================================
#is_chapter_page.update(true)
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 1: GEOGRAFI DAN IKLIM] \\
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 1: GEOGRAPHY AND CLIMATE]
  ]
)
#v(10pt)

{infografis_markup}

#pagebreak()
#is_chapter_page.update(false)

// ==========================================
// ISI BAB 1: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Kecamatan {nama_singkat} secara astronomis dan geografis terletak di wilayah pesisir dan daratan Kabupaten Mempawah, Provinsi Kalimantan Barat dengan ibukota kecamatan berada di {ibukota}. Wilayah ini terbagi ke dalam {len(desa_list)} desa/kelurahan dengan akses perhubungan darat dan air yang menghubungkan pusat-pusat kegiatan ekonomi lokal dengan ibukota kabupaten.
]
#v(12pt)

{t1_1_markup}
#pagebreak()

{t1_2_markup}
#v(10pt)
{t1_3_markup}
#pagebreak()

{t1_4_markup}
"""
