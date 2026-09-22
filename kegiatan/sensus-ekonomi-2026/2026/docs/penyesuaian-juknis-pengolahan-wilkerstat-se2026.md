# Penyesuaian Petunjuk Teknis Pengolahan Wilkerstat SE2026

Dokumen ini memuat rangkuman terstruktur dan telaah teknis resmi atas materi **Penyesuaian Petunjuk Teknis Pengolahan Wilkerstat SE2026 (Pengolahan Master, Peta, Geotagging, dan Muatan)** yang diterbitkan oleh Tim Wilkerstat Direktorat Metodologi Statistik dan Sains Data (DIT. MMSD) BPS RI tertanggal **18 September 2026**.

Materi ini merupakan acuan operasional terbaru menyusul pengarahan virtual (Briefing Inda Pengolahan Wilkerstat SE2026) terkait simplifikasi alur kerja pengolahan geospasial pasca-lapangan Sensus Ekonomi 2026.

---

## 📋 Informasi Dokumen

* **Judul Materi**: Penyesuaian Petunjuk Teknis Pengolahan Wilkerstat SE2026 (Pengolahan Master, Peta, Geotagging, dan Muatan)
* **Penyusun**: Tim Wilkerstat, Direktorat Metodologi Statistik dan Sains Data - Badan Pusat Statistik RI
* **Tanggal Rilis**: Jakarta, 18 September 2026
* **Berkas Sumber**: `pdf/2026-09-18_Penyesuaian_Juknis_Pengolahan_Wilkerstat.pdf` (12 Slide)

---

## 🚀 Ringkasan Perubahan Pokok (Core Adjustments)

Terdapat 3 (tiga) simplifikasi fundamental dalam pengolahan Wilkerstat SE2026 di tingkat BPS Kabupaten/Kota:

1. **Fokus Titik Bangunan Hanya pada SLS Berubah (PSLS)**:
   * *Sebelumnya*: Pengolahan titik geotagging direncanakan untuk seluruh SLS/Sub-SLS.
   * *Penyesuaian*: Pengolahan titik geotagging **hanya dilakukan pada SLS/Sub-SLS yang mengalami Perubahan pada Lapangan SE2026 (PSLS)**.
   * Model QGIS pengolahan titik dipangkas: **hanya menggunakan 2 model pengolahan**.

2. **Pengolahan Muatan Dialihkan Sepenuhnya ke BPS Pusat**:
   * *Sebelumnya*: Beban pengolahan dan perhitungan muatan bangunan/keluarga/usaha berada di BPS Kabupaten/Kota.
   * *Penyesuaian*: **Pengolahan muatan dilakukan seluruhnya oleh BPS Pusat**. BPS Pusat akan membandingkan muatan periode `2026_1` dengan `2025_2`, lalu mengeluarkan daftar (*list*) SLS/Sub-SLS anomali yang perlu diverifikasi ulang oleh BPS Kab/Kota.

3. **Penyediaan Tool Otomasi Python dari Pusat untuk Distribusi Beban Kerja**:
   * Mengingat volume data geotagging SE2026 yang masif, BPS Pusat menyediakan skrip Python otomasi beserta petunjuk teknisnya untuk memotong (*splitting*) data dan membungkusnya ke dalam arsip `.zip` per petugas pengolahan.

---

## 🔄 Matriks Perbandingan Alur Pengolahan

