#!/usr/bin/env python3
"""
apply_sheet_styling_kcda.py
===========================
Menerapkan styling visual profesional dan sistem warna intuitif pada 9 Google Spreadsheet KCDA 2026 perkecamatan:
1. Header Utama & Judul: Deep Navy Blue (#1E3A8A) dengan teks putih tebal.
2. Header Kolom Acuan (Baseline): Slate Blue (#1E40AF) dengan teks putih tebal.
3. Header Kolom Pengisian (Editable / Update 2026): Emerald Green (#059669) dengan teks putih tebal.
4. Baris Penomoran Kolom: Soft Gray (#F1F5F9) dengan teks miring abu-abu (#475569).
5. Area Data Acuan: Alternating row colors (Zebra striping halus: #FFFFFF dan #F8FAFC).
6. Area Sel Pengisian (Editable): Soft Pastel Mint (#ECFDF5) dengan border rapi, sehingga langsung jelas kolom mana yang perlu diisi oleh kecamatan.
7. Grid Borders: Garis tabel solid rapi (#CBD5E1).
8. Auto-fit column width & text wrapping.
"""

import sys
import json
import time
import requests
from typing import Dict, Any, List

sys.path.append('/root/.gemini/config/skills/gdrive/scripts')
from gdrive_tool import get_valid_access_token

KECAMATAN_LIST = [
    {
        "name": "Mempawah Hilir",
        "id": "1VB3k9opurqMccOdBMC4uKoP9UBiMOkzCroJEl7zriq4",
        "has_dusun": False
    },
    {
        "name": "Mempawah Timur",
        "id": "1rIf9ZuTD2kK4BOysQ__kh_e5ZtWmopttM5GrEYrZd9g",
        "has_dusun": True
    },
    {
        "name": "Sungai Pinyuh",
        "id": "1lEUFr2BTPtnuBPHje2MLAg4hZONO_dQE-BAGad6X9UA",
        "has_dusun": False
    },
    {
        "name": "Sungai Kunyit",
        "id": "1rj5c7TUhK1NvVDWaubXQrrr97661Hdw4Q_DHoOx7r00",
        "has_dusun": True
    },
    {
        "name": "Segedong",
        "id": "1Z-1MqJtT8mIXwdWjeSiFLdso52ECJCsBBYPi-5Cd-3c",
        "has_dusun": True
    },
    {
        "name": "Toho",
        "id": "15VShKwCXs-T5W7UmS1Cw1D3H2CAJiZLEJ3MjXOKfCbk",
        "has_dusun": True
    },
    {
        "name": "Jongkat",
        "id": "13hrB-jznRqBceBglwYZWL3tO464oPKpBmP6okwpCfLg",
        "has_dusun": True
    },
    {
        "name": "Anjongan",
        "id": "1iofOq1dSkm2F6FhKAKxRTYJH0hAyXmsJjC8briYcji0",
        "has_dusun": True
    },
    {
        "name": "Sadaniang",
        "id": "1jXSyjVD121WCUhy4cU1glzFDrBlHdi68itDhvEa-IHU",
        "has_dusun": True
    }
]

# Color constants (RGB 0.0 - 1.0)
COLOR_NAVY_TITLE = {"red": 0.118, "green": 0.227, "blue": 0.541}   # #1E3A8A
COLOR_SLATE_HEADER = {"red": 0.118, "green": 0.251, "blue": 0.686} # #1E40AF
COLOR_EMERALD_HEADER = {"red": 0.020, "green": 0.588, "blue": 0.412} # #059669
COLOR_GRAY_NUM = {"red": 0.945, "green": 0.961, "blue": 0.976}     # #F1F5F9
COLOR_TEXT_NUM = {"red": 0.282, "green": 0.337, "blue": 0.412}     # #475569
COLOR_WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}
COLOR_ZEBRA_ODD = {"red": 0.973, "green": 0.980, "blue": 0.988}   # #F8FAFC
COLOR_EDITABLE_MINT = {"red": 0.925, "green": 0.992, "blue": 0.961} # #ECFDF5
COLOR_BORDER_GRID = {"red": 0.796, "green": 0.835, "blue": 0.882}  # #CBD5E1
COLOR_BORDER_MINT = {"red": 0.655, "green": 0.906, "blue": 0.765}  # #A7F3D0

