"""Backcover generator for KCDA 2026."""

from typing import Dict, Any

COVER_BELAKANG_MAP = {
    "mempawah-hilir": "Mempawah hilir.png",
    "mempawah-timur": "Mempawah Timur.png",
    "sungai-pinyuh": "Sungai Pinyuh.png",
    "sungai-kunyit": "Sungai Kunyit.png",
    "segedong": "Segedong.png",
    "toho": "Toho.png",
    "jongkat": "Jongkat.png",
    "anjongan": "Anjongan.png",
    "sadaniang": "Sadaniang.png"
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
