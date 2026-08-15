# STANDAR OPERASIONAL PROSEDUR (SOP) PERMINTAAN DATA
## Hasil Pembinaan Desa Cinta Statistik (Desa Cantik) 2026
**Pemerintah Desa Sungai Bakau Kecil, Kecamatan Mempawah Timur, Kabupaten Mempawah**

---

### 1. Latar Belakang & Prinsip Layanan Cepat

Dalam rangka mewujudkan tata kelola Satu Data Indonesia (SDI) di tingkat desa serta mendukung keterbukaan informasi publik, Pemerintah Desa Sungai Bakau Kecil bersama Badan Pusat Statistik (BPS) Kabupaten Mempawah menyusun Standar Operasional Prosedur (SOP) Permintaan dan Pemanfaatan Data. Layanan ini menerapkan prinsip **pelayanan cepat, ringkas, dan bebas hambatan birokrasi**: permohonan data statistik yang bersifat **agregat (non-*by name by address*)** langsung diproses dan dirilis secara mandiri oleh **Petugas Agen Statistik Desa** tanpa memerlukan tanda tangan basah Pj. Kepala Desa Sungai Bakau Kecil.

---

### 2. Sumber Data & Batasan Data Terpadu (Hanya Non-BNBA)

Data yang dapat diakses bersumber dari basis data hasil sensus dan pendataan potensi kewilayahan Program Desa Cantik 2026, dengan batasan ketat **hanya menyajikan data agregat**:

- **Basis Data Kependudukan & Sosial Ekonomi**: Rekapitulasi jumlah penduduk (gender, rasio jenis kelamin), jumlah kepala keluarga (KK), sebaran tingkat pendidikan, kepemilikan dokumen administrasi kependudukan/BPJS, status ketenagakerjaan, kelompok UMKM, dan sebaran agregat penerima bantuan sosial (PKH, BPNT, BST, BLT).
- **Basis Data Sarana, Prasarana, & Potensi Wilayah**: Pemetaan geospasial sarana peribadatan, pendidikan, kesehatan, fasilitas ekonomi, perkantoran pemerintah, kondisi fisik lingkungan, jalan, penerangan, dan jaringan telekomunikasi.
- **Produk Statistik Turunan**: Buku Publikasi *Desa Sungai Bakau Kecil Dalam Angka 2026*, Buku *Potensi Desa Sungai Bakau Kecil 2026*, Monografi Desa, dan Infografis Statistik Demografi format resolusi tinggi (HD).
- **Pemberitahuan Khusus**: Seluruh data individu perorangan/keluarga (*by name by address*) **tidak dapat dimohonkan** demi mematuhi prinsip kerahasiaan statistik dan privasi warga.

---

### 3. Saluran Layanan Permintaan Data (Dual-Channel Delivery)

Layanan penyediaan data statistik Desa Cantik Sungai Bakau Kecil diselenggarakan melalui 2 (dua) saluran resmi:

| Saluran Layanan | Jalur Akses | Sasaran Pengguna | Durasi Layanan | Jenis Output |
| :--- | :--- | :--- | :---: | :--- |
| **Jalur 1: Layanan Mandiri Digital** (*Self-Service Online*) | Portal Website Resmi (`desa-sm.dvlp.asia`) & Open Data REST API | Masyarakat umum, akademisi, peneliti, mahasiswa, media massa, dan OPD | **Instan (0 Menit)** | File Spreadsheet Excel (`.xlsx`), Naskah Buku Publikasi PDF, Monografi, Infografis HD, JSON API |
| **Jalur 2: Layanan Fasilitasi Cepat** (*Offline & WhatsApp*) | Loket Kantor Desa & WhatsApp Agen Statistik (`+62 815-4928-3541`) | Instansi pemerintah, mahasiswa, perencana, atau pemohon data disagregasi agregat | **15 s.d. 30 Menit** | Lembar Rekapitulasi Data Agregat Terverifikasi Petugas Agen Statistik Desa |

---

### 4. Prosedur Operasional Rinci

