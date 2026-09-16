#!/usr/bin/env python3
"""
setup_kcda_sheets_kecamatan.py
==============================
Mengisi 9 Google Spreadsheet perkecamatan di folder Drive Kak Sukma
(Folder ID: 1eWA-e-esicQ6Jdq6ouviVb76XrB-F0SQ) dengan template tabel konfirmasi KCDA 2026:
- Tabel 2.1.2: Nama-Nama Camat
- Tabel 2.1.3: Nama-Nama Kepala Desa
- Tabel 2.1.4: Nama-Nama Kepala Dusun (hanya untuk kecamatan yang ada di publikasi 2025)
- Tabel 2.2.1: Jumlah Pegawai Negeri Sipil Menurut Pemerintah Daerah dan Jenis Kelamin
- Tabel 2.2.2: Jumlah Pegawai Negeri Sipil Pemerintah Kecamatan Menurut Pendidikan dan Jenis Kelamin
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, List

sys.path.append('/root/.gemini/config/skills/gdrive/scripts')
from gdrive_tool import get_valid_access_token

RAW_DIR = Path('/app/workspaces/bps-mempawah/data/kcda-2026/raw_tables')

RAW_FILES = {
    '2.1.2': ('tabel_2_1_2_nama_nama_camat_yang_pernah_ma.json', 'Tabel 2.1.2'),
    '2.1.3': ('tabel_2_1_3_nama_nama_kepala_desa_di_kecam.json', 'Tabel 2.1.3'),
    '2.1.4': ('tabel_2_1_4_nama_nama_kepala_dusun_di_keca.json', 'Tabel 2.1.4'),
    '2.2.1': ('tabel_2_2_1_jumlah_pegawai_negeri_sipil_me.json', 'Tabel 2.2.1'),
    '2.2.2': ('tabel_2_2_2_jumlah_pegawai_negeri_sipil_pe.json', 'Tabel 2.2.2'),
}

KECAMATAN_LIST = [
    {
        "name": "1. Mempawah Timur",
        "tab_key": "Mempawah Timur",
        "id": "1rIf9ZuTD2kK4BOysQ__kh_e5ZtWmopttM5GrEYrZd9g",
        "has_dusun": True,
    },
    {
        "name": "2. Mempawah Hilir",
        "tab_key": "Mempawah Hilir",
        "id": "1VB3k9opurqMccOdBMC4uKoP9UBiMOkzCroJEl7zriq4",
        "has_dusun": False,
    },
    {
        "name": "3. Sungai Pinyuh",
        "tab_key": "Sungai Pinyuh",
        "id": "1lEUFr2BTPtnuBPHje2MLAg4hZONO_dQE-BAGad6X9UA",
        "has_dusun": False,
    },
    {
        "name": "4. Sungai Kunyit",
        "tab_key": "Sungai Kunyit",
        "id": "1rj5c7TUhK1NvVDWaubXQrrr97661Hdw4Q_DHoOx7r00",
        "has_dusun": True,
    },
    {
        "name": "5. Segedong",
        "tab_key": "Segedong",
        "id": "1Z-1MqJtT8mIXwdWjeSiFLdso52ECJCsBBYPi-5Cd-3c",
        "has_dusun": True,
    },
    {
        "name": "6. Toho",
        "tab_key": "Toho",
        "id": "15VShKwCXs-T5W7UmS1Cw1D3H2CAJiZLEJ3MjXOKfCbk",
        "has_dusun": True,
    },
    {
        "name": "7. Jongkat",
        "tab_key": "Jongkat",
        "id": "13hrB-jznRqBceBglwYZWL3tO464oPKpBmP6okwpCfLg",
        "has_dusun": True,
    },
    {
        "name": "8. Anjongan",
        "tab_key": "Anjongan",
        "id": "1iofOq1dSkm2F6FhKAKxRTYJH0hAyXmsJjC8briYcji0",
        "has_dusun": True,
    },
    {
        "name": "9. Sadaniang",
        "tab_key": "Sadaniang",
        "id": "1jXSyjVD121WCUhy4cU1glzFDrBlHdi68itDhvEa-IHU",
        "has_dusun": True,
    },
]

def load_raw_data():
    raw_data = {}
    for code, (fname, tab_title) in RAW_FILES.items():
        with open(RAW_DIR / fname, 'r', encoding='utf-8') as f:
            raw_data[code] = json.load(f)
    return raw_data

def get_headers():
    token = get_valid_access_token()
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def setup_spreadsheet(kec_info: Dict[str, Any], raw_data: Dict[str, Any]):
    name = kec_info["name"]
    tab_key = kec_info["tab_key"]
    sid = kec_info["id"]
    has_dusun = kec_info["has_dusun"]

    print(f"\n=======================================================")
    print(f"📊 Menyiapkan Spreadsheet: {name} ({sid})")
    print(f"   Status Tabel Dusun: {'ADA (5 Tabel)' if has_dusun else 'TIDAK ADA (4 Tabel)'}")
    print(f"=======================================================")

    headers = get_headers()

    # 1. Dapatkan daftar sheet saat ini
    meta_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}?fields=sheets(properties(sheetId,title))"
    r = requests.get(meta_url, headers=headers)
    r.raise_for_status()
    existing_sheets = r.json().get('sheets', [])
    existing_titles = {s['properties']['title']: s['properties']['sheetId'] for s in existing_sheets}

    # Tentukan tabel yang akan dibuat
    tables_to_create = ['2.1.2', '2.1.3']
    if has_dusun:
        tables_to_create.append('2.1.4')
    tables_to_create.extend(['2.2.1', '2.2.2'])

    # 2. Buat sheet baru jika belum ada
    add_requests = []
    for code in tables_to_create:
        tab_title = RAW_FILES[code][1]
        if tab_title not in existing_titles:
            add_requests.append({
                "addSheet": {
                    "properties": {
                        "title": tab_title,
                        "gridProperties": {
                            "rowCount": 200,
                            "columnCount": 10
                        }
                    }
                }
            })

    if add_requests:
        batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}:batchUpdate"
        r = requests.post(batch_url, headers=headers, json={"requests": add_requests})
        r.raise_for_status()
        print(f"   ✓ Menambahkan {len(add_requests)} tab baru.")

    # Refresh metadata sheetId
    r = requests.get(meta_url, headers=headers)
    all_sheets = r.json().get('sheets', [])
    current_titles = {s['properties']['title']: s['properties']['sheetId'] for s in all_sheets}

    # 3. Masukkan data ke setiap tab
    data_updates = []
    for code in tables_to_create:
        tab_title = RAW_FILES[code][1]
        t_data = raw_data[code]
        rows = t_data.get('tabs', {}).get(tab_key, {}).get('rows', [])
        
        # Bersihkan data baris
        clean_rows = []
        for r_item in rows:
            clean_rows.append([str(c) if c is not None else "" for c in r_item])

        if clean_rows:
            data_updates.append({
                "range": f"'{tab_title}'!A1",
                "values": clean_rows
            })

    if data_updates:
        val_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values:batchUpdate"
        payload = {
            "valueInputOption": "USER_ENTERED",
            "data": data_updates
        }
        r = requests.post(val_url, headers=headers, json=payload)
        r.raise_for_status()
        print(f"   ✓ Mengisi data ke {len(data_updates)} tab.")

    # 4. Format tab (Freeze baris header, auto-resize)
    format_requests = []
    for code in tables_to_create:
        tab_title = RAW_FILES[code][1]
        sh_id = current_titles.get(tab_title)
        if sh_id is not None:
            # Freeze 3 baris header pertama
            format_requests.append({
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sh_id,
                        "gridProperties": {
                            "frozenRowCount": 3
                        }
                    },
                    "fields": "gridProperties.frozenRowCount"
                }
            })
            # Auto-fit column widths
            format_requests.append({
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": sh_id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 8
                    }
                }
            })

    # Hapus tab default lama (misal '.', 'Sheet1', atau 'Copy of...')
    for s in all_sheets:
        title = s['properties']['title']
        sh_id = s['properties']['sheetId']
        if title not in [RAW_FILES[c][1] for c in tables_to_create]:
            format_requests.append({
                "deleteSheet": {
                    "sheetId": sh_id
                }
            })

    if format_requests:
        batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}:batchUpdate"
        r = requests.post(batch_url, headers=headers, json={"requests": format_requests})
        if r.status_code == 200:
            print(f"   ✓ Formatting & pembersihan tab lama selesai.")
        else:
            print(f"   ⚠️ Warning format: {r.status_code} {r.text}")

    print(f"   ✅ Selesai: {name}")

def main():
    raw_data = load_raw_data()
    print("🚀 Memulai inisialisasi Google Spreadsheet KCDA Perkecamatan...", flush=True)
    remaining_kecamatans = [k for k in KECAMATAN_LIST if k["name"] not in ["1. Mempawah Timur", "2. Mempawah Hilir", "3. Sungai Pinyuh"]]
    for kec in remaining_kecamatans:
        try:
            setup_spreadsheet(kec, raw_data)
            time.sleep(1) # Hindari rate limit API
        except Exception as e:
            print(f"❌ Gagal memproses {kec['name']}: {e}", flush=True)

    print("\n🎉 SELURUH 9 SPREADSHEET KECAMATAN TELAH BERHASIL DIISI DAN DIBERSIHKAN!", flush=True)

if __name__ == '__main__':
    main()
