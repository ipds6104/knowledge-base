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

## POK BPS Kabupaten Mempawah TA 2026 (SAKTI Kemenkeu)
- **Sumber Data**: Sistem SAKTI Kementerian Keuangan (Rincian Kertas Kerja Satker).
- **Waktu Penarikan**: Rabu, 16 September 2026 pukul 09:00 WIB (dibagikan oleh Bang Ihza Karunia).
- **Berkas Data Lokal**: `data/POK_BPS_Mempawah_2026_SAKTI.xlsx`
- **Total Pagu Satker**: **Rp 9.224.066.000,-**
- **Ringkasan Program**:
  1. **Program Penyediaan dan Pelayanan Informasi Statistik (054.01.GG)**: **Rp 5.113.471.000,-**
     - Alokasi Terbesar: Kegiatan 2902 (Statistik Distribusi / Sensus Ekonomi 2026) sebesar **Rp 3.610.255.000,-**.
     - Sub-alokasi SE2026:
       - 2902.BMA.006 (Publikasi/Laporan Sensus Ekonomi baseline): Rp 348.639.000,-
       - 2902.BMA.006 (Penambahan alokasi dari SABA): Rp 2.564.322.000,-
       - 2902.FAN.ZZ1 (Pemenuhan Prioritas Direktif Presiden - SE2026): Rp 691.694.000,-
     - Kegiatan Statistik Lainnya: Statistik Harga (2903: Rp 495,2 jt), Kesra/Susenas (2906: Rp 385,2 jt), Pertanian (2910: Rp 211 jt), Kependudukan/Ketenagakerjaan (2905: Rp 141,1 jt), Industri (2904: Rp 87,3 jt), Peternakan/Perikanan (2909: Rp 69,1 jt), dll.
  2. **Program Dukungan Manajemen (054.01.WA / 2886)**: **Rp 4.110.595.000,-**
     - Gaji, tunjangan operasional, dan pemeliharaan perkantoran BPS Kabupaten Mempawah.

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
- **Deadline Laporan & Administrasi Inda**: **Rabu, 7 Oktober 2026** (Penyelesaian berkas administrasi dan laporan Instruktur Daerah oleh Bang Ihza Karunia untuk proses pencairan honor).

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








