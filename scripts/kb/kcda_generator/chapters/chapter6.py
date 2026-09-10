"""Chapter 6: Pariwisata, Transportasi dan Komunikasi Generator for KCDA 2026."""

from typing import Dict, Any, List
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table

def render_chapter6(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")
    desa_list = cfg["desa_list"]

    # --- 6.1.1 Sarana Transportasi Antardesa ---
    t611_rows = [[d, "...", "...", "..."] for d in desa_list]
    t611_markup = render_typst_table(
        table_no="6.1.1",
        title_id=f"Banyaknya Desa/Kelurahan Menurut Keberadaan Sarana Transportasi Antardesa di {nama_resmi}, 2025",
        title_en=f"Number of Villages by Inter-Village Transportation Infrastructure in {nama_en}, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Jenis Lalu Lintas", "Jenis Permukaan Jalan", "Dapat Dilalui Roda 4+"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t611_rows,
        col_widths=["2.2fr", "1.1fr", "1.2fr", "1.1fr"],
        source="BPS, Pendataan Potensi Desa (Podes) 2025"
    )

    # --- 6.2.1 Kantor Pos / Pos Pembantu / Agen Logistik ---
    pos_types = [
        "Kantor Pos / Pos Pembantu / Rumah Pos",
        "Perusahaan / Agen Jasa Ekspedisi Swasta"
    ]
    t621_rows = [[p, "...", "...", "..."] for p in pos_types]
    t621_markup = render_typst_table(
        table_no="6.2.1",
        title_id=f"Banyaknya Desa/Kelurahan Menurut Keberadaan Kantor Pos dan Ekspedisi Swasta di {nama_resmi}, 2023–2025",
        title_en=f"Number of Villages by Availability of Post Office and Private Courier in {nama_en}, 2023–2025",
        headers=["Jenis Fasilitas Pos / Logistik\nType of Postal/Courier Facility", "2023", "2024", "2025"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t621_rows,
        col_widths=["2.8fr", "1.0fr", "1.0fr", "1.0fr"],
        source="BPS, Pendataan Potensi Desa (Podes) 2025"
    )

    # --- 6.3.1 Menara BTS dan Sinyal Internet ---
    t631_rows = [[d, "...", "...", "..."] for d in desa_list]
    t631_markup = render_typst_table(
        table_no="6.3.1",
        title_id=f"Banyaknya Menara BTS dan Kekuatan Sinyal Internet Seluler Menurut Desa di {nama_resmi}, 2025",
        title_en=f"Number of BTS Towers and Cellular Internet Signal Strength by Village in {nama_en}, 2025",
        headers=["Desa/Kelurahan\nVillage/Subdistrict", "Jumlah Menara BTS", "Sinyal Telepon Seluler", "Sinyal Internet (4G/5G)"],
        col_numbers=["(1)", "(2)", "(3)", "(4)"],
        rows=t631_rows,
        col_widths=["2.2fr", "1.0fr", "1.2fr", "1.2fr"],
        source="BPS, Pendataan Potensi Desa (Podes) 2025"
    )

    return f"""
// ==========================================
// BAB 6: PARIWISATA, TRANSPORTASI & KOMUNIKASI
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 6: PARIWISATA, TRANSPORTASI & KOMUNIKASI] \\
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 6: TOURISM, TRANSPORTATION AND COMMUNICATION]
  ]
)
#v(10pt)

#text(8.5pt)[
Konektivitas wilayah di Kecamatan {nama_singkat} terhubung oleh jaringan jalan darat antardesa yang dapat dilalui kendaraan roda empat sepanjang tahun. Selain itu, penetrasi infrastruktur telekomunikasi bergerak (seluler) dan jaringan internet berkecepatan tinggi terus meluas, mempercepat arus informasi dan transaksi digital masyarakat.
]

#v(8pt)
{t611_markup}
#pagebreak()

{t621_markup}
#v(10pt)
{t631_markup}
#pagebreak()
"""
