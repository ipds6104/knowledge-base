#!/usr/bin/env python3
"""
Update Google Spreadsheet SE2026 Petugas Aulia Fitriani dari Single Source of Truth (SurrealDB / Local SQLite Mirror)
Spreadsheet ID: 1MjLYYtG2Mwx77VfvLstdJh3IdR2mAS3vcBXIelxTH5I
"""

import sys
import os
import sqlite3
import json
import requests

sys.path.insert(0, '/root/.gemini/config/skills/gdrive/scripts')
import gdrive_tool

SPREADSHEET_ID = '1MjLYYtG2Mwx77VfvLstdJh3IdR2mAS3vcBXIelxTH5I'
DB_PATH = '/app/shared_data/se2026_local.db'

def get_headers():
    token = gdrive_tool.get_valid_access_token()
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

def format_rupiah(val):
    try:
        n = float(val)
        return f"Rp {n:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return "-"

def update_spreadsheet():
    print("[*] Menghubungkan ke database lokal SQLite SE2026...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. Fetch all 171 active businesses
    cur.execute("""
        SELECT 
            u.level_6_full_code,
            u.level_6_name,
            u.nama_usaha,
            COALESCE(NULLIF(u.pengusaha, ''), g.nama_kk, '-') as nama_pengusaha_kk,
            u.keberadaan_usaha_label,
            u.kategori,
            u.kbli_akhir,
            u.kbli_label,
            COALESCE(NULLIF(u.keg_utama, ''), u.produk, '-') as keg_utama,
            u.total_tk_bayar,
            u.total_tk_jk,
            u.tk_dibayar,
            u.tk_tdk_dibayar,
            u.tk_laki,
            u.tk_pr,
            u.total_pendapatan,
            u.total_pengeluaran,
            COALESCE(NULLIF(u.hp, ''), '-') as hp,
            COALESCE(NULLIF(g.jalan_domisili, ''), u.sls_l, '-') as jalan,
            COALESCE(NULLIF(u.no_bang_l, ''), g.no_bang, '-') as no_bang,
            g.latitude,
            g.longitude
        FROM se2026_nested u
        LEFT JOIN assignment_geo g ON u.assignment_id = g.id
        WHERE u.keberadaan_usaha_value IN ('1', '2')
        ORDER BY u.level_6_full_code ASC, u.nama_usaha ASC;
    """)
    active_rows = cur.fetchall()
    print(f"[✓] Ditemukan {len(active_rows)} unit usaha aktif dari SurrealDB mirror.")

    headers_tab1 = [
        "No", "Kode SLS", "Nama SLS", "Nama Usaha", "Nama Pengusaha / KK",
        "Status Usaha", "Kategori", "Kode KBLI", "Deskripsi KBLI", "Kegiatan Utama / Produk",
        "Total TK", "TK Dibayar (Tetap)", "TK Tidak Dibayar (Keluarga)", "TK Laki-laki", "TK Perempuan",
        "Total Pendapatan", "Total Pengeluaran", "No HP / Telp", "Alamat & No Bangunan",
        "Latitude", "Longitude", "Link Google Maps", "Catatan Audit Lapangan (Koseka Rifky)"
    ]

    values_tab1 = [headers_tab1]
    audit_rows = []

    for idx, r in enumerate(active_rows, 1):
        lat = r["latitude"]
        lng = r["longitude"]
        maps_link = f"https://www.google.com/maps?q={lat},{lng}" if lat and lng else "-"
        alamat = f"{r['jalan']} (No Bang: {r['no_bang']})"

        # Logic audit anomali tenaga kerja
        catatan_audit = "-"
        is_audit = False
        kbli = str(r["kbli_akhir"] or "")
        tk_bayar = int(r["tk_dibayar"] or 0)
        
        if kbli in ["01122", "01121", "01262", "01291"] and tk_bayar > 0:
            is_audit = True
            catatan_audit = f"⚠️ AUDIT TK: Dicatat TK Dibayar={tk_bayar} org. Verifikasi apakah buruh panen/nebas harian lepas musiman dicatat sbg pekerja tetap!"
        elif tk_bayar >= 5:
            is_audit = True
            catatan_audit = f"⚠️ AUDIT TK: TK Dibayar={tk_bayar} org relatif tinggi untuk skala UMKM desa. Konfirmasi jenis hubungan kerja pekerja."

        row_data = [
            idx,
            r["level_6_full_code"],
            r["level_6_name"],
            r["nama_usaha"],
            r["nama_pengusaha_kk"],
            r["keberadaan_usaha_label"],
            r["kategori"],
            r["kbli_akhir"],
            r["kbli_label"] or f"[{r['kategori']}][{r['kbli_akhir']}]",
            r["keg_utama"],
            r["total_tk_bayar"],
            r["tk_dibayar"],
            r["tk_tdk_dibayar"],
            r["tk_laki"],
            r["tk_pr"],
            format_rupiah(r["total_pendapatan"]),
            format_rupiah(r["total_pengeluaran"]),
            r["hp"],
            alamat,
            lat or "-",
            lng or "-",
            maps_link,
            catatan_audit
        ]
        values_tab1.append(row_data)

        if is_audit:
            audit_rows.append([
                len(audit_rows) + 1,
                r["level_6_full_code"],
                r["level_6_name"],
                r["nama_usaha"],
                r["nama_pengusaha_kk"],
                r["kbli_akhir"],
                r["kbli_label"] or f"[{r['kategori']}][{r['kbli_akhir']}]",
                r["tk_dibayar"],
                r["tk_tdk_dibayar"],
                r["total_tk_bayar"],
                format_rupiah(r["total_pendapatan"]),
                format_rupiah(r["total_pengeluaran"]),
                r["hp"],
                maps_link,
                catatan_audit
            ])

    # 2. Rekap SLS
    cur.execute("""
        SELECT 
            level_6_full_code,
            level_6_name,
            SUM(CASE WHEN keberadaan_usaha_value = '1' THEN 1 ELSE 0 END) as ditemukan,
            SUM(CASE WHEN keberadaan_usaha_value = '2' THEN 1 ELSE 0 END) as baru,
            SUM(CASE WHEN keberadaan_usaha_value = '0' THEN 1 ELSE 0 END) as tdk_ditemukan,
            SUM(CASE WHEN keberadaan_usaha_value = '3' THEN 1 ELSE 0 END) as tutup,
            count(*) as total_prelist,
            SUM(CASE WHEN keberadaan_usaha_value IN ('1', '2') THEN 1 ELSE 0 END) as total_aktif,
            SUM(CASE WHEN keberadaan_usaha_value IN ('1', '2') AND kbli_akhir IN ('01122', '01121', '01262', '01291') AND tk_dibayar > 0 THEN 1 ELSE 0 END) as kasus_audit_tani
        FROM se2026_nested
        GROUP BY level_6_full_code, level_6_name
        ORDER BY level_6_full_code;
    """)
    rekap_sls = cur.fetchall()

    headers_tab_rekap = [
        "No", "Kode SLS", "Nama SLS", "1. Ditemukan", "2. Baru", 
        "0. Tdk Ditemukan", "3. Tutup", "Total Prelist DB", "Total Usaha Aktif Lapangan",
        "Kasus Audit TK Sawah/Tani", "Catatan Koseka Rifky"
    ]
    values_tab_rekap = [headers_tab_rekap]
    for idx, r in enumerate(rekap_sls, 1):
        cat = "Prioritas perbaikan TK sawah" if r["kasus_audit_tani"] > 10 else "Periksa sampel sawah"
        values_tab_rekap.append([
            idx,
            r["level_6_full_code"],
            r["level_6_name"],
            r["ditemukan"],
            r["baru"],
            r["tdk_ditemukan"],
            r["tutup"],
            r["total_prelist"],
            r["total_aktif"],
            r["kasus_audit_tani"],
            cat
        ])
    
    # Total row for rekap
    values_tab_rekap.append([
        "TOTAL", "6 SLS", "Desa Kepayang (Aulia Fitriani)",
        sum(r["ditemukan"] for r in rekap_sls),
        sum(r["baru"] for r in rekap_sls),
        sum(r["tdk_ditemukan"] for r in rekap_sls),
        sum(r["tutup"] for r in rekap_sls),
        sum(r["total_prelist"] for r in rekap_sls),
        sum(r["total_aktif"] for r in rekap_sls),
        sum(r["kasus_audit_tani"] for r in rekap_sls),
        f"Total {sum(r['kasus_audit_tani'] for r in rekap_sls)} kasus perlu konfirmasi buruh harian lepas"
    ])

    # 3. Headers Tab Audit
    headers_tab_audit = [
        "No", "Kode SLS", "Nama SLS", "Nama Usaha", "Nama Pengusaha / KK",
        "Kode KBLI", "Deskripsi KBLI", "TK Dibayar Terinput", "TK Keluarga",
        "Total TK", "Pendapatan", "Pengeluaran", "No HP", "Link Maps", "Rekomendasi Perbaikan Koseka"
    ]
    values_tab_audit = [headers_tab_audit] + audit_rows

    print(f"[*] Menyiapkan upload ke Google Spreadsheet ID: {SPREADSHEET_ID}...")
    headers = get_headers()

    # Step A: Update Tab Names and Clear Ranges
    sheets_api = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"
    
    # Rename Tab 1 to 'Data Master Unit Usaha'
    batch_meta = {
        "requests": [
            {
                "updateSheetProperties": {
                    "properties": {"sheetId": 0, "title": "Data Master Unit Usaha (SurrealDB)"},
                    "fields": "title"
                }
            },
            {
                "updateSheetProperties": {
                    "properties": {"sheetId": 1489102720, "title": "Audit Kasus TK Sawah (Rifky)"},
                    "fields": "title"
                }
            },
            {
                "updateSheetProperties": {
                    "properties": {"sheetId": 298099571, "title": "Rekap 6 SLS & Kasus"},
                    "fields": "title"
                }
            }
        ]
    }
    requests.post(f"{sheets_api}:batchUpdate", headers=headers, json=batch_meta)

    # Step B: Clear old contents
    requests.post(f"{sheets_api}/values:batchClear", headers=headers, json={
        "ranges": [
            "'Data Master Unit Usaha (SurrealDB)'!A1:Z1000",
            "'Audit Kasus TK Sawah (Rifky)'!A1:Z500",
            "'Rekap 6 SLS & Kasus'!A1:Z50"
        ]
    })

    # Step C: Write new data
    data_payload = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {
                "range": f"'Data Master Unit Usaha (SurrealDB)'!A1:W{len(values_tab1)}",
                "values": values_tab1
            },
            {
                "range": f"'Audit Kasus TK Sawah (Rifky)'!A1:O{len(values_tab_audit)}",
                "values": values_tab_audit
            },
            {
                "range": f"'Rekap 6 SLS & Kasus'!A1:K{len(values_tab_rekap)}",
                "values": values_tab_rekap
            }
        ]
    }
    resp = requests.post(f"{sheets_api}/values:batchUpdate", headers=headers, json=data_payload)
    if resp.status_code == 200:
        print("[✓] Berhasil mengunggah seluruh data ke Google Spreadsheet!")
        print(f"    - Tab 1: {len(values_tab1)-1} usaha aktif")
        print(f"    - Tab 2: {len(values_tab_audit)-1} kasus audit tenaga kerja sawah")
        print(f"    - Tab 3: {len(values_tab_rekap)-2} SLS + ringkasan")
    else:
        print(f"[!] Gagal batch update: {resp.status_code} - {resp.text}")

    # Step D: Apply Styling (Bold Headers, Frozen Header Row, Alternating Colors)
    style_payload = {
        "requests": [
            # Freeze header row on Tab 1
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": 0,
                        "gridProperties": {"frozenRowCount": 1}
                    },
                    "fields": "gridProperties.frozenRowCount"
                }
            },
            # Freeze header row on Tab Audit
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": 1489102720,
                        "gridProperties": {"frozenRowCount": 1}
                    },
                    "fields": "gridProperties.frozenRowCount"
                }
            },
            # Format header Tab 1 with deep navy blue background and white text
            {
                "repeatCell": {
                    "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 0.08, "green": 0.22, "blue": 0.38},
                            "textFormat": {"bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            },
            # Format header Tab Audit with dark red background and white text
            {
                "repeatCell": {
                    "range": {"sheetId": 1489102720, "startRowIndex": 0, "endRowIndex": 1},
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 0.55, "green": 0.12, "blue": 0.12},
                            "textFormat": {"bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            },
            # Format header Tab Rekap with dark green background
            {
                "repeatCell": {
                    "range": {"sheetId": 298099571, "startRowIndex": 0, "endRowIndex": 1},
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 0.12, "green": 0.42, "blue": 0.22},
                            "textFormat": {"bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            }
        ]
    }
    requests.post(f"{sheets_api}:batchUpdate", headers=headers, json=style_payload)
    print("[✓] Styling header tabel berhasil diterapkan.")

if __name__ == "__main__":
    update_spreadsheet()