| Komponen Alur | Kondisi Sebelumnya | Kondisi Penyesuaian (Juknis 18 Sept 2026) |
| :--- | :--- | :--- |
| **Cakupan Titik Geotagging** | Seluruh SLS/Sub-SLS tanpa kecuali. | **Hanya pada SLS/Sub-SLS yang mengalami Perubahan Batas (PSLS)** pada lapangan SE2026. |
| **Input Peta Dasar Titik** | Peta Lapangan SE2026 (Periode 2025 Semester 2). | Peta Lapangan SE2026 (2025 Semester 2) yang **sudah diedit di awal** jika terdapat perubahan batas di SE2026 (bukan pecah-gabung). |
| **Model QGIS Pengolahan Titik** | Kompleks multi-tahap (identifikasi, cek, update, muatan). | **Hanya menggunakan 2 Model Pengolahan Titik**. |
| **Pengolahan Muatan** | Dihitung manual/model oleh Kab/Kota. | **100% dilakukan BPS Pusat** setelah Kab/Kota unggah Peta Geotagging Koreksi & Peta Digital 2026_1. |
| **Unggah ke Geospatial System (GS)** | Titik sesuai kondisi lapangan sebelum editing. | **Titik hasil koreksi/editing** diunggah kembali ke GS (jumlah record wajib sama persis dengan unduhan awal). |

---

## 📍 Struktur Data Geotagging SE2026

### 1. Struktur Variabel Input Geotagging
Data mentah hasil geotagging SE2026 dari FASIH memuat atribut:
* `assignment_id`: Kode unik assignment usaha, keluarga, dan bangunan.
* `unique_bang`: ID unik per fisik bangunan.
* `level_6_full_code`: Kode ID Sub-SLS periode 2025 Semester 2 (16 digit).
* `no_bang`: Nomor urut fisik bangunan SE2026 per SLS.
* `geotagg_latitude`: Titik koordinat lintang.
* `geotagg_longitude`: Titik koordinat bujur.
* `kode_bang_value`: Kode penggunaan bangunan (1 = Usaha, 2 = Tempat Tinggal, 3 = Campuran, dst.).

### 2. Ketentuan Khusus Titik Lapangan:
* **Cut-Off Data**: Data geotagging SE2026 final yang digunakan adalah kondisi per **30 September 2026**.
* **Kawasan Khusus (Mal / Pasar / Ruko Bertingkat)**:
  * Pada kawasan yang memiliki banyak nomor bangunan tetapi secara fisik hanya terdiri dari satu gedung/bangunan besar, jika titik terdeteksi salah oleh model QGIS padahal posisinya sudah benar, **tidak perlu digeser**.
  * Cukup ubah nilai atribut **`flag_repair = 0`**.
* **Integritas Jumlah Titik**: Jumlah titik hasil koreksi yang diunggah ke GS **wajib sama persis** dengan jumlah titik awal yang diunduh (tidak boleh ada titik yang terhapus secara tidak sengaja).

---

## 📊 Skema Atribut Akhir Peta Geotag (Upload ke Geospatial System)

Peta titik geotagging hasil editing yang akan diunggah ke Geospatial System (GS) wajib memiliki skema 22 atribut berikut:

