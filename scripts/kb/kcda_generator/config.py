"""
KCDA Dynamic Configuration Module.
Loads regency and kecamatan configuration from config/regency.yaml or config/regency.example.yaml.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
CONFIG_FILE = REPO_ROOT / "config" / "regency.yaml"
EXAMPLE_CONFIG_FILE = REPO_ROOT / "config" / "regency.example.yaml"
TABLES_SCHEMA_FILE = REPO_ROOT / "config" / "tables_schema.json"

DEFAULT_REGENCY_RAW_CONFIG: Dict[str, Any] = {
    "kabupaten": {
        "nama_resmi": "Kabupaten Mempawah",
        "nama_singkat": "Mempawah",
        "nama_en": "Mempawah Regency",
        "kode_kabupaten": "6104",
        "ibukota_kabupaten": "Mempawah",
    },
    "instansi": {
        "nama_resmi": "Badan Pusat Statistik Kabupaten Mempawah",
        "nama_singkat": "BPS Kabupaten Mempawah",
        "nama_en": "BPS-Statistics of Mempawah Regency",
        "alamat": "Jl. Raden Kusno No. 1, Mempawah",
    },
    "publikasi": {
        "tahun_rilis": 2026,
    },
    "pimpinan": {
        "nama_lengkap": "Munawir, S.Si., M.M.",
        "nama_polos": "Munawir",
        "jabatan_resmi": "Kepala Badan Pusat Statistik Kabupaten Mempawah",
        "jabatan_singkat": "Kepala BPS Kabupaten Mempawah",
    },
    "is_template_default": False,
    "kecamatan": [
        {
            "slug": "mempawah-hilir",
            "nama_resmi": "Kecamatan Mempawah Hilir",
            "nama_singkat": "Mempawah Hilir",
            "nama_en": "Mempawah Hilir Subdistrict",
            "kode_wilayah": "6104050",
            "no_katalog": "1102001.6104050",
            "no_publikasi": "61040.26012",
            "pic_nama": "Sukma Andini, S.Tr.Stat.",
            "ibukota": "Tanjung",
            "desa_list": ["Tanjung", "Kuala Secapah", "Tengah", "Terusan", "Pasir", "Penibung", "Sengkubang", "Malikian"],
            "cover_depan": "assets/covers/depan/Mempawah-Hilir1.jpg",
            "cover_dalam": "assets/covers/depan/Mempawah-Hilir2.jpg",
            "gsheet_id": "",
            "volume": "Volume 17, 2026",
            "issn": "",
            "peta": "assets/maps/mempawah-hilir.jpg"
        },
        {
            "slug": "mempawah-timur",
            "nama_resmi": "Kecamatan Mempawah Timur",
            "nama_singkat": "Mempawah Timur",
            "nama_en": "Mempawah Timur Subdistrict",
            "kode_wilayah": "6104051",
            "no_katalog": "1102001.6104051",
            "no_publikasi": "61040.26004",
            "pic_nama": "Ahmad Aulia Rahman, S.Tr.Stat.",
            "ibukota": "Antibar",
            "desa_list": ["Pasir Wan Salim", "Sungai Bakau Kecil", "Pasir Panjang", "Pasir Palembang", "Pulau Pedalaman", "Antibar", "Sejegi", "Parit Banjar"],
            "cover_depan": "assets/covers/depan/Mempawah-Timur1.jpg",
            "cover_dalam": "assets/covers/depan/Mempawah-Timur2.jpg",
            "gsheet_id": "",
            "volume": "Volume 17, 2026",
            "issn": "",
            "peta": "assets/maps/mempawah-timur.jpg"
        },
        {
            "slug": "sungai-pinyuh",
            "nama_resmi": "Kecamatan Sungai Pinyuh",
            "nama_singkat": "Sungai Pinyuh",
            "nama_en": "Sungai Pinyuh Subdistrict",
            "kode_wilayah": "6104040",
            "no_katalog": "1102001.6104040",
            "no_publikasi": "61040.26011",
            "pic_nama": "Vaniya Dewi Wulandari, A.Md.Stat.",
            "ibukota": "Sungai Pinyuh",
            "desa_list": ["Sungai Purun Kecil", "Peniraman", "Nusapati", "Galang", "Sungai Rasau", "Sungai Pinyuh", "Sungai Batang", "Sungai Bakau Besar Laut", "Sungai Bakau Besar Darat"],
            "cover_depan": "assets/covers/depan/Sungai-Pinyuh1.jpg",
            "cover_dalam": "assets/covers/depan/Sungai-Pinyuh2.jpg",
            "gsheet_id": "",
            "volume": "Volume 17, 2026",
            "issn": "",
            "peta": "assets/maps/sungai-pinyuh.jpg"
        },
        {
            "slug": "sungai-kunyit",
            "nama_resmi": "Kecamatan Sungai Kunyit",
            "nama_singkat": "Sungai Kunyit",
            "nama_en": "Sungai Kunyit Subdistrict",
            "kode_wilayah": "6104060",
            "no_katalog": "1102001.6104060",
            "no_publikasi": "61040.26005",
            "pic_nama": "Sarah Pratiwi, S.Tr.Stat.",
            "ibukota": "Sungai Kunyit Laut",
            "desa_list": ["Semudun", "Semparong Parit Raden", "Mendalok", "Sungai Dungun", "Sungai Limau", "Sungai Kunyit Laut", "Sungai Kunyit Dalam", "Sungai Kunyit Hulu", "Bukit Batu", "Sungai Bundung Laut", "Sungai Duri I", "Sungai Duri II"],
            "cover_depan": "assets/covers/depan/Sungai-Kunyit1.jpg",
            "cover_dalam": "assets/covers/depan/Sungai-Kunyit2.jpg",
            "gsheet_id": "",
            "volume": "Volume 17, 2026",
            "issn": "",
            "peta": "assets/maps/sungai-kunyit.jpg"
        },
        {
            "slug": "segedong",
            "nama_resmi": "Kecamatan Segedong",
            "nama_singkat": "Segedong",
            "nama_en": "Segedong Subdistrict",
            "kode_wilayah": "6104030",
            "no_katalog": "1102001.6104030",
            "no_publikasi": "61040.26010",
            "pic_nama": "Listio Jati Nandhiko, S.Tr.Stat.",
            "ibukota": "Parit Bugis",
            "desa_list": ["Peniti Dalam I", "Sungai Burung", "Sungai Purun Besar", "Parit Bugis", "Peniti Besar", "Peniti Dalam II"],
            "cover_depan": "assets/covers/depan/Segedong1.jpg",
            "cover_dalam": "assets/covers/depan/Segedong2.jpg",
            "gsheet_id": "",
            "volume": "Volume 17, 2026",
            "issn": "",
            "peta": "assets/maps/segedong.jpg"
        },
        {
            "slug": "toho",
            "nama_resmi": "Kecamatan Toho",
            "nama_singkat": "Toho",
            "nama_en": "Toho Subdistrict",
            "kode_wilayah": "6104070",
            "no_katalog": "1102001.6104070",
            "no_publikasi": "61040.26006",
            "pic_nama": "Arini Faurizah, S.Tr.Stat.",
            "ibukota": "Toho",
            "desa_list": ["Sambora", "Benuang", "Pak Utan", "Sepang", "Pak Laheng", "Terap", "Kecurit", "Toho Ilir"],
            "cover_depan": "assets/covers/depan/Toho1.jpg",
            "cover_dalam": "assets/covers/depan/Toho2.jpg",
            "gsheet_id": "",
            "volume": "Volume 17, 2026",
            "issn": "",
            "peta": "assets/maps/toho.jpg"
        },
        {
            "slug": "jongkat",
            "nama_resmi": "Kecamatan Jongkat",
            "nama_singkat": "Jongkat",
            "nama_en": "Jongkat Subdistrict",
            "kode_wilayah": "6104020",
            "no_katalog": "1102001.6104020",
            "no_publikasi": "61040.26008",
            "pic_nama": "Ihza Fikri Zaki Karunia, S.Tr.Stat.",
            "ibukota": "Jungkat",
            "desa_list": ["Sungai Nipah", "Jungkat", "Wajok Hilir", "Wajok Hulu", "Peniti Luar"],
            "cover_depan": "assets/covers/depan/Jongkat1.jpg",
            "cover_dalam": "assets/covers/depan/Jongkat2.jpg",
            "gsheet_id": "",
            "volume": "Volume 17, 2026",
            "issn": "",
            "peta": "assets/maps/jongkat.jpg"
        },
        {
            "slug": "anjongan",
            "nama_resmi": "Kecamatan Anjongan",
            "nama_singkat": "Anjongan",
            "nama_en": "Anjongan Subdistrict",
            "kode_wilayah": "6104041",
            "no_katalog": "1102001.6104041",
            "no_publikasi": "61040.26009",
            "pic_nama": "Rifky Mullah Syadriawan, A.Md.Stat.",
            "ibukota": "Anjungan Melancar",
            "desa_list": ["Anjungan Melancar", "Anjungan Dalam", "Pak Bulu", "Dema", "Kepayang"],
            "cover_depan": "assets/covers/depan/Anjongan1.jpg",
            "cover_dalam": "assets/covers/depan/Anjongan2.jpg",
            "gsheet_id": "",
            "volume": "Volume 17, 2026",
            "issn": "",
            "peta": "assets/maps/anjongan.jpg"
        },
        {
            "slug": "sadaniang",
            "nama_resmi": "Kecamatan Sadaniang",
            "nama_singkat": "Sadaniang",
            "nama_en": "Sadaniang Subdistrict",
            "kode_wilayah": "6104080",
            "no_katalog": "1102001.6104080",
            "no_publikasi": "61040.26007",
            "pic_nama": "Budiman Aller Silaban, S.Tr.Stat.",
            "ibukota": "Pentek",
            "desa_list": ["Pentek", "Sekabuk", "Bum-Bun", "Amawang", "Ansiap", "Suak Barangan"],
            "cover_depan": "assets/covers/depan/Sadaniang1.jpg",
            "cover_dalam": "assets/covers/depan/Sadaniang2.jpg",
            "gsheet_id": "",
            "volume": "Volume 17, 2026",
            "issn": "",
            "peta": "assets/maps/sadaniang.jpg"
        }
    ]
}

def _load_raw_config() -> Dict[str, Any]:
    target = CONFIG_FILE if CONFIG_FILE.exists() else (EXAMPLE_CONFIG_FILE if EXAMPLE_CONFIG_FILE.exists() else None)
    if target and target.exists():
        with open(target, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            if isinstance(loaded, dict):
                return loaded
    return DEFAULT_REGENCY_RAW_CONFIG

REGENCY_RAW_CONFIG = _load_raw_config()
IS_TEMPLATE_DEFAULT = REGENCY_RAW_CONFIG.get("is_template_default", True)

# Build KCDA_KECAMATAN_CONFIG dictionary for backwards compatibility & fast lookup
KCDA_KECAMATAN_CONFIG: Dict[str, Dict[str, Any]] = {}
for kec in REGENCY_RAW_CONFIG.get("kecamatan", []):
    slug = kec.get("slug")
    if slug:
        KCDA_KECAMATAN_CONFIG[slug] = {
            "slug": slug,
            "nama_resmi": kec.get("nama_resmi", f"Kecamatan {slug.replace('-', ' ').title()}"),
            "nama_singkat": kec.get("nama_singkat", slug.replace('-', ' ').title()),
            "nama_en": kec.get("nama_en", f"{slug.replace('-', ' ').title()} Subdistrict"),
            "kode_wilayah": str(kec.get("kode_wilayah", "")),
            "no_katalog": str(kec.get("no_katalog", "")),
            "no_publikasi": str(kec.get("no_publikasi", "")),
            "pic_nama": kec.get("pic_nama", "Staf BPS"),
            "pic_nama_polos": kec.get("pic_nama", "Staf BPS").split(",")[0].strip(),
            "ibukota_kecamatan": kec.get("ibukota", ""),
            "desa_list": kec.get("desa_list", []),
            "cover_depan": kec.get("cover_depan", f"assets/covers/depan/{slug.title()}1.jpg"),
            "cover_dalam": kec.get("cover_dalam", f"assets/covers/depan/{slug.title()}2.jpg"),
            "gsheet_id": kec.get("gsheet_id", ""),
            "volume": kec.get("volume", "Volume 17, 2026"),
            "issn": kec.get("issn", ""),
            "peta": kec.get("peta", f"assets/maps/{slug}.jpg")
        }

def get_regency_info() -> Dict[str, Any]:
    """Mengembalikan informasi profil kabupaten/kota."""
    return REGENCY_RAW_CONFIG.get("kabupaten", {})

def get_instansi_info() -> Dict[str, Any]:
    """Mengembalikan informasi instansi BPS."""
    return REGENCY_RAW_CONFIG.get("instansi", {})

def get_publikasi_info() -> Dict[str, Any]:
    """Mengembalikan konfigurasi publikasi."""
    return REGENCY_RAW_CONFIG.get("publikasi", {})

def get_pimpinan_info() -> Dict[str, Any]:
    """Mengembalikan profil pimpinan BPS."""
    return REGENCY_RAW_CONFIG.get("pimpinan", {})

def get_tables_schema() -> List[Dict[str, Any]]:
    """Mengembalikan skema daftar tabel (wajib & opsional)."""
    if TABLES_SCHEMA_FILE.exists():
        with open(TABLES_SCHEMA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
