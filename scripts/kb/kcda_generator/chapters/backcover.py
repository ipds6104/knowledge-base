"""Backcover generator for KCDA 2026."""

from typing import Dict, Any

COVER_BELAKANG_MAP = {
    "mempawah-hilir": "Mempawah hilir.jpg",
    "mempawah-timur": "Mempawah Timur.jpg",
    "sungai-pinyuh": "Sungai Pinyuh.jpg",
    "sungai-kunyit": "Sungai Kunyit.jpg",
    "segedong": "Segedong.jpg",
    "toho": "Toho.jpg",
    "jongkat": "Jongkat.jpg",
    "anjongan": "Anjongan.jpg",
    "sadaniang": "Sadaniang.jpg"
}

def render_backcover(cfg: Dict[str, Any]) -> str:
    slug = cfg.get("slug", "")
    cover_belakang = COVER_BELAKANG_MAP.get(slug, "Anjongan.png")

    return f"""// ==========================================
// KOVER BELAKANG (BACK COVER) - DESAIN VISUAL RESMI
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("/kegiatan/kecamatan-dalam-angka/2026/assets/covers/belakang/{cover_belakang}", width: 100%, height: 100%)
]
"""
