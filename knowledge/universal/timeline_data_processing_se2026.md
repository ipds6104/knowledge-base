# Timeline & Panduan Teknis Data Processing SE2026 (Pemanfaatan IPAS)

> **Sumber Resmi**: Paparan Materi Direktorat Statistik Jasa / Tim Pengolahan SE2026 BPS RI (Workshop Data Processing SE2026, Oktober 2026).  
> **Arsip Berkas**: `knowledge/assets/Timeline_Data_Processing_SE2026_IPAS.jpg`

---

## 1. Tujuan Data Processing SE2026

Pemrosesan Data (*Data Processing*) adalah bentuk tindak lanjut atas hasil pendataan lapangan dan evaluasi pembersihan data (*data cleaning*) sehingga dapat menghasilkan data yang dapat diolah sesuai dengan kaidah dan kebutuhan statistik.

Secara spesifik, pemrosesan data mencakup 4 pilar utama:
1. **Eksplorasi Karakteristik & Pola Data**: Memahami struktur data serta mengidentifikasi anomali dan ketidakwajaran.
2. **Penanganan Ketidaklengkapan & Ketidakwajaran**: Dilakukan melalui tahapan editing, imputasi, dan metode pengolahan yang sesuai.
3. **Reviu & Validasi**: Memastikan kelengkapan, konsistensi, dan kesesuaian informasi, serta penentuan tindak lanjut atas temuan selama pengolahan.
4. **Penyusunan Tabulasi & Analisis Statistik**: Mendukung penyusunan tabulasi dan analisis statistik melalui pengolahan data sesuai kebutuhan pengguna data.

---

## 2. Proses Bisnis Statistik & Pemanfaatan Aplikasi IPAS

Dalam arsitektur proses bisnis statistik (Generic Statistical Business Process Model - GSBPM), pengolahan SE2026 berada pada sub-proses:
- **3.2 Pengklasifikasian dan Pengkodean**
- **3.3 Reviu dan Validasi**
- **3.4 Edit dan Imputasi**

Seluruh rangkaian pengolahan terintegrasi menggunakan aplikasi resmi:
**IPAS (*Integrated Processing and Analysis System*)**.

---

## 3. Timeline Kegiatan Data Processing SE2026

| No | Tahapan Kegiatan | Rentang Waktu / Tanggal | Penanggung Jawab / Keterangan |
|:---|:---|:---|:---|
| 1 | **Pilot Data Processing** | 16–17 Oktober 2026 | Dilaksanakan oleh Direktorat Statistik Jasa BPS RI |
| 2 | **Workshop Data Processing** | 21–22 Oktober 2026 | Sosialisasi & pembekalan teknis seluruh satker BPS |
| 3 | **Eksplorasi Data Processing dengan IPAS** | 23–25 Oktober 2026 | Pengujian awal, eksplorasi fitur, dan simulasi olah data di IPAS |
| 4 | **Penutupan Akses Fasih (Cut-Off)** | **25 Oktober 2026** | Batas akhir pengiriman / sinkronisasi data dari aplikasi Fasih |
| 5 | **Persiapan Environment IPAS** | 26–29 Oktober 2026 | Setup server, database, konfigurasi akun, dan migrasi data Fasih ke IPAS |
| 6 | **Pelaksanaan Data Processing (IPAS)** | **30 Oktober – 15 November 2026** | **Periode Utama Pengolahan (~15 hari)**: Editing, coding, imputasi, validasi, dan tabulasi |

> [!WARNING]
> **Rentang Pelaksanaan Sangat Ketat (15–17 Hari)**:  
> Pelaksanaan data processing aktif hanya berlangsung mulai **30 Oktober s.d. 15 November 2026**.  
> Wajib memastikan seluruh anomali data lapangan dan sinkronisasi Fasih selesai sebelum cut-off penutupan Fasih pada **25 Oktober 2026**.

---

## 4. Evaluasi Kualitas Data & Anomali Nilai Tambah

Dalam materi pemaparan monitoring pra-pengolahan:
1. **Tren Penurunan Temuan Agregat Nilai Tambah Negatif**:
   - Terjadi tren penurunan temuan agregat nilai tambah negatif sebesar **82,6%** (turun 138 temuan), dari 167 temuan (posisi 28 September 2026) menjadi **29 temuan** (posisi 21 Oktober 2026 siang).
   - *Catatan Kritis*: Masih terdapat beberapa wilayah kab/kota dengan nilai tambah negatif secara agregat. Diperlukan pemeriksaan kembali kesesuaian pada rincian pendapatan dan pengeluaran usaha.
2. **Benchmark Rasio Nilai Tambah terhadap Output**:
   - Acuan Rasio NT/Output (PDB 2025): **0,5063**
   - Acuan Rasio NT/Output (Tabel Inter-Regional Input-Output / Tabel IO 2020): **0,5243**
