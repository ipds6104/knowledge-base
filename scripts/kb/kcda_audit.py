"""KCDA 2026 Audit & Synchronizer Module."""

import os
import glob
import json
import time
import re
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

KECAMATANS = [
    'Mempawah Hilir', 'Mempawah Timur', 'Sungai Pinyuh', 'Sungai Kunyit',
    'Segedong', 'Toho', 'Jongkat', 'Anjongan', 'Sadaniang'
]

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

def normalize_kec(name):
    clean = re.sub(r'[^a-zA-Z\s]', '', name).strip().lower()
    for k, v in KEC_CANONICAL.items():
        if k in clean:
            return v
    return name.strip()

def download_all_kcda_tables():
    """Mengunduh seluruh 35 nested spreadsheet KCDA 2026 ke data/kcda-2026/raw_tables/."""
    catalog_path = 'kegiatan/kecamatan-dalam-angka/2026/katalog_tabel_kcda_2026.json'
    if not os.path.exists(catalog_path):
        print(f"❌ Error: Katalog {catalog_path} tidak ditemukan.")
        return

    with open(catalog_path, encoding='utf-8') as f:
        tables = json.load(f)

    os.makedirs('data/kcda-2026/raw_tables', exist_ok=True)
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)

    for idx, t in enumerate(tables, 1):
        sid = t.get('sheet_id')
        if not sid:
            continue

        no = t['no'].replace('.', '_').strip('_')
        nama_slug = re.sub(r'[^a-zA-Z0-9]', '_', t['nama'][:30]).strip('_').lower()
        out_file = f'data/kcda-2026/raw_tables/tabel_{no}_{nama_slug}.json'

        for attempt in range(3):
            try:
                meta = service.spreadsheets().get(spreadsheetId=sid).execute()
                sheet_titles = [s['properties']['title'] for s in meta['sheets']]
                ranges = [f'{title}!A1:Z60' for title in sheet_titles]
                batch_res = service.spreadsheets().values().batchGet(spreadsheetId=sid, ranges=ranges).execute()
                value_ranges = batch_res.get('valueRanges', [])

                tabs_data = {}
                for vr in value_ranges:
                    range_str = vr.get('range', '')
                    raw_title = range_str.split('!')[0].replace("'", '')
                    canon_name = normalize_kec(raw_title)
                    tabs_data[canon_name] = {
                        'raw_title': raw_title,
                        'rows': vr.get('values', [])
                    }

                data_to_save = {
                    'no': t['no'],
                    'nama': t['nama'],
                    'sumber': t['sumber'],
                    'disediakan_ipds': t['disediakan_ipds'],
                    'sheet_id': sid,
                    'spreadsheet_title': meta.get('properties', {}).get('title'),
                    'updated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'tabs': tabs_data
                }

                with open(out_file, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=2)

                print(f"[{idx}/{len(tables)}] OK: Tabel {t['no']} ({len(tabs_data)} tabs)")
                time.sleep(0.3)
                break
            except Exception as e:
                if attempt == 2:
                    print(f"[{idx}/{len(tables)}] ❌ ERR Tabel {t['no']}: {e}")
                time.sleep(1.5)


def run_kcda_audit(filter_kec=None):
    """Mengevaluasi kesiapan data per kecamatan."""
    json_files = sorted(glob.glob('data/kcda-2026/raw_tables/tabel_*.json'))
    if not json_files:
        print("❌ Data raw tabel belum ada. Jalankan `kb kcda sync` terlebih dahulu.")
        return

    audit_data = {kec: {'ready': [], 'partial': [], 'empty': []} for kec in KECAMATANS}

    for fpath in json_files:
        with open(fpath, encoding='utf-8') as f:
            t = json.load(f)

        no = t['no']
        tabs = t.get('tabs', {})

        for kec in KECAMATANS:
            tab_info = tabs.get(kec)
            if not tab_info:
                audit_data[kec]['empty'].append(no)
                continue

            rows = tab_info.get('rows', [])
            if len(rows) <= 3:
                audit_data[kec]['empty'].append(no)
                continue

            data_rows = []
            for r in rows[2:]:
                if any('(1)' in str(c) or '(2)' in str(c) for c in r):
                    continue
                if len(r) > 0 and r[0].strip() and not any(r[0].lower().startswith(x) for x in ['jumlah', 'total', 'sumber']):
                    data_rows.append(r)

            if not data_rows:
                audit_data[kec]['empty'].append(no)
                continue

            total_cells = 0
            filled_cells = 0
            for r in data_rows:
                for c in r[1:]:
                    total_cells += 1
                    c_str = str(c).strip()
                    if c_str and c_str not in ['-', '...', 'None']:
                        filled_cells += 1

            if total_cells == 0 or filled_cells == 0:
                audit_data[kec]['empty'].append(no)
            elif filled_cells >= total_cells * 0.75:
                audit_data[kec]['ready'].append(no)
            else:
                audit_data[kec]['partial'].append(no)

    total_tables = len(json_files)

    target_kecamatans = [filter_kec] if filter_kec and filter_kec in KECAMATANS else KECAMATANS

    print(f"\n=======================================================")
    print(f"  BPS KABUPATEN MEMPAWAH — AUDIT KESIAPAN KCDA 2026")
    print(f"  Total Tabel Acuan: {total_tables} tabel | Waktu: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    print(f"=======================================================")
    print(f"{'No':<3} | {'Kecamatan':<17} | {'Ready':<7} | {'Partial':<7} | {'Empty':<7} | {'% Siap':<7} | {'Status'}")
    print(f"----+-------------------+---------+---------+---------+---------+---------------------")

    ranked = []
    for idx, kec in enumerate(target_kecamatans, 1):
        ready = len(audit_data[kec]['ready'])
        partial = len(audit_data[kec]['partial'])
        empty = len(audit_data[kec]['empty'])
        pct = (ready / total_tables) * 100
        status = "🟢 SIAP CETAK" if pct >= 80 else ("🟡 BUTUH DATA" if pct >= 50 else "🔴 BELUM LENGKAP")
        ranked.append((kec, ready, partial, empty, pct, status))

    ranked.sort(key=lambda x: x[4], reverse=True)
    for i, (kec, ready, partial, empty, pct, status) in enumerate(ranked, 1):
        print(f"{i:<3} | {kec:<17} | {ready:<7} | {partial:<7} | {empty:<7} | {pct:>5.1f}%  | {status}")

    print(f"=======================================================")
    print(f"💡 Catatan: Laporan detail tersimpan di:")
    print(f"   👉 kegiatan/kecamatan-dalam-angka/2026/laporan-kesiapan-kcda-2026.md\n")
