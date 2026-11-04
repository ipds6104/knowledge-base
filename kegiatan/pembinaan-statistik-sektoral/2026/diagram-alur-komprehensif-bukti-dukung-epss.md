# PANDUAN KOMPREHENSIF ALUR PENYELENGGARAAN STATISTIK SEKTORAL & PENGELOLAAN BUKTI DUKUNG EPSS
## Dari Perencanaan, Rekomendasi ROMANTIK, Metadata INDAH, Diseminasi Portal SDI, hingga SIMBATIK & SPESIAL

> **Kode Dokumen:** `PSS2026-ALUR-BUKTI-DUKUNG`  
> **Sasaran:** Seluruh Tim Pembina BPS, Tim Walidata Diskominfo, dan Operator Data 23 Organisasi Perangkat Daerah (OPD) Kabupaten Mempawah.  
> **Prinsip Utama:** *"Effort Sekecil Mungkin, Nilai Kematangan (IPS EPSS) Setinggi Mungkin"*.

---

## 🗺️ 1. Diagram ASCII Alur Kerja End-to-End & Repositori Bukti

```text
+=======================================================================================================================+
|                                    ALUR KOMPREHENSIF PENYELENGGARAAN & EVALUASI STATISTIK SEKTORAL                    |
|                                            PEMERINTAH KABUPATEN MEMPAWAH - BPS KAB. MEMPAWAH                          |
+=======================================================================================================================+

 [ FASE 1: PERENCANAAN ]            [ FASE 2: PENGUMPULAN & OLAH ]           [ FASE 3: DISEMINASI ]         [ FASE 4: EVALUASI ]
=========================          ================================          ======================         ====================

  ORGANISASI PERANGKAT                ORGANISASI PERANGKAT                    PORTAL SATU DATA              TIM PENILAI (TPI/TPB)
     DAERAH (OPD)                        DAERAH (OPD)                         KABUPATEN MEMPAWAH
+-----------------------+          +-----------------------+               +----------------------+       +-----------------------+
| 1. Susun Rencana /    |          | 4. Pengumpulan &      |               | 7. Walidata Periksa  |       | 10. Pengunggahan      |
|    DPA / KAK Kegiatan |          |    Pembersihan Data   |               |    Kelayakan Data    |       |     Bukti ke SIMBATIK |
|    (Ada Jadwal Rilis) |          |    (Data Cleaning)    |               |    & Beri Persetujuan|       |     (TPI Pemkab)      |
+-----------+-----------+          +-----------+-----------+               +----------+-----------+       +-----------+-----------+
            |                                  |                                      |                               |
            v                                  v                                      v                               v
+-----------------------+          +-----------------------+               +----------------------+       +-----------------------+
| 2. Input Identifikasi |          | 5. Verifikasi Akurasi |               | 8. Publikasi Data &  |       | 11. Penilaian EPSS    |
|    & Kamus SDS        |          |    & Validasi Rumus   |               |    Metadata Terbuka  |       |     (TPB Penilai BPS) |
|    di GSheets Master  |          |    (Completeness)     |               |    (.csv, .xlsx, API)|       |     (38 Indikator)    |
+-----------+-----------+          +-----------+-----------+               +----------+-----------+       +-----------+-----------+
            |                                  |                                      |                               ^
            |                                  |                                      |                               |
            +-------------------+--------------+--------------------------------------+                               |
                                |                                                                                     |
                                v                                                                                     |
                   [ APLIKASI NASIONAL BPS & PEMDA ]                                                                  |
                   =================================                                                                  |
                   +-----------------------------------------------+                                                  |
                   | • INDAH / ROMANTIK BPS: indah.bps.go.id       |                                                  |
                   |   (Pengajuan Rekomendasi & Metadata MS-Keg)   |                                                  |
                   |                                               |                                                  |
                   | • PORTAL SDI DAERAH: satudata.mempawahkab.go.id|                                                 |
                   |   (Unggah Dataset, Visualisasi, API CKAN)     |                                                  |
                   |                                               |                                                  |
                   | • APLIKASI SPESIAL: spesial.web.bps.go.id     |                                                  |
                   |   (Perekaman TPSS Pembinaan BPS: IKU Satker)  |                                                  |
                   +-----------------------+-----------------------+                                                  |
                                           |                                                                          |
                                           v                                                                          |
                      [ PENGAMBILAN BUKTI (TANGKAPAN LAYAR / SS) ]                                                    |
                      ============================================                                                    |
                      1. Screenshot Bukti Registrasi ROMANTIK (Nomor K-26.6104...)                                    |
                      2. Screenshot Formulir Metadata MS-Keg & MS-Var di INDAH                                        |
                      3. Screenshot Status Dataset & API di Portal Satu Data                                          |
                      4. Screenshot Formula / Tabel Agregasi Excel (Bebas Salah Hitung)                               |
                      5. Surat / Dokumen Rutin Dinas (SK Tim, KAK, Pakta Integritas)                                  |
                                           |                                                                          |
                                           v                                                                          |
                      [ BLANGKO DOKUMEN BUKTI DUKUNG BER-KOP (1-2 HAL) ]                                              |
                      ==================================================                                              |
                      • Menggunakan Lembar Blangko Rapi ber-KOP Dinas Resmi.                                          |
                      • Operator HANYA menempelkan (paste) screenshot ke kotak.                                       |
                      • Dilengkapi: Tanggal, URL, Keterangan Bukti, & Paraf Pejabat.                                 |
                                           |                                                                          |
                                           +--------------------------------------------------------------------------+
                                           |
                                           v
+=====================================================================================================================+
|                                      STRUKTUR PENYIMPANAN CLOUD RESMI (GOOGLE DRIVE)                                |
+=====================================================================================================================+
|                                                                                                                     |
|  FOLDER MASTER GOOGLE DRIVE PSS 2026: (drive.google.com/.../1EyGVm_2DHLPsDBoHdwpGftk5yHgaJVtV)                     |
|  ├── 📁 01_DOMAIN_1_PRINSIP_SDI/                                                                                    |
|  │   ├── 📄 10101_Lembar_Standar_Data_Statistik_SDS_[OPD].pdf (Blangko + SS Kamus SDS)                             |
|  │   └── 📄 10201_Lembar_Metadata_Statistik_[OPD].pdf (Blangko + SS INDAH BPS)                                      |
|  ├── 📁 02_DOMAIN_2_KUALITAS_DATA/                                                                                  |
|  │   ├── 📄 20201_Lembar_Pemeriksaan_Akurasi_[OPD].pdf (Blangko + SS Cleaning Excel & Uji Petik)                     |
|  │   ├── 📄 20301_Lembar_Komitmen_Jadwal_Rilis_[OPD].pdf (KAK Rutin DPA + SS Jadwal)                                |
|  │   ├── 📄 20302_Lembar_Pemantauan_Waktu_Rilis_[OPD].pdf (Blangko + SS Tayang Portal SDI)                         |
|  │   └── 📄 20502_Lembar_Konsistensi_Data_[OPD].pdf (Tabel Runtun Waktu 5 Tahun Dinas)                              |
|  ├── 📁 03_DOMAIN_3_PROSES_BISNIS/                                                                                  |
|  │   ├── 📄 30101_Kerangka_Acuan_Kerja_KAK_[OPD].pdf (KAK DPA Dinas Ber-jadwal)                                     |
|  │   └── 📄 30302_Bab_Ulasan_Narasi_Analisis_[OPD].pdf (Laporan / Publikasi Dinas Ber-Grafik)                       |
|  ├── 📁 04_DOMAIN_4_KELEMBAGAAN/                                                                                    |
|  │   ├── 📄 40102_Surat_Komitmen_Netralitas_[OPD].pdf (Pakta Integritas / Surat Pernyataan)                         |
|  │   ├── 📄 40103_Lembar_Verifikasi_Mutu_Walidata.pdf (Paraf / Rekomendasi Diskominfo)                             |
|  │   └── 📄 40302_Paket_Forum_SDI_Mempawah_2026.pdf (Undangan Sekda + Daftar Hadir MCC + Notula)                   |
|  └── 📁 05_DOMAIN_5_STATISTIK_NASIONAL/                                                                             |
|      ├── 📄 50101_Pemanfaatan_Data_Dasar_LPPD.pdf (Ekstrak Bab LPPD / RPJMD Mempawah)                               |
|      └── 📄 50201_Surat_Rekomendasi_ROMANTIK_BPS.pdf (Surat Rekomendasi Resmi BPS)                                  |
|                                                                                                                     |
+=====================================================================================================================+
                                           |
                                           v
                       [ INTEGRASI KE APLIKASI PENILAIAN NASIONAL ]
                       ============================================
             +--------------------------------------------------------------+
             | 1. SIMBATIK EPSS (simbatik.bps.go.id):                       |
             |    • TPI mengunggah file PDF / link Google Drive folder.     |
             |    • Format Narasi SIMBATIK 3 Baris:                         |
             |      (i) Narasi Relevansi & Ringkasan Dokumen                |
             |      (ii) Nama File PDF di Google Drive                      |
             |      (iii) Nomor Halaman Dokumen                             |
             |                                                              |
             | 2. SPESIAL BPS (spesial.web.bps.go.id):                      |
             |    • BPS mengunggah link drive dokumen pembinaan untuk       |
             |      mengunci capaian TPSS Satker 6104 (Target IKU: 99.09).  |
             +--------------------------------------------------------------+
```

