#!/usr/bin/env python3
"""scripts/upload_pdf_gdrive_delta.py — High-Speed Thread-Safe Delta Uploader ke Google Drive."""

import os
import sys
import json
import hashlib
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

GDRIVE_FOLDER_ID = "1GVLa9UVOBJOr-rb62A539HnNK7UGyrXa"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDF_DIR = os.path.join(BASE_DIR, "kegiatan/sensus-ekonomi-2026/2026/pdf_verifikasi_rt")
RESULTS_DIR = os.path.join(BASE_DIR, "kegiatan/sensus-ekonomi-2026/2026/outputs")
FASIH_RESULTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "fasih-sync-monitoring", "results"))
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

def get_valid_access_token():
    """Dapatkan token OAuth2 yang valid dan otomatis refresh jika expired."""
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(f"token.json tidak ditemukan di {TOKEN_PATH}")
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds.token

def compute_file_md5(filepath: Path) -> str:
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_all_remote_files(access_token, folder_id):
    """Ambil seluruh file di GDrive folder menggunakan REST API v3 dengan pagination."""
    remote_map = {}
    page_token = None
    headers = {"Authorization": f"Bearer {access_token}"}
    print("🔍 Mengambil daftar berkas di Google Drive (dengan pagination)...")
    
    while True:
        url = "https://www.googleapis.com/drive/v3/files"
        params = {
            "q": f"'{folder_id}' in parents and trashed = false",
            "fields": "nextPageToken, files(id, name, webViewLink, md5Checksum)",
            "pageSize": 1000,
            "supportsAllDrives": "true",
            "includeItemsFromAllDrives": "true"
        }
        if page_token:
            params["pageToken"] = page_token
            
        res = requests.get(url, headers=headers, params=params, timeout=30)
        res.raise_for_status()
        data = res.json()
        
        for f in data.get("files", []):
            remote_map[f["name"]] = f
            
        page_token = data.get("nextPageToken")
        if not page_token:
            break
            
    print(f"  ✓ Ditemukan {len(remote_map)} berkas di Google Drive.")
    return remote_map

def upload_file_worker(task):
    """Worker fungsi upload untuk tiap thread."""
    file_path, existing_file, access_token, folder_id = task
    filename = os.path.basename(file_path)
    local_md5 = compute_file_md5(Path(file_path))
    headers = {"Authorization": f"Bearer {access_token}"}
    
    if existing_file:
        remote_md5 = existing_file.get("md5Checksum")
        file_id = existing_file["id"]
        web_link = existing_file.get("webViewLink", f"https://drive.google.com/file/d/{file_id}/view")
        
        if remote_md5 and remote_md5 == local_md5:
            return filename, "SKIP", web_link, None
            
        # Update file in-place (PATCH content)
        update_url = f"https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=media&supportsAllDrives=true"
        with open(file_path, "rb") as f:
            up_res = requests.patch(
                update_url,
                headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/pdf"},
                data=f,
                timeout=60
            )
        if up_res.status_code == 200:
            return filename, "UPDATE", web_link, None
        else:
            return filename, "FAIL", None, f"Update status {up_res.status_code}: {up_res.text[:200]}"

    # Create new file (Multipart upload)
    create_url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true"
    metadata = {
        "name": filename,
        "parents": [folder_id]
    }
    
    with open(file_path, "rb") as f:
        files_payload = {
            "data": ("metadata", json.dumps(metadata), "application/json; charset=UTF-8"),
            "file": (filename, f, "application/pdf")
        }
        cr_res = requests.post(create_url, headers=headers, files=files_payload, timeout=60)
        
    if cr_res.status_code in (200, 201):
        cr_data = cr_res.json()
        file_id = cr_data["id"]
        web_link = cr_data.get("webViewLink", f"https://drive.google.com/file/d/{file_id}/view")
        
        # Set anyone reader permission
        try:
            perm_url = f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions?supportsAllDrives=true"
            requests.post(perm_url, headers=headers, json={"role": "reader", "type": "anyone"}, timeout=15)
        except Exception:
            pass
            
        return filename, "CREATE", web_link, None
    else:
        return filename, "FAIL", None, f"Create status {cr_res.status_code}: {cr_res.text[:200]}"

