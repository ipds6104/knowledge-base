#!/usr/bin/env python3
"""Sync download background worker for 2025 KCDA reference files using requests streaming."""

import os
import sys
import json
import time
import requests
from pathlib import Path

FOLDER_2025 = '1aHjH-jQ7vGBJL7SHWIQOy4Ga7QSvLZa9'
TARGET_DIR = Path('/home/ihza/Projects/knowledge-base/kegiatan/kecamatan-dalam-angka/referensi-2025')
TOKEN_PATH = Path('/home/ihza/Projects/knowledge-base/token.json')

def get_token():
    with open(TOKEN_PATH) as fp:
        return json.load(fp)['token']

def get_drive_files(token):
    headers = {'Authorization': f'Bearer {token}'}
    url = f"https://www.googleapis.com/drive/v3/files?q='{FOLDER_2025}'+in+parents+and+trashed=false&fields=files(id,name,mimeType,size)"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json().get('files', [])

def download_file(fid, name, size, target_path, token):
    headers = {'Authorization': f'Bearer {token}'}
    url = f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media"
    
    # Download into temporary file first, then rename
    part_path = target_path.with_suffix(target_path.suffix + '.part')
    
    with requests.get(url, headers=headers, stream=True, timeout=60) as r:
        r.raise_for_status()
        downloaded = 0
        t0 = time.time()
        with open(part_path, 'wb') as fp:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    fp.write(chunk)
                    downloaded += len(chunk)
                    # print occasional progress
                    if downloaded % (5*1024*1024) < 1024*1024:
                        pct = (downloaded / size) * 100 if size > 0 else 0
                        speed = downloaded / max(1, (time.time() - t0)) / 1024
                        print(f"   [{pct:5.1f}%] {downloaded/(1024*1024):.1f}/{size/(1024*1024):.1f} MB ({speed:.0f} KB/s)", flush=True)
                        
    part_path.rename(target_path)

def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    token = get_token()
    
    print("🔍 Mengambil daftar berkas referensi KCDA 2025...")
    files = get_drive_files(token)
    
    # Sort files: smaller files first (docx & pdf), massive .rar last
    files.sort(key=lambda x: int(x.get('size', 0)))
    
    print(f"📦 Total target: {len(files)} berkas.")
    
    for idx, f in enumerate(files, 1):
        name = f['name']
        fid = f['id']
        size = int(f.get('size', 0))
        target_path = TARGET_DIR / name
        size_mb = size / (1024 * 1024)
        
        if target_path.exists() and target_path.stat().st_size == size:
            print(f"[{idx}/{len(files)}] ✓ [LENGKAP] {name} ({size_mb:.2f} MB)")
            continue
            
        print(f"\n[{idx}/{len(files)}] ⬇️ Mengunduh {name} ({size_mb:.2f} MB)...", flush=True)
        retries = 3
        while retries > 0:
            try:
                download_file(fid, name, size, target_path, token)
                print(f"✓ Selesai: {name}")
                break
            except Exception as e:
                retries -= 1
                print(f"⚠️ Gagal mengunduh ({e}), sisa percobaan: {retries}")
                time.sleep(3)
                token = get_token()  # refresh token if needed
                
    print("\n🎉 SELURUH BERKAS REFERENSI KCDA 2025 SELESAI DIUNDUH!")

if __name__ == '__main__':
    main()
