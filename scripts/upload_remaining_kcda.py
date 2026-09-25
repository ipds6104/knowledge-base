#!/usr/bin/env python3
import os
import sys
import json
import mimetypes
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "/root/.gemini/config/skills/gdrive/scripts")
from gdrive_tool import get_valid_access_token, set_drive_permissions

FOLDER_ID = "1l1rmVCaZay_1BTJOAMjkadHuAVof8GyJ"
BASE_DIR = Path("/app/workspaces/bps-mempawah/kegiatan/kecamatan-dalam-angka/2026/outputs")

KECAMATAN_LIST = [
    "jongkat",
    "sadaniang"
]

def upload_file(slug):
    pdf_path = BASE_DIR / slug / f"kcda-2026-{slug}.pdf"
    if not pdf_path.exists():
        print(f"File not found: {pdf_path}")
        return None

    file_name = pdf_path.name
    print(f"Starting upload: {file_name}...")
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
        print(f"Failed {file_name}: {resp.status_code} {resp.text}")
        return None

    res = resp.json()
    file_id = res.get("id")
    set_drive_permissions(token, file_id, share_type="anyone", role="reader")
    print(f"Done {file_name}: {res.get('webViewLink')}")
    return res

if __name__ == "__main__":
    print(f"Starting parallel upload for {len(KECAMATAN_LIST)} kecamatan...")
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(upload_file, slug): slug for slug in KECAMATAN_LIST}
        for f in as_completed(futures):
            res = f.result()
    print("All uploads finished!")
