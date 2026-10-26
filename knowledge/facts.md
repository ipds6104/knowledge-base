# 💡 Fakta & Parameter Umum: Workspace Default

*Dokumentasikan fakta penting, konfigurasi sistem umum, dan catatan harian di sini.*

- **Sistem**: Aina asisten mandiri berbasis Rust & Google Antigravity CLI.
- **Filosofi Nama Aina**: Diberikan oleh Bang Ihza Karunia. Berasal dari bahasa Arab "عَيْن" (Mata) yang melambangkan penglihatan jeli, cermat, dan teliti dalam mengolah data serta memperhatikan kebutuhan tim. Sekaligus singkatan/akronim dari "AI Native".
- **Foto Profil Aina**: Digenerate menggunakan Meta AI oleh Bang Ihza Karunia.
- **Zona Waktu**: Asia/Jakarta (WIB, UTC+7).
- **Aturan Pengingat Rapat/Zoom**: Otomatis pasang jadwal pengingat (*reminder*) 30 menit sebelum jam mulai untuk setiap undangan/info rapat Zoom/online (instruksi Bang Ihza Karunia pada 22 September 2026).
- **Indikator Kemiskinan Kab. Mempawah (BPS 6104)**:
  - Sumber: Spreadsheet Indikator Strategis BPS Mempawah (`s.bps.go.id/indikator_strategis6104`).
  - Tahun 2025: Persentase (P0) = 4,49%, Jumlah Penduduk Miskin = 12,38 ribu jiwa, Garis Kemiskinan = Rp 494.531,-, P1 = 0,47, P2 = 0,09.
  - Tahun 2024: Persentase (P0) = 4,83%, Jumlah Penduduk Miskin = 13,22 ribu jiwa, Garis Kemiskinan = Rp 471.845,-, P1 = 0,49, P2 = 0,09.
  - Tahun 2023: Persentase (P0) = 5,21%, Jumlah Penduduk Miskin = 14,15 ribu jiwa, Garis Kemiskinan = Rp 444.790,-, P1 = 0,51, P2 = 0,07.


## Indikator Strategis Makro Kabupaten Mempawah (s.bps.go.id/indikator_strategis6104)
- **Persentase Kemiskinan**:
  - 2023: 5,21%
  - 2024: 4,83% (turun 0,38%)
  - 2025: 4,49% (turun 0,34%)
- **IPM**: 2023: 68,91 | 2024: 69,63 | 2025: 70,59
- **Tingkat Pengangguran Terbuka (TPT)**: 2023: 7,33% | 2024: 6,78% | 2025: 4,74%
- **Pertumbuhan Ekonomi (y-o-y)**: 2023: 5,09% | 2024: 6,62% | 2025: 8,24%
- **Gini Ratio**: 2023: 0,291 | 2024: 0,254 | 2025: 0,257

## Sensus Ekonomi 2026 (SE2026) - Audit Matching Prelist DTSEN ke Regsosek CETAR
- **Konteks**: Prelist DTSEN desil rendah (< 7) yang berstatus tidak ditemukan di manapun di Kalbar.
- **Data Makro**: 7.509 KK di tingkat provinsi tidak ditemukan; setelah filter koordinasi dengan IPDS Provinsi diperoleh 6.662 KK.
- **Validasi Spasial CETAR**: Dari 6.662 KK tersebut, terdapat **1.839 KK** yang memiliki titik koordinat di database CETAR.
- **Rincian Catatan Petugas di CAPI/Fasih (6.662 KK)**:
  - 1.810 KK (27,2%): Catatan kosong di CAPI (hanya klik opsi STOP).
  - 162 KK (2,4%): Catatan tautologi (hanya menulis teks "tidak ada/nihil").
  - 2.269 KK (34,1%): Keterangan pindah domisili / merantau.
  - 626 KK (9,4%): Keterangan bukan warga / tidak dikenal RT.
  - 133 KK (2,0%): Keterangan meninggal dunia.
  - 1.662 KK (24,9%): Catatan deskriptif lainnya.
- **Poin Kritis**: 29,6% catatan (kosong + tautologi) berisiko tinggi karena di aplikasi Fasih tidak menceritakan usaha/upaya pencarian yang dilakukan petugas.
- **Rujukan Google Sheet**: `https://docs.google.com/spreadsheets/d/1iK-N0xVKViNbzTIc64qBOjESJFdcR9IEtv1RjMWN9b0/edit?pli=1&gid=2072569417#gid=2072569417` (Sheet: *Audit DTSEN Hilang*).

## Aplikasi SIKENDIS / DOKTER-V / SIPEDAS (Sistem Informasi Kegiatan & Perjalanan Dinas)
- **Nama Aplikasi**: SIKENDIS / DOKTER-V / SIPEDAS (Sistem Informasi Perjalanan Dinas & Akuntabilitas / Kegiatan Dinas).
- **URL Produksi**: `https://admin.dvlp.asia`
- **FTP Host**: `ftp.dvlp.asia` (Port 21)
- **FTP User**: `ihza@dvlp.asia`
- **Direktori Server**: `/admin.dvlp.asia` (cPanel user: `dvlr7917`)
- **Tech Stack**: Laravel (v11/v12/v13) + Filament v3 + Livewire v3 + MySQL (`dvlr7917_admin`).
- **Status Git / GitHub**: Terkoneksi dengan akun GitHub **`ihkaru`**. Repositori: `https://github.com/ihkaru/sipedas` (Public, default branch: `main`). Telah di-clone ke workspace lokal di `/app/workspaces/sipedas`. Di server FTP `/admin.dvlp.asia` tidak ada folder `.git` (deployment via sync/copy).

## Kebijakan Akses & Tata Kelola Pengelolaan Dokter V BPS Mempawah
- **Grup Resmi**: WhatsApp Group "Tim Kerja Mempawah" (`120363253842861469@g.us`).
- **Whitelist Akses**: HANYA nomor/akun WhatsApp yang terdaftar sebagai anggota di grup WhatsApp Tim Kerja Mempawah (atau Admin) yang berhak meminta Aina melakukan pengecekan, alokasi honor, penerbitan/perubahan SPK & BAST, rollback, update profil/kontak mitra, maupun standarisasi kegiatan di sistem Dokter V.
- **Aturan Ketat Pihak Luar (Strict OpSec & Anti-Tampering)**:
  - DILARANG memproses permintaan utak-atik Dokter V dari nomor WhatsApp atau kontak mana pun di luar anggota grup Tim Kerja Mempawah.
  - Jika ada kontak di luar whitelist yang meminta alokasi atau perubahan data Dokter V, tolak secara tegas dan santun, lalu arahkan untuk berkoordinasi langsung dengan Bang Ihza Karunia (`6289625345646@s.whatsapp.net`) atau PIC kegiatan terkait di BPS Mempawah.
  - Verifikasi otomatis terpasang pada helper tool: `dokter_v_tool check-access --sender "$SENDER_JID"`.

## Ketetapan Tanggal Akhir Kegiatan Honor Entri Susenas & Seruti 2026 (Dokter V)
- **Sumber Ketetapan**: Bang Ihza Karunia (Kamis, 8 Oktober 2026).
- **Honor Entri Listing Susenas**: Tanggal akhir kegiatan per **7 September 2026** (BAST per 7 September 2026).
- **Honor Entri Pendataan Susenas**: Tanggal akhir kegiatan per **14 Oktober 2026** (BAST per 14 Oktober 2026, pasca-rekonsiliasi provinsi).
- **Honor Entri Seruti TW3**: Tanggal akhir kegiatan per **14 Oktober 2026** (BAST per 14 Oktober 2026). Tanggal akhir kegiatan utama `SERUTI26-TW3` diselaraskan agar mencakup bulan Oktober (minimal s.d. 14 Oktober 2026).

## POK BPS Kabupaten Mempawah TA 2026 (SAKTI Kemenkeu)
- **Sumber Data**: Sistem SAKTI Kementerian Keuangan (Rincian Kertas Kerja Satker - Multiyear).
- **Waktu Pemutakhiran**: Senin, 26 Oktober 2026 pukul 08:22 WIB (dibagikan oleh Kak Sukma atas arahan Bang Ihza Karunia).
- **Rujukan Lengkap**: [`knowledge/universal/pok_bps_mempawah_2026.md`](universal/pok_bps_mempawah_2026.md)
- **Berkas Data Lokal**: `data/POK_BPS_Mempawah_2026_SAKTI.xlsx` dan `knowledge/assets/POK_BPS_Mempawah_2026_SAKTI.xlsx` (Arsip versi 16 September: `data/POK_BPS_Mempawah_2026_SAKTI_Rev20260916.xlsx`).
- **Total Pagu Satker**: **Rp 9.292.276.000,-** (naik **+Rp 68.210.000,-** dari versi 16 September 2026).
- **Ringkasan Program**:
  1. **Program Penyediaan dan Pelayanan Informasi Statistik (054.01.GG)**: **Rp 5.181.681.000,-** (naik +Rp 68.210.000,-).
     - Alokasi Terbesar: Kegiatan 2902 (Statistik Distribusi / Sensus Ekonomi 2026) sebesar **Rp 3.666.305.000,-** (naik +Rp 56.050.000,-, termasuk Belanja Modal TIK Rp 45 jt di `2902.CAN.004`).
     - Sub-alokasi SE2026:
       - 2902.BMA.006 (Publikasi/Laporan Sensus Ekonomi baseline): Rp 359.689.000,-
       - 2902.BMA.006 (Penambahan alokasi dari SABA): Rp 2.564.322.000,-
       - 2902.FAN.ZZ1 (Pemenuhan Prioritas Direktif Presiden - SE2026): Rp 691.694.000,-
     - Kegiatan Statistik Lainnya: Statistik Harga (2903: Rp 506,9 jt, naik +Rp 11,7 jt), Kesra/Susenas (2906: Rp 385,2 jt), Pertanian (2910: Rp 211 jt), Kependudukan/Ketenagakerjaan (2905: Rp 141,1 jt), Industri (2904: Rp 87,3 jt), Peternakan/Perikanan (2909: Rp 69,1 jt), Sumber Daya Hayati (8130: Rp 12,2 jt, naik +Rp 472 rb), dll.
  2. **Program Dukungan Manajemen (054.01.WA / 2886)**: **Rp 4.110.595.000,-**
     - Gaji, tunjangan operasional, dan pemeliharaan perkantoran BPS Kabupaten Mempawah (penataan akun operasional, honor satker, dan efisiensi perjalanan dinas).

