# 📋 Standar Operasional & Alur Kerja Default

1. **Troubleshooting Cepat**: Gunakan `scripts/model_control.py` untuk memeriksa status model.
2. **Pengorganisasian Proyek**: Jika muncul proyek baru berskala besar, jalankan `python3 scripts/workspace_manager.py create <nama_proyek>`.

## 3. SOP Pencarian & Kueri Data Sensus Ekonomi (SE2026 / DTSEN)
- **Sumber Data Tunggal & Resmi (Single Source of Truth)**: Seluruh pencarian data individu, keluarga, ART, pendapatan, koordinat, dan usaha Sensus Ekonomi 2026 **WAJIB LANGSUNG** bersumber dari database SurrealDB via script model `/app/workspaces/bps-mempawah/scripts/se2026_model.py` atau script kueri `/app/workspaces/bps-mempawah/scripts/query_surreal.py`.
- **Mekanisme Mirror Lokal Reliable (Anti-RTO & Offline-Ready)**:
  - Data di-mirror secara berkala/incremental ke database SQLite lokal `/app/shared_data/se2026_local.db` menggunakan script `/app/workspaces/bps-mempawah/scripts/sync_se2026_local.py sync --sls <sls>` atau `--desa <desa>`.
  - Kueri analitis cepat, filtering, dan audit dapat dieksekusi secara instan sub-milidetik dari mirror lokal (`python3 scripts/sync_se2026_local.py query "<SQL>"`).
- **DILARANG KERAS**: Mencari nama individu atau data survei ke Google Drive tim, membuka berkas PDF, Word, atau spreadsheet umum yang tidak relevan.
- **Pemetaan Tabel**:
  - `nested_dtsen_var`: Data level ART / individu (nama ART, ijazah, profesi, gaji pokok, tunjangan, dsb.).
  - `assignment`: Data level rumah tangga / bangunan (nama KK, alamat, RT/RW, koordinat latitude/longitude, total pendapatan keluarga).
  - `se2026_nested`: Data level unit usaha.
- **Timeboxing & Anti-Rabbit Hole**:
  - Jika kueri menghasilkan 0 record, langsung laporkan bahwa data tidak ditemukan.
  - Dilarang memperpanjang pencarian ke berkas-berkas eksternal tanpa instruksi eksplisit.

## 4. SOP Pengingat Otomatis Agenda / Undangan Rapat & Zoom (H-30 Menit)
- **Pemicu**: Menerima informasi/undangan kegiatan rapat virtual (Zoom, Google Meet, Webinar, dll.) dengan tanggal dan jam tertentu.
- **Aksi Wajib**: Selalu daftarkan pengingat (*reminder*) otomatis tepat **30 menit sebelum jam acara dimulai** menggunakan sistem pengingat / penjadwal aktif (`aina schedule add` atau scheduler terkait).
- **Target Pengingat**: Bang Ihza Karunia (`6289625345646@s.whatsapp.net`) dan/atau grup kerja terkait.
- **Konten Pengingat**: Nama agenda, waktu pelaksanaan, tautan/link Zoom, Meeting ID, dan Passcode agar siap langsung bergabung tanpa mencari-cari lagi.

## 5. SOP Penomoran & Registrasi Surat Keluar Dinas BPS Kabupaten Mempawah
- **Buku Agenda Penomoran Resmi**: Setiap pembuatan surat keluar resmi dari BPS Kabupaten Mempawah **WAJIB** mengambil/mem-booking nomor surat dari Google Spreadsheet Buku Agenda Surat BPS Mempawah:
  * URL: `https://docs.google.com/spreadsheets/d/1kbvTnpEwlyt6HbtIlD7at-Eg7zgTUt7GUHP9uJx2wgA/edit?usp=drivesdk`
  * Sheet Target: `Surat Keluar 2026` (atau sesuai tahun naskah dinas)
