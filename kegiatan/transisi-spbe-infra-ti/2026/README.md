---
nama: "Transisi dan Pengelolaan Infrastruktur TI SPBE 2026"
kategori: "non-survey"
rutinitas: "ad-hoc"
frekuensi: "tahunan"
peran: "ketua"
status: "aktif"
deadlines:
  - tanggal: "2026-09-30"
    kegiatan: "Batas Akhir Sosialisasi & Aktivasi Mandiri Akun SSO Baru (OTP 2FA Google Authenticator & Recovery Email)"
    status: "belum"
  - tanggal: "2026-10-01"
    kegiatan: "Cut-Off Transisi Email Baru (email.bps.go.id aktif, archivemail.bps.go.id read-only)"
    status: "belum"
  - tanggal: "2026-10-31"
    kegiatan: "Batas Akhir Migrasi VPN Global Protect & Penyesuaian Role Developer"
    status: "belum"
  - tanggal: "2026-12-31"
    kegiatan: "Hard Cut-Off Sistem Lama (FortiClient VPN, SSO Lama, & Archivemail Dimatikan Total)"
    status: "belum"
---

# Transisi dan Pengelolaan Infrastruktur TI SPBE BPS Kabupaten Mempawah TA 2026

> [!IMPORTANT]
> Program kerja strategis transisi infrastruktur teknologi informasi dan penguatan Sistem Pemerintahan Berbasis Elektronik (SPBE) BPS Kabupaten Mempawah (Satker 6104), menindaklanjuti sosialisasi nasional Direktorat Sistem Informasi Statistik (SIS) BPS RI pada forum **Kamis AIS (24 September 2026)**.
> **PIC SPBE Satker**: Ihza Karunia (Pranata Komputer / IPDS BPS Kabupaten Mempawah).

---

## 1. Latar Belakang & Urgensi Keamanan Siber

1. **Mandat Modernisasi SPBE BPS**:
   - Modernisasi arsitektur autentikasi, komunikasi surat elektronik, dan perimeter jaringan privat BPS secara terpusat dan berstandar industri.
   - Peningkatan skor maturitas indeks SPBE dan tata kelola domain TI BPS Kabupaten Mempawah.
2. **Mitigasi Insiden Siber Nasional**:
   - Merespons insiden peretasan data kredensial ASN yang dilaporkan BSSN pada **15 September 2026** (melibatkan lebih dari 600 akun email/SSO pegawai BPS yang terindikasi *compromised* / bocor akibat *infostealer* di perangkat pribadi).
   - Penegakan arsitektur keamanan *Zero Trust* dengan mewajibkan autentikasi multifaktor (MFA / 2FA) berbasis *Time-based One-Time Password* (TOTP).

---

## 2. Tiga Pilar Infrastruktur TI Baru BPS RI

### Pilar A: Single Sign-On (SSO) Terpadu (`accounts.bps.go.id`)
- **Portal Baru**: `https://accounts.bps.go.id`
- **Fitur Kunci**:
  * Autentikasi Multifaktor (2FA) menggunakan aplikasi TOTP (Google Authenticator / Microsoft Authenticator).
  * Pendaftaran *Recovery Email* (wajib menggunakan email pribadi/eksternal aktif seperti Gmail/Yahoo, bukan `@bps.go.id`) untuk pemulihan akses darurat.
  * Manajemen Perangkat Tepercaya (*Trusted Devices*) dan audit riwayat sesi login aktif secara *real-time*.
- **Instruksi Kritis untuk Pegawai**:
  * **DILARANG MENGHAPUS** entri OTP akun SSO lama di Google Authenticator. Sistem lama (seperti presensi online dan SIMPEG tertentu) masih dalam proses migrasi bertahap. Cukup tambahkan entri OTP baru untuk `accounts.bps.go.id`.
  * Pegawai yang terdampak notifikasi kebocoran kredensial BSSN wajib segera mereset kata sandi dan mengaktifkan 2FA paling lambat 30 September 2026.

### Pilar B: Layanan Email Baru Zimbra (`email.bps.go.id`)
- **Portal Webmail Baru**: `https://email.bps.go.id`
- **Portal Arsip Webmail Lama**: `https://archivemail.bps.go.id` (status *Read-Only* per 1 Oktober 2026).
- **Ketentuan Teknis**:
  * Kuota kotak surat (*mailbox quota*): **1 GB per akun pegawai**.
  * Mulai 1 Oktober 2026, seluruh lalu lintas surat dinas elektronik masuk (*inbound*) dan keluar (*outbound*) resmi dialihkan penuh ke `email.bps.go.id`.
  * **Penyelamatan Arsip Email**: Seluruh pegawai dan pemegang akun tim wajib melakukan ekspor berkas arsip mandiri (`.tgz`) melalui webmail lama sebelum **31 Desember 2026**. Setelah tanggal tersebut, server arsip akan dimatikan permanen dan data yang belum diekspor akan terhapus total.
  * **Tata Kelola Akun Tim/Seksi**: Menghentikan budaya pembagian kata sandi bersama (*password sharing*). Akses akun seksi/tim kerja dilakukan melalui mekanisme resmi **Delegasi / Sharing Folder** di Zimbra baru.

