"""Desa Metadata Config Registry for DDA Generator."""

DESA_CONFIGS = {
    "sungai-bakau-kecil": {
        "name_title": "Sungai Bakau Kecil",
        "name_upper": "SUNGAI BAKAU KECIL",
        "name_kebab": "sungai-bakau-kecil",
        "is_kelurahan": False,
        "admin_type": "Desa",
        "admin_type_en": "Village",
        "sub_region_type": "Dusun",
        "sub_region_type_en": "Hamlet",
        "sub_region_title": "Dusun Administrasi",
        "sub_region_title_en": "Administrative Hamlets",
        "sheet_id": "1kIn0Xn_R2C8HWznUruetLRAOeOjCzboslR0k1EDQBFI",
        "rt_tab": "Appsheet_RT",
        "fas_tab": "Appsheet_Fasilitas",
        "kecamatan": "Mempawah Timur",
        "kabupaten": "Mempawah",
        "provinsi": "Kalimantan Barat",
        "kades_title": "Plt. Kepala Desa Sungai Bakau Kecil",
        "kades_title_en": "Acting Head of Sungai Bakau Kecil Village",
        "kades_name": "Riandi Prayuda",
        "gov_name": "Pemerintah Desa Sungai Bakau Kecil",
        "gov_name_en": "Government of Sungai Bakau Kecil Village",
        "pemberita": "Tim Pembina Desa Cantik BPS Kabupaten Mempawah",
        "pub_no": "61040.2026.001",
        "year": 2026,
        "north": "Desa Pasir Palembang",
        "south": "Laut Natuna / Selat Karimata",
        "east": "Desa Sungai Bakau Besar",
        "west": "Kelurahan Pasir Wan Salim",
    },
    "pasir-palembang": {
        "name_title": "Pasir Palembang",
        "name_upper": "PASIR PALEMBANG",
        "name_kebab": "pasir-palembang",
        "is_kelurahan": False,
        "admin_type": "Desa",
        "admin_type_en": "Village",
        "sub_region_type": "Dusun",
        "sub_region_type_en": "Hamlet",
        "sub_region_title": "Dusun Administrasi",
        "sub_region_title_en": "Administrative Hamlets",
        "sheet_id": "19sh08E2kaP35brB3gUBJ0mEkXsBhoWM3zxuml1GgtnA",
        "rt_tab": "Sheet1",
        "fas_tab": "Sheet4",
        "kecamatan": "Mempawah Timur",
        "kabupaten": "Mempawah",
        "provinsi": "Kalimantan Barat",
        "kades_title": "Kepala Desa Pasir Palembang",
        "kades_title_en": "Head of Pasir Palembang Village",
        "kades_name": "As'ad Afriadi",
        "gov_name": "Pemerintah Desa Pasir Palembang",
        "gov_name_en": "Government of Pasir Palembang Village",
        "pemberita": "Tim Pembina Desa Cantik BPS Kabupaten Mempawah",
        "pub_no": "61040.2026.002",
        "year": 2026,
        "north": "Desa Pasir",
        "south": "Desa Sungai Bakau Kecil",
        "east": "Desa Antibar",
        "west": "Kelurahan Pasir Wan Salim",
    },
    "pasir-wan-salim": {
        "name_title": "Pasir Wan Salim",
        "name_upper": "PASIR WAN SALIM",
        "name_kebab": "pasir-wan-salim",
        "is_kelurahan": True,
        "admin_type": "Kelurahan",
        "admin_type_en": "Urban Village",
        "sub_region_type": "RW",
        "sub_region_type_en": "Community Unit",
        "sub_region_title": "Rukun Warga (RW)",
        "sub_region_title_en": "Community Units (RW)",
        "sheet_id": "1XJ8ywTVfDQqeOpgLcDSEsayA3B7k_PvT9HqUcihrMNw",
        "rt_tab": "Sheet1",
        "fas_tab": "",
        "kecamatan": "Mempawah Timur",
        "kabupaten": "Mempawah",
        "provinsi": "Kalimantan Barat",
        "kades_title": "Lurah Pasir Wan Salim",
        "kades_title_en": "Head of Pasir Wan Salim Urban Village",
        "kades_name": "H. Mulyadi, S.H.I",
        "gov_name": "Pemerintah Kelurahan Pasir Wan Salim",
        "gov_name_en": "Government of Pasir Wan Salim Urban Village",
        "pemberita": "Tim Pembina Desa Cantik BPS Kabupaten Mempawah",
        "pub_no": "61040.2026.003",
        "year": 2026,
        "north": "Desa Pasir",
        "south": "Laut Natuna",
        "east": "Desa Sungai Bakau Kecil",
        "west": "Kecamatan Mempawah Hilir",
    },
}


def get_desa_config(name_kebab: str, sheet_id: str = None, year: int = 2026) -> dict:
    """Mengambil atau mengonstruksi konfigurasi desa/kelurahan berdasarkan nama kebab."""
    key = name_kebab.strip().lower()
    if key in DESA_CONFIGS:
        cfg = DESA_CONFIGS[key].copy()
    else:
        title = key.replace("-", " ").title()
        is_kel = "kelurahan" in key
        adm_type = "Kelurahan" if is_kel else "Desa"
        adm_type_en = "Urban Village" if is_kel else "Village"
        sub_type = "RW" if is_kel else "Dusun"
        sub_type_en = "Community Unit" if is_kel else "Hamlet"
        sub_title = "Rukun Warga (RW)" if is_kel else "Dusun Administrasi"
        sub_title_en = "Community Units (RW)" if is_kel else "Administrative Hamlets"

        cfg = {
            "name_title": title,
            "name_upper": title.upper(),
            "name_kebab": key,
            "is_kelurahan": is_kel,
            "admin_type": adm_type,
            "admin_type_en": adm_type_en,
            "sub_region_type": sub_type,
            "sub_region_type_en": sub_type_en,
            "sub_region_title": sub_title,
            "sub_region_title_en": sub_title_en,
            "sheet_id": "",
            "kecamatan": "Mempawah Timur",
            "kabupaten": "Mempawah",
            "provinsi": "Kalimantan Barat",
            "kades_title": f"Lurah {title}" if is_kel else f"Kepala Desa {title}",
            "kades_title_en": f"Head of {title} {adm_type_en}",
            "kades_name": f"Lurah {title}" if is_kel else f"Kepala Desa {title}",
            "gov_name": f"Pemerintah {adm_type} {title}",
            "gov_name_en": f"Government of {title} {adm_type_en}",
            "pemberita": "Tim Pembina Desa Cantik BPS Kabupaten Mempawah",
            "pub_no": f"61040.{year}.999",
            "year": year,
            "north": "-",
            "south": "-",
            "east": "-",
            "west": "-",
        }

    if sheet_id:
        cfg["sheet_id"] = sheet_id
    if year:
        cfg["year"] = year

    return cfg
