"""Uploader module for KCDA 2026 drafts to Google Drive."""

from pathlib import Path
from typing import Dict, Any, List
from ..google_drive import get_drive_service, list_gdrive_contents, upload_or_update_file

DRAFT_PUBLIKASI_FOLDER_ID = "1l1rmVCaZay_1BTJOAMjkadHuAVof8GyJ"

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

_thread_local = threading.local()

def _get_thread_drive_service():
    if not hasattr(_thread_local, "service"):
        _thread_local.service = get_drive_service()
    return _thread_local.service

def _upload_single_draft(r: Dict[str, Any], folder_id: str, existing_files: Dict[str, Any]) -> Dict[str, Any]:
    pdf_path = Path(r["pdf_path"])
    if not pdf_path.exists():
        return None

    file_name = pdf_path.name
    existing = existing_files.get(file_name)
    action_desc = "Memperbarui" if existing else "Mengunggah baru"
    print(f"   📤 {action_desc}: {file_name}...")

    service = _get_thread_drive_service()
    file_meta, action = upload_or_update_file(
        service=service,
        local_path=pdf_path,
        parent_id=folder_id,
        existing_file=existing
    )

    drive_link = f"https://drive.google.com/file/d/{file_meta['id']}/view"
    print(f"      🔗 Berhasil ({action}): {file_name} -> {drive_link}")
    return {
        "slug": r["slug"],
        "nama_resmi": r["nama_resmi"],
        "file_name": file_name,
        "drive_id": file_meta["id"],
        "drive_link": drive_link,
        "action": action
    }

def upload_kcda_drafts(results: List[Dict[str, Any]], folder_id: str = DRAFT_PUBLIKASI_FOLDER_ID, max_workers: int = 5) -> List[Dict[str, Any]]:
    """Mengunggah seluruh hasil kompilasi PDF draf ke folder Google Drive secara paralel."""
    valid_results = [r for r in results if r.get("status") == "SUCCESS" and Path(r.get("pdf_path", "")).exists()]
    if not valid_results:
        print("⚠️ Tidak ada berkas PDF valid untuk diunggah.")
        return []

    print(f"\n☁️  Menyiapkan pengunggahan {len(valid_results)} draf KCDA 2026 ke Google Drive secara paralel ({max_workers} threads)...")
    service = get_drive_service()
    existing_files = list_gdrive_contents(service, folder_id)

    upload_results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_upload_single_draft, r, folder_id, existing_files)
            for r in valid_results
        ]
        for f in as_completed(futures):
            res = f.result()
            if res:
                upload_results.append(res)

    print(f"✅ Selesai mengunggah {len(upload_results)} publikasi ke Google Drive!")
    return upload_results

