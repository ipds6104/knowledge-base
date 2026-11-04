---
name: satudata-mempawah
description: >-
  Gunakan skill ini untuk mencari, mengaudit, memverifikasi, dan mengunduh dataset statistik sektoral dari Portal Resmi Satu Data Kabupaten Mempawah (https://satudata.mempawahkab.go.id/) berbasis CKAN 2.9 API. Mendukung pencarian 426+ dataset, 3.992+ berkas resources (CSV/XLSX), 23 OPD produsen data, preview tabular real-time, integrasi bukti dukung EPSS & Pembinaan Statistik Sektoral (PSS).
---

# Portal Satu Data Kabupaten Mempawah (CKAN 2.9 API Integration)

Skill ini membekali agen AI dan analis dengan integrasi langsung ke **Portal Resmi Satu Data Kabupaten Mempawah** (`https://satudata.mempawahkab.go.id/`), gateway interoperabilitas Satu Data Indonesia (SDI) tingkat daerah yang dikelola oleh Dinas Komunikasi dan Informatika (Diskominfo) selaku Walidata Daerah Kabupaten Mempawah.

Portal ini menyediakan antarmuka terstandarisasi **CKAN 2.9 API** (`/api/3/action/`) untuk membaca metadata, mencari paket dataset, menginspeksi struktur kolom, serta mengunduh berkas tabel (CSV, XLSX, dsb.) secara deterministik.

---

## 🏛️ Arsitektur & Spesifikasi Portal

- **Domain Portal**: `https://satudata.mempawahkab.go.id/`
- **Base Endpoint API**: `https://satudata.mempawahkab.go.id/api/3/action/`
- **Engine Kompatibilitas**: CKAN 2.9.7 API Compat (Backend Laravel 13)
- **Status Akses**: Akses Publik (Read-Only) tanpa memerlukan token autentikasi rahasia.
- **Kapasitas Portal Saat Ini**:
  - **426 Dataset Publik**
  - **3.992 Berkas Resources** (CSV, XLSX, PDF, dsb.)
  - **23 OPD Produsen Data**
  - **10 Kategori / Topik Sektoral**
  - **207 Tag / Kata Kunci**

---

## 🛠️ CLI Tool: `satudata_tool.py`

CLI tool executable berstandar agent-ready tersedia di:
```bash
.agents/skills/satudata-mempawah/scripts/satudata_tool.py
```

### Karakteristik Tool:
1. **Machine-Readability First**: Setiap subperintah mendukung flag `--json` untuk keluaran terstruktur murni bagi AI agent.
2. **Zero Dependency Bloat**: Menggunakan pustaka standar Python 3 + `openpyxl` untuk preview XLSX streaming.
3. **Deterministic Exit Codes**:
   - `0`: Berhasil dieksekusi.
   - `1`: Kesalahan API / HTTP error / Resource not found.
   - `2`: Kesalahan argumen / invalid syntax.
4. **Streaming Data Preview**: Dapat langsung membaca dan menampilkan cuplikan baris tabel CSV/XLSX tanpa perlu menyimpan berkas manual ke disk!

---

## 📋 Daftar Subperintah & Contoh Penggunaan

### 1. Cek Status & Kesehatan Portal (`status`)
Memeriksa status hidup portal, versi engine CKAN, dan ringkasan metrik.
```bash
# Tampilan Visual / Tabel
.agents/skills/satudata-mempawah/scripts/satudata_tool.py status

# Format JSON (Agent Mode)
.agents/skills/satudata-mempawah/scripts/satudata_tool.py status --json
```

### 2. Rekapitulasi Statistik Portal (`stats`)
Melihat ringkasan total dataset publik, berkas, organisasi, topik, dan tag.
```bash
.agents/skills/satudata-mempawah/scripts/satudata_tool.py stats
```

### 3. Pencarian Dataset (`search`)
Mencari dataset berdasarkan kata kunci judul/catatan, filter OPD, atau kategori sektoral.
```bash
# Pencarian kata kunci umum
.agents/skills/satudata-mempawah/scripts/satudata_tool.py search "kesehatan"

# Filter berdasarkan OPD produsen (BPKAD)
.agents/skills/satudata-mempawah/scripts/satudata_tool.py search --opd badan-pengelola-keuangan-dan-aset-daerah

# Filter berdasarkan OPD DPMPTSP
.agents/skills/satudata-mempawah/scripts/satudata_tool.py search --opd dinas-penanaman-modal-koperasi-ukm-dan-pelayanan-terpadu-satu-pintu

# Filter dengan pagination (halaman 2, limit 15)
.agents/skills/satudata-mempawah/scripts/satudata_tool.py search "penduduk" --rows 15 --start 15
```

### 4. Detail Lengkap Dataset (`dataset` / `show`)
Melihat metadata, produsen data, tanggal pemutakhiran, dan daftar semua berkas lampiran beserta link unduhnya.
```bash
# Menggunakan Slug Nama Dataset
.agents/skills/satudata-mempawah/scripts/satudata_tool.py dataset jumlah-pendapatan-daerah-kabupaten-mempawah-tahun-2020

# Menggunakan UUID Dataset
.agents/skills/satudata-mempawah/scripts/satudata_tool.py dataset b385338a-5df6-4a8a-bea0-331eddda241e
```

### 5. Daftar Seluruh OPD Produsen Data (`opds` / `organizations`)
Menampilkan 23 Organisasi Perangkat Daerah yang terdaftar di portal.
```bash
.agents/skills/satudata-mempawah/scripts/satudata_tool.py opds
```

### 6. Detail OPD & Dataset yang Dihasilkan (`opd` / `organization`)
Menampilkan profil satu instansi beserta daftar dataset yang telah diterbitkannya.
```bash
.agents/skills/satudata-mempawah/scripts/satudata_tool.py opd badan-pengelola-keuangan-dan-aset-daerah
.agents/skills/satudata-mempawah/scripts/satudata_tool.py opd dinas-penanaman-modal-koperasi-ukm-dan-pelayanan-terpadu-satu-pintu
```

### 7. Daftar Topik Sektoral & Tag (`groups` / `tags`)
```bash
# Daftar 10 Kategori Sektoral
.agents/skills/satudata-mempawah/scripts/satudata_tool.py groups

# Cari Tag Tertentu
.agents/skills/satudata-mempawah/scripts/satudata_tool.py tags -q "pajak"
.agents/skills/satudata-mempawah/scripts/satudata_tool.py tags -q "izin"
```

### 8. Preview Data Tabular Streaming (`preview`)
Melihat cuplikan $N$ baris pertama dari file CSV atau XLSX langsung di terminal tanpa harus mengunduh file manual. Delimiter (`;` atau `,`) dan sheet Excel dideteksi secara otomatis.
```bash
# Preview CSV PAD BPKAD (5 baris)
.agents/skills/satudata-mempawah/scripts/satudata_tool.py preview \
  "https://satudata.mempawahkab.go.id/datasets/jumlah-pendapatan-daerah-kabupaten-mempawah-tahun-2020/resources/01a0439d-6a8c-73fe-9678-f47fdbf6aae3/download" \
  --rows 5

# Preview XLSX DPMPTSP OSS Perizinan (10 baris)
.agents/skills/satudata-mempawah/scripts/satudata_tool.py preview \
  "https://satudata.mempawahkab.go.id/datasets/realisasi-jumlah-perizinan-oss-rba-tahun-2021/resources/01a0439d-5cd8-73e8-b386-026c885010ff/download" \
  --rows 10
```

### 9. Unduh Berkas Resource (`download`)
Mengunduh berkas tabel ke disk lokal secara cepat dan aman.
```bash
.agents/skills/satudata-mempawah/scripts/satudata_tool.py download \
  "https://satudata.mempawahkab.go.id/datasets/jumlah-pendapatan-daerah-kabupaten-mempawah-tahun-2020/resources/01a0439d-6a8c-73fe-9678-f47fdbf6aae3/download" \
  -o data/bpkad_pad_2022.csv
```

---

## 🎯 Peta 23 OPD Produsen Data & Slug Resmi

Gunakan slug nama di bawah ini saat memfilter data (`--opd <slug>`):

| No | Slug OPD | Nama Resmi Instansi |
| :-: | :--- | :--- |
| 1 | `badan-kepegawaian-dan-sumber-daya-manusia` | Badan Kepegawaian dan Sumber Daya Manusia (BKPSDM) |
| 2 | `badan-kesatuan-bangsa-dan-politik` | Badan Kesatuan Bangsa dan Politik (Bakesbangpol) |
| 3 | `badan-penanggulangan-bencana-daerah` | Badan Penanggulangan Bencana Daerah (BPBD) |
| 4 | `badan-pengelola-keuangan-dan-aset-daerah` | **Badan Pengelola Keuangan dan Aset Daerah (BPKAD)** *(Lokus Emas)* |
| 5 | `badan-pengelola-pajak-dan-retribusi-daerah` | Badan Pengelola Pajak dan Retribusi Daerah (BPPRD) |
| 6 | `badan-perencanaan-pembangunan-daerah` | Bapperida (Bappeda Litbang) |
| 7 | `dinas-kependudukan-dan-pencatatan-sipil` | Dinas Kependudukan dan Pencatatan Sipil (Disdukcapil) |
| 8 | `dinas-kesehatan-pengendalian-penduduk-dan-keluarga-berencana` | Dinas Kesehatan, PPKB |
| 9 | `dinas-komunikasi-dan-informatika` | Dinas Komunikasi dan Informatika (Diskominfo - Walidata) |
| 10 | `dinas-pekerjaan-umum-dan-penataan-ruang` | Dinas PUPR |
| 11 | `dinas-penanaman-modal-koperasi-ukm-dan-pelayanan-terpadu-satu-pintu` | **DPMPTSP-KUKM** *(Lokus Emas)* |
| 12 | `dinas-pendidikan-pemuda-olahraga-dan-pariwisata` | Dinas Dikporapar |
| 13 | `dinas-perhubungan-dan-lingkungan-hidup` | Dinas Perhubungan dan LH |
| 14 | `dinas-perindustrian-perdagangan-dan-tenaga-kerja` | Disperindagnaker |
| 15 | `dinas-perpustakaan-dan-kearsipan` | Dinas Perpustakaan dan Kearsipan |
| 16 | `dinas-pertanian-ketahanan-pangan-dan-perikanan` | DPKPP |
| 17 | `dinas-perumahan-kawasan-permukiman-dan-pertanahan` | Disperkimtan |
| 18 | `dinsospppapmpemdes` | DINSOSPPPAPMPEMDES |
| 19 | `inspektorat-daerah` | Inspektorat Daerah Kabupaten Mempawah |
| 20 | `rsud-dr-rubini` | RSUD dr. Rubini Mempawah |
| 21 | `satuan-polisi-pamong-praja` | Satuan Polisi Pamong Praja (Satpol PP) |
| 22 | `sekretariat-daerah` | Sekretariat Daerah |
| 23 | `sekretariat-dprd` | Sekretariat DPRD |

---

## ⚡ Integrasi Pembinaan Statistik Sektoral (PSS) & EPSS

Skill ini menjadi senjata operasional utama dalam mendukung kegiatan **Pembinaan Statistik Sektoral 2026** dan **Evaluasi Penyelenggaraan Statistik Sektoral (EPSS)**:

### 1. Pengambilan Baseline Data untuk 2 Lokus Utama (Pertemuan 2)
- **Lokus BPKAD (Realisasi Pendapatan Asli Daerah / PAD)**:
  Dataset `jumlah-pendapatan-daerah-kabupaten-mempawah-tahun-2020` memuat berkas berkala realisasi PAD tahun 2020, 2021, dan 2022. Gunakan perintah `preview` atau `download` untuk langsung memasok data ke **Template G (Uji Konsistensi 5 Tahun)** dan **Template E (Akurasi 4 Tahap)**.
- **Lokus DPMPTSP (Perizinan Berusaha OSS-RBA)**:
  Dataset `realisasi-jumlah-perizinan-oss-rba-tahun-2021` memuat data series bulanan NIB, Sertifikat Standar, Izin Usaha, dan Persetujuan Lingkungan tahun 2021–2023.

### 2. Bukti Dukung EPSS Domain 4 (Diseminasi & Portal SDI)
- Membuktikan bahwa produsen data Pemerintah Kabupaten Mempawah telah menyalurkan data sektoral secara terbuka dalam format terbuka (*open formats*: CSV, XLSX) sesuai prinsip Satu Data Indonesia (Indikator 20301 Interoperabilitas Data & Indikator 40101 Akses Media Diseminasi).

### 3. Audit Mutu Data Pra-Penyusunan Kamus SDS
- Analis dan agen AI dapat menggunakan perintah `preview` untuk menginspeksi apakah nama kolom yang digunakan OPD sudah mematuhi kaidah baku Kamus Standar Data Statistik (misal: `kode_kemendagri_kabupaten`, `satuan`, `anggaran`, `relisasi`).