def main():
    if len(sys.argv) > 1:
        target_dir = os.path.abspath(sys.argv[1])
    else:
        target_dir = PDF_DIR

    if not os.path.exists(target_dir):
        print(f"❌ Folder tidak ditemukan: {target_dir}")
        return

    pdf_files = sorted([os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith(".pdf")])
    if not pdf_files:
        print(f"⚠️ Tidak ada berkas PDF di {target_dir}")
        return

    print("==================================================================")
    print(f"🚀 GOOGLE DRIVE DELTA UPLOADER — BPS KABUPATEN MEMPAWAH")
    print(f"📁 Folder Lokal : {target_dir} ({len(pdf_files)} PDF)")
    print(f"☁️ Target GDrive : {GDRIVE_FOLDER_ID}")
    print("==================================================================")

    access_token = get_valid_access_token()
    remote_map = get_all_remote_files(access_token, GDRIVE_FOLDER_ID)

    # Siapkan token_user.json untuk kompatibilitas Node.js juga
    try:
        with open(TOKEN_PATH, "r", encoding="utf-8") as f:
            p_token = json.load(f)
        node_token = {
            "access_token": p_token.get("token"),
            "refresh_token": p_token.get("refresh_token"),
            "scope": " ".join(SCOPES),
            "token_type": "Bearer"
        }
        fasih_tok_path = os.path.abspath(os.path.join(BASE_DIR, "..", "fasih-sync-monitoring", "token_user.json"))
        if os.path.exists(os.path.dirname(fasih_tok_path)):
            with open(fasih_tok_path, "w", encoding="utf-8") as f:
                json.dump(node_token, f, indent=2)
    except Exception:
        pass

    link_mapping = {}
    skipped_count = 0
    updated_count = 0
    created_count = 0
    failed_count = 0

    tasks = []
    for fp in pdf_files:
        fn = os.path.basename(fp)
        existing = remote_map.get(fn)
        tasks.append((fp, existing, access_token, GDRIVE_FOLDER_ID))

    print(f"\nMemulai Delta Upload ({len(tasks)} berkas) dengan 12 thread paralel...")

    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_file = {executor.submit(upload_file_worker, t): t[0] for t in tasks}
        
        for i, future in enumerate(as_completed(future_to_file), 1):
            fp = future_to_file[future]
            fn = os.path.basename(fp)
            code_prefix = fn.split("_")[0] if "_" in fn else fn[:16]
            
            try:
                filename, action, web_link, err = future.result()
                if action == "SKIP":
                    skipped_count += 1
                elif action == "UPDATE":
                    updated_count += 1
                elif action == "CREATE":
                    created_count += 1
                elif action == "FAIL":
                    failed_count += 1
                    print(f"  ❌ [{i}/{len(tasks)}] Gagal {fn}: {err}")
                    
                if web_link and code_prefix:
                    link_mapping[code_prefix] = web_link
                    
            except Exception as e:
                failed_count += 1
                print(f"  ❌ [{i}/{len(tasks)}] Error {fn}: {e}")

            if i % 100 == 0 or i == len(tasks):
                print(f"  Progres: {i}/{len(tasks)} diproses (Skip/Identik: {skipped_count}, Update: {updated_count}, Baru: {created_count}, Gagal: {failed_count})")

    # Simpan mapping link
    for out_dir in [RESULTS_DIR, FASIH_RESULTS_DIR]:
        if os.path.exists(os.path.dirname(out_dir)):
            os.makedirs(out_dir, exist_ok=True)
            map_path = os.path.join(out_dir, "pdf_gdrive_links.json")
            with open(map_path, "w", encoding="utf-8") as f:
                json.dump(link_mapping, f, indent=2)
            print(f"💾 Link mapping disimpan ke: {map_path}")

    print("\n==================================================================")
    print(f"🎉 SUKSES DELTA UPLOAD!")
    print(f"  • Identik (di-Skip) : {skipped_count}")
    print(f"  • Berhasil Update   : {updated_count}")
    print(f"  • Berkas Baru       : {created_count}")
    print(f"  • Gagal             : {failed_count}")
    print(f"  • Total Link Aktif  : {len(link_mapping)}")
    print("==================================================================")

if __name__ == "__main__":
    main()
