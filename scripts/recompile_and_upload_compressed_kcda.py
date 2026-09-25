#!/usr/bin/env python3
import sys
import os
import json
import mimetypes
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "/root/.gemini/config/skills/gdrive/scripts")
from gdrive_tool import get_valid_access_token, set_drive_permissions

sys.path.insert(0, "scripts/kb")
from kcda_generator.compiler import compile_all_kcda
from kcda_generator.config import KCDA_KECAMATAN_CONFIG

FOLDER_ID = "1l1rmVCaZay_1BTJOAMjkadHuAVof8GyJ"
BASE_DIR = Path("/app/workspaces/bps-mempawah/kegiatan/kecamatan-dalam-angka/2026/outputs")

def upload_single_file(slug):
    pdf_path = BASE_DIR / slug / f"kcda-2026-{slug}.pdf"
    if not pdf_path.exists():
        return None

    file_name = pdf_path.name
    token = get_valid_access_token()
    content_type, _ = mimetypes.guess_type(str(pdf_path))
    if not content_type:
        content_type = "application/octet-stream"

    metadata = {
        "name": file_name,
        "parents": [FOLDER_ID]
    }

    boundary = "-------314159265358979323846"
    delimiter = f"\r\n--{boundary}\r\n"
    close_delim = f"\r\n--{boundary}--\r\n"

    with open(pdf_path, "rb") as f:
        file_bytes = f.read()

    multipart_body = (
        delimiter
        + 'Content-Type: application/json; charset=UTF-8\r\n\r\n'
        + json.dumps(metadata)
        + delimiter
        + f'Content-Type: {content_type}\r\n\r\n'
    ).encode("utf-8") + file_bytes + close_delim.encode("utf-8")

    upload_url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,webViewLink"
    resp = requests.post(
        upload_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
        },
        data=multipart_body,
        timeout=180
    )
    if resp.status_code not in (200, 201):
        print(f"Upload failed for {file_name}: {resp.status_code}")
        return None

    res = resp.json()
    file_id = res.get("id")
    set_drive_permissions(token, file_id, share_type="anyone", role="reader")
    sz_mb = round(pdf_path.stat().st_size / (1024 * 1024), 2)
    print(f"Uploaded {file_name} ({sz_mb} MB) -> {res.get('webViewLink')}")
    return {
        "slug": slug,
        "name": file_name,
        "size_mb": sz_mb,
        "drive_link": f"https://drive.google.com/file/d/{file_id}/view"
    }

if __name__ == "__main__":
    print("🚀 1. Recompiling all 9 kecamatan...")
    results = compile_all_kcda()
    for r in results:
        print(f"   {r['slug']}: {r.get('file_size_kb', 0)/1024:.2f} MB, {r.get('pages')} pages, status={r.get('status')}")

    print("\n☁️ 2. Uploading compressed PDFs to Google Drive...")
    uploaded = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(upload_single_file, slug): slug for slug in KCDA_KECAMATAN_CONFIG.keys()}
        for f in as_completed(futures):
            res = f.result()
            if res:
                uploaded.append(res)

    print("\n✅ All done! Uploaded files:")
    for u in sorted(uploaded, key=lambda x: x["slug"]):
        print(f"• {u['slug']}: {u['size_mb']} MB -> {u['drive_link']}")
