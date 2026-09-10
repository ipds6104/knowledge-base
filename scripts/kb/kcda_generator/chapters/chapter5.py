"""Chapter 5: Pertanian Generator for KCDA 2026."""

from typing import Dict, Any, List
from ..data_loader import get_kecamatan_tab_rows, clean_cell_value
from ..table_renderer import render_typst_table

def render_chapter5(cfg: Dict[str, Any]) -> str:
    nama_resmi = cfg["nama_resmi"]
    nama_en = cfg["nama_en"]
    nama_singkat = nama_resmi.replace("Kecamatan ", "")

    # --- 5.1 & 5.2 Sayuran ---
    sayuran_list = [
        "Bawang Merah / Shallots",
        "Cabai Besar / Big Chili",
        "Cabai Rawit / Cayenne Pepper",
        "Tomat / Tomato",
        "Terung / Eggplant",
        "Kacang Panjang / Long Beans",
        "Ketimun / Cucumber",
        "Kangkung / Water Spinach",
        "Bayam / Spinach"
    ]
    t51_rows = [[s, "...", "...", "...", "..."] for s in sayuran_list]
    t51_markup = render_typst_table(
        table_no="5.1",
        title_id=f"Luas Panen Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di {nama_resmi}, 2022–2025",
        title_en=f"Harvested Area of Seasonal Vegetables and Fruits by Kind of Plants in {nama_en}, 2022–2025",
        headers=["Jenis Tanaman\nKind of Plants", "2022 (ha)", "2023 (ha)", "2024 (ha)", "2025 (ha)"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t51_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS)"
    )

    t52_rows = [[s, "...", "...", "...", "..."] for s in sayuran_list]
    t52_markup = render_typst_table(
        table_no="5.2",
        title_id=f"Produksi Tanaman Sayuran dan Buah-buahan Semusim Menurut Jenis Tanaman di {nama_resmi}, 2022–2025",
        title_en=f"Production of Seasonal Vegetables and Fruits by Kind of Plants in {nama_en}, 2022–2025",
        headers=["Jenis Tanaman\nKind of Plants", "2022 (ku)", "2023 (ku)", "2024 (ku)", "2025 (ku)"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t52_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-SBS)"
    )

    # --- 5.3 & 5.4 Biofarmaka ---
    bio_list = [
        "Jahe / Ginger",
        "Lengkuas / Galangal",
        "Kencur / East Indian Galangal",
        "Kunyit / Turmeric",
        "Lempuyang",
        "Temulawak / Java Turmeric"
    ]
    t53_rows = [[b, "...", "...", "...", "..."] for b in bio_list]
    t53_markup = render_typst_table(
        table_no="5.3",
        title_id=f"Luas Panen Tanaman Biofarmaka Menurut Jenis Tanaman di {nama_resmi}, 2022–2025",
        title_en=f"Harvested Area of Medicinal Plants by Kind of Plants in {nama_en}, 2022–2025",
        headers=["Jenis Tanaman\nKind of Plants", "2022 (m²)", "2023 (m²)", "2024 (m²)", "2025 (m²)"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t53_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF)"
    )

    t54_rows = [[b, "...", "...", "...", "..."] for b in bio_list]
    t54_markup = render_typst_table(
        table_no="5.4",
        title_id=f"Produksi Tanaman Biofarmaka Menurut Jenis Tanaman di {nama_resmi}, 2022–2025",
        title_en=f"Production of Medicinal Plants by Kind of Plants in {nama_en}, 2022–2025",
        headers=["Jenis Tanaman\nKind of Plants", "2022 (kg)", "2023 (kg)", "2024 (kg)", "2025 (kg)"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t54_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-TBF)"
    )

    # --- 5.7 Buah-buahan ---
    buah_list = [
        "Durian / Durian",
        "Mangga / Mango",
        "Jeruk Siam / Siamese Orange",
        "Pisang / Banana",
        "Pepaya / Papaya",
        "Nanas / Pineapple",
        "Rambutan / Rambutan"
    ]
    t57_rows = [[f, "...", "...", "...", "..."] for f in buah_list]
    t57_markup = render_typst_table(
        table_no="5.7",
        title_id=f"Produksi Buah-Buahan dan Sayuran Tahunan Menurut Jenis Tanaman di {nama_resmi}, 2022–2025",
        title_en=f"Production of Annual Fruits and Vegetables by Kind of Plants in {nama_en}, 2022–2025",
        headers=["Jenis Tanaman\nKind of Plants", "2022 (ku)", "2023 (ku)", "2024 (ku)", "2025 (ku)"],
        col_numbers=["(1)", "(2)", "(3)", "(4)", "(5)"],
        rows=t57_rows,
        col_widths=["2.6fr", "0.9fr", "0.9fr", "0.9fr", "0.9fr"],
        source="BPS - Kementerian Pertanian, Survei Pertanian Hortikultura (SPH-BST)"
    )

    return f"""
// ==========================================
// BAB 5: PERTANIAN
// ==========================================
#v(0.5cm)
#block(
  fill: rgb("#FEF3C7"),
  inset: 12pt,
  width: 100%,
  stroke: (left: 4pt + rgb("#D97706")),
  [
    #text(14pt, weight: "bold", fill: rgb("#92400E"))[BAB 5: PERTANIAN] \\
    #text(10pt, style: "italic", fill: rgb("#B45309"))[CHAPTER 5: AGRICULTURE]
  ]
)
#v(10pt)

#text(8.5pt)[
Sektor pertanian merupakan salah satu pilar penopang perekonomian masyarakat di Kecamatan {nama_singkat}. Komoditas sayuran semusim, tanaman biofarmaka, serta buah-buahan tahunan dibudidayakan secara intensif oleh rumah tangga petani guna memenuhi kebutuhan pasar domestik dan regional Kabupaten Mempawah.
]

#v(8pt)
{t51_markup}
#pagebreak()

{t52_markup}
#pagebreak()

{t53_markup}
#v(10pt)
{t54_markup}
#pagebreak()

{t57_markup}
#pagebreak()
"""
