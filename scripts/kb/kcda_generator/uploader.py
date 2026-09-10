"""Uploader module for KCDA 2026 drafts to Google Drive."""

from pathlib import Path
from typing import Dict, Any, List
from ..google_drive import get_drive_service, list_gdrive_contents, upload_or_update_file

DRAFT_PUBLIKASI_FOLDER_ID = "1l1rmVCaZay_1BTJOAMjkadHuAVof8GyJ"

def upload_kcda_drafts(results: List[Dict[str, Any]], folder_id: str = DRAFT_PUBLIKASI_FOLDER_ID) -> List[Dict[str, Any]]:
    """Mengunggah seluruh hasil kompilasi PDF draf ke folder Google Drive."""
    print(f"\n☁️  Menyiapkan pengunggahan draf KCDA 2026 ke Google Drive...")
    service = get_drive_service()
    existing_files = list_gdrive_contents(service, folder_id)

    upload_results = []
    for r in results:
        if r.get("status") != "SUCCESS":
            continue

        pdf_path = Path(r["pdf_path"])
        if not pdf_path.exists():
            continue

        file_name = pdf_path.name
        existing = existing_files.get(file_name)
        action_desc = "Memperbarui" if existing else "Mengunggah baru"
        print(f"   📤 {action_desc}: {file_name}...")

        file_meta, action = upload_or_update_file(
            service=service,
            local_path=pdf_path,
            parent_id=folder_id,
            existing_file=existing
        )

        drive_link = f"https://drive.google.com/file/d/{file_meta['id']}/view"
        print(f"      🔗 Berhasil ({action}): {drive_link}")
        upload_results.append({
            "slug": r["slug"],
            "nama_resmi": r["nama_resmi"],
            "file_name": file_name,
            "drive_id": file_meta["id"],
            "drive_link": drive_link,
            "action": action
        })

    return upload_results
