"""kb/google_sheets.py — Google Sheets API connections and operations."""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    """Menginisialisasi Sheets API service dengan OAuth 2.0."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        if not creds:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "Berkas 'credentials.json' tidak ditemukan. "
                    "Pastikan Anda telah mengunduh OAuth Credentials dari Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('sheets', 'v4', credentials=creds)

def ensure_sheet_tab(service, spreadsheet_id: str, title: str, headers: list[str]) -> None:
    """Memastikan tab dengan judul tertentu ada dan memiliki header."""
    try:
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])
        existing_titles = [s.get('properties', {}).get('title') for s in sheets]
        
        # Jika tab belum ada, buat baru
        if title not in existing_titles:
            print(f"Tab '{title}' tidak ditemukan. Membuat tab baru...")
            body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': title
                        }
                    }
                }]
            }
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body
            ).execute()
            
            # Tulis header langsung ke tab baru
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"'{title}'!A1",
                valueInputOption='USER_ENTERED',
                body={'values': [headers]}
            ).execute()
            print(f"Tab '{title}' berhasil dibuat beserta header kolomnya.")
    except Exception as e:
        print(f"Gagal memverifikasi/membuat tab '{title}': {e}")
        raise e

def push_rows(service, spreadsheet_id: str, title: str, headers: list[str], rows: list[list]) -> None:
    """Menghapus isi tab lama dan melakukan bulk write untuk data baru."""
    # Pastikan tab ada
    ensure_sheet_tab(service, spreadsheet_id, title, headers)
    
    try:
        # 1. Bersihkan data lama dari baris A2 s.d. akhir kolom Z
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=f"'{title}'!A2:Z1000"
        ).execute()
        
        # 2. Tulis ulang Header di A1 (jika terhapus atau berubah)
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"'{title}'!A1",
            valueInputOption='USER_ENTERED',
            body={'values': [headers]}
        ).execute()
        
        # 3. Tulis data baru dari baris A2
        if rows:
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"'{title}'!A2",
                valueInputOption='USER_ENTERED',
                body={'values': rows}
            ).execute()
            
        print(f"Sukses melakukan sinkronisasi massal ke tab '{title}' ({len(rows)} baris terkirim).")
    except Exception as e:
        print(f"Gagal melakukan sinkronisasi data ke tab '{title}': {e}")
        raise e

def push_readme_tab(service, spreadsheet_id: str) -> None:
    """Membuat dan mengisi tab 'README' dengan dokumentasi penggunaan di Google Sheets."""
    title = "README"
    headers = ["Kunci/Informasi", "Detail / Penjelasan", "Contoh"]
    
    rows = [
        ["DATABASE TENGGAT WAKTU & METRIK KEGIATAN TERPADU - BPS KABUPATEN MEMPAWAH", "", ""],
        ["Dokumen ini adalah database terpadu untuk menyimpan seluruh milestone, deadlines, dan metrik progres kegiatan di BPS Kabupaten Mempawah.", "", ""],
        ["PENTING: Jangan mengedit isi data di tab 'unified_milestones' secara manual. Tab ini di-update secara otomatis oleh repositori basis pengetahuan (knowledge-base) via CLI command 'python scripts/kb.py sync-sheets'.", "", ""],
        ["", "", ""],
        ["DAFTAR TAB & DEKLARASI DATA:", "", ""],
        ["1. Tab 'unified_milestones'", "Menyimpan seluruh kalender jadwal kegiatan (Milestones & Deadlines).", ""],
        ["2. Tab 'unified_metrics'", "Menyimpan progres target dan realisasi kuantitatif kegiatan.", ""],
        ["", "", ""],
        ["STRUKTUR KOLOM TAB 'unified_milestones':", "", ""],
        ["Nama Kolom", "Keterangan", "Contoh Nilai"],
        ["activity_id", "ID unik kegiatan (slug) untuk pemfilteran.", "latsar-cpns-2026"],
        ["kategori", "Pengelompokan jenis kegiatan.", "survey, non-survey, kepegawaian"],
        ["tanggal", "Tanggal pelaksanaan/tenggat waktu (YYYY-MM-DD).", "2026-07-30"],
        ["kegiatan", "Deskripsi atau detail tenggat waktu.", "Kelompok 2: Sync Seminar Rancangan"],
        ["status", "Status pengerjaan (otomatis diperbarui harian).", "selesai, belum, overdue"],
        ["pic", "Kode penanggung jawab utama.", "ketua, anggota"],
        ["attributes_json", "Metadata kustom kegiatan dalam format JSON (kelompok, nomor surat, path, dll).", '{"kelompok": 2, "activity_name": "Latsar CPNS 2026"}']
    ]
    
    # Pastikan tab 'README' terbuat
    ensure_sheet_tab(service, spreadsheet_id, title, headers)
    
    try:
        # Tulis data ke tab README (A1 s.d. C17)
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"'{title}'!A1",
            valueInputOption='USER_ENTERED',
            body={'values': rows}
        ).execute()
        print("Tab 'README' berhasil diperbarui di Google Sheets.")
    except Exception as e:
        print(f"Gagal memperbarui tab 'README' di Google Sheets: {e}")

