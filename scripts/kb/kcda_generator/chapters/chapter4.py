"""Chapter 4: Sosial dan Kesejahteraan Rakyat Generator for KCDA 2026."""

from typing import Dict, Any, List
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table

def render_chapter4(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")
    desa_list = cfg["desa_list"]

    # --- 4.1.1 Fasilitas Pendidikan di Desa (Podes) ---
    t411_rows = []
    for d in desa_list:
        t411_rows.append([d, "...", "...", "...", "..."])
    t411_markup = render_typst_table(
        table_no="4.1.1",
        title_id=f"Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan di {nama_resmi}, 2025",
        title_en=f"Number of Villages Having Educational Facilities by Level in {nama_en}, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "SD / MI", "SMP / MTs", "SMA / SMK / MA", "Akademi / PT"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t411_rows,
        col_widths=["2.2fr", "1.0fr", "1.0fr", "1.1fr", "1.1fr"],
        source="BPS, Pendataan Potensi Desa (Podes) 2025"
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
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Listrik PLN", "Listrik Non-PLN", "Bukan Listrik"],
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

    return f"""
// ==========================================
// BAB 4: SOSIAL DAN KESEJAHTERAAN RAKYAT
// ==========================================
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

#text(8.5pt)[
Pembangunan bidang sosial kemasyarakatan di Kecamatan {nama_singkat} ditopang oleh perluasan aksesibilitas sarana pendidikan dasar hingga menengah, peningkatan mutu fasilitas kesehatan masyarakat, ketersediaan energi penerangan rumah tangga, serta kesiapsiagaan dalam menghadapi potensi bencana lingkungan hidup.
]

#v(8pt)
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
#pagebreak()
"""
