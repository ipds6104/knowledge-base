#!/usr/bin/env python3
"""
update_sheets_tabel_2_1_3.py
============================
Memperbarui tab 'Tabel 2.1.3' pada 9 Google Spreadsheet KCDA perkecamatan.
Menggunakan daftar desa resmi dari Master SLS 6104 untuk memastikan kebersihan data
(menghilangkan baris artifak seperti 'Kecamatan...' dan '-2') serta menyiapkan kolom
konfirmasi nama Kepala Desa / Lurah untuk tahun 2026.
"""

import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, List

sys.path.append('/root/.gemini/config/skills/gdrive/scripts')
from gdrive_tool import get_valid_access_token

RAW_KADES_FILE = Path('/app/workspaces/bps-mempawah/data/kcda-2026/raw_tables/tabel_2_1_3_nama_nama_kepala_desa_di_kecam.json')

KECAMATAN_DATA = [
    {
        "nama": "Mempawah Hilir",
        "sheet_id": "1VB3k9opurqMccOdBMC4uKoP9UBiMOkzCroJEl7zriq4",
        "desa": ["Tanjung", "Kuala Secapah", "Tengah", "Terusan", "Pasir", "Penibung", "Sengkubang", "Malikian"]
    },
    {
        "nama": "Mempawah Timur",
        "sheet_id": "1rIf9ZuTD2kK4BOysQ__kh_e5ZtWmopttM5GrEYrZd9g",
        "desa": ["Pasir Wan Salim", "Sungai Bakau Kecil", "Pasir Panjang", "Pasir Palembang", "Pulau Pedalaman", "Antibar", "Sejegi", "Parit Banjar"]
    },
    {
        "nama": "Sungai Pinyuh",
        "sheet_id": "1lEUFr2BTPtnuBPHje2MLAg4hZONO_dQE-BAGad6X9UA",
        "desa": ["Sungai Purun Kecil", "Peniraman", "Nusapati", "Galang", "Sungai Rasau", "Sungai Pinyuh", "Sungai Batang", "Sungai Bakau Besar Laut", "Sungai Bakau Besar Darat"]
    },
    {
        "nama": "Sungai Kunyit",
        "sheet_id": "1rj5c7TUhK1NvVDWaubXQrrr97661Hdw4Q_DHoOx7r00",
        "desa": ["Semudun", "Semparong Parit Raden", "Mendalok", "Sungai Dungun", "Sungai Limau", "Sungai Kunyit Laut", "Sungai Kunyit Dalam", "Sungai Kunyit Hulu", "Bukit Batu", "Sungai Bundung Laut", "Sungai Duri I", "Sungai Duri II"]
    },
    {
        "nama": "Segedong",
        "sheet_id": "1Z-1MqJtT8mIXwdWjeSiFLdso52ECJCsBBYPi-5Cd-3c",
        "desa": ["Peniti Dalam I", "Sungai Burung", "Sungai Purun Besar", "Parit Bugis", "Peniti Besar", "Peniti Dalam II"]
    },
    {
        "nama": "Toho",
        "sheet_id": "15VShKwCXs-T5W7UmS1Cw1D3H2CAJiZLEJ3MjXOKfCbk",
        "desa": ["Sambora", "Benuang", "Pak Utan", "Sepang", "Pak Laheng", "Terap", "Kecurit", "Toho Ilir"]
    },
    {
        "nama": "Jongkat",
        "sheet_id": "13hrB-jznRqBceBglwYZWL3tO464oPKpBmP6okwpCfLg",
        "desa": ["Sungai Nipah", "Jungkat", "Wajok Hilir", "Wajok Hulu", "Peniti Luar"]
    },
    {
        "nama": "Anjongan",
        "sheet_id": "1iofOq1dSkm2F6FhKAKxRTYJH0hAyXmsJjC8briYcji0",
        "desa": ["Anjungan Melancar", "Anjungan Dalam", "Pak Bulu", "Dema", "Kepayang"]
    },
    {
        "nama": "Sadaniang",
        "sheet_id": "1jXSyjVD121WCUhy4cU1glzFDrBlHdi68itDhvEa-IHU",
        "desa": ["Pentek", "Sekabuk", "Bumbun", "Amawang", "Ansiap", "Suak Barangan"]
    }
]

