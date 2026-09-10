#!/usr/bin/env python3
"""
Upload Sakernas Agustus 2026 Mempawah Dataset to Google Drive (35. Sakernas / 2026-08).
Organizes files into a clean hierarchy:
- 01_Dataset_Utama/
- 02_Tabel_Mikro/
- 03_Metadata_dan_Kamus_Data/
"""

import os
import sys
from pathlib import Path

# Add scripts directory to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from kb.google_drive import (
    get_drive_service,
    get_or_create_gdrive_folder,
    list_gdrive_contents,
    upload_or_update_file
)

ROOT_FOLDER_ID = "140jAM_Zcv_t7p7T2X4yYOmOG79zzCkSS"  # 35. Sakernas
PERIOD_NAME = "2026-08"
RAW_DATA_DIR = Path(BASE_DIR) / "kegiatan" / "sakernas" / "2026-08" / "raw_data"


def main():
    print(f"🚀 Memulai sinkronisasi dataset Sakernas ke Google Drive...")
    print(f"   Target Root : 35. Sakernas (ID: {ROOT_FOLDER_ID})")
    print(f"   Subfolder   : {PERIOD_NAME}")

    service = get_drive_service()

    # 1. Pastikan folder periode '2026-08' ada
    period_folder_id = get_or_create_gdrive_folder(service, PERIOD_NAME, ROOT_FOLDER_ID)
    print(f"✓ Folder periode '{PERIOD_NAME}' siap (ID: {period_folder_id})")

    # 2. Siapkan subfolder rapi di dalam 2026-08
    folder_mapping = {
        "01_Dataset_Utama": [
            RAW_DATA_DIR / "sakernas_agustus_2026_mempawah_master_flat.xlsx",
            RAW_DATA_DIR / "sakernas_agustus_2026_mempawah_master_flat.csv",
        ],
        "02_Tabel_Mikro": [
            RAW_DATA_DIR / "art_roster_mempawah_full_637cols.xlsx",
            RAW_DATA_DIR / "art_roster_mempawah_full_637cols.csv",
            RAW_DATA_DIR / "root_table_mempawah_full_120cols.xlsx",
            RAW_DATA_DIR / "root_table_mempawah_full_120cols.csv",
            RAW_DATA_DIR / "base_table_assignment_mempawah_full_86cols.xlsx",
            RAW_DATA_DIR / "base_table_assignment_mempawah_full_86cols.csv",
            RAW_DATA_DIR / "petugas_mempawah_full_21cols.xlsx",
            RAW_DATA_DIR / "petugas_mempawah_full_21cols.csv",
        ],
        "03_Metadata_dan_Kamus_Data": [
            RAW_DATA_DIR / "kamus_variabel_sakernas_202608.xlsx",
            Path(BASE_DIR) / "kegiatan" / "sakernas" / "2026-08" / "metadata_tables_sakernas.json",
        ]
    }

    uploaded_summary = []

    for subfolder_name, file_list in folder_mapping.items():
        print(f"\n📁 Mengelola subfolder: {subfolder_name}...")
        subfolder_id = get_or_create_gdrive_folder(service, subfolder_name, period_folder_id)
        existing_items = list_gdrive_contents(service, subfolder_id)

        for filepath in file_list:
            if not filepath.exists():
                print(f"   ⚠️ Berkas lokal tidak ditemukan: {filepath.name}")
                continue

            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"   ⬆️ Mengunggah {filepath.name} ({size_mb:.2f} MB)...", end="", flush=True)

            existing = existing_items.get(filepath.name)
            item, action = upload_or_update_file(service, filepath, subfolder_id, existing)
            file_id = item.get("id")
            print(f" ✓ ({action} - ID: {file_id})")

            uploaded_summary.append({
                "subfolder": subfolder_name,
                "filename": filepath.name,
                "size_mb": f"{size_mb:.2f} MB",
                "file_id": file_id,
                "link": f"https://drive.google.com/file/d/{file_id}/view"
            })

    print(f"\n🎉 Seluruh berkas berhasil diunggah ke Google Drive secara rapi!")
    print(f"🔗 URL Folder Utama: https://drive.google.com/drive/folders/{period_folder_id}")


if __name__ == "__main__":
    main()
