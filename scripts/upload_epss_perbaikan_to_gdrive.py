#!/usr/bin/env python3
"""
Upload Dokumen Perbaikan EPSS Pleno 2026 to Google Drive folder:
Target: '4. Perbaikan EPSS Pleno' (ID: 1yTYQRuy7rCWpEHYofkgZxRCz8KC1xoHd)
Specifically uploads and updates all documents across 01 to 11, including 07_40102.
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
    upload_or_update_file,
    compute_file_md5
)

ROOT_FOLDER_ID = "1yTYQRuy7rCWpEHYofkgZxRCz8KC1xoHd"  # 4. Perbaikan EPSS Pleno
DOKUMEN_PERBAIKAN_DIR = Path(BASE_DIR) / "kegiatan" / "evaluasi-epss" / "2026" / "dokumen-perbaikan"


def main():
    print(f"🚀 Memulai sinkronisasi Dokumen Perbaikan EPSS ke Google Drive...")
    print(f"   Target Root : 4. Perbaikan EPSS Pleno (ID: {ROOT_FOLDER_ID})")
    print(f"   Sumber Data : {DOKUMEN_PERBAIKAN_DIR}\n")

    service = get_drive_service()

    # Ambil daftar subfolder di root GDrive
    root_contents = list_gdrive_contents(service, ROOT_FOLDER_ID)

    total_created = 0
    total_updated = 0
    total_skipped = 0

    # Iterasi setiap folder di lokal
    local_subdirs = sorted([d for d in DOKUMEN_PERBAIKAN_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")])

    for subdir in local_subdirs:
        folder_name = subdir.name
        print(f"\n📂 Memproses Folder: {folder_name}")

        # Pastikan folder ada di GDrive
        if folder_name in root_contents:
            subfolder_id = root_contents[folder_name]["id"]
        else:
            subfolder_id = get_or_create_gdrive_folder(service, folder_name, ROOT_FOLDER_ID)
            print(f"   [+] Membuat subfolder di GDrive: {folder_name} (ID: {subfolder_id})")

        # Ambil daftar isi di subfolder remote
        remote_files = list_gdrive_contents(service, subfolder_id)

        # Hapus file remote yang memiliki ekstensi .typ atau .md
        for r_name, r_info in list(remote_files.items()):
            ext = os.path.splitext(r_name)[1].lower()
            if ext in [".typ", ".md"]:
                try:
                    service.files().delete(fileId=r_info["id"]).execute()
                    print(f"   🗑️  [HAPUS REMOTE] {r_name} (Sesuai instruksi exclude .typ & .md)")
                    del remote_files[r_name]
                except Exception as e:
                    print(f"   ⚠️  [GAGAL HAPUS REMOTE] {r_name}: {e}")

        # Iterasi file di dalam subdir lokal (kecualikan .typ dan .md)
        local_files = [
            f for f in subdir.iterdir()
            if f.is_file() and not f.name.startswith(".") and f.suffix.lower() not in [".typ", ".md"]
        ]

        for local_file in sorted(local_files):
            file_name = local_file.name
            existing_file = remote_files.get(file_name)

            # Cek MD5 jika file sudah ada
            if existing_file:
                local_md5 = compute_file_md5(local_file)
                remote_md5 = existing_file.get("md5Checksum")
                if local_md5 == remote_md5:
                    print(f"   ⚡ [IDENTIK] {file_name} (Lewati)")
                    total_skipped += 1
                    continue

            # Upload atau Update
            try:
                res, action = upload_or_update_file(service, local_file, subfolder_id, existing_file)
                if action == "CREATE":
                    print(f"   ✨ [BARU]    {file_name} -> Upload berhasil (ID: {res['id']})")
                    total_created += 1
                else:
                    print(f"   🔄 [UPDATE]  {file_name} -> Diperbarui (ID: {res['id']})")
                    total_updated += 1
            except Exception as e:
                print(f"   ❌ [GAGAL]   {file_name}: {e}")

    # Hapus file panduan .md di root jika ada
    if "panduan-dokumen-perbaikan-epss-2026.md" in root_contents:
        try:
            service.files().delete(fileId=root_contents["panduan-dokumen-perbaikan-epss-2026.md"]["id"]).execute()
            print(f"\n🗑️  [HAPUS REMOTE ROOT] panduan-dokumen-perbaikan-epss-2026.md")
        except Exception as e:
            print(f"\n⚠️  [GAGAL HAPUS REMOTE ROOT] panduan: {e}")

    print("\n" + "=" * 60)
    print(f"SINKRONISASI SELESAI!")
    print(f"   - Berkas Baru Diupload : {total_created}")
    print(f"   - Berkas Diperbarui    : {total_updated}")
    print(f"   - Berkas Identik/Skip  : {total_skipped}")
    print("=" * 60)


if __name__ == "__main__":
    main()
