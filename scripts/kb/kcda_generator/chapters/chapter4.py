"""Chapter 4: Sosial dan Kesejahteraan Rakyat Generator for KCDA 2026."""

from typing import Dict, Any, List, Optional
from pathlib import Path
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table
from ..chart_generator import get_chapter4_charts

def render_chapter4(cfg: Dict[str, Any], out_dir: Optional[Any] = None) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")
    desa_list = cfg["desa_list"]
    slug = cfg.get("slug", "")

    # Grafik dinamis data-driven dari Google Sheets
    charts_markup = get_chapter4_charts(slug, nama_singkat, nama_en, Path(out_dir) if out_dir else None)
    chart_section = f"\n{charts_markup}\n#pagebreak()\n" if charts_markup.strip() else "\n#v(8pt)\n"

    # --- 4.1.1 Fasilitas Pendidikan di Desa (Podes) ---
    rows_411_raw = get_kecamatan_tab_rows("4.1.1", nama_singkat)
    t411_rows = []
    if len(rows_411_raw) > 2:
        for r in rows_411_raw[2:]:
            if r and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['sumber', 'catatan']):
                jenjang = r[0].split('\n')[0].strip()
                # Kolom data: jika ada 2022 di col 1, maka 2023=col 2, 2024=col 3, 2025=col 4
                y2023 = clean_cell_value(r[2] if len(r) > 2 else (r[1] if len(r) > 1 else "..."))
                y2024 = clean_cell_value(r[3] if len(r) > 3 else "...")
                y2025 = clean_cell_value(r[4] if len(r) > 4 else "...")
                t411_rows.append([jenjang, y2023, y2024, y2025])
    if not t411_rows:
        default_jenjang = [
            "Taman Kanak-Kanak (TK)", "Raudatul Athfal (RA)", "Sekolah Dasar (SD)",
            "Madrasah Ibtidaiyah (MI)", "Sekolah Menengah Pertama (SMP)", "Madrasah Tsanawiyah (MTs)",
            "Sekolah Menengah Atas (SMA)", "Sekolah Menengah Kejuruan (SMK)", "Madrasah Aliyah (MA)", "Akademi/Perguruan Tinggi"
        ]
        t411_rows = [[j, "...", "...", "..."] for j in default_jenjang]

    t411_markup = render_typst_table(
        table_no="4.1.1",
        title_id=f"Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di {nama_resmi}, 2023–2025",
        title_en=f"Number of Villages Having Educational Facilities by Educational Level in {nama_en}, 2023–2025",
        headers=["Tingkat Pendidikan\nEducational Level", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t411_rows,
        col_widths=["2.6fr", "1.0fr", "1.0fr", "1.0fr"],
        source="BPS, Pendataan Potensi Desa (Podes)"
    )

    # --- 4.1.2 Satuan Pendidikan (TK, SD, SMP, SMA) ---
    jenjang_list = [
        "Taman Kanak-Kanak (TK)", "Raudatul Athfal (RA)",
        "Sekolah Dasar (SD)", "Madrasah Ibtidaiyah (MI)",
        "Sekolah Menengah Pertama (SMP)", "Madrasah Tsanawiyah (MTs)",
        "Sekolah Menengah Atas (SMA)", "Sekolah Menengah Kejuruan (SMK)",
        "Madrasah Aliyah (MA)", "Jumlah / Total"
    ]
    t412_rows = [[j, "...", "...", "..."] for j in jenjang_list]
    t412_markup = render_typst_table(
        table_no="4.1.2",
        title_id=f"Jumlah Satuan Pendidikan Menurut Tingkat Pendidikan di {nama_resmi}, 2024/2025",
        title_en=f"Number of Educational Units by Education Level in {nama_en}, 2024/2025",
        headers=["Tingkat Pendidikan\nEducational Level", "Negeri\nPublic", "Swasta\nPrivate", "Jumlah\nTotal"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t412_rows,
        col_widths=["2.5fr", "1.0fr", "1.0fr", "1.0fr"],
        source="Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama"
    )

    # --- 4.1.3 Pendidik/Guru ---
    t413_rows = [[j, "...", "...", "..."] for j in jenjang_list]
    t413_markup = render_typst_table(
        table_no="4.1.3",
        title_id=f"Jumlah Kepala Sekolah dan Guru Menurut Tingkat Pendidikan di {nama_resmi}, 2024/2025",
        title_en=f"Number of Principals and Teachers by Education Level in {nama_en}, 2024/2025",
        headers=["Tingkat Pendidikan\nEducational Level", "Negeri\nPublic", "Swasta\nPrivate", "Jumlah\nTotal"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t413_rows,
        col_widths=["2.5fr", "1.0fr", "1.0fr", "1.0fr"],
        source="Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama"
    )

    # --- 4.1.4 Siswa/Peserta Didik ---
    t414_rows = [[j, "...", "...", "..."] for j in jenjang_list]
    t414_markup = render_typst_table(
        table_no="4.1.4",
        title_id=f"Jumlah Peserta Didik Menurut Tingkat Pendidikan di {nama_resmi}, 2024/2025",
        title_en=f"Number of Students by Education Level in {nama_en}, 2024/2025",
        headers=["Tingkat Pendidikan\nEducational Level", "Negeri\nPublic", "Swasta\nPrivate", "Jumlah\nTotal"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t414_rows,
        col_widths=["2.5fr", "1.0fr", "1.0fr", "1.0fr"],
        source="Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi & Kementerian Agama"
    )

    # --- 4.2.1 Sarana Kesehatan ---
    sarana_kes = [
        "Rumah Sakit / Hospital",
        "Puskesmas Rawat Inap / Inpatient PHC",
        "Puskesmas Tanpa Rawat Inap / Outpatient PHC",
        "Puskesmas Pembantu (Pustu)",
        "Poliklinik / Balai Pengobatan",
        "Apotek / Pharmacy"
    ]
    t421_rows = [[s, "...", "...", "..."] for s in sarana_kes]
    t421_markup = render_typst_table(
        table_no="4.2.1",
        title_id=f"Banyaknya Sarana Kesehatan Menurut Jenis Sarana di {nama_resmi}, 2023–2025",
        title_en=f"Number of Health Facilities by Type in {nama_en}, 2023–2025",
        headers=["Jenis Sarana Kesehatan\nType of Health Facility", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t421_rows,
        col_widths=["2.5fr", "1.0fr", "1.0fr", "1.0fr"],
        source="Dinas Kesehatan, Pengendalian Penduduk dan KB Kabupaten Mempawah / Podes 2025"
    )

    # --- 4.3.1 Sumber Penerangan & 4.3.2 Bahan Bakar ---
    list_desa_energi = [[d, "...", "...", "..."] for d in desa_list]
    t431_markup = render_typst_table(
        table_no="4.3.1",
        title_id=f"Banyaknya Keluarga Menurut Sumber Penerangan Utama di {nama_resmi}, 2025",
        title_en=f"Number of Families by Main Electricity Source in {nama_en}, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Listrik PLN\nPLN Electricity", "Listrik Non-PLN\nNon-PLN Electricity", "Bukan Listrik\nNon-Electricity"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=list_desa_energi,
        col_widths=["2.2fr", "1.0fr", "1.0fr", "1.0fr"],
        source="BPS, Pendataan Potensi Desa (Podes) 2025"
    )

    # --- 4.4.1 Bencana Alam ---
    bencana_types = [
        "Tanah Longsor / Landslide",
        "Banjir / Flood",
        "Banjir Bandang / Flash Flood",
        "Gempa Bumi / Earthquake",
        "Gelombang Pasang Laut / Tidal Wave",
        "Angin Puyuh / Puting Beliung",
        "Kebakaran Hutan dan Lahan / Forest Fire"
    ]
    t441_rows = [[b, "...", "...", "..."] for b in bencana_types]
    t441_markup = render_typst_table(
        table_no="4.4.1",
        title_id=f"Banyaknya Kejadian Bencana Alam Menurut Jenis Bencana di {nama_resmi}, 2023–2025",
        title_en=f"Number of Natural Disaster Events by Type in {nama_en}, 2023–2025",
        headers=["Jenis Bencana Alam\nType of Disaster", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t441_rows,
        col_widths=["2.6fr", "1.0fr", "1.0fr", "1.0fr"],
        source="Badan Penanggulangan Bencana Daerah (BPBD) Kabupaten Mempawah / Podes 2025"
    )

    # Infografis Halaman Bab 4
    infografis_markup = f"\n{charts_markup}\n" if charts_markup.strip() else """
#v(1.5cm)
#align(center)[
  #rect(width: 95%, height: 11cm, fill: rgb("#FFFBEB"), stroke: (paint: rgb("#F59E0B"), thickness: 1.5pt, dash: "dashed"), radius: 6pt)[
    #align(center + horizon)[
      #text(12pt, weight: "bold", fill: rgb("#B45309"))[INFOGRAFIS SOSIAL & KESEJAHTERAAN RAKYAT]\
      #v(6pt)
      #text(8.5pt, fill: rgb("#92400E"), style: "italic")[Kecamatan """ + nama_singkat + """]
    ]
  ]
]
"""

    return f"""
// ==========================================
// BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT (HALAMAN PEMBATAS & INFOGRAFIS)
// ==========================================
#is_chapter_page.update(true)
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT] \\
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 4: SOCIAL AND WELFARE]
  ]
)
#v(10pt)

{infografis_markup}

#pagebreak()
#is_chapter_page.update(false)

// ==========================================
// ISI BAB 4: ULASAN NARASI & TABEL DATA
// ==========================================
#text(8.5pt)[
Pembangunan bidang sosial kemasyarakatan di Kecamatan {nama_singkat} ditopang oleh perluasan aksesibilitas sarana pendidikan dasar hingga menengah, peningkatan mutu fasilitas kesehatan masyarakat, ketersediaan energi penerangan rumah tangga, serta kesiapsiagaan dalam menghadapi potensi bencana lingkungan hidup.
]
#v(12pt)

{t411_markup}
#pagebreak()

{t412_markup}
#v(10pt)
{t413_markup}
#pagebreak()

{t414_markup}
#v(10pt)
{t421_markup}
#pagebreak()

{t431_markup}
#v(10pt)
{t441_markup}
"""
