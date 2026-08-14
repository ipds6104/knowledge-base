# STANDAR OPERASIONAL PROSEDUR (SOP) PERMINTAAN DATA
## Hasil Pembinaan Desa Cinta Statistik (Desa Cantik) 2026
**Pemerintah Desa Pasir Palembang, Kecamatan Mempawah Timur, Kabupaten Mempawah**

---

### 1. Latar Belakang
Dalam rangka mewujudkan tata kelola Satu Data Indonesia (SDI) di tingkat desa serta mendukung keterbukaan informasi publik, Pemerintah Desa Pasir Palembang bersama Badan Pusat Statistik (BPS) Kabupaten Mempawah menyusun Standar Operasional Prosedur (SOP) Permintaan dan Pemanfaatan Data. SOP ini mengatur mekanisme aksesibilitas data bagi masyarakat, akademisi, perangkat daerah, dan pemangku kepentingan secara transparan, akuntabel, dan cepat.

---

### 2. Sumber Data & Basis Data Terpadu
Data yang dapat diakses bersumber dari basis data hasil sensus dan pendataan potensi kewilayahan Program Desa Cantik 2026:
*   **Basis Data RT & Demografi (`Sheet1` / AppSheet)**: Karakteristik penduduk (gender, rasio jenis kelamin), rumah tangga (KK), tingkat pendidikan, kepemilikan dokumen adminduk/BPJS, status ketenagakerjaan, kegiatan UMKM, dan sebaran penerima bantuan sosial (PKH, BPNT, BST, BLT).
*   **Basis Data Fasilitas (`Sheet4` / AppSheet)**: Pemetaan geospasial sarana peribadatan, pendidikan, kesehatan, fasilitas ekonomi, pemerintahan, kondisi fisik bangunan, jalan, listrik, dan jaringan telekomunikasi.
*   **Produk Statistik Turunan**: Buku Publikasi *Desa Pasir Palembang Dalam Angka 2026*, Buku *Potensi Desa Pasir Palembang 2026*, Monografi Desa, dan Infografis Statistik Demografi format resolusi tinggi (HD).

---

### 3. Saluran Layanan Permintaan Data (Dual-Channel Delivery)

Layanan penyediaan data statistik Desa Cantik Pasir Palembang diselenggarakan melalui 2 (dua) saluran resmi:

| Saluran Layanan | Jalur Akses | Sasaran Pengguna | Durasi Layanan | Jenis Output |
| :--- | :--- | :--- | :---: | :--- |
| **Jalur 1: Layanan Mandiri Digital** (*Self-Service Online*) | Portal Website Resmi (`desa-sm.dvlp.asia`) & Open Data REST API | Masyarakat umum, akademisi, peneliti, mahasiswa, media massa, dan OPD | **Instan (0 Menit)** | File Spreadsheet Excel (`.xlsx`), Naskah Buku Publikasi PDF, Monografi, Infografis HD, JSON API |
| **Jalur 2: Layanan Fasilitasi Khusus** (*Offline & WhatsApp*) | Loket Kantor Desa & WhatsApp Agen Statistik (`+62 857-5171-8089`) | Instansi resmi, riset khusus, atau pemohon data disagregasi/legalisir | **Maksimal 1 Hari Kerja** | Berkas Data Rekapitulasi Resmi bertanda tangan Kepala Desa Pasir Palembang |

---

### 4. Prosedur Operasional Rinci

#### A. Jalur 1: Layanan Mandiri Digital (*Self-Service Direct Download & Open API*) — Instan (0 Menit)
Jalur ini ditujukan bagi publik, mahasiswa, akademisi, dan instansi yang memerlukan data terbuka tingkat agregat tanpa memerlukan surat pengantar atau verifikasi birokrasi manual:

1. **Akses Portal Website Resmi**:
   - Pemohon mengunjungi portal web Desa Cantik: `https://desa-sm.dvlp.asia/desa-cantik/desapasirpalembang`
2. **Pilih Menu Layanan dan Unduh Mandiri**:
   - **Dataset Excel (SDI)**: Masuk ke section *Daftar Potensi RT*, lalu klik tombol **"Unduh Data Tabel (Excel)"** untuk mendapatkan file spreadsheet lengkap (`.xlsx`).
   - **Buku Publikasi Digital**: Masuk ke section *Publikasi & Bukti Dukung*, klik **"Unduh Publikasi"** untuk mengunduh naskah PDF resmi Desa Dalam Angka atau Potensi Desa.
   - **Monografi & Infografis**: Masuk ke section *Produk Statistik & SOP*, klik **"Unduh Monografi"** atau **"Unduh Versi HD"** untuk materi infografis visual.
3. **Integrasi Open API (Bagi Pengembang / Sistem Eksternal)**:
   - Akses data terstruktur via REST API (JSON):
     - `GET https://desa-sm.dvlp.asia/desa-cantik/api/pasirpalembang/Sheet1`
     - `GET https://desa-sm.dvlp.asia/desa-cantik/api/pasirpalembang/Sheet4`

---

#### B. Jalur 2: Layanan Fasilitasi / Permintaan Khusus (*Offline & WhatsApp*) — Maksimal 1 Hari Kerja
Jalur ini ditujukan bagi pemohon yang membutuhkan data disagregasi khusus, konsultasi statistik sektoral, atau berkas data bertanda tangan resmi Kepala Desa Pasir Palembang:

| Tahap | Pelaku | Aktivitas | Durasi | Output |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Pemohon Data | Mengajukan permohonan di loket Kantor Desa Pasir Palembang atau menghubungi Agen Statistik Desa via WhatsApp (`+62 857-5171-8089`) dengan menyampaikan maksud keperluan. | 10 Menit | Formulir Permohonan Tercatat |
| **2** | Kasi Pemerintahan / Kepala Desa Pasir Palembang | Memverifikasi kesesuaian permohonan data dan memberikan persetujuan rilis data statistik. | Maks 2 Jam | Disposisi Persetujuan Rilis |
| **3** | Agen Statistik Desa | Melakukan ekstraksi data dari basis data terpadu Desa Cantik. | 15 Menit | Berkas Rekapitulasi Data |
| **4** | Agen Statistik Desa | Menyerahkan berkas data resmi (cetak bertanda tangan atau file elektronik terotentikasi via WhatsApp/Email). | 5 Menit | Tanda Terima & Berkas Data |

---

### 5. Aturan Hak Akses & Keamanan Data Pribadi
1. **Perlindungan Data Pribadi (UU No. 27/2022)**: Data individu/mikro (*by name by address*) bersifat rahasia dan **tidak dipublikasikan** untuk melindungi privasi warga.
2. **Level Diseminasi**: Data yang diserahkan kepada publik berupa data agregat tingkat Rukun Tetangga (RT), Dusun/RW, atau inventarisasi fasilitas umum.
3. **Pemanfaatan Non-Komersial**: Data hasil kegiatan Desa Cantik disediakan untuk kepentingan perencanaan pembangunan, perumusan kebijakan, penelitian akademis, dan pelayanan publik. Penggunaan untuk tujuan komersial wajib memperoleh izin tertulis dari Pemerintah Desa.

---

### 6. Pengesahan & Tanda Tangan

Pasir Palembang, 6 Agustus 2026

**Mengesahkan,**  
**Kepala Desa Pasir Palembang**

<br><br><br>

**<u>AS'AD AFRIADI</u>**
