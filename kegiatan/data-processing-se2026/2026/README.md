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
