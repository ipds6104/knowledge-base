import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Kita butuh akses penuh untuk membaca & menulis spreadsheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    creds = None
    # Token.json menyimpan kredensial akses pengguna setelah otorisasi pertama
    if os.path.exists('token.json'):
        print("Menemukan token.json lama, mencoba memvalidasi...")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # Jika token tidak ada atau tidak valid, lakukan alur login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Token kedaluwarsa, memperbarui secara otomatis...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print("Gagal memperbarui token secara otomatis, harus login ulang:", e)
                creds = None
                
        if not creds:
            print("Memulai Alur Autentikasi OAuth 2.0...")
            if not os.path.exists('credentials.json'):
                print("Error: File credentials.json tidak ditemukan di root repositori!")
                return
                
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            # Menjalankan server lokal untuk menangkap redirect uri dari browser
            creds = flow.run_local_server(port=0)
            
        # Simpan kredensial untuk dijalankan berikutnya
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            print("Token berhasil disimpan ke token.json")
            
    print("\n" + "=" * 50)
    print("🎉 AUTENTIKASI BERHASIL ATAS NAMA EMAIL ANDA!")
    print("=" * 50)
    
    # Hubungkan ke Google Sheets API untuk verifikasi
    try:
        service = build('sheets', 'v4', credentials=creds)
        print("Koneksi ke Google Sheets API berhasil terbentuk.")
    except Exception as e:
        print("Koneksi API gagal:", e)

if __name__ == '__main__':
    main()
