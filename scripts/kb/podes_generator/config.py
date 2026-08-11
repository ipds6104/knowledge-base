"""Configuration Registry for BPS Potensi Desa (PODES) Publication Generator."""

PODES_SHEET_ID = "1xNPk7PZeK_MvYtRWpBUYMiIWxyg7LXSVfNTkzDWznsg"

PODES_VILLAGE_CONFIGS = {
    "pasir-palembang": {
        "name_title": "Pasir Palembang",
        "name_upper": "PASIR PALEMBANG",
        "name_kebab": "pasir-palembang",
        "admin_type": "Desa",
        "admin_type_en": "Village",
        "bps_code": "6104101004",
        "pub_no": "61040.2026.101",
        "col_name": "Desa Pasir Palembang (6104101004)",
        "kades_title": "Kepala Desa Pasir Palembang",
        "kades_title_en": "Head of Pasir Palembang Village",
        "kades_name": "As'ad Afriadi",
        "gov_name": "Pemerintah Desa Pasir Palembang",
        "gov_name_en": "Government of Pasir Palembang Village",
        "kecamatan": "Mempawah Timur",
        "kabupaten": "Mempawah",
        "provinsi": "Kalimantan Barat",
        "year": 2026,
        "data_year": 2025,
    },
    "sungai-bakau-kecil": {
        "name_title": "Sungai Bakau Kecil",
        "name_upper": "SUNGAI BAKAU KECIL",
        "name_kebab": "sungai-bakau-kecil",
        "admin_type": "Desa",
        "admin_type_en": "Village",
        "bps_code": "6104101002",
        "pub_no": "61040.2026.102",
        "col_name": "Desa Sungai Bakau Kecil (6104101002)",
        "kades_title": "Pj. Kepala Desa Sungai Bakau Kecil",
        "kades_title_en": "Acting Head of Sungai Bakau Kecil Village",
        "kades_name": "Agus Junaidi",
        "gov_name": "Pemerintah Desa Sungai Bakau Kecil",
        "gov_name_en": "Government of Sungai Bakau Kecil Village",
        "kecamatan": "Mempawah Timur",
        "kabupaten": "Mempawah",
        "provinsi": "Kalimantan Barat",
        "year": 2026,
        "data_year": 2025,
    },
    "pasir-wan-salim": {
        "name_title": "Pasir Wan Salim",
        "name_upper": "PASIR WAN SALIM",
        "name_kebab": "pasir-wan-salim",
        "admin_type": "Kelurahan",
        "admin_type_en": "Urban Village",
        "bps_code": "6104101001",
        "pub_no": "61040.2026.103",
        "col_name": "Kelurahan Pasir Wan Salim (6104101001)",
        "kades_title": "Lurah Pasir Wan Salim",
        "kades_title_en": "Head of Pasir Wan Salim Urban Village",
        "kades_name": "H. Mulyadi, S.H.I",
        "gov_name": "Pemerintah Kelurahan Pasir Wan Salim",
        "gov_name_en": "Government of Pasir Wan Salim Urban Village",
        "kecamatan": "Mempawah Hilir",
        "kabupaten": "Mempawah",
        "provinsi": "Kalimantan Barat",
        "year": 2026,
        "data_year": 2025,
    },
}


def get_podes_config(name_kebab: str) -> dict:
    """Mengambil konfigurasi desa PODES berdasarkan slug kebab-case."""
    key = name_kebab.lower().strip()
    if key not in PODES_VILLAGE_CONFIGS:
        raise KeyError(f"Konfigurasi PODES untuk desa '{name_kebab}' tidak ditemukan.")
    return PODES_VILLAGE_CONFIGS[key]
