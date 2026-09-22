"""
Frontmatter: Cover & Title Page for KCDA 2026.
Menangani Kover Depan dan Halaman Judul Utama (Halaman i).
"""

from typing import Dict, Any

COVER_DEPAN_MAP = {
    "mempawah-hilir": "Mempawah Hilir1.png",
    "mempawah-timur": "Mempawah Timur1.png",
    "sungai-pinyuh": "Sungai Pinyuh1.png",
    "sungai-kunyit": "Sungai Kunyit1.png",
    "segedong": "Segedong1.png",
    "toho": "Toho1.png",
    "jongkat": "Jongkat1.png",
    "anjongan": "Anjongan1.png",
    "sadaniang": "Sadaniang1.png"
}

COVER_DALAM_MAP = {
    "mempawah-hilir": "Mempawah Hilir2.png",
    "mempawah-timur": "Mempawah Timur2.png",
    "sungai-pinyuh": "Sungai Pinyuh2.png",
    "sungai-kunyit": "Sungai Kunyit2.png",
    "segedong": "Segedong2.png",
    "toho": "Toho2.png",
    "jongkat": "Jongkat2.png",
    "anjongan": "Anjongan2.png",
    "sadaniang": "Sadaniang2.png"
}

def render_cover_and_title_page(cfg: Dict[str, Any]) -> str:
    slug = cfg.get("slug", "")
    cover_depan = COVER_DEPAN_MAP.get(slug, "Anjongan1.png")
    cover_dalam = COVER_DALAM_MAP.get(slug, "Anjongan2.png")

    return f"""// ==========================================
// 1. KOVER DEPAN (FRONT COVER) - DESAIN RESMI TERBARU
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/depan/{cover_depan}", width: 100%, height: 100%)
]

// ==========================================
// HALAMAN KOSONG DI BALIK KOVER DEPAN (INSIDE COVER / FLYLEAF)
// Sesuai Pedoman Pembuatan Publikasi BPS 2023 Subbab 4.1.2 Poin 6 (Hal. 45) & Terbitan Statistik Indonesia BPS RI.
// Halaman setelah kover depan tidak dihitung sebagai halaman dan tidak diberi nomor halaman.
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[ ]

// ==========================================
// 2. HALAMAN JUDUL UTAMA / TITLE PAGE (HALAMAN i)
// Terletak pada halaman ganjil (rekto/kanan) sesuai Pedoman Publikasi BPS 2023 Subbab 4.3.1 (Hal. 75).
// Perhitungan angka romawi resmi dimulai pada Halaman Judul Utama (halaman i).
// ==========================================
#counter(page).update(1)

#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/depan/{cover_dalam}", width: 100%, height: 100%)
]
"""
