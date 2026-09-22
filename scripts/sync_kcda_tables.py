"""
Script untuk mengunduh/menyinkronkan seluruh tabel Google Sheets KCDA 2026 ke data/kcda-2026/raw_tables/.
Menggunakan token dari /app/data/google_token.json tanpa dependensi library google-api-python-client.
"""

import os
import re
import json
import time
import sys
from pathlib import Path
import requests

sys.path.insert(0, '/root/.gemini/config/skills/gdrive/scripts')
import gdrive_tool

KEC_CANONICAL = {
    'mempawah hilir': 'Mempawah Hilir',
    'mempawah timur': 'Mempawah Timur',
    'sungai pinyuh': 'Sungai Pinyuh',
    'sungai kunyit': 'Sungai Kunyit',
    'segedong': 'Segedong',
    'toho': 'Toho',
    'jongkat': 'Jongkat',
    'anjongan': 'Anjongan',
    'sadaniang': 'Sadaniang'
}

def normalize_kec(name: str) -> str:
    clean = re.sub(r'[^a-zA-Z\s]', '', name).strip().lower()
    for k, v in KEC_CANONICAL.items():
        if k in clean:
            return v
    return name.strip()

def sync_all_tables():
    catalog_path = Path('kegiatan/kecamatan-dalam-angka/2026/katalog_tabel_kcda_2026.json')
    if not catalog_path.exists():
        print(f"❌ Error: Katalog {catalog_path} tidak ditemukan.")
        return

    with open(catalog_path, encoding='utf-8') as f:
        tables = json.load(f)

    out_dir = Path('data/kcda-2026/raw_tables')
    out_dir.mkdir(parents=True, exist_ok=True)

    token = gdrive_tool.get_valid_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    total = len(tables)
    print(f"🚀 Memulai sinkronisasi {total} tabel KCDA 2026 dari Google Sheets ke {out_dir}...")

    success_count = 0
    for idx, t in enumerate(tables, 1):
        sid = t.get('sheet_id')
        if not sid:
            print(f"⚠️ [{idx:>2}/{total}] Lewati Tabel {t.get('no')}: sheet_id kosong.")
            continue

        no = t['no'].replace('.', '_').strip('_')
        nama_slug = re.sub(r'[^a-zA-Z0-9]', '_', t['nama'][:30]).strip('_').lower()
        out_file = out_dir / f"tabel_{no}_{nama_slug}.json"

        # Coba ambil data
        for attempt in range(3):
            try:
                # 1. Ambil list sheets
                meta_res = requests.get(f"https://sheets.googleapis.com/v4/spreadsheets/{sid}?fields=sheets.properties.title", headers=headers, timeout=15)
                if meta_res.status_code == 401:
                    token = gdrive_tool.get_valid_access_token()
                    headers = {"Authorization": f"Bearer {token}"}
                    meta_res = requests.get(f"https://sheets.googleapis.com/v4/spreadsheets/{sid}?fields=sheets.properties.title", headers=headers, timeout=15)

                if meta_res.status_code != 200:
                    raise RuntimeError(f"Gagal get metadata ({meta_res.status_code}): {meta_res.text[:100]}")

                meta = meta_res.json()
                sheet_titles = [s["properties"]["title"] for s in meta.get("sheets", [])]

                # 2. Batch get all sheets
                ranges = [f"'{title}'!A1:Z70" for title in sheet_titles]
                val_res = requests.get(
                    f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values:batchGet",
                    headers=headers,
                    params=[("ranges", r) for r in ranges],
                    timeout=20
                )
                if val_res.status_code != 200:
                    raise RuntimeError(f"Gagal batchGet ({val_res.status_code}): {val_res.text[:100]}")

                value_ranges = val_res.json().get('valueRanges', [])
                tabs_data = {}
                for vr in value_ranges:
                    range_str = vr.get('range', '')
                    raw_title = range_str.split('!')[0].replace("'", "")
                    canon_name = normalize_kec(raw_title)
                    tabs_data[canon_name] = {
                        'raw_title': raw_title,
                        'rows': vr.get('values', [])
                    }

                data_to_save = {
                    'no': t['no'],
                    'nama': t['nama'],
                    'sumber': t.get('sumber', ''),
                    'disediakan_ipds': t.get('disediakan_ipds', ''),
                    'sheet_id': sid,
                    'spreadsheet_title': t.get('nama'),
                    'updated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'tabs': tabs_data
                }

                with open(out_file, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=2)

                print(f"   ✅ [{idx:>2}/{total}] Sukses: Tabel {t['no']:<6} ({len(tabs_data)} tabs)")
                success_count += 1
                break
            except Exception as e:
                if attempt == 2:
                    print(f"   ❌ [{idx:>2}/{total}] Gagal Tabel {t['no']}: {e}")
                time.sleep(1.0)

    print(f"\n🎉 Sinkronisasi selesai: {success_count}/{total} tabel berhasil diperbarui ke lokal!")

if __name__ == "__main__":
    sync_all_tables()