#### A. Jalur 1: Layanan Mandiri Digital (*Self-Service Direct Download & Open API*) — Instan (0 Menit)
Jalur ini ditujukan bagi publik, mahasiswa, akademisi, dan instansi yang memerlukan data terbuka tingkat agregat tanpa memerlukan surat pengantar atau verifikasi birokrasi manual:

1. **Akses Portal Website Resmi**:
   - Pemohon mengunjungi portal web Desa Cantik: `https://desa-sm.dvlp.asia/desa-cantik/desasungaibakaukecil`
2. **Pilih Menu Layanan dan Unduh Mandiri**:
   - **Dataset Excel (SDI)**: Masuk ke section *Daftar Potensi RT*, lalu klik tombol **"Unduh Data Tabel (Excel)"** untuk mendapatkan file spreadsheet lengkap (`.xlsx`).
   - **Buku Publikasi Digital**: Masuk ke section *Publikasi & Bukti Dukung*, klik **"Unduh Publikasi"** untuk mengunduh naskah PDF resmi Desa Dalam Angka atau Potensi Desa.
   - **Monografi & Infografis**: Masuk ke section *Produk Statistik & SOP*, klik **"Unduh Monografi"** atau **"Unduh Versi HD"** untuk materi infografis visual.
3. **Integrasi Open API (Bagi Pengembang / Sistem Eksternal)**:
   - Akses data terbuka terstruktur via REST API (JSON):
     - `https://desa-sm.dvlp.asia/desa-cantik/api/sungaibakaukecil` (format JSON terstandarisasi untuk integrasi aplikasi).

---

#### B. Jalur 2: Layanan Fasilitasi Cepat (*Offline & WhatsApp*) — 15 s.d. 30 Menit
Jalur ini ditujukan bagi pemohon yang memerlukan data disagregasi agregat khusus atau bantuan konsultasi teknis statistik, diproses langsung secara cepat oleh Petugas Agen Statistik Desa:

| Tahap | Pelaku | Aktivitas | Durasi | Output |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Pemohon Data | Mengajukan kebutuhan data agregat di loket Kantor Desa Sungai Bakau Kecil atau via WhatsApp Agen Statistik (`+62 815-4928-3541`). | 5 Menit | Permohonan Tercatat |
| **2** | Agen Statistik Desa | Memverifikasi bahwa data yang diminta adalah data agregat (non-*by name by address*). | 5 Menit | Permohonan Terverifikasi |
| **3** | Agen Statistik Desa | Melakukan ekstraksi rekapitulasi data dari basis data terpadu Desa Cantik. | 10 Menit | Berkas Rekapitulasi Data |
| **4** | Agen Statistik Desa | Menyerahkan lembar rekapitulasi data terverifikasi (file digital via WhatsApp/Email atau cetak langsung). | 5 Menit | Data Selesai Diterima |

---

### 5. Aturan Hak Akses & Keamanan Data Pribadi
1. **Wajib Non-*By Name By Address* (UU No. 27/2022)**: Data individu/mikro perorangan dan identitas keluarga bersifat rahasia dan **sama sekali tidak dapat diberikan kepada pemohon manapun** guna melindungi data pribadi penduduk.
2. **Level Diseminasi Legal**: Data yang dapat dilayani murni merupakan data agregat/makro tingkat Rukun Tetangga (RT), Dusun/RW, desa/kelurahan, atau sebaran fasilitas umum.
3. **Pemanfaatan Data**: Data hasil pembinaan Desa Cantik disediakan untuk perencanaan pembangunan, riset akademik, evaluasi program, dan perumusan kebijakan publik. Penggunaan untuk tujuan komersial wajib memperoleh izin tertulis dari Pemerintah Desa.

---

### 6. Pengesahan Dokumen SOP

Sungai Bakau Kecil, 6 Agustus 2026

**Menetapkan,**  
**Pj. Kepala Desa Sungai Bakau Kecil**

<br><br><br>

**<u>AGUS JUNAIDI</u>**
