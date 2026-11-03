---
nama: "Data Processing SE2026"
kategori: "pengolahan"
rutinitas: "non-rutin"
frekuensi: "10-tahunan"
peran: "anggota"
status: "aktif"
deadlines:
  - tanggal: "2026-10-22"
    kegiatan: "Workshop Data Processing SE2026 (21–22 Oktober 2026)"
    status: "selesai"
  - tanggal: "2026-10-25"
    kegiatan: "Batas Akhir Eksplorasi Data Processing dengan IPAS (23–25 Oktober 2026)"
    status: "belum"
  - tanggal: "2026-10-25"
    kegiatan: "Penutupan Akses Fasih SE2026 (Cut-Off Sinkronisasi Data Lapangan)"
    status: "belum"
  - tanggal: "2026-10-29"
    kegiatan: "Selesai Persiapan Environment IPAS (26–29 Oktober 2026)"
    status: "belum"
  - tanggal: "2026-10-30"
    kegiatan: "Batas Akhir Penyelesaian Anomali & Cleaning SE2026 (Flag 3 NTB, KBLI, Sosek)"
    status: "belum"
  - tanggal: "2026-10-30"
    kegiatan: "Mulai Pelaksanaan Data Processing SE2026 via IPAS (30 Oktober – 15 November 2026)"
    status: "belum"
  - tanggal: "2026-11-15"
    kegiatan: "Batas Akhir Pelaksanaan Data Processing SE2026 via IPAS"
    status: "belum"
---

# Data Processing SE2026 (Pemanfaatan Aplikasi IPAS)

> [!IMPORTANT]
> **Dasar Informasi**: Paparan Workshop Data Processing SE2026 oleh BPS RI / Dit. Statistik Jasa.  
> **Aplikasi Pengolahan**: **IPAS (*Integrated Processing and Analysis System*)**.  
> **Jadwal Pelaksanaan Lapangan/Pengolahan**: **30 Oktober – 15 November 2026 (~15–17 hari kalender)**.  
> **Arsip Salinan Slide**: `knowledge/assets/Timeline_Data_Processing_SE2026_IPAS.jpg`.

---

## 1. Deskripsi & Ruang Lingkup Pengolahan

Pemrosesan Data (*Data Processing*) SE2026 adalah tahapan tindak lanjut atas pendataan lapangan dan pembersihan anomali (*data cleaning*) untuk menghasilkan dataset SE2026 yang bersih, konsisten, dan siap ditabulasi.

Proses pengolahan meliputi:
- **Eksplorasi Karakteristik Data**: Memeriksa sebaran dan mendeteksi anomali/pencilan.
- **Validasi & Reviu**: Memastikan konsistensi antar-variabel (termasuk anomali nilai tambah agregat).
- **Klasifikasi & Pengkodean**: Standardisasi KBLI / KBJI / kode komoditas.
- **Editing & Imputasi**: Penanganan nilai kosong atau inkonsisten.
- **Tabulasi & Analisis**: Pembentukan tabel agregasi statistik.

---

## 2. Rincian Milestone & Jadwal Kritis

| No | Tahap / Milestone | Tanggal | Keterangan & Tindak Lanjut |
|:---|:---|:---|:---|
| 1 | **Pilot Data Processing** | 16–17 Oktober 2026 | Pilot pengolahan oleh Dit. Statistik Jasa BPS RI |
| 2 | **Workshop Data Processing** | 21–22 Oktober 2026 | Pembekalan alur kerja pengolahan untuk satker daerah |
| 3 | **Eksplorasi Data Processing IPAS** | 23–25 Oktober 2026 | Trial sistem IPAS dan uji coba fungsionalitas |
| 4 | **Penutupan Akses Fasih (Cut-Off)** | **25 Oktober 2026** | **KRITIS**: Pastikan pembersihan data anomali di Fasih tuntas |
| 5 | **Persiapan Environment IPAS** | 26–29 Oktober 2026 | Setup database & migrasi data Fasih ke server IPAS |
| 6 | **Pelaksanaan Data Processing IPAS** | **30 Okt – 15 Nov 2026** | **Pelaksanaan Inti (~15 hari)** pengolahan data SE2026 di IPAS |

---

## 3. Catatan Pengawasan Mutu & Anomali
- **Anomali Nilai Tambah Negatif**: BPS RI mencatat penurunan 82,6% anomali secara nasional (dari 167 menjadi 29 per 21 Oktober). Daerah wajib memastikan pendapatan dan pengeluaran usaha telah seimbang dan wajar.
- **Benchmark Rasio NT/Output**: PDB 2025 (0,5063) dan Tabel IO 2020 (0,5243).

### 3.1 Parameter Batas Ambang (Threshold) Anomali Flag 3 per Kategori KBLI
Pemeriksaan anomali Flag 3 (Rasio NTB / Output) menggunakan batas bawah (`min_threshold`) dan batas atas (`max_threshold`) yang spesifik per Kategori KBLI:

| Kategori KBLI | Deskripsi Singkat Sektor | Batas Bawah (`min_threshold`) | Batas Atas (`max_threshold`) |
|:---:|:---|:---:|:---:|
| **A** | Pertanian, Kehutanan, Perikanan | 0,513439 (51,3%) | 0,939247 (93,9%) |
| **B** | Pertambangan & Penggalian | 0,284912 (28,5%) | 0,812709 (81,3%) |
| **C** | Industri Pengolahan | 0,150841 (15,1%) | 0,608632 (60,9%) |
| **D** | Pengadaan Listrik & Gas | 0,126166 (12,6%) | 0,684314 (68,4%) |
| **E** | Pengelolaan Air & Sampah | 0,289389 (28,9%) | 0,468601 (46,9%) |
| **F** | Konstruksi | 0,335258 (33,5%) | 0,441865 (44,2%) |
| **G** | Perdagangan Besar & Eceran | 0,640878 (64,1%) | 0,776476 (77,6%) |
| **H** | Pengangkutan & Pergudangan | 0,294401 (29,4%) | 0,644955 (64,5%) |
| **I** | Akomodasi & Makan Minum | 0,361260 (36,1%) | 0,691123 (69,1%) |
| **J** | Informasi & Komunikasi | 0,359357 (35,9%) | 0,731950 (73,2%) |
| **K** | Jasa Keuangan & Asuransi | 0,499192 (49,9%) | 0,715383 (71,5%) |
| **L** | Real Estat | 0,457849 (45,8%) | 0,860635 (86,1%) |
| **M** | Jasa Profesional & Ilmiah | 0,502904 (50,3%) | 0,993978 (99,4%) |
| **N** | Jasa Persewaan & Ketenagakerjaan | 0,442595 (44,3%) | 0,569721 (57,0%) |
| **O** | Administrasi Pemerintahan | 0,541090 (54,1%) | 0,658005 (65,8%) |
| **P** | Pendidikan | *NULL* | *NULL* |
| **Q** | Jasa Kesehatan & Sosial | 0,266371 (26,6%) | 0,816782 (81,7%) |
| **R** | Kesenian, Hiburan & Rekreasi | 0,196566 (19,7%) | 0,595456 (59,5%) |
| **S** | Jasa Lainnya | 0,208683 (20,9%) | 0,571536 (57,2%) |
| **T** | Aktivitas RT Pemberi Kerja | 0,295452 (29,5%) | 0,691123 (69,1%) |
| **U** | Aktivitas Badan Internasional | *NULL* | *NULL* |
