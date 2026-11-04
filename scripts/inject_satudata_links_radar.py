#!/usr/bin/env python3
"""
scripts/inject_satudata_links_radar.py
Injects verified Satu Data Mempawah dataset links into Column I of tab 'Radar 23 OPD'.
"""

import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = '19mp02bfJv3I_FPky6dUU9ZIRSbW7wEQlkgbXFdK6g6M'
TAB_NAME = 'Radar 23 OPD'
TAB_ID = 1351606795

# 23 OPD Data mapping (Rows 5 to 27)
# Hanya OPD Kelompok A & B dengan kesesuaian variabel terbukti yang ditautkan
DATA_LINKS = [
    # Row 5: 1. BPKAD (Lokus 1) - Realisasi Pendapatan & Belanja
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/jumlah-pendapatan-daerah-kabupaten-mempawah-tahun-2020", "🔗 Realisasi Pendapatan Daerah")',
    # Row 6: 2. BKPSDM - ASN menurut Pendidikan
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/jumlah-aparatur-sipil-negara-asn-menurut-tingkat-pendidikan", "🔗 Jumlah ASN Menurut Pendidikan")',
    # Row 7: 3. Bakesbangpol - Ormas Terdaftar
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/organisasi-kemasyarakatan-ormas-terdaftar-pada-bagian-kesbangpol-sekretariat-daerah-tahun-2019", "🔗 Ormas Terdaftar")',
    # Row 8: 4. BPPRD - Retribusi Daerah
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/target-dan-realisasi-retribusi-daerah-tahun-2019", "🔗 Realisasi Retribusi Daerah")',
    # Row 9: 5. Inspektorat - SAKIP
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/nilai-sakip-pemerintah-daerah-kabupaten-mempawah-tahun-2025", "🔗 Nilai SAKIP Pemkab")',
    # Row 10: 6. DPMPTSP (Lokus 2) - Perizinan OSS RBA
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/realisasi-jumlah-perizinan-oss-rba-tahun-2021", "🔗 Realisasi Perizinan OSS RBA")',
    # Row 11: 7. Dinkes - AKB
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/angka-kematian-balita-per-1000-kelahiran-hidup", "🔗 Angka Kematian Balita (AKB)")',
    # Row 12: 8. RSUD dr. Rubini - BOR
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/keterisian-tempat-tidur-di-rsud-dr-rubini-tahun-2019", "🔗 BOR Tempat Tidur RSUD")',
    # Row 13: 9. Dinsos (Belum mengisi LK-01 / belum ada padanan spesifik)
    '-',
    # Row 14: 10. Disdukcapil - Jumlah Penduduk
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/jumlah-penduduk-kabupaten-mempawah", "🔗 Jumlah Penduduk Kab. Mempawah")',
    # Row 15: 11. Disperindagnaker - Pencari Kerja AK-1
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/pencari-kerja-terdaftar-berdasarkan-jenjang-pendidikan-tahun-2020", "🔗 Pencari Kerja Terdaftar (AK-1)")',
    # Row 16: 12. DPKPP - Produksi Peternakan
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/jumlah-produksi-peternakan-di-kabupaten-mempawah-tahun-2020-2023", "🔗 Produksi Peternakan")',
    # Row 17: 13. Dishub LH - Sampah Harian
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/produksi-sampah-kabupaten-mempawah-per-hari-tahun-2019", "🔗 Timbulan Sampah Harian")',
    # Row 18: 14. PUPR - Kemantapan Jalan
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/kondisi-jalan-di-kab-mempawah-tahun-2019", "🔗 Kondisi Kemantapan Jalan")',
    # Row 19: 15. Disperkimtan - RTLH
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/jumlah-rumah-tidak-layak-huni-rtlh-tahun-2019", "🔗 Data RTLH Terverifikasi")',
    # Row 20: 16. BPBD - Bantuan Korban Bencana
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/jumlah-penduduk-korban-bencana-yang-dibantu-tahun-2019-2023", "🔗 Realisasi Bantuan Bencana")',
    # Row 21: 17. Satpol PP - Pelanggaran Perda
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/jumlah-pelanggaran-peraturan-daerah-perda-tahun-2019", "🔗 Penegakan Peraturan Daerah")',
    # Row 22: 18. Dispusip (Belum mengisi LK-01)
    '-',
    # Row 23: 19. Sekretariat DPRD - Rapat Paripurna/Komisi
    '=HYPERLINK("https://satudata.mempawahkab.go.id/datasets/jumlah-rapat-dewan-perwakilan-rakyat-daerah-dprd-di-kabupaten-mempawah-tahun-2022", "🔗 Rapat Paripurna & Komisi")',
    # Row 24: 20. Bapperida (Belum mengisi LK-01)
    '-',
    # Row 25: 21. Diskominfo (Belum ada dataset spesifik sesuai indikator LK-01)
    '-',
    # Row 26: 22. Dikporapar (Indikator LK-01 ruang kelas beda dengan portal)
    '-',
    # Row 27: 23. Setda (Belum mengisi LK-01)
    '-',
    # Row 28: Total baris
    '-'
]


