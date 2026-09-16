#!/usr/bin/env python3
"""
Sync AppSheet Master Data to 9 Primary KCDA Google Sheets
---------------------------------------------------------
Script ini membaca data mutakhir hasil kunjungan lapangan dari AppSheet Master:
(KCDA 2026 - Master Konfirmasi Lapangan Kantor Camat: 1eoHZM10Hok8woNlylPO9AJavaShUSjd28NsBfjwyDoM)
dan dapat mem-push nilai bersih (hard values) atau menyegarkan formula IMPORTRANGE ke 9 spreadsheet sumber utama KCDA.
"""

import os, sys, json, re, requests, urllib.parse

sys.path.append('/root/.gemini/config/skills/gdrive/scripts')
from gdrive_tool import get_valid_access_token

APP_SHEET_ID = '1eoHZM10Hok8woNlylPO9AJavaShUSjd28NsBfjwyDoM'

KCDA_TABLES = {
    '1.2_jarak': '14FvPtJSYS2EgAQ1nzKzY-CX8l7t7A1rWJeHCgCZ3XzY',
    '1.3_batas': '12Ohl8ShLolVXWRD7dBBtNNPqNfX_9pgAFFVYNbMLJ0U',
    '1.4_jarak_camat': '10DAiZQaRpS7-w0qfA6OO_D6oIPCLzmVODciMRdu5Guo',
    '2.1.1_rt_rw_dusun': '1Z-0jhg8zWUhqZrL1Raaju-W5fpGUwn_gBCViU-ZeL88',
    '2.1.2_camat': '1BjxvpODk5TZR8aLXCbzzPt4yoa9F9vpQ4t1nIXQG2gg',
    '2.1.3_kades': '1x-XjDE3rupSaBIwFGqyHpyYjz6S9ur0PVFORXY9AdW4',
    '2.1.4_kadus': '10eEof1SE5ucO6hUAvP7EJ8X7GQLyuGwiRpM4Ltc_Vkk',
    '2.2.1_pns_gender': '1Vqx2_TCs27HqnxYcoYHhLASZROf6gEJDvo6J6CjEQ8g',
    '2.2.2_pns_pendidikan': '1gc5ZbcBNwU17rBqE6tcIlXxzR7RfFzi_F9OVI6HtJIQ'
}

def get_headers():
    token = get_valid_access_token()
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def status():
    headers = get_headers()
    print("=== STATUS INTEGRASI APPSHEET -> KCDA 2026 ===")
    for name, sid in KCDA_TABLES.items():
        try:
            r = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{sid}?fields=properties.title,sheets.properties.title', headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                title = data.get('properties', {}).get('title', '')
                sheets = [s['properties']['title'] for s in data.get('sheets', [])]
                has_ref = any('_REF_' in s for s in sheets)
                print(f"✅ {name:<20} | {title[:35]:<35} | Ref Sheet: {'Aktif' if has_ref else 'Belum'}")
            else:
                print(f"❌ {name:<20} | HTTP {r.status_code}")
        except Exception as e:
            print(f"⚠️ {name:<20} | Error: {e}")

if __name__ == '__main__':
    status()