- **Struktur Format Nomor Surat BPS**:
  `B-[Nomor Urut]/[Kode Satker]/[Kode Klasifikasi Arsip]/[Bulan (opsional)]/[Tahun]`
  * `B-`: Sifat naskah dinas biasa
  * `[Nomor Urut]`: Running number berurutan dari baris terakhir terisi pada kolom `Nomor Surat`
  * `[Kode Satker]`:
    - `61040`: Pimpinan / Kepala BPS Kabupaten Mempawah
    - `61041`: Subbagian Umum / Tata Usaha
    - `61042`: Statistik Sosial
    - `61043`: Statistik Produksi
    - `61044`: Statistik Distribusi
    - `61045`: Neraca Wilayah dan Analisis Statistik (Nerwilis)
    - `61046`: Integrasi Pengolahan dan Diseminasi Statistik (IPDS)
  * `[Kode Klasifikasi Arsip]`: Mengacu pada tab sheet `Klasifikasi` / `Klasifikasi_1` (misal `SS.190` untuk Koordinasi Sensus, `HM.310` untuk Permintaan Data/Publikasi, `VS.220` untuk Pelatihan Survei, `KS.200` untuk Rilis Publikasi, dsb.).
  * `[Tahun]`: Tahun naskah dinas (misal `2026`).
- **Alur Penomoran**:
  1. Akses spreadsheet `Agenda Surat BPS Mempawah` (`1kbvTnpEwlyt6HbtIlD7at-Eg7zgTUt7GUHP9uJx2wgA`).
  2. Buka tab `Surat Keluar <Tahun>` (misal `Surat Keluar 2026`).
  3. Cari baris paling akhir yang terisi di kolom C (`Nomor Surat`).
  4. Ambil nomor urut berikutnya (misal nomor terakhir 1107 -> nomor baru 1108).
  5. Booking baris baru tersebut dengan mengisi: Tanggal Surat, Nomor Surat lengkap, Perihal, Tujuan, Pembuat (Tim Kerja), dan Nama File/Lampiran.
  6. Cantumkan nomor resmi tersebut pada naskah surat dan lampiran.

### 6. Standar Layout & Format Kop Surat Dinas Keluar BPS Kabupaten Mempawah
Seluruh pembuatan surat dinas/surat keluar BPS Kabupaten Mempawah (untuk konteks kegiatan apapun) wajib mematuhi standar layout berikut:
- **Komposisi Kolom Kop**:
  * **Logo Kiri**: Logo resmi BPS (lebar ~54pt s.d. 60px).
  * **Teks Instansi & Alamat**: Berada di sebelah kanan logo BPS dengan jarak proporsional (*gutter / left padding* ~12–14px), format **rata kiri (*left-aligned*)**:
    - `BADAN PUSAT STATISTIK` (13pt, **Bold**, *Italic*, warna navy `#0a2540`).
    - `KABUPATEN MEMPAWAH` (13pt, **Bold**, *Italic*, warna navy `#0a2540`).
    - Alamat instansi, telepon, laman web, dan email resmi (8pt, regular, warna `#222222`).
  * **Logo Kanan**: Logo kegiatan spesifik (misal Logo SE2026 ~86pt) atau dikosongkan untuk surat umum.
- **Garis Pembatas Kop**: Garis horizontal 2pt warna navy `#0a2540` membentang 100% lebar halaman.
- **Tanda Tangan Resmi**: Ditandatangani oleh Kepala BPS Kabupaten Mempawah (Munawir, S.E., M.M.).

## 7. SOP Pengingat Presensi Harian BPS (Akhir Bulan)
- **Aturan Disiplin Presensi**: Pada setiap hari terakhir hari kerja di bulan berjalan, seluruh pegawai/staf wajib memastikan aplikasi Presensi BPS berstatus bersih tanpa ada status **"tanpa kabar" (TK)** atau **"terlambat" (TL)** yang menggantung.
- **Tindak Lanjut Administrasi**: Jika terdapat pegawai yang sakit, cuti, atau sedang tugas lapangan/dinas luar (SPD/Surat Tugas), seluruh berkas administrasi dan approval atasan langsung harus sudah tuntas di sistem sebelum *cut-off* perhitungan kehadiran bulanan dan tunjangan kinerja.
- **Otomasi Pengingat**: Sistem Aina otomatis memasukkan pengingat ini ke dalam ringkasan briefing deadline harian dan memberikan alert khusus menjelang penutupan hari kerja terakhir setiap bulan.