def get_headers():
    token = get_valid_access_token()
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def style_tab_table(sid: str, sheet_id: int, tab_title: str, total_rows: int, total_cols: int, fill_start_col: int, kec_name: str) -> List[Dict[str, Any]]:
    """
    Menghasilkan request batchUpdate untuk memberi warna tabel:
    - Row 0: Title (Navy Blue)
    - Row 1: Headers (Col 0..fill_start_col-1: Slate Blue, Col fill_start_col..total_cols-1: Emerald Green)
    - Row 2: Numbering (Col 0..total_cols-1: Soft Gray)
    - Row 3..total_rows-1: Data rows
      * Col 0..fill_start_col-1: Zebra striping (#FFFFFF dan #F8FAFC)
      * Col fill_start_col..total_cols-1: Soft Mint (#ECFDF5)
    - Grid borders halus
    """
    reqs = []

    # 1. Row 0: Judul Tabel
    reqs.append({
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': total_cols
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': COLOR_NAVY_TITLE,
                    'textFormat': {
                        'bold': True,
                        'fontSize': 11,
                        'foregroundColor': COLOR_WHITE
                    },
                    'verticalAlignment': 'MIDDLE',
                    'wrapStrategy': 'WRAP'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,verticalAlignment,wrapStrategy)'
        }
    })

    # 2. Row 1: Header Acuan (Slate Blue)
    if fill_start_col > 0:
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2,
                    'startColumnIndex': 0,
                    'endColumnIndex': fill_start_col
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': COLOR_SLATE_HEADER,
                        'textFormat': {
                            'bold': True,
                            'fontSize': 10,
                            'foregroundColor': COLOR_WHITE
                        },
                        'horizontalAlignment': 'CENTER',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)'
            }
        })

    # 3. Row 1: Header Kolom Pengisian / Update (Emerald Green)
    if fill_start_col < total_cols:
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2,
                    'startColumnIndex': fill_start_col,
                    'endColumnIndex': total_cols
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': COLOR_EMERALD_HEADER,
                        'textFormat': {
                            'bold': True,
                            'fontSize': 10,
                            'foregroundColor': COLOR_WHITE
                        },
                        'horizontalAlignment': 'CENTER',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)'
            }
        })

    # 4. Row 2: Nomor Kolom (Soft Gray)
    reqs.append({
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': 2,
                'endRowIndex': 3,
                'startColumnIndex': 0,
                'endColumnIndex': total_cols
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': COLOR_GRAY_NUM,
                    'textFormat': {
                        'italic': True,
                        'fontSize': 9,
                        'foregroundColor': COLOR_TEXT_NUM
                    },
                    'horizontalAlignment': 'CENTER',
                    'verticalAlignment': 'MIDDLE'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)'
        }
    })

    # 5. Data Rows: Kolom Acuan (Zebra Striping)
    if fill_start_col > 0 and total_rows > 3:
        for r_idx in range(3, total_rows):
            bg = COLOR_WHITE if (r_idx % 2 == 1) else COLOR_ZEBRA_ODD
            reqs.append({
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': r_idx,
                        'endRowIndex': r_idx + 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': fill_start_col
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': bg,
                            'textFormat': {'fontSize': 10},
                            'verticalAlignment': 'MIDDLE'
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat,verticalAlignment)'
                }
            })

    # 6. Data Rows: Kolom Isian (Soft Mint Editable Highlight)
    if fill_start_col < total_cols and total_rows > 3:
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 3,
                    'endRowIndex': total_rows,
                    'startColumnIndex': fill_start_col,
                    'endColumnIndex': total_cols
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': COLOR_EDITABLE_MINT,
                        'textFormat': {'fontSize': 10},
                        'verticalAlignment': 'MIDDLE'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,verticalAlignment)'
            }
        })

    # 7. Grid Borders
    reqs.append({
        'updateBorders': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': 1,
                'endRowIndex': total_rows,
                'startColumnIndex': 0,
                'endColumnIndex': total_cols
            },
            'top': {'style': 'SOLID', 'color': COLOR_BORDER_GRID},
            'bottom': {'style': 'SOLID', 'color': COLOR_BORDER_GRID},
            'left': {'style': 'SOLID', 'color': COLOR_BORDER_GRID},
            'right': {'style': 'SOLID', 'color': COLOR_BORDER_GRID},
            'innerHorizontal': {'style': 'SOLID', 'color': COLOR_BORDER_GRID},
            'innerVertical': {'style': 'SOLID', 'color': COLOR_BORDER_GRID}
        }
    })

    # 8. Auto-fit column widths
    reqs.append({
        'autoResizeDimensions': {
            'dimensions': {
                'sheetId': sheet_id,
                'dimension': 'COLUMNS',
                'startIndex': 0,
                'endIndex': total_cols
            }
        }
    })

    return reqs