---

## 📌 2. Penjelasan 4 Fase Penyelenggaraan Statistik Sektoral

### Fase 1: Perencanaan & Legalitas Awal (Hulu)
1. **Kegiatan Rutin Dinas (DPA/KAK)**:
   - Setiap OPD menyelenggarakan kegiatan pengumpulan data berbasis anggaran yang sudah ada (DPA).
   - *Kunci Utama:* Di dalam KAK atau jadwal dinas, wajib ada klausul bulan/tanggal publikasi data dirilis ke publik.
2. **Identifikasi & Pengajuan Rekomendasi (ROMANTIK)**:
   - OPD mengidentifikasi kegiatan statistik sektoralnya (Sensus, Survei, atau Kompilasi Produk Administrasi/KOMPROMIN) pada Google Sheets Master Radar (Form LK-01).
   - Mengajukan permohonan Rekomendasi Kegiatan Statistik ke BPS melalui portal **INDAH BPS** (`https://indah.bps.go.id/`).
3. **Penyusunan Metadata Statistik**:
   - Mendaftarkan formulir Metadata Kegiatan (MS-Keg) dan Metadata Variabel (MS-Var) pada portal INDAH.

### Fase 2: Pengumpulan, Pemeriksaan Akurasi, & Pengolahan Data
1. **Pengumpulan Data Lapangan / Administrasi**:
   - Pengumpulan data dari unit sumber (faskes, sekolah, perusahaan mitra, kecamatan/desa).