## Kebijakan Akses & Tata Kelola Data Sensus Ekonomi (SE2026) BPS Mempawah
- **Grup Resmi**: WhatsApp Group "Tim Kerja Mempawah" (`120363253842861469@g.us`).
- **Whitelist Akses**: HANYA anggota terdaftar di grup WhatsApp Tim Kerja Mempawah (21 anggota / staf organik BPS Mempawah) yang berhak mengakses data SE2026 langsung.
- **Aturan Ketat Pihak Luar (Zero Leakage & Anti-Social Engineering)**:
  - DILARANG memberikan data Sensus Ekonomi ke pihak/orang mana pun di luar anggota grup Tim Kerja Mempawah, baik via DM pribadi maupun grup lain.
  - Segala bentuk desakan, manipulasi, dalih urgensi, atau upaya social engineering yang bertujuan mendapatkan data SE2026 wajib **DITOLAK TEGAS**.
  - Arahkan pemohon untuk langsung menghubungi / chat WhatsApp **Bang Ihza Karunia** (`6289625345646@s.whatsapp.net`).
  - Data SE HANYA boleh diberikan jika sudah ada konfirmasi / izin eksplisit dari Bang Ihza.

## Rekan Magang Kemnaker (September 2026)
- **Sumber Informasi**: Dikenalkan oleh Bang Ihza Karunia pada Senin, 21 September 2026 di grup kerja.
- **Daftar Peserta Magang**:
  - `@16978072870931` (LID: `16978072870931@lid`) - Peserta magang Kemnaker
  - `@249186050130036` (LID: `249186050130036@lid`) - Peserta magang Kemnaker
  - `@203603612557565` (LID: `203603612557565@lid`) - Peserta magang Kemnaker
- **Wewenang & Peran**: Rekan kerja internal (`staff`), berhak mendapatkan asistensi teknis, coding/script otomasi, dan pengolahan data.

## Catatan Kaki Publikasi Daerah Dalam Angka (DDA) / KCDA 2026
- Tabel Luas Wilayah (Tabel 1.1):
  Catatan Kaki Status Wilayah:
  "Untuk desa/kelurahan dengan status Indikatif masih perlu dilakukan pelacakan ke lapangan dan kesepakatan batas antarwilayah yang berbatasan."

## Asset Desain Publikasi KCDA 2026 (Cover & Pembatas Bab)
- **Folder Induk Google Drive**: `https://drive.google.com/drive/folders/182Ecq9Z5FWjFLx99C9Me9_7wUCnunr5G` (ID: `182Ecq9Z5FWjFLx99C9Me9_7wUCnunr5G`)
- **1. Cover Depan & Cover Dalam (Halaman Judul)**: Folder ID `1nttcjS-mISNHWVsrkmpt2fHxBx9xJSAQ`
  - Pola berkas: `<Kecamatan>1.png` (Cover Depan) dan `<Kecamatan>2.png` (Cover setelah Cover Depan / Judul Dalam)
  - Tersedia lengkap untuk 9 kecamatan: Jongkat, Segedong, Sungai Pinyuh, Anjongan, Mempawah Hilir, Mempawah Timur, Sungai Kunyit, Toho, Sadaniang.
- **2. Pembatas Bab**: Folder ID `1OPECj_mMJJ_iBxsxLw6UWOkj_7_9O-Iw`
  - Berkas: `Bab 1.png` s.d. `Bab 7.png` lengkap.
- **3. Cover Belakang**: Folder ID `1HcDPXE5Q-kGc3mD-BOKVV11IznuHXaW1`
  - Pola berkas: `<Kecamatan>.png`
  - Tersedia lengkap untuk seluruh 9 kecamatan.

## Tabel 2.1.5 & 2.1.6 KCDA 2026 (Pemerintahan)
- **Tabel 2.1.5 (Klasifikasi Desa/Kelurahan Perdesaan dan Perkotaan di Kecamatan XXX, 2024)**:
  - Tahun Data: **2024** (disamakan dengan KCDA tahun sebelumnya / Perka BPS No 120 Tahun 2020).
  - Spreadsheet GDrive: `https://docs.google.com/spreadsheets/d/1mv1gRkm6lQl97LS4G08g5mKnApvmvsP7QzhTZ_7hpnQ/edit?usp=sharing`
  - Telah diisi lengkap untuk 9 kecamatan (Mempawah Hilir, Toho, Sungai Pinyuh, Jongkat, Sungai Kunyit, Segedong, Sadaniang, Anjongan, Mempawah Timur).
- **Tabel 2.1.6 (Status Desa berdasarkan Indeks Desa Membangun di Kecamatan XXX, 2024)**:
  - Tahun Data: **2024** (disamakan dengan KCDA tahun sebelumnya / Rekomendasi IDM Kalbar 2023).
  - Spreadsheet GDrive: `https://docs.google.com/spreadsheets/d/1qdrqJe5xgh2JW0A1RiIQdHgSSawMMdcNXZpsnSNE9EU/edit?usp=sharing`
  - Header tahun diupdate menjadi `2024` dan seluruh status per desa/kelurahan telah diisi lengkap untuk 9 kecamatan.
- **Monitoring Master KCDA 2026**:
  - Spreadsheet `1vVNdy6uOlMWrvXdD0ZZzoRKik85oMKAhAX7rvqFci18` (Tab `Tabel Mempawah 2026`): Tahun data pada kolom C untuk baris Tabel 2.1.5 dan 2.1.6 telah disesuaikan menjadi **2024**, dan link spreadsheet 2.1.5 telah dicantumkan di kolom E.

## Inventarisasi Data Sementara & Baseline Estimasi (Perlu Penyempurnaan Kedepan)

*Dicatat pada 22 September 2026 atas arahan Bang Ihza Karunia.*

### 1. Pemadanan & Analisis Pendapatan Pejabat Pemda (SE2026)
- **1.420 NIK Berstatus "Tidak Ditemukan" (27,8%)**:
  - *Saat ini*: Dibatasi hanya pencarian di database SE2026 BPS Kab. Mempawah.
  - *Ideal*: Pemadanan lintas satker/kabupaten se-Kalbar (khususnya Pontianak & Kubu Raya karena faktor komuter/domisili) serta crosscheck prelist susulan.
- **Catatan Petugas Lapangan (PPL)**:
  - *Saat ini*: Diambil dari `assignment.root_catatan` (catatan level keluarga/bangunan sensus), bukan catatan spesifik per individu pejabat.
  - *Ideal*: Konfirmasi wawancara langsung ke PPL/PML apakah diisi sendiri oleh ASN bersangkutan atau via proxy/ART lain.
- **Petugas Pencacah (PPL)**:
  - *Saat ini*: Mengambil `current_user_username` (akun penugasan sistem terakhir).
  - *Ideal*: Sinkronisasi dengan master SK/alokasi PPL awal bila ada reassignment lapangan.
- **Klasifikasi Status Anomali Pendapatan**:
  - *Saat ini*: Menggunakan ambang batas heuristik (0/tidak bekerja, <1 jt, >100 jt).
  - *Ideal*: Verifikasi status kepegawaian ke BKPSDM (cuti di luar tanggungan negara, tugas belajar, pensiun, dll.).
- **Master List Pejabat Sheet 6104**:
  - *Saat ini*: Snapshot Excel statis per awal tahun.
  - *Ideal*: Sinkronisasi berkala mutasi/promosi ASN terkini dari BPKAD/BKPSDM.

### 2. Estimasi Gaji & Tunjangan ASN Pemda Mempawah
- **Gaji Pokok**:
  - *Saat ini*: Asumsi tabel PP 5/2024 dan Perpres 11/2024 dengan MKG awal / estimasi NIP TMT CPNS.
  - *Ideal*: Master payroll riil BPKAD (memperhitungkan SK KGB & pangkat riil).
- **Tunjangan & TPP**:
  - *Saat ini*: Baru estimasi tunjangan umum dan uang makan standar.
  - *Ideal*: Mengintegrasikan TPP (Tambahan Penghasilan Pegawai) riil Pemda Mempawah sesuai Perbup (kelas jabatan, presensi), tunjangan jabatan fungsional/struktural, dan tunjangan keluarga riil.
- **Non-ASN**:
  - *Saat ini*: Dipatok flat standar UMK Mempawah (Rp 2.704.337,-).
  - *Ideal*: Nilai riil DPA/kontrak per OPD.

### 3. Publikasi KCDA 2026 (Kecamatan Dalam Angka) & DDA
- **Luas Wilayah (Tabel 1.1)**:
  - *Saat ini*: Masih terdapat desa/kelurahan berstatus batas "Indikatif".
  - *Ideal*: Penetapan batas definitif desa berdasarkan Permendagri/Perbup terbaru.
- **Data Pendidikan (Bab 4 - Kemendikbud & Kemenag)**:
  - *Saat ini*: Scraping data portal/agregasi semester berjalan.
  - *Ideal*: Berita Acara Rekonsiliasi Satu Data bersama Disdikbud dan Kemenag Mempawah.
- **Fasilitas & Potensi Desa (Bab 4 & 5 - Podes)**:
  - *Saat ini*: Ekstraksi OCR/Vision VLM dari publikasi Podes 2025.
  - *Ideal*: Menggunakan raw data mikro tabular Podes clean dari IPDS.
- **Status Desa & IDM (Tabel 2.1.5 & 2.1.6)**:
  - *Saat ini*: Menggunakan baseline tahun 2024.
  - *Ideal*: Rilis penetapan status IDM definitif Kemendesa tahun berjalan.

## Status Penyelesaian Publikasi KCDA 2026 (9 Kecamatan)
- **Status Upload Web / ARC**: **SELESAI (100%)** per Rabu, 23 September 2026 (dikonfirmasi oleh Bang Ihza Karunia). Seluruh file publikasi KCDA 2026 untuk 9 kecamatan di Kabupaten Mempawah telah tuntas diunggah ke sistem ARC portal web BPS.
- **Fase Quality Control (QC) & Koreksi Ulang (24–27 September 2026)**: Catatan penting dari Kak Sukma bahwa meskipun naskah sudah terunggah ke sistem ARC, seluruh publikasi KCDA 9 kecamatan tetap wajib diteliti dan dikoreksi ulang bersama sebelum tanggal rilis resmi.
- **Milestone Berikutnya**: Jadwal Rilis Resmi Publikasi di website BPS Kabupaten Mempawah pada **Senin, 28 September 2026**.

