# Data Pegawai BPS Kabupaten Mempawah

Direktori ini menyimpan data referensial pegawai aktif BPS Kabupaten Mempawah.

## Format File

File Data_Pegawai.csv memuat kolom-kolom berikut:

| Kolom      | Keterangan                                      |
|------------|-------------------------------------------------|
| Nama     | Nama lengkap pegawai beserta gelar              |
| Email    | Email kantor BPS (@bps.go.id)                 |
| Jabatan  | Jabatan fungsional/struktural saat ini          |
| Panggilan| Nama panggilan yang digunakan dalam sistem AI   |

## Cara Update (Saat Ada Mutasi/CPNS Baru)

1. Buka Data_Pegawai.csv di editor teks atau VS Code
2. Tambah baris baru di bawah untuk pegawai baru, atau edit/hapus baris untuk mutasi/pensiun
3. Format nama: tanpa tanda baca berlebih, cukup gelar singkat (S.Tr.Stat., S.E., dll.)
4. Simpan, lakukan git add data/pegawai/Data_Pegawai.csv dan git commit
5. Git akan menampilkan diff yang jelas baris mana yang berubah

## Catatan Keamanan

- **Tidak ada NIP atau nomor WA** — data ini aman untuk publik
- Email BPS bersifat publik dan digunakan sebagai kunci identifikasi pengguna repo
- File .env lokal (gitignored) menyimpan KB_USER_EMAIL untuk identitas pengguna di tiap laptop

## Penggunaan oleh AI Agent

Modul scripts/kb/user_identity.py membaca file ini untuk mendeteksi siapa pengguna
aktif repo (cascade: .env → git config email → tidak dikenali).