2. **Pemeriksaan Akurasi Data (Data Cleaning)**:
   - Memastikan kelengkapan (*completeness*), menghapus data ganda (*de-duplication*), dan mengunci rumus Excel (*formula validation*).
   - *Bukti Fisik:* Tangkapan layar spreadsheet/aplikasi saat proses validasi rumus dan foto kunjungan dinas ke lapangan.

### Fase 3: Diseminasi Melalui Walidata Daerah (Portal SDI)
1. **Penyerahan ke Walidata (Dinas Kominfo)**:
   - Produsen data menyampaikan dataset tabular beserta metadatanya kepada Walidata Daerah.
2. **Verifikasi Mutu oleh Walidata**:
   - Walidata memeriksa kesesuaian 4 Prinsip Satu Data Indonesia (Standar Data, Metadata, Interoperabilitas, Kode Referensi).
3. **Penayangan Terbuka**:
   - Dataset ditayangkan pada **Portal Satu Data Indonesia Kabupaten Mempawah** (`https://satudata.mempawahkab.go.id/`) dalam format terbuka (.csv, .xlsx) dan API.

### Fase 4: Evaluasi EPSS & Pelaporan TPSS (Hilir)
1. **Pengunggahan ke SIMBATIK EPSS**:
   - Tim Penilai Internal (TPI Diskominfo/BPS) mengunggah tautan Google Drive dan berkas bukti dukung untuk dinilai oleh Tim Penilai Badan (TPB BPS).
2. **Perekaman Capaian TPSS di SPESIAL**:
   - Tim Pembina BPS mengunggah bukti pelaksanaan pembinaan (notula, daftar hadir, surat tugas, capaian aliran data) untuk mengamankan nilai IKU Satker 6104.

---

## 📄 3. Standar Format "Blangko Bukti Dukung Berbasis Screenshot"