| No | Nama Atribut | Tipe Data | Keterangan & Aturan Pengisian |
| :---: | :--- | :--- | :--- |
| 1 | `assignment_id` | Text (string) | Kode unik tagging per-keluarga / assignment |
| 2 | `flag_repair` | Integer (32-bit) | Status posisi titik terhadap batas SLS: `0` = Berada dalam batas, `1` = Berada di luar batas |
| 3 | `flag_position` | Integer (32-bit) | Status pergeseran posisi: `0` = Tidak digeser, `1` = Posisi digeser saat editing |
| 4 | `idsubsls_origin` | Text (string) | ID Sub-SLS seharusnya sesuai hasil SE2026 (master 2025 Semester 2) |
| 5 | `idsubsls_edited` | Text (string) | ID Sub-SLS yang menempel pada peta SLS yang digunakan di lapangan |
| 6 | `latitude_origin` | Decimal (double) | Koordinat latitude sebelum editing/pergeseran |
| 7 | `longitude_origin` | Decimal (double) | Koordinat longitude sebelum editing/pergeseran |
| 8 | `latitude_edited` | Decimal (double) | Koordinat latitude setelah editing/pergeseran |
| 9 | `longitude_edited` | Decimal (double) | Koordinat longitude setelah editing/pergeseran |
| 10 | `no_bang` | Integer (32-bit) | Nomor bangunan fisik unik per SLS/Sub-SLS |
| 11 | `kode_bang_value` | Integer (32-bit) | Jenis bangunan (`1` = Usaha, `2` = Tempat Tinggal, `3` = Campuran, dst.) |
| 12 | `kdprov` | Text (string) | Kode Provinsi (misal: `61`) |
| 13 | `nmprov` | Text (string) | Nama Provinsi (`KALIMANTAN BARAT`) |
| 14 | `kdkab` | Text (string) | Kode Kabupaten/Kota (`04`) |
| 15 | `nmkab` | Text (string) | Nama Kabupaten/Kota (`MEMPAWAH`) |
| 16 | `kdkec` | Text (string) | Kode Kecamatan (`101`, dst.) |
| 17 | `nmkec` | Text (string) | Nama Kecamatan |
| 18 | `kddesa` | Text (string) | Kode Desa/Kelurahan (`007`, dst.) |
| 19 | `nmdesa` | Text (string) | Nama Desa/Kelurahan |
| 20 | `idsls` | Text (string) | ID SLS sesuai peta lapangan SE2026 (14 digit) |
| 21 | `nmsls` | Text (string) | Nama SLS sesuai peta lapangan SE2026 |
| 22 | `sls` | Text (string) | Nama SLS sesuai atribut titik bangunan |

---

## 📦 Alur Pengolahan Muatan Terpusat (Centralized Load Processing)

Alur perhitungan muatan baru SE2026:
```
[BPS Kab/Kota]
  ├─ Unggah Peta Digital Periode 2026_1
  └─ Unggah Peta Geotagging Hasil Koreksi
          │
          ▼ (Geospatial System)
[BPS Pusat]
  ├─ Eksekusi Pengolahan Muatan Otomatis
  ├─ Perhitungan Muatan 2026_1 vs 2025_2
  └─ Penerbitan List SLS/Sub-SLS Perlu Verifikasi
          │
          ▼ (Shared Link)
[BPS Kab/Kota & Provinsi]
  └─ Verifikasi Lapangan / Konfirmasi Anomali Muatan
          │
          ▼
[Hasil Akhir]
  └─ Master Wilkerstat 2026 Semester 1 dengan Muatan Terverifikasi
```

---

## 📅 Timeline Operasional Pengolahan Wilkerstat SE2026

```
30 Sep 2026  : Batas akhir perubahan Master di FRS (Surat B-362) & Estimasi Closing Data Lapangan SE2026
01 - 03 Okt  : Finalisasi & transfer data geotagging SE2026 dari FASIH ke Tim Wilkerstat BPS Pusat
04 - 09 Okt  : Preprocessing & splitting data geotagging serta finalisasi pengolahan Master 2026_1 di BPS Pusat
10 - 12 Okt  : Estimasi tersedianya data Geotagging SE2026 di Geospatial System (GS) *)
01 - 12 Okt  : Operasional Awal BPS Kab/Kota:
               • Scanning peta sketsa lapangan, identifikasi perubahan SLS, georeferencing
               • Pengolahan perubahan batas (edit batas di awal pada peta 2025_2)
13 Okt - 06 Nov : Pengolahan Utama BPS Kab/Kota:
               • Pengolahan Geotagging (hanya pada SLS/Sub-SLS yang berubah batas / PSLS dengan 2 Model QGIS)
               • Pengolahan Peta Digital (pemekaran, penggabungan, cleaning topologi, dan validasi)
23 Okt - 20 Nov : Unggah Peta Digital Periode 2026 Semester 1 ke Geospatial System (BPS Kab/Kota)
               • DEADLINE MAKSIMAL UPLOAD PETA DIGITAL: 20 November 2026
02 - 20 Nov  : Rekonsiliasi Batas Antar Kab/Kota dan Provinsi (Daring)
02 - 27 Nov  : Approval dan Checking Peta Digital di Geospatial System oleh BPS Provinsi
               • BATAS MAKSIMAL APPROVAL PETA DIGITAL: 27 November 2026
16 Nov - 04 Des : Unggah Peta Geotagging Hasil Koreksi ke Geospatial System (BPS Kab/Kota)
               • BATAS MAKSIMAL UPLOAD GEOTAGGING: 04 Desember 2026
01 - 18 Des  : Cleaning Akhir di BPS Pusat, Pengolahan Muatan Terpusat oleh BPS Pusat, dan Verifikasi Muatan oleh Kab/Kota
               • Master Wilkerstat Periode 2026 Semester 1 Final rilis 18 Desember 2026
```
*(Catatan: Timeline dapat berubah sewaktu-waktu menyesuaikan ketersediaan dan kesiapan data SE2026)*