### Pilar C: Jaringan Privat Virtual Global Protect (`vpn.bps.go.id`)
- **Portal Unduh Installer**: `https://vpn.bps.go.id`
- **Penggantian Klien**: Menggantikan aplikasi FortiClient VPN secara bertahap hingga dipensiunkan penuh pada 31 Desember 2026.
- **Kebijakan Akses Jaringan Lokal (SD-WAN Awareness)**:
  * Pegawai yang terhubung ke jaringan kabel LAN kantor atau Wi-Fi resmi kantor BPS Kabupaten Mempawah yang telah dilengkapi infrastruktur SD-WAN **TIDAK PERLU** mengaktifkan VPN Global Protect untuk mengakses aplikasi internal BPS.
  * VPN Global Protect hanya digunakan ketika pegawai bekerja di luar kantor (*Work from Home*, dinas luar, atau jaringan publik).
- **Pengguna Khusus (Developer & Database Admin)**:
  * Pemetaan IP/port dan hak akses khusus server database/aplikasi lokal dikompilasi dan diajukan penyesuaian role-nya ke SIS BPS RI sebelum 31 Oktober 2026.

---

## 3. Matriks Jadwal & Tenggat Waktu Kritis (Timeline)

| Tanggal | Tonggak Capaian (Milestone) | Dampak Operasional | Aksi PIC SPBE Mempawah |
| :--- | :--- | :--- | :--- |
| **24 Sep 2026** | Peluncuran & Sosialisasi Kamis AIS | Pengumuman resmi arsitektur TI baru oleh Direktur SIS | Penyusunan panduan ringkas & rencana aksi satker |
| **30 Sep 2026** | **Deadline Aktivasi Mandiri SSO** | Batas akhir aktivasi mandiri 2FA & recovery email | Asistensi walk-in di IPDS & rekapitulasi pegawai aktif 100% |
| **01 Okt 2026** | **Cut-Off Layanan Email** | Webmail lama beralih ke `archivemail.bps.go.id` (read-only), webmail baru aktif penuh | Verifikasi penerimaan email dinas & panduan backup .tgz |
| **31 Okt 2026** | **Deadline Transisi VPN & Dev** | Batas akhir integrasi SSO aplikasi internal & role dev | Uji coba koneksi Global Protect luar kantor & request role |
| **31 Des 2026** | **Hard Cut-Off Sistem Lama** | FortiClient mati, SSO lama tutup, server archivemail dimatikan | Audit pembersihan total & pemastian backup email 100% tuntas |
| **01 Jan 2027** | **Operasional Penuh 100%** | Sistem baru beroperasi penuh tanpa sistem legacy | Laporan evaluasi akhir transisi SPBE ke pimpinan |

---

## 4. Rencana Aksi Kerja PIC SPBE BPS Kabupaten Mempawah

### Tahap 1: Onboarding Kilat & Asistensi 2FA (25 – 30 September 2026)
1. **Siaran Informasi Terstruktur (Broadcast WhatsApp)**:
   - Menyebarkan panduan aktivasi praktis ke grup internal BPS Kabupaten Mempawah.
   - Menekankan pesan peringatan: *Jangan hapus OTP lama di Google Authenticator*.
2. **Klinik Asistensi Mandiri (Helpdesk Walk-in IPDS)**:
   - Menyediakan meja bantuan teknis di ruang IPDS untuk mendampingi rekan kerja yang mengalami kendala sinkronisasi jam perangkat (*time sync error*), aktivasi OTP, atau penautan email pemulihan.
3. **Penyisiran Akun Berisiko Tinggi**:
   - Memastikan pegawai yang namanya terindikasi dalam daftar insiden BSSN (15 September 2026) telah mengganti kata sandi dan mengaktifkan 2FA.

### Tahap 2: Pengawalan Cut-Off Email & Penyelamatan Arsip (1 – 7 Oktober 2026)
1. **Monitoring Transisi Email Masuk/Keluar**:
   - Menjalankan uji kirim dan terima email lintas instansi (Pemda Mempawah, KPPN, BPS Provinsi Kalbar).