Untuk mencegah penolakan bukti oleh asesor (akibat screenshot mentah tanpa KOP) dan mencegah beban mengetik laporan panjang bagi operator OPD, seluruh bukti tangkapan layar ditempelkan pada **Blangko 1 Halaman Ber-KOP Resmi** berikut:

```markdown
PEMERINTAH KABUPATEN MEMPAWAH
DINAS / BADAN ..............................................................
Kompleks Perkantoran Pemerintah Kabupaten Mempawah, Jl. Raden Kusno, Mempawah, Kalimantan Barat
Pos-el: dinas@mempawahkab.go.id
-------------------------------------------------------------------------------------------------

LEMBAR BUKTI DUKUNG PENYELENGGARAAN STATISTIK SEKTORAL
INDIKATOR [KODE]: [NAMA INDIKATOR EPSS]

1. Nama Produsen Data    : Dinas / Badan .......................................................
2. Nama Kegiatan Data    : Kompilasi Data [Objek Data] Kabupaten Mempawah Tahun 2026
3. Aplikasi / Sistem     : Portal INDAH BPS / Portal Satu Data Mempawah / Aplikasi Internal
4. Tanggal Pelaksanaan   : .....................................................................

TANGKAPAN LAYAR (SCREENSHOT) BUKTI FAKTUAL:
+-----------------------------------------------------------------------------------------------+
|                                                                                               |
|                                                                                               |
|                         [ TEMPELKAN TANGKAPAN LAYAR SCREENSHOT ]                              |
|                                        DI SINI                                                |
|                                                                                               |
|                                                                                               |
+-----------------------------------------------------------------------------------------------+

Keterangan Teknis Bukti Gambar:
Tangkapan layar di atas membuktikan bahwa [Nama Produsen Data] telah melaksanakan [Nama Aktivitas /
Pendaftaran Metadata / Pengajuan Rekomendasi / Pembersihan Rumus Excel] secara riil pada sistem
[Nama Sistem] dengan nomor registrasi / status: ............................................... .

Mempawah, .............................. 2026
Petugas Pengelola / Entri Data,             Mengetahui Pejabat Pengawas / Kepala Bidang,
(tanda tangan)                              (tanda tangan basah & cap dinas)



[NAMA PETUGAS OPERATOR]                     [NAMA KEPALA BIDANG LENGKAP]
NIP. ...................................    NIP. .......................................
```

---

## 📝 4. SOP Penulisan Narasi Bukti Dukung di SIMBATIK (Wajib 3 Poin)

Sesuai Petunjuk Teknis Penilaian EPSS dari BPS Pusat, setiap pengunggahan bukti dukung di aplikasi **SIMBATIK** wajib memuat narasi dalam 3 baris terpisah:

1. **Baris 1 (i)**: Narasi penjelasan relevansi indikator dengan bukti dukung, serta ringkasan isi file.
2. **Baris 2 (ii)**: Nama File bukti dukung yang diunggah (bila tautan Google Drive, sebutkan nama file PDF-nya).
3. **Baris 3 (iii)**: Nomor halaman yang dimaksud (bila file multi-halaman).

#### Contoh Konkret Pengisian Narasi SIMBATIK:
```text
(i) Dokumen lembar bukti dukung menunjukkan bahwa Dinas Penanaman Modal telah mendaftarkan rancangan kegiatan statistik dan metadata variabel pada sistem INDAH BPS serta memperoleh status terverifikasi.
(ii) 10201_Lembar_Metadata_Statistik_DPMPTSPKUKM.pdf
(iii) Halaman 1-2
```

---

## 🔗 Tautan Terkait
*   [Matriks Rubrik 38 Indikator EPSS (Google Sheets)](https://docs.google.com/spreadsheets/d/1_sdYBPe1SYX8UY0HeVuuwX7L9gWalk03_b2XVyFx1IQ/edit)
*   [Folder Bank Template Dokumen Resmi (Google Drive)](https://drive.google.com/drive/folders/11WSZICmBrfZrE5AwhPjNKj5mks2NvE2i)
*   [Folder Master Bukti Dukung PSS 2026 (Google Drive)](https://drive.google.com/drive/folders/1EyGVm_2DHLPsDBoHdwpGftk5yHgaJVtV)
*   [README Pembinaan Statistik Sektoral 2026](README.md)
*   [README Evaluasi EPSS 2026](../../evaluasi-epss/2026/README.md)