---

## 👥 Matriks Pembagian Peran Satuan Kerja

### 1. BPS Kabupaten / Kota (Kab. Mempawah)
* Mengidentifikasi SLS yang mengalami perubahan batas (PSLS) hasil lapangan SE2026.
* Mengedit peta digital SLS 2025_2 untuk batas yang berubah (bukan pecah-gabung).
* Menjalankan 2 Model QGIS Pengolahan Titik untuk SLS yang berubah (PSLS).
* Mengunggah Peta Digital 2026 Semester 1 ke GS paling lambat **20 November 2026** (periode unggah: 23 Okt – 20 Nov).
* Mengunggah Peta Geotagging Hasil Koreksi ke GS paling lambat **04 Desember 2026** (periode unggah: 16 Nov – 04 Des).
* Mengikuti rekonsiliasi batas antar-kabupaten/kota dan provinsi secara daring (02 – 20 Nov).
* Melakukan verifikasi anomali muatan berdasarkan daftar yang dirilis BPS Pusat.

### 2. BPS Provinsi (Kalimantan Barat)
* Koordinasi, pemantauan, dan asistensi teknis pengolahan peta & geotagging di satker kab/kota.
* Rekonsiliasi batas wilayah antar-kabupaten/kota dalam provinsi dan antar-provinsi.
* Approval dan pengecekan kelayakan peta digital di Geospatial System (maksimal **27 November 2026**).
* Monitoring kelengkapan unggah peta digital, peta geotagging, dan verifikasi muatan.

### 3. BPS Pusat (Dit. Metodologi Statistik & Sains Data)
* Preprocessing dan transfer data geotagging dari FASIH ke Geospatial System.
* Penyediaan skrip Python tools pembagi beban kerja mitra pengolahan.
* Pemrosesan dan perhitungan seluruh muatan SLS SE2026 secara terpusat.
* Evaluasi rekonsiliasi batas wilayah nasional.
* Cleaning akhir peta dan rilis Master Wilkerstat Periode 2026 Semester 1 final (hingga 18 Desember 2026).

---

## 📂 Berkas Terkait

* **Salinan PDF Resmi**: [`pdf/2026-09-18_Penyesuaian_Juknis_Pengolahan_Wilkerstat.pdf`](pdf/2026-09-18_Penyesuaian_Juknis_Pengolahan_Wilkerstat.pdf)
* **Dokumen Rujukan Terkait**:
  * [Surat Perubahan Jumlah Petugas & Moda Pelatihan Wilkerstat SE2026](surat-perubahan-petugas-dan-moda-pelatihan-wilkerstat-se2026.md)
  * [Surat Pelatihan Petugas Pengolahan Wilkerstat SE2026](surat-pelatihan-petugas-pengolahan-wilkerstat-se2026.md)
  * [Katalog Materi Pengolahan Wilkerstat SE2026 (10 Modul)](../materi-pengolahan/README.md)