def load_raw_kades() -> Dict[str, Any]:
    with open(RAW_KADES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_headers():
    token = get_valid_access_token()
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def update_kades_table_for_kecamatan(kec: Dict[str, Any], raw_kades_data: Dict[str, Any]):
    name = kec["nama"]
    sid = kec["sheet_id"]
    desa_list = kec["desa"]

    print(f"🔄 Memproses Tabel 2.1.3 untuk: {name} ({sid})...", flush=True)

    tab_raw = raw_kades_data.get('tabs', {}).get(name, {}).get('rows', [])
    kades_map = {}
    for r in tab_raw:
        if len(r) >= 3 and str(r[0]).strip() not in ["2025", "No", "(1)"]:
            d_name = str(r[1]).split("\n")[0].strip().lower()
            k_name = str(r[2]).split("\n")[0].strip() if len(r) > 2 else ""
            if k_name and k_name != "–" and k_name != "-":
                kades_map[d_name] = k_name

    rows = []
    rows.append([f"Tabel 2.1.3 Nama-Nama Kepala Desa / Lurah di Kecamatan {name}, 2025 dan 2026", "", "", "", ""])
    rows.append([
        "No",
        "Desa / Kelurahan",
        "Nama Kepala Desa / Lurah (Kondisi 2025)",
        "Nama Kepala Desa / Pj. Kepala Desa (Kondisi 2026 / Terkini)",
        "Catatan / Keterangan (Status Pj/Plt/Definitif, Periode, dll)"
    ])
    rows.append(["(1)", "(2)", "(3)", "(4)", "(5)"])

    for idx, desa in enumerate(desa_list, 1):
        kades_acuan = kades_map.get(desa.lower(), "")
        rows.append([str(idx), desa, kades_acuan, "", ""])

    # Tambahkan baris kosong pengisi jika ada sisa baris lama untuk menimpa
    for _ in range(5):
        rows.append(["", "", "", "", ""])

    headers = get_headers()
    update_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.1.3!A1:E{len(rows)}?valueInputOption=USER_ENTERED"
    r = requests.put(update_url, headers=headers, json={"range": f"Tabel 2.1.3!A1:E{len(rows)}", "values": rows}, timeout=15)
    r.raise_for_status()

    # Dapatkan sheetId untuk auto-resize
    meta_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}?fields=sheets(properties(sheetId,title))"
    r_meta = requests.get(meta_url, headers=headers, timeout=15)
    sheets_info = r_meta.json().get('sheets', [])
    sheet_id = None
    for s in sheets_info:
        if s['properties']['title'] == 'Tabel 2.1.3':
            sheet_id = s['properties']['sheetId']
            break

    if sheet_id is not None:
        batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}:batchUpdate"
        format_req = {
            "requests": [
                {
                    "autoResizeDimensions": {
                        "dimensions": {
                            "sheetId": sheet_id,
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": 5
                        }
                    }
                }
            ]
        }
        requests.post(batch_url, headers=headers, json=format_req, timeout=15)

    print(f"   ✅ Sukses {name}: {len(desa_list)} desa resmi telah terisi.", flush=True)

def main():
    raw_kades = load_raw_kades()
    print("🚀 Memulai pembersihan dan pembaruan Tabel 2.1.3 di seluruh 9 spreadsheet kecamatan...\n", flush=True)
    for kec in KECAMATAN_DATA:
        try:
            update_kades_table_for_kecamatan(kec, raw_kades)
            time.sleep(0.5)
        except Exception as e:
            print(f"   ❌ Gagal pada {kec['nama']}: {e}", flush=True)
    print("\n🎉 SELURUH TABEL 2.1.3 BERHASIL DIBERSIHKAN DAN DISINKRONKAN DENGAN MASTER SLS!", flush=True)

if __name__ == '__main__':
    main()