def prepare_tab_data_and_style(kec: Dict[str, Any], headers: Dict[str, str]):
    sid = kec["id"]
    name = kec["name"]
    has_dusun = kec["has_dusun"]

    print(f"\n=======================================================", flush=True)
    print(f"🎨 Memproses Pewarnaan & Styling: {name} ({sid})", flush=True)
    print(f"=======================================================", flush=True)

    # 1. Ambil metadata seluruh tab
    meta_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}?fields=sheets(properties(sheetId,title))"
    r = requests.get(meta_url, headers=headers, timeout=15)
    r.raise_for_status()
    sheets_info = r.json().get('sheets', [])
    sheet_map = {s['properties']['title']: s['properties']['sheetId'] for s in sheets_info}

    batch_requests = []

    # =========================================================================
    # TABEL 2.1.2: Nama-Nama Camat
    # =========================================================================
    if 'Tabel 2.1.2' in sheet_map:
        sh_id = sheet_map['Tabel 2.1.2']
        # Baca data saat ini
        val_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.1.2!A1:G100"
        r_val = requests.get(val_url, headers=headers, timeout=15)
        raw_rows = r_val.json().get('values', [])
        
        # Susun data yang rapi dengan kolom koreksi/update
        new_rows = []
        new_rows.append([f"Tabel 2.1.2 Nama-Nama Camat yang Pernah dan Masih Menjabat di Kecamatan {name}", "", "", "", ""])
        new_rows.append([
            "No",
            "Nama-Nama Camat",
            "Periode Jabatan (Acuan)",
            "Koreksi / Perubahan Nama / Status Camat (Update 2026)",
            "Catatan / Keterangan"
        ])
        new_rows.append(["(1)", "(2)", "(3)", "(4)", "(5)"])

        data_camat = []
        for r_item in raw_rows:
            if len(r_item) >= 2 and str(r_item[0]).strip() not in ["2025", "No", "-1", "(1)"]:
                no = str(r_item[0]).strip()
                c_nama = str(r_item[1]).strip()
                c_per = str(r_item[2]).strip() if len(r_item) > 2 else ""
                c_upd = str(r_item[3]).strip() if len(r_item) > 3 else ""
                c_not = str(r_item[4]).strip() if len(r_item) > 4 else ""
                data_camat.append([no, c_nama, c_per, c_upd, c_not])

        if not data_camat:
            # Fallback jika data kosong
            for i in range(1, 5):
                data_camat.append([str(i), "", "", "", ""])

        # Tambahkan baris entri camat baru jika ada pergantian
        data_camat.append(["+", "Camat Baru (jika ada pergantian jabatan)", "", "", ""])

        new_rows.extend(data_camat)

        # Update values
        put_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.1.2!A1:E{len(new_rows)}?valueInputOption=USER_ENTERED"
        requests.put(put_url, headers=headers, json={"range": f"Tabel 2.1.2!A1:E{len(new_rows)}", "values": new_rows}, timeout=15)

        # Tambahkan styling: Total col = 5, fill_start_col = 3 (Kolom 4 & 5 isian)
        batch_requests.extend(style_tab_table(sid, sh_id, 'Tabel 2.1.2', len(new_rows), 5, 3, name))
        print(f"   ✓ Tabel 2.1.2 di-update ({len(new_rows)} baris, 5 kolom)", flush=True)

    # =========================================================================
    # TABEL 2.1.3: Nama-Nama Kepala Desa
    # =========================================================================
    if 'Tabel 2.1.3' in sheet_map:
        sh_id = sheet_map['Tabel 2.1.3']
        val_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.1.3!A1:G100"
        r_val = requests.get(val_url, headers=headers, timeout=15)
        raw_rows = r_val.json().get('values', [])
        actual_rows = len([r for r in raw_rows if any(r)])
        if actual_rows < 4:
            actual_rows = 12

        # Styling: Total col = 5, fill_start_col = 3 (Kolom 4 & 5 isian)
        batch_requests.extend(style_tab_table(sid, sh_id, 'Tabel 2.1.3', actual_rows, 5, 3, name))
        print(f"   ✓ Tabel 2.1.3 di-style ({actual_rows} baris, 5 kolom)", flush=True)

    # =========================================================================
    # TABEL 2.1.4: Nama-Nama Kepala Dusun (hanya untuk kecamatan yang ada dusun)
    # =========================================================================
    if has_dusun and 'Tabel 2.1.4' in sheet_map:
        sh_id = sheet_map['Tabel 2.1.4']
        val_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.1.4!A1:G250"
        r_val = requests.get(val_url, headers=headers, timeout=15)
        raw_rows = r_val.json().get('values', [])

        new_rows = []
        new_rows.append([f"Tabel 2.1.4 Nama-Nama Kepala Dusun di Kecamatan {name}, 2025 dan 2026", "", "", "", "", ""])
        new_rows.append([
            "No",
            "Desa / Kelurahan",
            "Nama Dusun",
            "Nama Kepala Dusun (Acuan 2025)",
            "Nama Kepala Dusun (Kondisi 2026 / Terkini)",
            "Catatan / Keterangan"
        ])
        new_rows.append(["(1)", "(2)", "(3)", "(4)", "(5)", "(6)"])

        data_dusun = []
        for r_item in raw_rows:
            if len(r_item) >= 2 and str(r_item[0]).strip() not in ["2025", "No", "-1", "(1)"]:
                no = str(r_item[0]).strip()
                desa = str(r_item[1]).strip()
                dusun = str(r_item[2]).strip() if len(r_item) > 2 else ""
                kd_acuan = str(r_item[3]).strip() if len(r_item) > 3 else ""
                kd_upd = str(r_item[4]).strip() if len(r_item) > 4 else ""
                cat = str(r_item[5]).strip() if len(r_item) > 5 else ""
                data_dusun.append([no, desa, dusun, kd_acuan, kd_upd, cat])

        if not data_dusun:
            for i in range(1, 10):
                data_dusun.append([str(i), "", "", "", "", ""])

        new_rows.extend(data_dusun)

        put_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.1.4!A1:F{len(new_rows)}?valueInputOption=USER_ENTERED"
        requests.put(put_url, headers=headers, json={"range": f"Tabel 2.1.4!A1:F{len(new_rows)}", "values": new_rows}, timeout=15)

        # Styling: Total col = 6, fill_start_col = 4 (Kolom 5 & 6 isian)
        batch_requests.extend(style_tab_table(sid, sh_id, 'Tabel 2.1.4', len(new_rows), 6, 4, name))
        print(f"   ✓ Tabel 2.1.4 di-update ({len(new_rows)} baris, 6 kolom)", flush=True)

    # =========================================================================
    # TABEL 2.2.1: Jumlah PNS Menurut Pemerintah Daerah & Jenis Kelamin
    # =========================================================================
    if 'Tabel 2.2.1' in sheet_map:
        sh_id = sheet_map['Tabel 2.2.1']
        val_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.2.1!A1:G100"
        r_val = requests.get(val_url, headers=headers, timeout=15)
        raw_rows = r_val.json().get('values', [])

        new_rows = []
        new_rows.append([f"Tabel 2.2.1 Jumlah Pegawai Negeri Sipil Menurut Pemerintah Daerah dan Jenis Kelamin di Kecamatan {name}", "", "", ""])
        new_rows.append([
            "Pemerintah Daerah / Instansi",
            "Laki-Laki [KOLOM ISIAN]",
            "Perempuan [KOLOM ISIAN]",
            "Jumlah [KOLOM ISIAN]"
        ])
        new_rows.append(["(1)", "(2)", "(3)", "(4)"])

        for r_item in raw_rows:
            if len(r_item) >= 1:
                val_0 = str(r_item[0]).strip()
                if val_0 not in ["2025", "Pemerintah Daerah\nLocal Government", "Pemerintah Daerah", "(1)", "-1"]:
                    c1 = str(r_item[1]).strip() if len(r_item) > 1 else ""
                    c2 = str(r_item[2]).strip() if len(r_item) > 2 else ""
                    c3 = str(r_item[3]).strip() if len(r_item) > 3 else ""
                    new_rows.append([val_0, c1, c2, c3])

        put_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.2.1!A1:D{len(new_rows)}?valueInputOption=USER_ENTERED"
        requests.put(put_url, headers=headers, json={"range": f"Tabel 2.2.1!A1:D{len(new_rows)}", "values": new_rows}, timeout=15)

        # Styling: Total col = 4, fill_start_col = 1 (Kolom 2, 3, 4 isian semua!)
        batch_requests.extend(style_tab_table(sid, sh_id, 'Tabel 2.2.1', len(new_rows), 4, 1, name))
        print(f"   ✓ Tabel 2.2.1 di-update ({len(new_rows)} baris, 4 kolom)", flush=True)

    # =========================================================================
    # TABEL 2.2.2: Jumlah PNS Menurut Pendidikan & Jenis Kelamin
    # =========================================================================
    if 'Tabel 2.2.2' in sheet_map:
        sh_id = sheet_map['Tabel 2.2.2']
        val_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.2.2!A1:G100"
        r_val = requests.get(val_url, headers=headers, timeout=15)
        raw_rows = r_val.json().get('values', [])

        new_rows = []
        new_rows.append([f"Tabel 2.2.2 Jumlah Pegawai Negeri Sipil Pemerintah Kecamatan Menurut Pendidikan dan Jenis Kelamin di Kecamatan {name}", "", "", ""])
        new_rows.append([
            "Tingkat Pendidikan",
            "Laki-Laki [KOLOM ISIAN]",
            "Perempuan [KOLOM ISIAN]",
            "Jumlah [KOLOM ISIAN]"
        ])
        new_rows.append(["(1)", "(2)", "(3)", "(4)"])

        for r_item in raw_rows:
            if len(r_item) >= 1:
                val_0 = str(r_item[0]).strip()
                if val_0 not in ["2025", "Tingkat Pendidikan\n Educational Level", "Tingkat Pendidikan", "(1)", "-1"]:
                    c1 = str(r_item[1]).strip() if len(r_item) > 1 else ""
                    c2 = str(r_item[2]).strip() if len(r_item) > 2 else ""
                    c3 = str(r_item[3]).strip() if len(r_item) > 3 else ""
                    new_rows.append([val_0, c1, c2, c3])

        put_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/Tabel%202.2.2!A1:D{len(new_rows)}?valueInputOption=USER_ENTERED"
        requests.put(put_url, headers=headers, json={"range": f"Tabel 2.2.2!A1:D{len(new_rows)}", "values": new_rows}, timeout=15)

        # Styling: Total col = 4, fill_start_col = 1 (Kolom 2, 3, 4 isian semua!)
        batch_requests.extend(style_tab_table(sid, sh_id, 'Tabel 2.2.2', len(new_rows), 4, 1, name))
        print(f"   ✓ Tabel 2.2.2 di-update ({len(new_rows)} baris, 4 kolom)", flush=True)

    # Eksekusi batchUpdate formatting
    if batch_requests:
        batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}:batchUpdate"
        # Pecah ke batch kecil jika terlalu besar (maks 100 requests per call)
        chunk_size = 80
        for i in range(0, len(batch_requests), chunk_size):
            chunk = batch_requests[i:i + chunk_size]
            res = requests.post(batch_url, headers=headers, json={"requests": chunk}, timeout=20)
            res.raise_for_status()
        print(f"   ✨ Styling dan Pewarnaan {name} SELESAI!", flush=True)

def main():
    headers = get_headers()
    print("🚀 Memulai styling dan pewarnaan visual tabel untuk seluruh 9 spreadsheet kecamatan...\n", flush=True)
    for kec in KECAMATAN_LIST:
        try:
            prepare_tab_data_and_style(kec, headers)
            time.sleep(1) # Jeda rate-limit API
        except Exception as e:
            print(f"❌ Gagal memproses styling {kec['name']}: {e}", flush=True)

    print("\n🎉 SEMUA TABEL DI 9 GOOGLE SPREADSHEET TELAH DIBERI PEWARNAAN VISUAL YANG INDAH DAN USER-FRIENDLY!", flush=True)

if __name__ == '__main__':
    main()
