# STANDAR OPERASIONAL PROSEDUR (SOP) PERMINTAAN DATA
## Hasil Pembinaan Kelurahan Cinta Statistik (Kelurahan Cantik) 2026
**Pemerintah Kelurahan Pasir Wan Salim, Kecamatan Mempawah Timur, Kabupaten Mempawah**

---

### 1. Latar Belakang
Dalam rangka mewujudkan tata kelola Satu Data Indonesia (SDI) di tingkat kelurahan serta mendukung keterbukaan informasi publik, Pemerintah Kelurahan Pasir Wan Salim bersama Badan Pusat Statistik (BPS) Kabupaten Mempawah menyusun Standar Operasional Prosedur (SOP) Permintaan dan Pemanfaatan Data. SOP ini mengatur mekanisme aksesibilitas data bagi masyarakat, akademisi, perangkat daerah, dan pemangku kepentingan secara transparan, akuntabel, dan cepat.

---

### 2. Sumber Data & Basis Data Terpadu
Data yang dapat diakses bersumber dari basis data hasil sensus dan pendataan potensi kewilayahan Program Kelurahan Cantik 2026:
*   **Basis Data RT & Demografi (`Sheet1` / AppSheet)**: Karakteristik penduduk (gender, rasio jenis kelamin), rumah tangga (KK), tingkat pendidikan, kepemilikan dokumen adminduk/BPJS, status ketenagakerjaan, kegiatan UMKM, dan sebaran penerima bantuan sosial (PKH, BPNT, BST, BLT).
*   **Produk Statistik Turunan**: Buku Publikasi *Kelurahan Pasir Wan Salim Dalam Angka 2026*, Buku *Potensi Kelurahan Pasir Wan Salim 2026*, Monografi Kelurahan, dan Infografis Statistik Demografi format resolusi tinggi (HD).

---

### 3. Saluran Layanan Permintaan Data (Dual-Channel Delivery)

Layanan penyediaan data statistik Kelurahan Cantik Pasir Wan Salim diselenggarakan melalui 2 (dua) saluran resmi:

| Saluran Layanan | Jalur Akses | Sasaran Pengguna | Durasi Layanan | Jenis Output |
| :--- | :--- | :--- | :---: | :--- |
| **Jalur 1: Layanan Mandiri Digital** (*Self-Service Online*) | Portal Website Resmi (`desa-sm.dvlp.asia`) & Open Data REST API | Masyarakat umum, akademisi, peneliti, mahasiswa, media massa, dan OPD | **Instan (0 Menit)** | File Spreadsheet Excel (`.xlsx`), Naskah Buku Publikasi PDF, Monografi, Infografis HD, JSON API |
| **Jalur 2: Layanan Fasilitasi Khusus** (*Offline & WhatsApp*) | Loket Kantor Kelurahan & WhatsApp Agen Statistik (`+62 897-7539-550`) | Instansi resmi, riset khusus, atau pemohon data disagregasi/legalisir | **Maksimal 1 Hari Kerja** | Berkas Data Rekapitulasi Resmi bertanda tangan Lurah Pasir Wan Salim |

---

### 4. Prosedur Operasional Rinci

#### A. Jalur 1: Layanan Mandiri Digital (*Self-Service Direct Download & Open API*) — Instan (0 Menit)
Jalur ini ditujukan bagi publik, mahasiswa, akademisi, dan instansi yang memerlukan data terbuka tingkat agregat tanpa memerlukan surat pengantar atau verifikasi birokrasi manual:

1. **Akses Portal Website Resmi**:
   - Pemohon mengunjungi portal web Kelurahan Cantik: `https://desa-sm.dvlp.asia/desa-cantik/kelurahanpasirwansalim`
2. **Pilih Menu Layanan dan Unduh Mandiri**:
   - **Dataset Excel (SDI)**: Masuk ke section *Daftar Potensi RT*, lalu klik tombol **"Unduh Data Tabel (Excel)"** untuk mendapatkan file spreadsheet lengkap (`.xlsx`).
   - **Buku Publikasi Digital**: Masuk ke section *Publikasi & Bukti Dukung*, klik **"Unduh Publikasi"** untuk mengunduh naskah PDF resmi Kelurahan Dalam Angka atau Potensi Kelurahan.
   - **Monografi & Infografis**: Masuk ke section *Produk Statistik & SOP*, klik **"Unduh Monografi"** atau **"Unduh Versi HD"** untuk materi infografis visual.
3. **Integrasi Open API (Bagi Pengembang / Sistem Eksternal)**:
   - Akses data terstruktur via REST API (JSON):
     - `GET https://desa-sm.dvlp.asia/desa-cantik/api/pasirwansalim/Sheet1`

---

#### B. Jalur 2: Layanan Fasilitasi / Permintaan Khusus (*Offline & WhatsApp*) — Maksimal 1 Hari Kerja
Jalur ini ditujukan bagi pemohon yang membutuhkan data disagregasi khusus, konsultasi statistik sektoral, atau berkas data bertanda tangan resmi Lurah Pasir Wan Salim:

| Tahap | Pelaku | Aktivitas | Durasi | Output |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Pemohon Data | Mengajukan permohonan di loket Kantor Kelurahan Pasir Wan Salim atau menghubungi Agen Statistik Kelurahan via WhatsApp (`+62 897-7539-550`) dengan menyampaikan maksud keperluan. | 10 Menit | Formulir Permohonan Tercatat |
| **2** | Kasi Pemerintahan / Lurah Pasir Wan Salim | Memverifikasi kesesuaian permohonan data dan memberikan persetujuan rilis data statistik. | Maks 2 Jam | Disposisi Persetujuan Rilis |
| **3** | Agen Statistik Kelurahan | Melakukan ekstraksi data dari basis data terpadu Kelurahan Cantik. | 15 Menit | Berkas Rekapitulasi Data |
| **4** | Agen Statistik Kelurahan | Menyerahkan berkas data resmi (cetak bertanda tangan atau file elektronik terotentikasi via WhatsApp/Email). | 5 Menit | Tanda Terima & Berkas Data |

---

### 5. Aturan Hak Akses & Keamanan Data Pribadi
1. **Perlindungan Data Pribadi (UU No. 27/2022)**: Data individu/mikro (*by name by address*) bersifat rahasia dan **tidak dipublikasikan** untuk melindungi privasi warga.
2. **Level Diseminasi**: Data yang diserahkan kepada publik berupa data agregat tingkat Rukun Tetangga (RT), Dusun/RW, atau inventarisasi fasilitas umum.
3. **Pemanfaatan Non-Komersial**: Data hasil kegiatan Kelurahan Cantik disediakan untuk kepentingan perencanaan pembangunan, perumusan kebijakan, penelitian akademis, dan pelayanan publik. Penggunaan untuk tujuan komersial wajib memperoleh izin tertulis dari Pemerintah Kelurahan.

---

### 6. Pengesahan & Tanda Tangan

Pasir Wan Salim, 6 Agustus 2026

**Mengesahkan,**  
**Lurah Pasir Wan Salim**

<br><br><br>

**<u>H. MULYADI, S.H.I</u>**