2. **Edukasi Ekspor Backup `.tgz`**:
   - Menyebarkan tutorial langkah demi langkah mengunduh arsip email lama dari `archivemail.bps.go.id`.
   - Mengawal ekspor arsip untuk pimpinan satker, pejabat pembuat komitmen (PPK), bendahara, dan akun persuratan kantor (`bps6104@bps.go.id`).
3. **Konfigurasi Hak Akses Delegasi Zimbra**:
   - Membantu pembagian hak akses (*sharing folder*) email tim kerja tanpa membagikan kata sandi akun induk.

### Tahap 3: Standardisasi Klien VPN & Akses Khusus (8 – 31 Oktober 2026)
1. **Distribusi Installer Global Protect**:
   - Menyediakan cermin lokal (*mirror*) file instalasi Global Protect (Windows/macOS/Linux) di repositori intranet lokal untuk menghemat *bandwidth*.
2. **Edukasi SD-WAN Kantor**:
   - Mengedukasi seluruh staf agar tidak menyalakan VPN saat berada di jaringan LAN/Wi-Fi kantor guna mencegah penurunan kecepatan akses (*overhead bottleneck*).
3. **Pengajuan Tiket Akses Pengembang / Sysadmin**:
   - Menginventarisasi kebutuhan port/IP server pengolahan, database mirror, dan server otomasi (Aina Agentic Engine) ke SIS BPS via form evaluasi Inka.

### Tahap 4: Audit Akhir Pra-Hard Cut-Off (November – Desember 2026)
1. **Pengecekan Residu Data Email Lama**:
   - Melakukan survei singkat memastikan tidak ada arsip dokumen penting dinas yang tertinggal di `archivemail.bps.go.id`.
2. **Penghapusan Klien Warisan (Legacy Cleanup)**:
   - Menginstruksikan uninstalasi FortiClient VPN di seluruh laptop dinas dan PC kerja.

---

## 5. Direktori Tautan & Layanan Resmi SIS BPS RI

| Layanan | Tautan Resmi | Deskripsi |
| :--- | :--- | :--- |
| **SSO Baru** | `https://accounts.bps.go.id` | Portal manajemen akun, profil, 2FA, dan sesi aktif |
| **Webmail Baru** | `https://email.bps.go.id` | Webmail Zimbra aktif produksi untuk surat-menyurat harian |
| **Arsip Webmail** | `https://archivemail.bps.go.id` | Portal baca arsip surat lama & ekspor backup `.tgz` |
| **VPN Baru** | `https://vpn.bps.go.id` | Portal login dan pengunduhan klien Global Protect VPN |
| **Bantuan SSO** | `https://s.bps.go.id/layanan-sso` | Panduan PDF resmi & formulir tiket kendala SSO |
| **Bantuan Email** | `https://s.bps.go.id/layanan-email` | Panduan ekspor/impor Zimbra & formulir tiket kendala email |
| **Repo VPN** | `https://s.bps.go.id/repo-VPN` | Repositori alternatif berkas instalasi VPN Global Protect |
| **Feedback Inka** | `https://s.bps.go.id/feedback-inka` | Formulir eskalasi kendala infrastruktur & permohonan role khusus |

---

## 6. Pertanyaan Umum & FAQ Operasional

1. **T: Apakah OTP di Google Authenticator lama untuk presensi dan SIMPEG boleh dihapus setelah SSO baru aktif?**
   - **J**: **JANGAN DIHAPUS**. Aplikasi seperti presensi dan SIMPEG masih dalam tahap integrasi bertahap. Tambahkan entri baru untuk akun SSO yang baru.
2. **T: Mengapa saya tidak bisa mengakses webmail lama setelah 1 Oktober 2026?**
   - **J**: Mulai 1 Oktober 2026, webmail lama dialihkan ke `archivemail.bps.go.id` dengan status *read-only*. Anda tetap bisa membaca dan mengekspor email lama di alamat arsip tersebut hingga 31 Desember 2026.
3. **T: Apakah saya wajib selalu menyalakan VPN Global Protect saat bekerja di kantor?**
   - **J**: **TIDAK**. Jaringan LAN dan Wi-Fi kantor BPS Kabupaten Mempawah sudah menerapkan teknologi SD-WAN terhubung langsung ke intranet BPS pusat. VPN hanya digunakan saat bekerja di luar kantor (*remote*).
4. **T: Bagaimana cara mengelola akun email seksi/tim tanpa berbagi kata sandi?**
   - **J**: Gunakan fitur *Preferences > Accounts > Share / Delegate Access* di webmail baru Zimbra untuk memberikan izin baca/kirim kepada akun individu anggota tim.