def main():
    token_file = Path('token.json')
    if not token_file.exists():
        print("Error: token.json tidak ditemukan", file=sys.stderr)
        return 1

    creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # 1. Update Values: I4 (Header) and I5:I28 (Data & Total)
    header = "Tautan Portal Satu Data (SDI)"
    all_values = [[header]] + [[v] for v in DATA_LINKS]

    body = {
        'values': all_values
    }

    range_name = f"{TAB_NAME}!I4:I28"
    print(f"Mengirim {len(all_values)} nilai ke range {range_name}...")
    res = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    print(f"✅ Berhasil mengupdate nilai: {res.get('updatedCells')} sel.")

    # 2. Update Formatting: Header I4 & Data I5:I28
    requests = [
        # Format Header (I4: col index 8, row index 3 to 4)
        {
            'repeatCell': {
                'range': {
                    'sheetId': TAB_ID,
                    'startRowIndex': 3,
                    'endRowIndex': 4,
                    'startColumnIndex': 8,
                    'endColumnIndex': 9
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.051, 'green': 0.231, 'blue': 0.400},
                        'horizontalAlignment': 'CENTER',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {
                            'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                            'fontFamily': 'Calibri',
                            'fontSize': 11,
                            'bold': True
                        },
                        'borders': {
                            'top': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.796, 'green': 0.835, 'blue': 0.878}},
                            'bottom': {'style': 'DOUBLE', 'width': 3, 'color': {'red': 0.290, 'green': 0.333, 'blue': 0.408}},
                            'left': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.796, 'green': 0.835, 'blue': 0.878}},
                            'right': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.796, 'green': 0.835, 'blue': 0.878}}
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat,borders)'
            }
        },
        # Format Data Rows (I5:I28: col index 8, row index 4 to 28)
        {
            'repeatCell': {
                'range': {
                    'sheetId': TAB_ID,
                    'startRowIndex': 4,
                    'endRowIndex': 28,
                    'startColumnIndex': 8,
                    'endColumnIndex': 9
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'LEFT',
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP',
                        'textFormat': {
                            'fontFamily': 'Calibri',
                            'fontSize': 10
                        },
                        'borders': {
                            'top': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.796, 'green': 0.835, 'blue': 0.878}},
                            'bottom': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.796, 'green': 0.835, 'blue': 0.878}},
                            'left': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.796, 'green': 0.835, 'blue': 0.878}},
                            'right': {'style': 'SOLID', 'width': 1, 'color': {'red': 0.796, 'green': 0.835, 'blue': 0.878}}
                        }
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat,borders)'
            }
        },
        # Auto-set Column Width Column I (Col index 8) to 270px
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': TAB_ID,
                    'dimension': 'COLUMNS',
                    'startIndex': 8,
                    'endIndex': 9
                },
                'properties': {
                    'pixelSize': 270
                },
                'fields': 'pixelSize'
            }
        }
    ]

    print("Menerapkan styling sel & lebar kolom...")
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={'requests': requests}
    ).execute()
    print("✅ Berhasil menerapkan styling dan format kolom I.")
    return 0


if __name__ == '__main__':
    sys.exit(main())

