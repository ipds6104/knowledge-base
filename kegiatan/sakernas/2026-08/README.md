---
nama: "Sakernas"
kategori: "survey"
rutinitas: "rutin"
frekuensi: "semesteran"
peran: "ketua"
status: "aktif"
deadlines:
  - tanggal: "2026-07-25"
    kegiatan: "Pelatihan Petugas Sakernas"
    status: "belum"
  - tanggal: "2026-08-01"
    kegiatan: "Mulai Pemutakhiran (Updating) Rumah Tangga"
    status: "belum"
  - tanggal: "2026-08-10"
    kegiatan: "Batas Akhir Pemutakhiran Rumah Tangga"
    status: "belum"
  - tanggal: "2026-08-14"
    kegiatan: "Penarikan Sampel Rumah Tangga oleh PML/Kabupaten"
    status: "belum"
  - tanggal: "2026-08-15"
    kegiatan: "Mulai Pencacahan Rumah Tangga Sampel (CAPI)"
    status: "belum"
  - tanggal: "2026-08-31"
    kegiatan: "Batas Akhir Pencacahan Rumah Tangga Sampel (CAPI)"
    status: "belum"
  - tanggal: "2026-09-05"
    kegiatan: "Batas Akhir Pemeriksaan Dokumen & Verifikasi PML"
    status: "belum"
---
# Sakernas (2026-08)

## Deskripsi Kegiatan
Survei Angkatan Kerja Nasional (Sakernas) Agustus 2026 merupakan kegiatan survei sampel rutin semesteran BPS untuk mengumpulkan data ketenagakerjaan, tingkat pengangguran terbuka (TPT), partisipasi angkatan kerja, dan karakteristik pekerja di Indonesia. 

---

## ⚙️ Kendala Teknis & Petunjuk Operasional FASIH SM

Berdasarkan dinamika teknis aplikasi FASIH SM menjelang pelaksanaan pemutakhiran (24 Juli 2026):

1. **Ketersediaan Prelist (Panel vs Komplemen)**:
   * **SLS Komplemen**: Prelist sudah tersedia di FASIH SM dan Admin dapat langsung melakukan *assign* ke petugas pencacah.
   * **SLS Panel**: Prelist telah disiapkan di FASIH SM. Admin wajib melakukan verifikasi kelengkapan prelist sesuai DSSLS sebelum penugasan.
2. **Prosedur Khusus SLS Komplemen Mei (Perbaikan Error Blok 5)**:
   * *Penanganan Sistem*: Assignment lama yang sempat mengalami masalah pada Blok 5 telah dihapus dari sistem dan prelist baru telah di-upload ulang oleh Pusat.
   * *Langkah Admin*: Admin Kabupaten/Koseka **wajib melakukan re-assign** petugas agar prelist hasil unggah ulang masuk ke akun petugas pencacah.
   * *Langkah Petugas (PPL)*: Setelah Admin melakukan re-assign, petugas **WAJIB melakukan *Sync* seluruh penugasan** di aplikasi FASIH SM untuk menggantikan assignment lama dengan assignment baru secara bersih.

---

## ⚠️ Mitigasi Irisan Sampel Sakernas & SE2026 (Respondent Burden)

 Pelaksanaan Pemutakhiran Sakernas Agustus 2026 beririsan langsung dengan jadwal CAPI/Door-to-door Sensus Ekonomi 2026 (SE2026). Pada SLS sampel yang sama (`idsubsls`), hal ini memicu kelelahan responden (*respondent burden*) dan penolakan warga/RT.

### 1. Strategi & SOP Mitigasi Lapangan
* **Pendampingan Penguasa Wilayah (RT/Kadus/Kades)**:
  * Apabila petugas menghadapi resistensi warga/RT, **wajib menggandeng Penguasa Wilayah setempat** (Ketua RT, Kepala Dusun, atau Kades/Lurah) untuk mengedukasi dan menjelaskan legalitas serta pentingnya pendataan BPS.
* **Pemanfaatan Result Pendataan SE2026 untuk Updating**:
  * Untuk SLS sampel Sakernas yang **sudah pencacahan SE2026**, PPL/PML dapat memanfaatkan hasil pendataan SE2026 sebagai bahan rujukan awal pemutakhiran keberadaan keluarga, guna meminimalkan pengulangan pertanyaan yang memberatkan responden.
