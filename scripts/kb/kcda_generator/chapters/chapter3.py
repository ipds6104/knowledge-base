"""Chapter 3: Kependudukan Generator for KCDA 2026."""

from typing import Dict, Any, List
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table

def render_chapter3(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")
    desa_list = cfg["desa_list"]

    # --- 3.1 Penduduk & Kepadatan ---
    rows_31_raw = get_kecamatan_tab_rows("3.1", nama_singkat)
    pop_map = {}
    for r in rows_31_raw[3:]:
        if len(r) > 1 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['jumlah', 'total', 'sumber']):
            lk = clean_cell_value(r[1] if len(r) > 1 else "...")
            pr = clean_cell_value(r[2] if len(r) > 2 else "...")
            jml = clean_cell_value(r[3] if len(r) > 3 else "...")
            pct = clean_cell_value(r[4] if len(r) > 4 else "...")
            kepadatan = clean_cell_value(r[5] if len(r) > 5 else "...")
            pop_map[r[0].strip().lower()] = [lk, pr, jml, pct, kepadatan]

    t31_rows = []
    for d in desa_list:
        v = pop_map.get(d.lower(), ["...", "...", "...", "...", "..."])
        t31_rows.append([d, v[0], v[1], v[2], v[3], v[4]])

    t31_markup = render_typst_table(
        table_no="3.1",
        title_id=f"Penduduk, Distribusi Persentase, dan Kepadatan Penduduk Menurut Desa/Kelurahan di {nama_resmi}, 2025",
        title_en=f"Population, Percentage Distribution, and Density by Village/Subdistrict in {nama_en}, 2025",
        headers=[
            "Desa/Kelurahan\nVillage/Subdistrict",
            "Laki-laki\nMale",
            "Perempuan\nFemale",
            "Jumlah\nTotal",
            "Persentase\nPercentage (%)",
            "Kepadatan\nDensity (jiwa/km²)"
        ],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)", "(6)"],
        rows=t31_rows,
        col_widths=["2.0fr", "1.0fr", "1.0fr", "1.1fr", "1.0fr", "1.2fr"],
        source="Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah (Semester II 2025)"
    )

    return f"""
// ==========================================
// BAB 3: KEPENDUDUKAN
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 3: KEPENDUDUKAN] \\
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 3: POPULATION]
  ]
)
#v(10pt)

#text(8.5pt)[
Berdasarkan data registrasi semester II tahun 2025 dari Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah, jumlah penduduk Kecamatan {nama_singkat} terdistribusi di {len(desa_list)} desa/kelurahan dengan struktur demografi yang produktif. Komposisi penduduk laki-laki dan perempuan relatif berimbang, mencerminkan kestabilan demografis wilayah.
]

#v(8pt)
{t31_markup}
#pagebreak()
"""
