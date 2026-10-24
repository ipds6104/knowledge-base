# Paparan Kondisi Nilai Tambah Bruto (NTB) SE2026 & Timeline Data Processing

> **Sumber Resmi**: Paparan Materi *"Kondisi NTB SE 2026"*, Jakarta, 22 Oktober 2026.  
> **Penyusun**: Bidang Analisis dan Pengawalan Kualitas Data, Tim Teknis SE2026 BPS RI.  
> **Arsip Berkas PDF**: [`kegiatan/sensus-ekonomi-2026/2026/docs/pdf/2026-10-22_Kondisi_NTB_SE2026.pdf`](pdf/2026-10-22_Kondisi_NTB_SE2026.pdf)  
> **Tautan Data Online**: `http://s.bps.go.id/KondisiNTB2026_Data` dan `http://s.bps.go.id/UpdateRasioSE2026`

---

## 1. Tujuan Data Processing SE2026

Pemrosesan data (*Data Processing*) merupakan tindak lanjut atas hasil pendataan lapangan dan evaluasi *data cleaning* untuk menghasilkan basis data yang dapat diolah sesuai dengan kaidah dan kebutuhan statistik:
1. **Mengeksplorasi Karakteristik & Pola Data**: Memahami struktur data serta mengidentifikasi anomali dan ketidakwajaran.
2. **Menangani Ketidaklengkapan & Ketidakwajaran Data**: Melalui editing, imputasi, dan metode pengolahan yang sesuai.
3. **Melakukan Reviu & Validasi**: Memastikan kelengkapan, konsistensi, dan kesesuaian informasi, serta penentuan tindak lanjut atas temuan selama pengolahan.
4. **Mendukung Penyusunan Tabulasi & Analisis Statistik**: Mempersiapkan tabulasi data sesuai kebutuhan dan tujuan analisis SE2026.

Tahap pengolahan pada Proses Bisnis Statistik (GSBPM) mencakup:
- Sub-proses 3.2: Pengklasifikasian dan Pengkodean
- Sub-proses 3.3: Reviu dan Validasi
- Sub-proses 3.4: Edit dan Imputasi

Aplikasi pengolahan resmi yang digunakan adalah **IPAS (*Integrated Processing and Analysis System*)**.

---

## 2. Timeline Kegiatan Data Processing SE2026

| Tahapan Kegiatan | Rentang Waktu | Penanggung Jawab / Keterangan |
|:---|:---|:---|
| **Pilot Data Processing** | 16–17 Oktober 2026 | Dilaksanakan oleh Direktorat Statistik Jasa BPS RI |
| **Workshop Data Processing** | 21–22 Oktober 2026 | Pembekalan satker pusat dan daerah |
| **Eksplorasi Data Processing dengan IPAS** | 23–25 Oktober 2026 | Uji coba fitur dan simulasi pengolahan daerah |
| **Penutupan Akses Fasih (Cut-Off)** | **25 Oktober 2026** | **Batas akhir sinkronisasi dan perbaikan data lapangan** |
| **Persiapan Environment IPAS** | 26–29 Oktober 2026 | Setup server dan migrasi data Fasih ke sistem IPAS |
| **Pelaksanaan Data Processing** | **30 Oktober – 15 November 2026** | **Periode utama pengolahan (~15 hari kalender)** |

---

## 3. Evaluasi Agregat Nilai Tambah & Benchmark Rasio

### A. Tren Penurunan Temuan Nilai Tambah Negatif
- Tren temuan agregat nilai tambah negatif secara nasional **turun 82,6%** (dari 167 temuan per 28 September menjadi **29 temuan** per 21 Oktober 2026 siang).
- *Catatan Kritis*: Masih terdapat wilayah yang memiliki agregat nilai tambah negatif. Daerah wajib memeriksa kembali apakah terdapat ketidaksesuaian antara rincian pendapatan dan pengeluaran usaha.

### B. Benchmark Rasio Nilai Tambah terhadap Output
- Benchmark Rasio NT/Output (PDB 2025): **0,5063**
- Benchmark Rasio NT/Output (Tabel IO 2020): **0,5243**
- **Posisi Kalimantan Barat (Provinsi 61)**:
  - 28 Sep: 0,6648
  - 14 Okt: 0,7369
  - 15 Okt: 0,7379
  - 18 Okt: 0,5611
  - 21 Okt: **0,5507** *(stabil dan mendekati benchmark nasional IO 2020)*

### C. Benchmark Rasio Upah terhadap Nilai Tambah
- Benchmark Rasio Upah/NT (Tabel IO 2016): **0,4490**
- Benchmark Rasio Upah/NT (Tabel IO 2020): **0,3861**
- **Posisi Kalimantan Barat (Provinsi 61)**:
  - Posisi 21 Okt: **0,1353** (relatif stabil, evaluasi nasional mencatat belum ada perbaikan berarti pada rasio upah di beberapa provinsi).

### D. Struktur Nilai Tambah SE2026 terhadap PDRB 2025
- Rasio agregat nilai tambah SE2026 terhadap PDRB 2025 Kalbar mencapai **80,18%** (Nilai Tambah SE2026 Rp263,46 Triliun dibandingkan PDRB 2025 Rp328,57 Triliun).

---

## 4. Anomali Kritis yang Perlu Penanganan Daerah

1. **KBLI Usaha di Luar Cakupan SE2026**:
   - Terdapat usaha dengan KBLI kategori non-cakupan SE2026 (seperti kategori P, R, S, T, U pemerintah atau kegiatan yang bukan sasaran SE).
   - Di Provinsi Kalimantan Barat tercatat beberapa kasus: Kategori P (2 kasus), R (87 kasus), S (1 kasus), T (57 kasus), U (9 kasus).
   - *Tindak Lanjut*: Lakukan pemeriksaan apakah KBLI sudah sesuai dengan aktivitas riil usaha atau salah entri kode.
2. **Sekolah & Fasilitas Kesehatan (Faskes) Negeri dengan Rincian Tidak Wajar**:
   - Ditemukan banyak entitas sekolah/faskes negeri dengan nilai tambah negatif besar karena pendapatan tercatat Rp0 atau sangat minim, sementara biaya produksi/operasional dan upah tercatat ratusan juta hingga miliaran rupiah.
   - *Tindak Lanjut*: Cermati kembali rincian pendapatan pemerintah/hibah/APBD (r27a) dan komponen pembiayaan operasional.
3. **Perusahaan Daerah Air Minum (PDAM) dengan Nilai Tambah Rendah**:
   - Dari 135 Perusahaan Daerah Air Minum yang teridentifikasi secara nasional, terdapat entitas dengan NTB negatif atau KBLI yang kurang tepat.
   - *Tindak Lanjut*: Verifikasi pendapatan (r27a), biaya produksi (r26b), biaya operasional (r26d), serta konsistensi KBLI untuk seluruh BUMD air minum.
4. **Perbandingan Pendapatan Utama (r27a) vs Pendapatan Lainnya (r27b)**:
   - Ditemukan usaha dengan selisih pendapatan ekstrem, di mana pendapatan lainnya jauh melebihi pendapatan utama (terindikasi tertukar kolom atau salah input nominal).