## Survei Kebutuhan Data (SKD) 2026 - Upload Portal SKM
- **Portal Unggah**: `https://skm.go.id/`
- **Batas Akhir (Deadline)**: **Rabu, 30 September 2026**
- **PIC / Sumber Catatan**: Kak Sukma (Staff IPDS Mempawah)
- **Keterangan**: Batas akhir pengunggahan laporan & hasil Survei Kebutuhan Data (SKD) BPS ke portal SKM (https://skm.go.id/).

## Transisi Infrastruktur TI SPBE BPS 2026 (Kamis AIS 24 September 2026)
- **PIC SPBE Satker 6104**: Ihza Karunia (IPDS BPS Kabupaten Mempawah).
- **Latar Belakang**: Peluncuran arsitektur TI baru oleh Direktorat SIS BPS RI pada Kamis AIS (24 Sep 2026) pasca insiden breach kredensial BSSN (15 Sep 2026).
- **Tiga Pilar Layanan Utama**:
  1. **SSO Baru (`accounts.bps.go.id`)**: Wajib 2FA Google Authenticator + Recovery Email non-BPS. Batas sosialisasi & aktivasi mandiri: **30 September 2026**. Peringatan: OTP lama jangan dihapus.
  2. **Email Zimbra Baru (`email.bps.go.id`)**: Cut-off per **1 Oktober 2026** (webmail lama jadi read-only di `archivemail.bps.go.id`). Kuota mailbox 1 GB. Ekspor backup arsip `.tgz` wajib sebelum **31 Desember 2026**. Fitur *Delegation* untuk email tim/seksi (stop password sharing).
  3. **VPN Global Protect (`vpn.bps.go.id`)**: Menggantikan FortiClient VPN. Download di `vpn.bps.go.id`. Tidak perlu aktif saat terhubung ke jaringan LAN/Wi-Fi kantor BPS yang sudah ber-SD-WAN. Batas transisi & role developer: **31 Oktober 2026**.
- **Hard Cut-Off**: **31 Desember 2026** (FortiClient VPN dimatikan total, server archivemail lama dihapus permanen, operasional 100% sistem baru per 1 Januari 2027).
- **Tautan Resmi**:
  - SSO: `https://accounts.bps.go.id` (Panduan: `https://s.bps.go.id/layanan-sso`)
  - Webmail Baru: `https://email.bps.go.id` | Arsip: `https://archivemail.bps.go.id` (Panduan: `https://s.bps.go.id/layanan-email`)
  - VPN: `https://vpn.bps.go.id` (Repo: `https://s.bps.go.id/repo-VPN`)
  - Evaluasi & Eskalasi: `https://s.bps.go.id/feedback-inka`

## Pengolahan Peta Wilkerstat SE2026 BPS Kabupaten Mempawah
- **Status Pelatihan Petugas Pengolahan Peta**: **SELESAI** per 25 September 2026.
- **Deadline Laporan & Administrasi Inda**: **SELESAI** per 8 Oktober 2026 (Berkas administrasi dan laporan Instruktur Daerah telah diselesaikan oleh Bang Ihza Karunia untuk proses pencairan honor).
- **Template Laporan Inda**: Tersimpan di `kegiatan/sensus-ekonomi-2026/2026/docs/template-laporan-inda-wilkerstat-se2026.md` dan `.docx`. Terdiri dari surat laporan ke Pusdiklat BPS serta 5 lampiran wajib (bahan ajar 4 slide, presensi harian mengajar, jadwal, notulensi/Q&A, dan foto dokumentasi).

## Perawatan Perangkat IT - Pelengkapan Aplikasi Mania TW 3 2026
- **Tenggat Waktu**: **Rabu, 30 September 2026** (akhir Triwulan 3 TA 2026).
- **PIC SPBE Satker 6104**: Ihza Karunia (IPDS BPS Kabupaten Mempawah).
- **5 Butir Kewajiban Aplikasi Mania**:
  1. *Update Status BMN TI*: Kondisi fisik/operasional perangkat (Baik/Rusak Ringan/Rusak Berat).
  2. *Update Alokasi BMN TI*: Penyesuaian pemegang unit (fitur masih belum aktif/tahap pengembangan).
  3. *Laporan Aset AB (Aset Berwujud) & ATB (Aset Tak Berwujud)*: Laporan mutasi/inventarisasi barang dan software/lisensi.
  4. *Upload Bukti Penggunaan Office 365*: Bukti riil pemanfaatan akun kedinasan (Word, Excel, Teams, OneDrive, Outlook).
  5. *Penamaan Host PC/Laptop Sesuai No BMN*: Standarisasi hostname PC/laptop kantor memuat nomor BMN.
- **Poin Kritis Evaluasi BPS Pusat**:
  - Banyak laporan TW 1 Aset AB & ATB yang belum disetujui (approval) Kepala Kantor.
  - Banyak bukti upload Office 365 ditolak pusat (pastikan screenshot valid dan menunjukkan akun BPS aktif).
  - Lisensi Office 365 berisiko ditarik pusat bila tidak aktif/tidak digunakan.
  - Himbauan mencicil dokumen di sela padatnya lapangan Sensus Ekonomi 2026 (SE2026).

## Target Kualitas Data Susenas September 2026 & SERUTI TW 3 2026
- **Tenggat Waktu**: **Rabu, 30 September 2026**.
- **Target Kualitas**:
  - **100% Clean Data Susenas September 2026**.
  - **100% Clean Data SERUTI Triwulan 3 2026**.
- **Keterangan**: Pembersihan dan validasi anomali/error data hasil pencacahan rumah tangga sampel pada sistem pengolahan/Fasih BPS Kabupaten Mempawah sebelum evaluasi kualitas data tingkat provinsi.

## Aturan Baku Presensi Harian BPS & Pengingat Akhir Bulan
- **Sumber Arahan**: Bang Ihza Karunia (Senin, 28 September 2026).
- **Aplikasi**: Presensi BPS (Portal Kehadiran Pegawai BPS RI).
- **Aturan Baku Akhir Bulan**: Pada setiap hari terakhir hari kerja di bulan berjalan, seluruh pegawai wajib memastikan tidak ada status **"tanpa kabar" (TK)** atau **"terlambat" (TL)** yang menggantung tanpa penyelesaian.
- **Tindak Lanjut & Administrasi**: Segala bentuk dinas luar, keterlambatan yang beralasan sah, sakit, cuti, atau penugasan lapangan harus sudah terunggah dan disetujui (approved) atasan sebelum cut-off perhitungan tunjangan kinerja (tukin) dan rekapitulasi kehadiran bulanan.
- **Mekanisme Pengingat**: Didaftarkan ke scheduler sistem dan masuk ke dalam rekap deadline mingguan/bulanan agar otomatis diingatkan menjelang penutupan hari kerja terakhir tiap bulan.

## Pengisian Kinerja Pegawai (KipApp) & SKP Triwulan III 2026
- **Aplikasi**: KipApp (Kinerja Pegawai Application) BPS RI.
- **Periode**: September 2026 (Triwulan III: Juli – September 2026).
- **Rentang Pengisian**: **28 September 2026 pukul 00.00 WIB s.d. 2 Oktober 2026 pukul 17.00 WIB**.
- **Jadwal Pembukaan Menu SPJ**: **3 Oktober 2026 pukul 00.00 WIB**.
- **Sasaran**: Seluruh pegawai ASN BPS Kabupaten Mempawah (@all).
- **Dokumentasi Kegiatan**: Tercatat dalam kegiatan terdedikasi di `kegiatan/kipapp/2026/README.md`.
- **Sumber Arahan**: Pengumuman resmi KipApp & instruksi Bang Ihza Karunia (Senin, 28 September 2026).

## Regenerasi & Sinkronisasi Publikasi KCDA 2026 (28 September 2026)
- **Status Draft PDF**: **SELESAI DIREGENERASI (100%)** pada 28 September 2026.
- **Tautan Folder Google Drive**: `3. Draft Publikasi` (`1l1rmVCaZay_1BTJOAMjkadHuAVof8GyJ`).
- **File PDF Siap Telaah**:
  1. Kecamatan Mempawah Hilir (89 halaman)
  2. Kecamatan Mempawah Timur (88 halaman)
  3. Kecamatan Sungai Pinyuh (89 halaman)
  4. Kecamatan Sungai Kunyit (89 halaman)
  5. Kecamatan Segedong (89 halaman)
  6. Kecamatan Toho (89 halaman)
  7. Kecamatan Jongkat (88 halaman)
  8. Kecamatan Anjongan (88 halaman)
  9. Kecamatan Sadaniang (89 halaman)
- **Poin Penyempurnaan yang Diterapkan**:
  - Penataan judul pada Daftar Isi (TOC) menjadi dua baris terpisah (Bahasa Indonesia di baris atas dan Bahasa Inggris di baris bawah).
  - Sinkronisasi Penjelasan Teknis 7 Bab merujuk pada format standar KCDA 2025.
  - Narasi Ulasan Dinamis terhubung langsung dengan tabel agregat (PNS, kepala desa, komoditas unggulan pertanian, fasilitas akomodasi, dan koperasi).
- **Langkah Selanjutnya**: Review dan penyesuaian/revisi isi tabel bersama tim (Mba Akma Batrisyia dkk.).

## Surat Dinas B-362 (FRS) & Penyesuaian Pengolahan Wilkerstat SE2026
- **Surat Dinas B-362/02300/VS.100/2026**:
  - Mengatur batas akhir perubahan Master di FRS (Format Rekapitulasi Spasial / FRS-MFDOnline) dan estimasi closing data lapangan SE2026 per **30 September 2026**.
  - Wajib memastikan seluruh usulan perubahan wilayah SLS (pemekaran, penggabungan, perubahan kode/nama) dari lapangan sudah diajukan dan disetujui di FRS-MFDOnline sebelum cut-off.
- **Penyesuaian Juknis Pengolahan Wilkerstat SE2026 (18 September 2026 - Dit. MMSD BPS RI)**:
  - **Fokus Titik Geotagging**: Pengolahan titik geotagging di BPS Kab/Kota HANYA dilakukan pada SLS/Sub-SLS yang mengalami perubahan batas (PSLS). SLS yang tidak berubah batas tidak perlu diedit titiknya.
  - **Simplifikasi Model QGIS**: Dipangkas menjadi hanya 2 model QGIS (`01 Identifikasi Titik.model3` dan `02 Pengecekan Titik.model3`).
  - **Muatan 100% Diambil Alih BPS Pusat**: BPS Kab/Kota tidak perlu menghitung muatan bangunan/usaha di QGIS. Pusat yang menghitung dan membandingkan 2026_1 vs 2025_2 secara agregat; daerah cukup mengonfirmasi daftar anomali yang diturunkan.
- **Milestone Pengolahan Pasca 30 September 2026**:
  - *01–12 Oktober*: Tahap awal Kab/Kota (scanning peta WB/WS sketsa lapangan, identifikasi PSLS, georeferencing, edit batas awal di layer 2025_2).
  - *01–09 Oktober*: Finalisasi transfer data Fasih, preprocessing, dan finalisasi Master 2026_1 di BPS Pusat.
  - *10–12 Oktober*: Pengunduhan data geotagging per kabupaten dari Geospatial System (GS).
  - *13 Oktober – 06 November*: Periode utama pengolahan QGIS Kab/Kota (running 2 model khusus PSLS).
  - *20 November 2026*: Batas akhir unggah peta digital ke Geospatial System.
  - *27 November 2026*: Batas akhir approval peta digital oleh BPS Provinsi.
  - *04 Desember 2026*: Batas akhir unggah peta geotagging hasil koreksi ke Geospatial System.
  - *18 Desember 2026*: Finalisasi Master Wilkerstat 2026 Semester 1 oleh BPS Pusat.
- **Kertas Kendali & Verifikasi PSLS SE2026 (Google Sheets Kolaboratif)**:
  - Tautan Spreadsheet: https://docs.google.com/spreadsheets/d/1XrnJEuJi5Se34K21j83S8VmcDlaMBXeO4O4EJ-2m6cY/edit?usp=sharing
  - Memuat 4 lembar kerja: `1. Kendali Verifikasi Berkas` (QC Visual Magang), `2. Draf Input FRS Online` (Bahan Baku Bang Ihza input FRS-MFDOnline), `3. Progres Per Kecamatan` (Rekapitulasi 9 kecamatan), dan `Panduan & SOP Verifikasi`.

## Penyesuaian & Koreksi Final Tabel Publikasi KCDA 2026 (05 Oktober 2026)
- **Status Publikasi**: Selesai direvisi dan seluruh berkas PDF (9 kecamatan) telah dikompilasi ulang serta diperbarui in-place di Google Drive (`1l1rmVCaZay_1BTJOAMjkadHuAVof8GyJ`).
- **Rincian Penyesuaian yang Diterapkan (Feedback Review Akma Batrisyia & Tim BPS)**:
  1. **Tabel 1.1 & 1.2**: Penyesuaian sumber, header dwibahasa, dan sinkronisasi data jarak/luas wilayah resmi.
  2. **Tabel 2.1.1**: Penambahan baris total kecamatan untuk seluruh 9 kecamatan sesuai Google Sheet master.
  3. **Tabel 2.1.4**: Penambahan tahun data 2025 pada judul dan TOC; dikecualikan untuk Mempawah Hilir & Sungai Pinyuh.
  4. **Tabel 2.2.1**: Penyesuaian rujukan bilingual pegawai pemerintah daerah, koreksi data Anjongan (8 laki-laki), serta penyesuaian baris kecamatan Toho (6 L, 2 P, 8 total).
  5. **Tabel 3.1**:
     - Sumber diubah menjadi `Dinas Kependudukan dan Pencatatan Sipil Kabupaten Mempawah/Population and Civil Registration Service of Mempawah Regency` (tanpa keterangan semester).
     - Judul disesuaikan menjadi `Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Desa/Kelurahan di Kecamatan [Nama], 2025` (ID) dan `Population, Percentage Distribution of Population, Population Density, and Population Sex Ratio by Villages/Subdistricts in [Nama] District, 2025` (EN).
     - Header kolom di halaman lanjutan diganti menjadi `Distribusi Penduduk / Population Distribution (%)`.
     - Baris terbawah dihapus kata "Total", menyisakan nama kecamatan saja (contoh: `Kecamatan Mempawah Hilir`).
  6. **Tabel 4.1.2**:
     - Sumber diperbarui menjadi 2 rujukan resmi: `¹ Kementerian Pendidikan Dasar dan Menengah; Sistem Data Pokok Pendidikan; data semester ganjil laporan sampai dengan 30 November` dan `² Kementerian Agama; EMIS; data semester genap laporan sampai dengan 30 Juni`.
     - Angka penanda 1 dan 2 pada kolom tingkat pendidikan diformat sebagai footnote superskrip (`¹`, `²`).
  7. **Tabel 4.1.3**:
     - Judul tabel dan TOC diubah menjadi `Jumlah Kepala Sekolah dan Pendidik Menurut Tingkat Pendidikan di Kecamatan [Nama], 2024/2025 dan 2025/2026` (ID) dan `Number of Headmasters and Teachers by Educational Level in [Nama] District, 2024/2025 dan 2025/2026` (EN).
     - Sumber diperbarui menjadi 2 rujukan resmi yang sama.
     - Angka 1 dan 2 pada kolom tingkat pendidikan diformat sebagai footnote superskrip, dan footnote nomor 3 dihapus bersih.
  8. **Tabel 4.1.4**:
     - Sumber diperbarui menjadi 2 rujukan resmi yang sama.
     - Angka 1 dan 2 pada kolom tingkat pendidikan diformat sebagai footnote superskrip.

## Penyesuaian KCDA 2026 Kecamatan Toho & Jongkat (06 Oktober 2026)
- **Sumber Arahan**: Kak Sukma (Staff IPDS BPS Mempawah).
- **Rincian Penyesuaian**:
  1. **Tabel 2.1.2 (Toho)**: 
     - Sinkronisasi data Camat terbaru dari Google Sheet (No. 20: `Bennidiktus, S.IP., M.AP` - Periode: `Oktober 2025 - saat ini`).
     - Judul tabel dan entri Daftar Tabel (TOC) disesuaikan menjadi tahun **2026** (`Nama-Nama Camat yang Pernah/Masih Menjabat di Kecamatan Toho, 2026`).
  2. **Tabel 2.1.3, 2.1.4, 2.2.1, dan 2.2.2 (Toho)**:
     - Seluruh sel data yang tidak tersedia diisi tanda titik tiga (`...`) sesuai notasi baku statistik BPS untuk data tidak tersedia.
     - Tabel 2.1.3: Kolom nama kepala desa untuk seluruh 8 desa diisi `...`.
     - Tabel 2.1.4: Kolom nama kepala dusun untuk seluruh 21 dusun diisi `...`.
     - Tabel 2.2.1: Baris Pemerintah Daerah Kecamatan Toho (Laki-laki, Perempuan, Jumlah) diisi `...`.
     - Tabel 2.2.2: Seluruh jenjang tingkat pendidikan PNS kecamatan diisi `...`.
  3. **Tabel 1.4 (Toho & Jongkat)**:
     - Baris "Makam Juang Mandor" dihapus pada publikasi Kecamatan Toho dan Kecamatan Jongkat, serta penomoran baris diselaraskan kembali secara berurutan.

## Penyesuaian Tabel 4.2.1 & Pengembangan Ulasan Naratif Seluruh Bab KCDA 2026 (06 Oktober 2026)
- **Sumber Arahan**: Kak Sukma (Staff IPDS BPS Mempawah).
- **Rincian Pekerjaan**:
  1. **Sinkronisasi Tabel 4.2.1**: Sinkronisasi data sarana kesehatan terbaru tahun 2025 untuk seluruh 9 kecamatan dari Google Sheet master ke `tabel_4_2_1_banyaknya_desa_kelurahan_yang.json`. Angka tahun 2025 (Rumah Sakit, Puskesmas rawat inap, Puskesmas tanpa rawat inap, Apotek) telah terisi data terbaru tanpa simbol placeholder `...` atau nilai 0.
  2. **Pengembangan Ulasan Naratif Bab 1 s.d. Bab 7 Seluruh Kecamatan**:
     - *Bab 1 (Geografi & Iklim)*: Menambahkan analisis aksesibilitas dan jarak antarwilayah (desa terjauh dan terdekat ke ibukota kecamatan dari Tabel 1.2 serta jarak kantor camat ke ibukota kabupaten dari Tabel 1.4).
     - *Bab 2 (Pemerintahan)*: Memperkaya ulasan dengan rekapitulasi status Indeks Desa Membangun (IDM: Mandiri, Maju, Berkembang) dan data aparatur sipil negara (PNS) dari Tabel 2.2.1.
     - *Bab 3 (Kependudukan)*: Memperkaya analisis kependudukan dengan rincian jumlah penduduk menurut jenis kelamin, rasio jenis kelamin, tingkat kepadatan antardesa, serta desa dengan konsentrasi penduduk terbesar dan terkecil.
     - *Bab 4 (Sosial & Kesejahteraan Rakyat)*: Memperbarui narasi fasilitas kesehatan secara dinamis merujuk Tabel 4.2.1 (keberadaan Rumah Sakit, Puskesmas rawat inap & non-rawat inap, serta Apotek) dan memperkaya ulasan pendidikan yang mencakup SD/MI, SMP/MTs, dan SMA/SMK/MA.
     - *Bab 5 (Pertanian)*: Mengembangkan ulasan hortikultura dengan ekstraksi komoditas unggulan 2025 (sayuran semusim, biofarmaka, buah tahunan) dengan penamaan dwibahasa yang rapi dan kontekstual.
     - *Bab 6 (Pariwisata, Transportasi & Komunikasi)*: Memperkaya ulasan akomodasi (hotel/penginapan), moda transportasi antardesa (darat vs air), dan sarana komunikasi/kantor pos/agen ekspedisi swasta.
     - *Bab 7 (Perbankan, Koperasi & Perdagangan)*: Menghadirkan ulasan perbankan dan koperasi aktif serta sarana perdagangan (pasar permanen/semi-permanen, kelompok pertokoan, minimarket).
  3. **Kompilasi & Pembaruan Google Drive**:
     - Seluruh 9 kecamatan berhasil dikompilasi ulang dengan Typst menjadi PDF resmi BPS.
     - Seluruh berkas PDF telah diperbarui secara in-place di Google Drive folder `1l1rmVCaZay_1BTJOAMjkadHuAVof8GyJ` menggunakan HTTP PATCH media sehingga File ID dan tautan view tetap terjaga.
  4. **Repositori Git**: Perubahan kode generator dan berkas tabel telah di-commit dan di-push ke GitHub repo `ipds6104/kcda-agent` (branch `main`).

## Pembaruan Angka Tabel 4.1.1 KCDA 2026 (07 Oktober 2026)
- **Status Publikasi**: Selesai diperbarui, dikompilasi ulang dengan Typst, dan disinkronkan langsung (_in-place_) ke Google Drive (`1l1rmVCaZay_1BTJOAMjkadHuAVof8GyJ`).
- **Rincian Perubahan**:
  - Mengupdate angka pada **Tabel 4.1.1** (_Banyaknya Desa/Kelurahan yang Memiliki Fasilitas Sekolah Menurut Tingkat Pendidikan, 2023–2025_) merujuk tabel bagian bawah (**"Template yang dipakai"**) pada spreadsheet master.
  - Pembaruan mencakup seluruh 9 kecamatan di Kabupaten Mempawah: Mempawah Hilir, Mempawah Timur, Sungai Pinyuh, Sungai Kunyit, Segedong, Toho, Jongkat, Anjongan, dan Sadaniang.
  - Nilai 2023, 2024, dan 2025 kini sepenuhnya selaras dengan angka template master.
  - Kode generator dan data tabel `data/raw_tables/tabel_4_1_1_banyaknya_desa1_kelurahan_yang.json` di `ipds6104/kcda-agent` telah disinkronkan dan di-push ke GitHub.

## Aset Tanda Tangan Digital Mitra & Pegawai BPS
- **Amalia Faisya** (Mitra Petugas Entri Susenas September 2026 & Seruti TW3 2026, ID Sobat: `610422100016`):
  - Format: PNG transparan bersih tanpa noise border/sudut (655x421 px).
  - Varian: Monokrom hitam (`ttd_amalia_faisya.png`, `ttd_amalia_faisya_hitam.png`) dan tinta biru (`ttd_amalia_faisya_biru.png`).
  - Lokasi Berkas:
    - Global Assets: `assets/ttd_amalia_faisya.png`
    - Knowledge Assets: `knowledge/assets/ttd_amalia_faisya.png`
    - Susenas September: `kegiatan/susenas-september/2026-09/assets/ttd_amalia_faisya.png`
    - Seruti TW3: `kegiatan/seruti-tw3/2026/assets/ttd_amalia_faisya.png`
- **Muhammad Deny Hafizzul Muttaqin** (Mitra Petugas Entri Susenas September 2026 & Seruti TW3 2026, ID Sobat: `617122110049`):
  - Format: PNG transparan bersih tanpa noise border/sudut (803x526 px).
  - Varian: Monokrom hitam (`ttd_muhammad_deny.png`, `ttd_deny_hafizzul.png`, `ttd_muhammad_deny_hitam.png`) dan tinta biru (`ttd_muhammad_deny_biru.png`).
  - Lokasi Berkas:
    - Global Assets: `assets/ttd_muhammad_deny.png`
    - Knowledge Assets: `knowledge/assets/ttd_muhammad_deny.png`
    - Susenas September: `kegiatan/susenas-september/2026-09/assets/ttd_muhammad_deny.png`
    - Seruti TW3: `kegiatan/seruti-tw3/2026/assets/ttd_muhammad_deny.png`
- **Putri Setia Ariani** (Mitra Petugas Entri Susenas September 2026 & Seruti TW3 2026, ID Sobat: `610422050003`):
  - Format: PNG transparan bersih tanpa noise border/sudut (440x361 px).
  - Varian: Monokrom hitam (`ttd_putri_setia.png`, `ttd_putri_setia_ariani.png`, `ttd_putri_setia_hitam.png`) dan tinta biru (`ttd_putri_setia_biru.png`).
  - Lokasi Berkas:
    - Global Assets: `assets/ttd_putri_setia.png`
    - Knowledge Assets: `knowledge/assets/ttd_putri_setia.png`
    - Susenas September: `kegiatan/susenas-september/2026-09/assets/ttd_putri_setia.png`
    - Seruti TW3: `kegiatan/seruti-tw3/2026/assets/ttd_putri_setia.png`
- **Ihza Fikri Zaki Karunia, S.Tr.Stat.** (Pranata Komputer Ahli Pertama BPS Mempawah):
  - Format: PNG transparan (biru/hitam).
  - Lokasi Berkas: `assets/ttd_ihza_karunia.png`, `assets/ttd_ihza_karunia_hitam.png`, `assets/ttd_ihza_karunia_biru.png`.

## Kebijakan Langkah Strategis Belanja K/L Triwulan IV TA 2026 (Kementerian Keuangan)
- **Sumber Regulasi**: Surat Menteri Keuangan Republik Indonesia hal Langkah Strategis Belanja K/L Triwulan IV TA 2026 dan Optimalisasi Belanja Akhir Tahun (penajaman Surat Menkeu S-89/MK.03/2026 dan S-292/MK.03/2026).
- **Tanggal Cut-Off Kebijakan**: **8 Oktober 2026**.
- **Poin Pokok Penghematan & Penundaan**:
  1. **Penghematan Perjalanan Dinas (Akun 524 & 525115) Sebesar 30%**:
     - Dikenakan pada sisa pagu perjalanan dinas yang belum diajukan SPM per 8 Oktober 2026.
     - Pertemuan dialihkan daring, pembatasan perjalanan non-prioritas, efisiensi frekuensi tanpa mengganggu target utama.
     - Pagu hasil penghematan dicatat pada **Halaman IV DIPA (blokir)** dengan kode **9 (*automatic adjustment*)**.
  2. **Penundaan Belanja Pendukung Aparatur (Non-Gaji & Layanan Dasar)**:
     - Berlaku untuk belanja yang belum ada perikatan/kontrak per 8 Oktober 2026:
       - Pengadaan kendaraan bermotor baru (Akun 532111)
       - Pembangunan/pengadaan rumah dinas baru (Akun 533121)
       - Renovasi/rehabilitasi gedung/kantor (Akun 523111 dan 533111)
     - Dicatat pada **Halaman IV DIPA (blokir)** dengan kode **9 (*automatic adjustment*)**.
  3. **Ketentuan Akhir Tahun Anggaran Lainnya**: Batas akhir revisi anggaran Kemenkeu, mekanisme Rekening Penampungan Akhir Tahun Anggaran (RPATA), pengawasan UP/TUP, alokasi sisa belanja barang & RO Khusus direktif Presiden, serta percepatan penyaluran DAK Nonfisik (PMK 119/2025).
- **Dokumentasi Lengkap**: Tersimpan di [`knowledge/langkah_strategis_belanja_tw4_2026.md`](langkah_strategis_belanja_tw4_2026.md).

## Pedoman Pemutakhiran Data Individu Manajemen Talenta ASN BPS (SIMPEG & GOJAGS)
- **Portal SIMPEG (`simpeg.bps.go.id`)**:
  - Penilaian Prestasi Kerja / SKP Tahun 2025.
  - SK Pelaksana Harian (Plh) / Pelaksana Tugas (Plt), jika ada.
  - SK Hukuman Disiplin tahun 2021 sampai sekarang, jika ada.
  - Penghargaan & Prestasi Individu (Pegawai Terbaik/IST, Latsar/Diklat Teknis, HKI, Publikasi Ilmiah/Best Paper, Prestasi TB, Juara Hackathon/Web Design/Infografis BPS/KL, Olahraga/Seni, hingga Penghargaan Tim WBK/Desa Cantik).
- **Portal GOJAGS (`gojags.bps.go.id`)**:
  - Sertifikat Diklat Fungsional / Diklat Penjenjangan (2021 s.d. sekarang).
  - Sertifikat Pelatihan & Pengembangan Kompetensi (2021 s.d. sekarang).
- **Dokumentasi Lengkap**: Tersimpan di [`kegiatan/kepegawaian/2026/manajemen-talenta-simpeg-gojags.md`](../kegiatan/kepegawaian/2026/manajemen-talenta-simpeg-gojags.md).

## Kosakata & Istilah Dialek Melayu Pontianak / Mempawah
- **Leter / Beleter / Kena Leter**: Kena omel / membebel / ngomel-ngomel (bukan "letter" bahasa Inggris yang artinya surat). Diajarkan oleh Kak Lina Agustin & Kak Syarifah Apriani pada 13 Oktober 2026.
- **Kamek**: Saya / kami.
- **Kitak**: Kamu / kalian.
- **Aok / Aok lah**: Iya / iya deh.
- **Cemane / Macam mane**: Bagaimana / seperti apa.
- **Lengkok**: Cengkok / intonasi / gaya bicara.

## Survei Pola Konsumsi Rumah Tangga (SPKRT) 2027 (15 Oktober 2026)
- **Dasar Surat**: Surat BPS Provinsi Kalimantan Barat Nomor `B-852/61000/VS.300/2026` tanggal 15 Oktober 2026 hal *Pemberitahuan Jadwal Pelaksanaan Lapangan Identifikasi Rumah Tangga dan Spesifikasi Instrumen SPKRT 2027* (menindaklanjuti Surat Direktur Statistik Harga BPS RI No. `B-217/06200/VS.300/2026` tgl 14 Oktober 2026).
- **Jadwal Pelaksanaan & Batas Akhir (Deadline)**:
  - **06 – 12 Desember 2026**: Pelaksanaan pendataan lapangan kegiatan **Identifikasi Rumah Tangga Sampel SPKRT 2027 Triwulan I**.
  - **Tahun 2027**: Pelaksanaan pencacahan lapangan berkala SPKRT 2027.
- **Tautan Resmi**:
  - Kuesioner siap cetak: http://s.bps.go.id/KuesionerSPKRT2027
  - Alokasi sampel dan kebutuhan perlengkapan petugas: http://s.bps.go.id/Alokasi_Petugas_Kues_SPKRT2027
- **Pengadaan Mandiri Satuan Kerja Daerah**:
  1. **Pencetakan Kuesioner (7 Jenis)**: VPKRT27-BL (A4 booklet 16/8 hal), VPKRT27-BLp (A5 lipat 2 karton biru 160 gr), VPKRT27-HR (A4 blok note 10 lbr samson lem panas), VPKRT27-HRp (A5 lipat 2 karton hijau 160 gr), VPKRT27-LK (A4 booklet 99/50 hal), VPKRT27-KK (A4 2/1 hal), dan VPKRT27-S (A4 booklet 84/42 hal).
  2. **Pengadaan Barang Lapangan**: Timbangan digital dapur (kapasitas 5 kg / 10 kg, ketelitian 1 gr, fitur tare/zero, layar LCD, daya baterai) dengan pagu harga satuan maksimal **Rp50.000,00 per unit** (termasuk pajak).
- **Lokasi Dokumentasi Knowledge Base**:
  - `kegiatan/spkrt-2027/2027/README.md`
  - Berkas surat & lampiran: `kegiatan/spkrt-2027/2027/docs/`

## SBR pasca Sensus Ekonomi 2026 (15 Oktober 2026)
- **Nama Kegiatan**: SBR pasca Sensus Ekonomi 2026
- **Pengawasan & Pelaksanaan**: Pengisian dokumen Non-Disclosure Agreement (NDA) diawasi oleh Kak Sukma, pencetakan dibantu oleh Dwi.
- **Deadline Kunci**:
  - **Jumat, 16 Oktober 2026**: Batas akhir pengisian, penandatanganan, dan upload dokumen NDA bagi seluruh tim organik SBR dan rekan magang.
- **Dokumentasi KB**: [`kegiatan/sbr-pasca-se2026/2026/README.md`](../kegiatan/sbr-pasca-se2026/2026/README.md).

## Kontak Layanan & Fasilitas Kantor BPS Kabupaten Mempawah
- **Laporan Keluhan WiFi / Internet IndiHome Kantor**:
  - **Nama Kontak**: Pak Benu Telkom
  - **Nomor HP / WhatsApp**: `+62 851-0555-5474` (`6285105555474@s.whatsapp.net`)
  - **Peran**: Teknisi / PIC Telkom untuk penanganan gangguan dan keluhan jaringan internet IndiHome kantor BPS Kabupaten Mempawah.
  - **Sumber**: Disimpan atas arahan Bang Ihza Karunia pada Senin, 19 Oktober 2026.

## Monitoring Kinerja Triwulan III Tahun 2026 BPS Kabupaten Mempawah (5 Oktober 2026)
- **Rapat**: Senin, 5 Oktober 2026 (08.00 – 12.00 WIB) di Ruang Rapat BPS Kabupaten Mempawah.
- **Pimpinan**: Kepala BPS Kabupaten Mempawah (Munawir, SE., MM.) | **Notulis**: Rifky Mullah Syadriawan.
- **Capaian Kinerja IKU Satker**:
  - Terhadap Target Triwulanan (TW III): **113,33%**
  - Terhadap Target Tahunan (PK 2026): **13,57%** (mayoritas publikasi selesai di TW IV)
- **Realisasi Keuangan s.d. Triwulan III**:
  - Pagu Awal DIPA 2026: Rp 5.948.099.000
  - Pagu Revisi s.d. TW III: Rp 9.290.958.000
  - Realisasi Belanja: **Rp 7.170.858.488** (**77,18%**)
  - Riwayat Revisi DIPA: Telah terlaksana s.d. **Revisi ke-12**
- **Efisiensi Kantor**: Penerapan 9 langkah efisiensi (listrik/air LED, in-house & hybrid training, efisiensi ATK/telepon, shutdown elektronik, rapat virtual, serta WFH rutin tiap hari Jumat berdasar Surat Sestama B-209/2026).
- **Rujukan Lengkap**: [`knowledge/universal/notula_monitoring_kinerja_tw3_2026.md`](universal/notula_monitoring_kinerja_tw3_2026.md) dan berkas PDF di [`knowledge/assets/Notula_Monitoring_Kinerja_Triwulan_III_BPS_Kabupaten_Mempawah.pdf`](assets/Notula_Monitoring_Kinerja_Triwulan_III_BPS_Kabupaten_Mempawah.pdf).

## Jadwal ARC Publikasi Statistik Kesejahteraan Rakyat Kabupaten Mempawah 2026 (21 Oktober 2026)
- **Nama Publikasi**: *Statistik Kesejahteraan Rakyat Kabupaten Mempawah 2026* (*Welfare Statistics of Mempawah Regency 2026*).
- **Status ARC**: Terdaftar di portal ARC web BPS (satu-satunya publikasi tersisa di antrean ARC per 21 Oktober 2026, dikonfirmasi oleh Kak Sukma & Bang Ihza).
- **Tenggat Waktu**:
  - **Batas Akhir Upload Naskah ke Portal ARC**: **1 Desember 2026** (Selasa).
  - **Jadwal Rilis Resmi**: **4 Desember 2026** (Jumat).
  - **Reminder Persiapan Upload (H-3 Kerja)**: **26 November 2026** (Kamis).
- **Rujukan Berkas**: [`kegiatan/publikasi-kesra-2026/2026/README.md`](../kegiatan/publikasi-kesra-2026/2026/README.md).

## SOP & Ketentuan Cleaning Data SE2026: Pemberian Remark & Tim Organik (21 Oktober 2026)
- **Arahan Pimpinan Terkait Pelaksana**:
  - Pimpinan BPS Provinsi Kalimantan Barat menegaskan bahwa proses cleaning data SE2026 **HANYA dilakukan oleh pegawai organik BPS** dan **DILARANG diserahkan kepada anak/mahasiswa magang**. Hal ini terkait kewajiban penandatanganan NDA (*Non-Disclosure Agreement*) dan perlindungan kerahasiaan data mikro sensus.
  - Urgensi: Capaian progres cleaning data SE2026 Provinsi Kalimantan Barat masih berada di bawah rata-rata nasional sehingga memerlukan percepatan serentak di seluruh satker kab/kota.
  - Setiap pemeriksaan dan perbaikan anomali data mikro **wajib diberikan Remark**.
- **Standar Format Kode Remark (Arahan Deputi NAS tanggal 15 Oktober 2026)**:
  Format penulisan kode remark resmi disederhanakan dari `#DC_00` s.d. `#DC_04` menjadi `#0` s.d. `#4`:
  - **`#0`** (sebelumnya `#DC_00`): *Data tidak mengalami perubahan* (Data dinyatakan sesuai kondisi lapangan, sehingga tidak dilakukan perubahan).
  - **`#1`** (sebelumnya `#DC_01`): *Data mengalami perubahan* (Perbaikan dilakukan karena kesalahan pemahaman petugas terhadap konsep atau kesalahan entri kuesioner).
  - **`#2`** (sebelumnya `#DC_02`): *Data mengalami perubahan* (Hasil konfirmasi/revisit langsung kepada responden).
  - **`#3`** (sebelumnya `#DC_03`): *Data mengalami perubahan* (Informasi yang bersumber dari survei rutin BPS lain atau data administrasi dinas/instansi).
  - **`#4`** (sebelumnya `#DC_04`): *Data mengalami perubahan* (Metode atau informasi lain selain kriteria kode #1, #2, dan #3).
  - *Catatan Retrospektif*: Kode lama yang sudah terlanjur diinput (`#DC_0x`) tetap berlaku sah dan tidak perlu diubah ulang. Untuk pengerjaan selanjutnya menggunakan kode baru `#0` s.d. `#4`.
- **Rujukan**: Dokumen surat resmi dan tangkapan layar di `media/AC32E2C46AA145CCC4B310F33C381861.jpg` dan `media/AC6060FF7383A27E9706E3BD5B5433DA.jpg`.

## Arsitektur Monitoring Cleaning Data SE2026 (Sheet `Mon Ini` & Tab Merah)
- **Tautan Spreadsheet**: [`Monitoring Cleaning Data SE 2026`](https://docs.google.com/spreadsheets/d/1EWoctuipZZgfERnqDLmvdDXdC1XiFtFB6Pbcw9U2rz0/edit?gid=104338933#gid=104338933).
- **Desain Tab `Mon Ini`**:
  - Dibuat untuk merekapitulasi beban target dan progres tindak lanjut cleaning per petugas pemeriksa/PJ.
  - Tab anomali yang dijadikan sumber data adalah tab-tab bertanda warna merah (*tabColor: red*):
    1. `rantab_dbnas` (Anomali rasio nilai tambah neraca)
    2. `rekap_usaha_A` (Rekapitulasi usaha sektor pertanian/A)
    3. `rekomendasi_kbli_anomali_layer2_18102026` (Anomali layer 2 per 18 Okt 2026)
    4. `rekomendasi_kbli_anomali_18102026` (Anomali KBLI layer 1 per 18 Okt 2026)
    5. `sosek_tabel19` (Tabel konsistensi sosial ekonomi)
  - Struktur Kolom Utama:
    - *Kolom A*: Nama Petugas
    - *Kolom B*: Progres Total Sudah Tindak Lanjut (%)
    - *Kolom C*: Jumlah Total Sudah Tindak Lanjut
    - *Kolom D*: Jumlah Total Target
    - *Kolom E–G, H–J, dst*: Pasangan metrik (*Sudah Tindak Lanjut*, *Target Tindak Lanjut*, *Progres Tindak Lanjut*) untuk masing-masing tab anomali merah.

## Intisari Sosialisasi Sistem Backend Website BPS Baru (21 Oktober 2026)
- **Waktu Pelaksanaan**: Rabu, 21 Oktober 2026 (08.00 – 12.00 WIB daring via LMS BPS).
- **Portal Backend Baru**: `https://web-be.apps.bps.go.id`.
- **Peserta BPS Kab. Mempawah**: Ihza Karunia & Akma Batrisyia.
- **Timeline & Jadwal Kunci (Hasil Transkrip Sosialisasi)**:
  - **Mulai Hari Ini (Rabu, 21 Oktober 2026)**: Backend baru sudah bisa mulai diakses dan digunakan satker untuk uji coba serta mencicil pairing metadata.
  - **Jumat Sore, 23 Oktober 2026 (Pukul 16.00 / 18.00 WIB)**: Batas akhir bagi daerah untuk mengunggah / memperbarui konten di sistem lama.
  - **Jumat Malam, 23 Oktober 2026 (Pukul 19.00 WIB)**: Akses backend lama (archive & webdesk) **DITUTUP TOTAL (CUT-OFF)** untuk proses migrasi database ke mesin/server baru oleh Tim Inka SIS BPS RI.
  - **Senin, 26 Oktober 2026**: Go-Live resmi Website BPS Versi 5.0 nasional. Backend lama tidak dapat diakses lagi dan seluruh satker wajib menggunakan sistem backend baru.
  - **Januari 2027**: Target konsistensi penuh pencatatan statistik pengunjung website di Webdash berbasis Google Analytics.
- **Poin Kunci Sistem**:
  - *Standardisasi Frontend*: Tampilan muka web publik seragam nasional (Sabang–Merauke). Seluruh kustomisasi konten daerah dikontrol lewat sistem *Backend*.
  - *Akses Terpusat*: Menggunakan akun Single Sign-On (SSO Baru BPS) teraktivasi dengan OTP pengaman.
  - *Manajemen Multi-Satker*: Memilih lingkup website berdasarkan kode MFD (misal Pusat `0000`, Provinsi Kalbar `6100`, Mempawah `6104`).
  - *Fitur Konten & Indikator*:
    - Master Indikator dengan interface sel mirip Excel (mendukung *copy-paste* langsung dari file Excel dan unduh template).
    - Tabel Statis dengan klasifikasi subjek statistik (CSA), mapping metadata SIMDASI, dan unggah berkas Excel.
    - Kolom *Headline* SEO-friendly untuk meningkatkan keterbacaan publik di mesin pencari dan media sosial tanpa merusak struktur judul baku rilis BPS.
- **Rujukan Lengkap**: [`kegiatan/sosialisasi-backend-website/2026/README.md`](../kegiatan/sosialisasi-backend-website/2026/README.md) dan salinan transkrip di [`knowledge/transkrip_zoom_backend.txt`](transkrip_zoom_backend.txt).



- **Laporan Keluhan WiFi / Internet Dukodu Kantor**:
  - **Nama Kontak**: Rim Teguh Sanjaya (Dukodu)
  - **Nomor HP / WhatsApp**: `+62 858-4913-3259` (`6285849133259@s.whatsapp.net`)
  - **Data Pelanggan FTTH Mempawah (Wajib dicantumkan saat menghubungi)**:
    - Paket/Layanan: Dukodu - Pelanggan FTTH Mempawah
    - Atas Nama: Rifky Mullah Syadriawan (`002003000992@dukodu.id`)
    - Kontak PIC: `0895704961475`
    - Alamat: Jl. Raden Kusno, kantor Badan Pusat Statistik
  - **SOP Penanganan Kendala Sebelum Lapor**: Coba colokkan ulang semua kabel + restart router terlebih dahulu. Jika masih belum normal, foto kondisi router lalu kirimkan ke kontak di atas beserta data pelanggan.
  - **Sumber**: Disimpan atas arahan Bang Ihza Karunia pada Senin, 19 Oktober 2026.

## Monitoring Kinerja Triwulan III Tahun 2026 BPS Kabupaten Mempawah (5 Oktober 2026)
- **Rapat**: Senin, 5 Oktober 2026 (08.00 – 12.00 WIB) di Ruang Rapat BPS Kabupaten Mempawah.
- **Pimpinan**: Kepala BPS Kabupaten Mempawah (Munawir, SE., MM.) | **Notulis**: Rifky Mullah Syadriawan.
- **Capaian Kinerja IKU Satker**:
  - Terhadap Target Triwulanan (TW III): **113,33%**
  - Terhadap Target Tahunan (PK 2026): **13,57%** (mayoritas publikasi selesai di TW IV)
- **Realisasi Keuangan s.d. Triwulan III**:
  - Pagu Awal DIPA 2026: Rp 5.948.099.000
  - Pagu Revisi s.d. TW III: Rp 9.290.958.000
  - Realisasi Belanja: **Rp 7.170.858.488** (**77,18%**)
  - Riwayat Revisi DIPA: Telah terlaksana s.d. **Revisi ke-12**
- **Efisiensi Kantor**: Penerapan 9 langkah efisiensi (listrik/air LED, in-house & hybrid training, efisiensi ATK/telepon, shutdown elektronik, rapat virtual, serta WFH rutin tiap hari Jumat berdasar Surat Sestama B-209/2026).
- **Rujukan Lengkap**: [`knowledge/universal/notula_monitoring_kinerja_tw3_2026.md`](universal/notula_monitoring_kinerja_tw3_2026.md) dan berkas PDF di [`knowledge/assets/Notula_Monitoring_Kinerja_Triwulan_III_BPS_Kabupaten_Mempawah.pdf`](assets/Notula_Monitoring_Kinerja_Triwulan_III_BPS_Kabupaten_Mempawah.pdf).

## Jadwal ARC Publikasi Statistik Kesejahteraan Rakyat Kabupaten Mempawah 2026 (21 Oktober 2026)
- **Nama Publikasi**: *Statistik Kesejahteraan Rakyat Kabupaten Mempawah 2026* (*Welfare Statistics of Mempawah Regency 2026*).
- **Status ARC**: Terdaftar di portal ARC web BPS (satu-satunya publikasi tersisa di antrean ARC per 21 Oktober 2026, dikonfirmasi oleh Kak Sukma & Bang Ihza).
- **Tenggat Waktu**:
  - **Batas Akhir Upload Naskah ke Portal ARC**: **1 Desember 2026** (Selasa).
  - **Jadwal Rilis Resmi**: **4 Desember 2026** (Jumat).
  - **Reminder Persiapan Upload (H-3 Kerja)**: **26 November 2026** (Kamis).
- **Rujukan Berkas**: [`kegiatan/publikasi-kesra-2026/2026/README.md`](../kegiatan/publikasi-kesra-2026/2026/README.md).

## SOP & Ketentuan Cleaning Data SE2026: Pemberian Remark & Tim Organik (21 Oktober 2026)
- **Arahan Pimpinan Terkait Pelaksana**:
  - Pimpinan BPS Provinsi Kalimantan Barat menegaskan bahwa proses cleaning data SE2026 **HANYA dilakukan oleh pegawai organik BPS** dan **DILARANG diserahkan kepada anak/mahasiswa magang**. Hal ini terkait kewajiban penandatanganan NDA (*Non-Disclosure Agreement*) dan perlindungan kerahasiaan data mikro sensus.
  - Urgensi: Capaian progres cleaning data SE2026 Provinsi Kalimantan Barat masih berada di bawah rata-rata nasional sehingga memerlukan percepatan serentak di seluruh satker kab/kota.
  - Setiap pemeriksaan dan perbaikan anomali data mikro **wajib diberikan Remark**.
- **Standar Format Kode Remark (Arahan Deputi NAS tanggal 15 Oktober 2026)**:
  Format penulisan kode remark resmi disederhanakan dari `#DC_00` s.d. `#DC_04` menjadi `#0` s.d. `#4`:
  - **`#0`** (sebelumnya `#DC_00`): *Data tidak mengalami perubahan* (Data dinyatakan sesuai kondisi lapangan, sehingga tidak dilakukan perubahan).
  - **`#1`** (sebelumnya `#DC_01`): *Data mengalami perubahan* (Perbaikan dilakukan karena kesalahan pemahaman petugas terhadap konsep atau kesalahan entri kuesioner).
  - **`#2`** (sebelumnya `#DC_02`): *Data mengalami perubahan* (Hasil konfirmasi/revisit langsung kepada responden).
  - **`#3`** (sebelumnya `#DC_03`): *Data mengalami perubahan* (Informasi yang bersumber dari survei rutin BPS lain atau data administrasi dinas/instansi).
  - **`#4`** (sebelumnya `#DC_04`): *Data mengalami perubahan* (Metode atau informasi lain selain kriteria kode #1, #2, dan #3).
  - *Catatan Retrospektif*: Kode lama yang sudah terlanjur diinput (`#DC_0x`) tetap berlaku sah dan tidak perlu diubah ulang. Untuk pengerjaan selanjutnya menggunakan kode baru `#0` s.d. `#4`.
- **Rujukan**: Dokumen surat resmi dan tangkapan layar di `media/AC32E2C46AA145CCC4B310F33C381861.jpg` dan `media/AC6060FF7383A27E9706E3BD5B5433DA.jpg`.

## Arsitektur Monitoring Cleaning Data SE2026 (Sheet `Mon Ini` & Tab Merah)
- **Tautan Spreadsheet**: [`Monitoring Cleaning Data SE 2026`](https://docs.google.com/spreadsheets/d/1EWoctuipZZgfERnqDLmvdDXdC1XiFtFB6Pbcw9U2rz0/edit?gid=104338933#gid=104338933).
- **Desain Tab `Mon Ini`**:
  - Dibuat untuk merekapitulasi beban target dan progres tindak lanjut cleaning per petugas pemeriksa/PJ.
  - Tab anomali yang dijadikan sumber data adalah tab-tab bertanda warna merah (*tabColor: red*):
    1. `rantab_dbnas` (Anomali rasio nilai tambah neraca)
    2. `rekap_usaha_A` (Rekapitulasi usaha sektor pertanian/A)
    3. `rekomendasi_kbli_anomali_layer2_18102026` (Anomali layer 2 per 18 Okt 2026)
    4. `rekomendasi_kbli_anomali_18102026` (Anomali KBLI layer 1 per 18 Okt 2026)
    5. `sosek_tabel19` (Tabel konsistensi sosial ekonomi)
  - Struktur Kolom Utama:
    - *Kolom A*: Nama Petugas
    - *Kolom B*: Progres Total Sudah Tindak Lanjut (%)
    - *Kolom C*: Jumlah Total Sudah Tindak Lanjut
    - *Kolom D*: Jumlah Total Target
    - *Kolom E–G, H–J, dst*: Pasangan metrik (*Sudah Tindak Lanjut*, *Target Tindak Lanjut*, *Progres Tindak Lanjut*) untuk masing-masing tab anomali merah.

## Intisari Sosialisasi Sistem Backend Website BPS Baru (21 Oktober 2026)
- **Waktu Pelaksanaan**: Rabu, 21 Oktober 2026 (08.00 – 12.00 WIB daring via LMS BPS).
- **Portal Backend Baru**: `https://web-be.apps.bps.go.id`.
- **Peserta BPS Kab. Mempawah**: Ihza Karunia & Akma Batrisyia.
- **Timeline & Jadwal Kunci (Hasil Transkrip Sosialisasi)**:
  - **Mulai Hari Ini (Rabu, 21 Oktober 2026)**: Backend baru sudah bisa mulai diakses dan digunakan satker untuk uji coba serta mencicil pairing metadata.
  - **Jumat Sore, 23 Oktober 2026 (Pukul 16.00 / 18.00 WIB)**: Batas akhir bagi daerah untuk mengunggah / memperbarui konten di sistem lama.
  - **Jumat Malam, 23 Oktober 2026 (Pukul 19.00 WIB)**: Akses backend lama (archive & webdesk) **DITUTUP TOTAL (CUT-OFF)** untuk proses migrasi database ke mesin/server baru oleh Tim Inka SIS BPS RI.
  - **Senin, 26 Oktober 2026**: Go-Live resmi Website BPS Versi 5.0 nasional. Backend lama tidak dapat diakses lagi dan seluruh satker wajib menggunakan sistem backend baru.
  - **Januari 2027**: Target konsistensi penuh pencatatan statistik pengunjung website di Webdash berbasis Google Analytics.
- **Poin Kunci Sistem**:
  - *Standardisasi Frontend*: Tampilan muka web publik seragam nasional (Sabang–Merauke). Seluruh kustomisasi konten daerah dikontrol lewat sistem *Backend*.
  - *Akses Terpusat*: Menggunakan akun Single Sign-On (SSO Baru BPS) teraktivasi dengan OTP pengaman.
  - *Manajemen Multi-Satker*: Memilih lingkup website berdasarkan kode MFD (misal Pusat `0000`, Provinsi Kalbar `6100`, Mempawah `6104`).
  - *Fitur Konten & Indikator*:
    - Master Indikator dengan interface sel mirip Excel (mendukung *copy-paste* langsung dari file Excel dan unduh template).
    - Tabel Statis dengan klasifikasi subjek statistik (CSA), mapping metadata SIMDASI, dan unggah berkas Excel.
    - Kolom *Headline* SEO-friendly untuk meningkatkan keterbacaan publik di mesin pencari dan media sosial tanpa merusak struktur judul baku rilis BPS.
- **Rujukan Lengkap**: [`kegiatan/sosialisasi-backend-website/2026/README.md`](../kegiatan/sosialisasi-backend-website/2026/README.md) dan salinan transkrip di [`knowledge/transkrip_zoom_backend.txt`](transkrip_zoom_backend.txt).





## Pelatihan Rekomendasi Kegiatan Statistik (Romantik) 2026
- **Dasar Surat**: Surat Kepala BPS Provinsi Kalimantan Barat Nomor B-875/61000/ES/2026 tanggal 21 Oktober 2026 hal *Permintaan Peserta Pelatihan*, menindaklanjuti Surat Deputi Bidang Metodologi dan Informasi Statistik Nomor B-101/03000/ES/2026 tanggal 19 Oktober 2026.
- **Penyelenggara**: Pusdiklat BPS bekerjasama dengan Direktorat Metodologi dan Informasi Statistik BPS RI.
- **Metode**: Daring (Online via Pusdiklat BPS & Zoom).
- **Alokasi Peserta**: 1 orang per BPS Kabupaten/Kota se-Kalbar. Seluruh peserta dari Provinsi Kalimantan Barat mengikuti **Gelombang 2**.
- **Deadline Registrasi & Grup Diskusi (Kritis)**:
  - Tautan: `http://s.bps.go.id/pesertaRS26`
  - Batas Akhir: **Jumat, 23 Oktober 2026**.
- **Jadwal Pelatihan Gelombang 2 (Kalbar)**:
  - **Kamis, 19 November 2026 (08:00–10:15 WIB)**: Pleno Persiapan, Pembukaan & Overview Kebijakan Teknis.
  - **Jumat, 20 November 2026**: Pembelajaran Mandiri MOOC (1 hari @3 JP).
  - **Rabu, 25 November 2026 (07:30–15:00 WIB / 08:30–16:00 WITA)**: Ceramah Eselon 2, Pretest, Pengenalan & Mekanisme Romantik, Identifikasi Kegiatan Statistik, Desain Survei, Asynchronous.
  - **Kamis, 26 November 2026 (07:00–13:45 WIB / 08:00–14:45 WITA)**: Pemeriksaan & Rekomendasi, Aplikasi Romantik, Post-test, Reviu Pelatihan.
  - **Jumat, 27 November 2026 (08:00–08:45 WIB)**: Pleno Persiapan & Penutupan Bersama.
- **Rujukan Lengkap**: [`kegiatan/pelatihan-romantik/2026/README.md`](../kegiatan/pelatihan-romantik/2026/README.md) dan arsip berkas di [`knowledge/assets/Surat_Permintaan_Peserta_Pelatihan_Romantik_2026.pdf`](assets/Surat_Permintaan_Peserta_Pelatihan_Romantik_2026.pdf).


## Data Processing SE2026 (Pemanfaatan Aplikasi IPAS)
- **Sumber Resmi**: Workshop Data Processing SE2026 (Direktorat Statistik Jasa / BPS RI, Oktober 2026).
- **Aplikasi Resmi Pengolahan**: **IPAS (*Integrated Processing and Analysis System*)**.
- **Jadwal Pelaksanaan Pengolahan Inti**: **30 Oktober – 15 November 2026** (periode aktif pengolahan ~15 hari kalender).
- **Tahapan & Milestone Penting**:
  - *16–17 Oktober 2026*: Pilot Data Processing oleh Direktorat Statistik Jasa BPS RI.
  - *21–22 Oktober 2026*: Workshop Data Processing nasional.
  - *23–25 Oktober 2026*: Eksplorasi Data Processing dengan IPAS.
  - *25 Oktober 2026*: **Penutupan Akses Fasih (Cut-off)** untuk sinkronisasi data lapangan.
  - *26–29 Oktober 2026*: Persiapan Environment IPAS (setup database & migrasi data Fasih ke server IPAS).
  - *30 Oktober – 15 November 2026*: **Pelaksanaan Data Processing** (klasifikasi, koding, reviu, validasi, editing, imputasi, dan tabulasi).
- **Kualitas Data & Evaluasi Nilai Tambah**:
  - Tren penurunan agregat nilai tambah negatif secara nasional mencapai 82,6% (-138 temuan), tersisa 29 temuan per 21 Oktober 2026.
  - Benchmark Rasio NT/Output: PDB 2025 (0,5063) dan Tabel IO 2020 (0,5243).
- **Rujukan Lengkap**: [`knowledge/kegiatan/data-processing-se2026/2026/README.md`](kegiatan/data-processing-se2026/2026/README.md), [`knowledge/universal/timeline_data_processing_se2026.md`](universal/timeline_data_processing_se2026.md), dan salinan slide materi di [`knowledge/assets/Timeline_Data_Processing_SE2026_IPAS.jpg`](assets/Timeline_Data_Processing_SE2026_IPAS.jpg).

## Data Processing SE2026 & Kondisi NTB (22 Oktober 2026)
- **Sumber Resmi**: Paparan *"Kondisi NTB SE 2026"*, Bidang Analisis dan Pengawalan Kualitas Data BPS RI (22 Oktober 2026).
- **Aplikasi Resmi**: **IPAS (*Integrated Processing and Analysis System*)**.
- **Jadwal Pelaksanaan Inti**: **30 Oktober – 15 November 2026** (~15 hari kalender).
- **Milestone Kritis**:
  - *21–22 Oktober 2026*: Workshop Data Processing.
  - *23–25 Oktober 2026*: Eksplorasi Data Processing IPAS.
  - *25 Oktober 2026*: **Penutupan Akses Fasih (Cut-off)** untuk sinkronisasi data lapangan.
  - *26–29 Oktober 2026*: Persiapan Environment IPAS (setup database & migrasi data Fasih).
  - *30 Oktober – 15 November 2026*: **Pelaksanaan Pengolahan IPAS** (editing, koding, imputasi, validasi, tabulasi).
- **Kualitas Data & Evaluasi Nilai Tambah**:
  - Tren penurunan agregat nilai tambah negatif nasional sebesar 82,6% (tersisa 29 temuan per 21 Okt siang).
  - Benchmark Rasio NT/Output: PDB 2025 (`0,5063`), Tabel IO 2020 (`0,5243`). Posisi Kalbar: `0,5507` (mendekati benchmark).
  - Benchmark Rasio Upah/NT: Tabel IO 2016 (`0,4490`), Tabel IO 2020 (`0,3861`). Posisi Kalbar: `0,1353`.
  - Struktur NT SE2026 vs PDRB 2025 Kalbar: Rasio 80,18% (NT SE2026 Rp263,46 T / PDRB 2025 Rp328,57 T).
  - Isu Anomali Perhatian: KBLI di luar cakupan (P, R, S, T, U), faskes/sekolah negeri dengan rincian pendapatan Rp0 & biaya tinggi, serta audit 135 PDAM/air minum.
- **Rujukan Berkas**:
  - Dokumen analisis: [`kegiatan/sensus-ekonomi-2026/2026/docs/kondisi-ntb-se2026-22-oktober-2026.md`](../kegiatan/sensus-ekonomi-2026/2026/docs/kondisi-ntb-se2026-22-oktober-2026.md)
  - Berkas PDF resmi: [`kegiatan/sensus-ekonomi-2026/2026/docs/pdf/2026-10-22_Kondisi_NTB_SE2026.pdf`](../kegiatan/sensus-ekonomi-2026/2026/docs/pdf/2026-10-22_Kondisi_NTB_SE2026.pdf)