* **Pemahaman Perbedaan Konsep Keberadaan/Keluarga**:
  * PPL/PML wajib menguasai perbedaan konsep keberadaan keluarga antara SE2026 (unit usaha/keluarga ekonomi) dan Sakernas (keluarga/rumah tangga bias biasa). Rujukan resmi mengacu pada **Surat Pengiriman DSSLS Sakernas Agustus 2026 (Tanggal 2 Juli 2026)**.
* **Mekanisme Pelaporan Penolakan Responden/Wilayah**:
  * Kasus penolakan kategori berat (warga RT/Ketua RT menolak secara kolektif) wajib didokumentasikan dan dilaporkan secara resmi melalui link monitoring penolakan pimpinan: [Link Pelaporan Penolakan Sakernas (OneDrive Form)](https://onedrive.live.com/:x:/g/personal/558299a3e91fcbcc/IQA_ddax6LSTT6gxXdU-nMdRAV_r1YoqQSH92i1UZ9JGzrk) untuk segera ditindaklanjuti dengan pembinaan pimpinan/pembina wilayah BPS.

### 2. Akar Masalah Resistensi & Strategi Komunikasi Responden
* **Persepsi Kurang Tepat di Masyarakat**:
  1. *Apatisme Data*: Masyarakat kurang memahami nilai penting data statistik dalam perencanaan pembanguan negara, sehingga merasa terganggu oleh kunjungan berulang.
  2. *Ekspektasi Bantuan Sosial (Bansos)*: Kunjungan pendataan sering diidentikkan dengan penerimaan bansos. Warga yang tidak pernah menerima bansos cenderung menolak karena merasa pendataan tidak memberikan manfaat langsung bagi mereka.
* **Solusi Pendekatan Multi-Pihak**:
  * Melibatkan tokoh agama, tokoh masyarakat/cendikiawan, aparatur pemerintah (desa hingga kecamatan), dan media lokal untuk memberikan sosialisasi berkelanjutan mengenai sifat pendataan BPS yang bebas dari kaitannya dengan penyaluran bansos langsung.

---

## 🛠️ Pembakuan Penarikan Data Prelist Updating (Irisan SE2026)

Untuk memanfaatkan data mikro hasil pencacahan SE2026 pada 48 Sub-SLS sampel Sakernas yang beririsan, penarikan data telah dibakukan menggunakan skrip otomatis SQL Lab API:

* **Skrip Ekstraktor Otomatis**: [scripts/extract_sakernas_intersect.py](file:///home/ihza/Projects/knowledge-base/scripts/extract_sakernas_intersect.py)
* **Kamus Data & Spesifikasi Query SQL**: Merujuk pada dokumentasi resmi [Panduan Integrasi Superset SQL Lab & Kamus Data FASIH SE 2026](file:///home/ihza/Projects/knowledge-base/kegiatan/sensus-ekonomi-2026/2026/docs/panduan-sql-lab-fasih-se2026.md) (khususnya Tabel `nested_dtsen` untuk data Keluarga dan `nested_dtsen_var` untuk KRT/ART).
* **Perintah Penarikan**:
  ```bash
  # Mode Cepat (Menggunakan cache lokal SLS chunks yang sudah ada)
  python3 scripts/extract_sakernas_intersect.py
  
  # Mode Force Refresh (Menarik data ulang secara utuh dari server Superset)
  python3 scripts/extract_sakernas_intersect.py --force
  ```
* **Output Berkas**: Hasil penarikan otomatis disimpan ke:
  * **CSV**: [prelist_updating_sakernas_se2026_intersect_final.csv](prelist_updating_sakernas_se2026_intersect_final.csv)
  * **Excel (Styled)**: [prelist_updating_sakernas_se2026_intersect_final.xlsx](prelist_updating_sakernas_se2026_intersect_final.xlsx) (Dilengkapi format header slate-gray, gridlines, auto-column width, dan freeze-panes).

---

## 📦 Ekstraksi Data Mikro Penuh Sakernas Agustus 2026 (Zero-Pruning 100% Kolom)

Penarikan data mikro 100% lengkap tanpa meninggalkan satu kolom pun untuk seluruh sampel Sakernas Agustus 2026 Kabupaten Mempawah (6104) telah berhasil dieksekusi secara otomatis:

* **Skrip Ekstraktor**: [scripts/extract_sakernas_full_data.py](file:///home/ihza/Projects/knowledge-base/scripts/extract_sakernas_full_data.py)
* **Kamus Skema & Kolom**: [metadata_tables_sakernas.json](metadata_tables_sakernas.json) (Memetakan 1.036 kolom dari 11 tabel skema `tok_3fd42e0e`)
* **Metode**: *Deterministic Column-Chunking* (membagi puluhan kolom ke dalam paket 22-kolom untuk mem-bypass batasan query Superset max 25 kolom per SQL statement tanpa kehilangan satu kolom pun)
* **Perintah Penarikan Ulang**:
  ```bash
  python3 scripts/extract_sakernas_full_data.py
  python3 scripts/upload_sakernas_to_gdrive.py
  ```
* **Tautan Google Drive Resmi (35. Sakernas / 2026-08)**: [Folder Google Drive 2026-08](https://drive.google.com/drive/folders/16dOgtUV9C1SbuZlbg2OATciFr7p7adSH)

### 📂 Berkas Output Dataset & Struktur Google Drive:
Folder Google Drive `2026-08/` telah ditata ke dalam 3 subfolder rapi:
1. **`01_Dataset_Utama/`**:
   * [`sakernas_agustus_2026_mempawah_master_flat.xlsx`](https://drive.google.com/file/d/19xg5FGXUeUTqWgEevr2WKmnF0OmXr-Kc/view) (8.73 MB)
   * [`sakernas_agustus_2026_mempawah_master_flat.csv`](https://drive.google.com/file/d/1nivycxQppWN3q9hc_gyOmPywC1otbARu/view) (16.35 MB) — **1.756 baris ART** × **861 kolom unik** (Hasil penggabungan ART + Rumah Tangga + Assignment + Petugas).
2. **`02_Tabel_Mikro/`**:
   * **`art_roster` (Individu/ART)**: [`art_roster_mempawah_full_637cols.xlsx`](https://drive.google.com/file/d/188A4G5M2gcOrogbkjn8CmqhoMBT23fWi/view) (4.17 MB) & [`.csv`](https://drive.google.com/file/d/1Hg2WqWLm7JXrU9_sFz3znnODE3f7Fvyy/view) (4.61 MB) | **1.756 baris** × **637 kolom lengkap**.
   * **`root_table` (Rumah Tangga)**: [`root_table_mempawah_full_120cols.xlsx`](https://drive.google.com/file/d/18VwvNzxX44PKZpUqdwg3S8Tf7iTNX0Kq/view) (380 KB) & [`.csv`](https://drive.google.com/file/d/15t3wsSMAcUvTQJARTHT91Q6aBujYkeOT/view) (892 KB) | **479 baris** × **120 kolom lengkap**.
   * **`base_table_assignment` (Status Assignment)**: [`base_table_assignment_mempawah_full_86cols.xlsx`](https://drive.google.com/file/d/1-mPAFREyrPDnjM2kV3-mZl4GmsyUgDgS/view) (400 KB) & [`.csv`](https://drive.google.com/file/d/1od3SOwES5lsaDQBaIIuewiruYAI1SrQB/view) (2.01 MB) | **479 baris** × **86 kolom lengkap**.
   * **`petugas` (Petugas Lapangan)**: [`petugas_mempawah_full_21cols.xlsx`](https://drive.google.com/file/d/1YEmJO-r-UNjeDYNH92WlRsZxZk2sIFo8/view) (70 KB) & [`.csv`](https://drive.google.com/file/d/1A966mbJ369K3rVK4kIllRu1MM5d37WON/view) (190 KB) | **479 baris** × **21 kolom lengkap**.
3. **`03_Metadata_dan_Kamus_Data/`**:
   * [`kamus_variabel_sakernas_202608.xlsx`](https://drive.google.com/file/d/1OpXmVpMTqQie29XdUTJjOQ7VwP4_OaD7/view) — Buku kamus daftar 1.036 variabel seluruh tabel dalam format Excel siap baca.
   * [`metadata_tables_sakernas.json`](https://drive.google.com/file/d/1LxIMvf2ynhts210YSj5yNi5TCr8CXcaG/view) — Skema database asli dalam format JSON.



