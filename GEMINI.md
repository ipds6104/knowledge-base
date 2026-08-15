# BPS Kabupaten Mempawah Knowledge Base - AI Agent Guidelines (GEMINI.md)

Dokumen ini berisi pedoman perilaku persisten, standar teknis, dan SOP operasional bagi AI agent (Gemini, Antigravity, dll.) yang bekerja di repositori ini. Repositori ini menampung multi-kegiatan statistik BPS (Sensus, Survei, Evaluasi) di berbagai periode waktu.

---

## 👤 SOP Deteksi Identitas Pengguna (First-Run & Setiap Sesi)

**WAJIB dijalankan sebagai langkah pertama di setiap sesi baru**, sebelum menjawab pertanyaan apapun:

1. **Cek identitas pengguna** dengan menjalankan `python scripts/kb.py whoami`.
2. **Jika hasilnya "belum terkonfigurasi"** (output mengandung kata "Jalankan: ... setup"):
   - Informasikan kepada pengguna bahwa ini tampaknya adalah instalasi baru atau laptop yang belum dikonfigurasi.
   - **Langsung arahkan** pengguna untuk menjalankan: `python scripts/kb.py setup`
   - Tunggu hingga setup selesai sebelum melanjutkan permintaan apapun.
3. **Jika berhasil dikenali**: Sapa pengguna dengan panggilan (`Panggilan`) yang sesuai dari data pegawai, dan lanjutkan dengan tugas yang diminta.
4. **Cara update data pegawai** saat ada mutasi: edit `data/pegawai/Data_Pegawai.csv` — tambah baris baru (pegawai masuk), hapus baris (mutasi keluar), lalu commit.

**Referensi modul:**
- `scripts/kb/user_identity.py` — logika deteksi (cascade: `.env` → `git config`)
- `scripts/kb/cmd_setup.py` — wizard interaktif setup pertama kali
- `data/pegawai/Data_Pegawai.csv` — master data pegawai (Nama, Email, Jabatan, Panggilan)

---



## 📋 SOP Monitoring & Evaluasi Multi-Kegiatan

Setiap kali pengguna menanyakan status progres, evaluasi, atau intervensi harian (misal: *"bagaimana progres kita hari ini?"* atau *"apa yang perlu diintervensi?"*):

1.  **Deteksi Konteks Kegiatan**: Identifikasi kegiatan mana yang dimaksud oleh pengguna (misal: *Sensus Ekonomi 2026*, *Sakernas*, *Susenas*, dll.) beserta periode aktifnya.
2.  **Rujuk README Kegiatan**: Buka dan baca berkas `README.md` di dalam folder kegiatan terkait (misal: `kegiatan/sensus-ekonomi-2026/2026/README.md`) untuk mencari tahu apakah ada SOP monitoring terstandardisasi atau perintah CLI khusus yang wajib dijalankan.
3.  **SOP Khusus Sensus Ekonomi 2026 (Aktif Juni-Agustus 2026)**:
    *   Jika pengguna menanyakan: *"oke di mana posisi kita hari ini untuk SE 2026 dan apakah ada yang perlu diintervensi agar on target?"* (atau variannya).
        - **Wajib** secara otomatis menjalankan `./scripts/kb.py se-monitor -r` dan menyajikan laporan 6-seksi baku secara utuh.
    *   Jika pengguna menanyakan: *"bagaimana kondisi SE 2026 mempawah saat ini"* (atau variannya):
        - **Wajib** secara otomatis menjalankan `./scripts/kb.py se-monitor -r` (serta `./scripts/kb.py se-monitor --prov` dan `python3 scratch/run_worst_projections.py`).
        - **Wajib** menyajikan laporan 6-seksi baku, ditambah dengan informasi:
          1. **Estimasi Selesai Terlama Kabupaten Mempawah**: Mengidentifikasi PPL terlama selesai (dari output `run_worst_projections.py`), nama PML, PJ, target unit, progres, dan tanggal estimasinya.
          2. **Estimasi Selesai Terlama Provinsi Kalbar**: Mengidentifikasi Kabupaten/Kota di Kalbar dengan progres terkecil/selesai terlama (dari output `--prov`), persentase selesai, dan tanggal estimasinya.
          3. **Formula Kalkulasi Estimasi**: Menjelaskan secara transparan bahwa estimasi dihitung real secara matematis oleh sistem berdasarkan data, bukan menebak-nebak:
             $$\text{Kecepatan Harian} = \frac{\text{Done \%}}{\text{Hari Lapangan Berjalan}}$$
             $$\text{Sisa Hari} = \frac{100\% - \text{Done \%}}{\text{Kecepatan Harian}}$$
             $$\text{Est. Tanggal Selesai} = \text{Hari Ini} + \text{Sisa Hari}$$
          4. **Diagnosis Penyebab di Level PPL**: Menganalisis penyebab kelambatan di tingkat PPL berdasarkan data (target besar, verifikasi PML menumpuk/bottleneck, laju pengerjaan lambat karena petugas baru, penolakan wilayah seperti di Purun Sungai Burung, atau kendala blank spot sinyal internet di Kecamatan Toho dan Sadaniang dengan pengecekan apakah mereka bisa bergeser ke 1 atau 2 desa oase sinyal untuk pelaporan progres/sinkronisasi berkala via WhatsApp).
4.  **Format Analisis Ad-Hoc PML-PPL (SE 2026)**:
    *   Apabila pengguna meminta pemeriksaan detail kinerja PML tertentu, asisten AI **wajib** menyajikan laporan dalam dua tabel standar (Tabel 1: Klasemen Makro PML vs Rata-rata/Lainnya, Tabel 2: Detail PPL di bawah PML tersebut diurutkan berdasarkan `Done %` terkecil) beserta diagnosis bottleneck dan rekomendasi tindakan taktis.
    *   **Tabel 1** wajib menyertakan baris metrik: `Target Harian (Approve/Hari)`.
    *   **Tabel 2** wajib menyertakan kolom metrik: `Tgt Submit/Hari` (target submit harian PPL) dan `Est. Selesai` (tanggal proyeksi selesai jika dihitung dengan kecepatan progres saat ini).
5.  **Penyajian Tabel untuk Monitoring**: Setiap kali membahas monitoring atau menyajikan data progres (seperti daftar intervensi, peringkat, perbandingan wilayah, dll.), asisten AI **wajib** sebisa mungkin menyajikannya dalam bentuk **tabel** untuk memudahkan keterbacaan dan analisis cepat.

---

## 💬 SOP Pemrosesan WhatsApp Chat Logs

Untuk menganalisis, mengambil keputusan, atau menyinkronkan timeline berdasarkan riwayat obrolan grup WhatsApp kegiatan:

1. **Penyimpanan Berkas**: 
   - Berkas ekspor obrolan disimpan dalam format `.zip` langsung di dalam folder kegiatan terkait (contoh: `kegiatan/evaluasi-epss/2026/`).
   - Format penamaan disarankan: `WhatsApp Chat with [Nama Grup].zip`.
2. **Kueri Chat Melalui CLI**:
   - Gunakan perintah `kb chat` untuk menganalisis isi obrolan.
   - Pindai daftar chat yang tersedia dengan `kb chat list`.
   - Lihat statistik keaktifan pengirim dengan `kb chat info [index]`.
   - Tampilkan pesan terbaru dengan `kb chat tail [index] -l [jumlah]`.
   - Ekstrak link yang dibagikan dengan `kb chat links [index]`.
   - Lakukan kueri pencarian teks dengan `kb chat search [index] -q "[kata_kunci]"`.
   - Deteksi tanggal/tenggat waktu potensial dengan `kb chat extract [index]`.
3. **Membaca Chat Terbaru (Tail/Limit)**:
   - Jika ingin membatasi analisis pada pesan-pesan terbaru untuk menghindari kebisingan data lama, gunakan argumen `--limit [jumlah]` atau subcommand `kb chat tail [index] -l [jumlah]`.
   - Contoh untuk membaca 100 pesan terbaru: `kb chat tail [index] -l 100`.
4. **Alur Tindak Lanjut**:
   - Setelah menemukan tanggal tenggat waktu penting atau revisi juknis dari obrolan, asisten AI wajib memperbarui berkas `README.md` kegiatan di bagian `deadlines` atau `Catatan Pelaksanaan` dan memicu `kb sync-sheets` untuk memperbarui Google Sheets.

---

## ⚙️ Logika Bisnis & Batas Kritis Dinamis (SE 2026)

Logika di bawah ini ter-isolasi khusus di dalam sub-package monitoring Sensus Ekonomi 2026 (`kb/se_monitor/`):

### 1. Deteksi PPL Terlambat Terkritis
Batas progres PPL lambat dihitung secara **dinamis** terhadap target ideal hari ini (`expected_pct`):
$$\text{ppl\_threshold} = \text{max}(3.00\%, \frac{\text{expected\_pct}}{100} \times 0.25)$$
*   Petugas disaring jika memiliki `target > 200` and `completed_rate < ppl_threshold`.

### 2. Diagnosis Warna Status Progres PPL
*   **🟢 Hijau**: Progres $\ge$ $\text{max}(10.00\%, \frac{\text{expected\_pct}}{100} \times 0.70)$ (Sehat).
*   **🔴 Merah**: Progres $<$ $\text{max}(3.00\%, \frac{\text{expected\_pct}}{100} \times 0.25)$ (Lambat/Kritis).
*   **🟡 Kuning**: Progres di antara batas Merah dan Hijau (Warning).
*   **Penggunaan Emoji**: Status warna ini wajib direpresentasikan menggunakan emoji (`🟢`, `🟡`, `🔴`) baik pada laporan analisis ad-hoc maupun pada visualisasi output terminal/CLI.

### 3. Deteksi PML Bottleneck (Antrean Kritis)
PML dianggap menumpuk verifikasi berkas (*bottleneck*) jika:
*   Berkas masuk dalam antrean (`submitted`) $> 20$ dokumen.
*   Tingkat pemeriksaan/kelulusan berkas (`approval_rate`) $< 20.00\%$ ($0.20$).

### 4. Perhitungan Target Harian PPL & PML Tepat Waktu (Tenggat 15 Agustus 2026)
Untuk memastikan seluruh dokumen selesai tepat waktu sebelum target internal **15 Agustus 2026**, target harian dihitung secara dinamis terhadap sisa hari lapangan:
*   **Sisa Hari Lapangan**:
    $$\text{remaining\_days} = \text{max}(1, (\text{TARGET\_DATE} - \text{today}).\text{days})$$
    di mana $\text{TARGET\_DATE}$ di-hardcode ke 15 Agustus 2026 (`2026-08-15`).
*   **Target Harian Submisi PPL**:
    $$\text{ppl\_daily\_target} = \text{max}(0.0, \frac{\text{target} - \text{completed}}{\text{remaining\_days}})$$
*   **Target Harian Pemeriksaan/Approval PML**:
    $$\text{pml\_daily\_target} = \text{max}(0.0, \frac{\text{target} - \text{approved}}{\text{remaining\_days}})$$

### 5. Format Jawaban untuk Kueri Petugas Terkritis ("Siapa yang kemungkinan paling lama selesainya?")
Apabila pengguna menanyakan siapa petugas PPL yang diproyeksikan selesai paling lama atau paling lambat:
*   **Logika Pengurutan & Prioritas Kritis**:
    1.  **Prioritas 1 (Belum Mulai)**: Petugas dengan progres $0.00\%$ (`Tdk Terproyeksi`), diurutkan berdasarkan beban target unit terbesar.
    2.  **Prioritas 2 (Sedang Berjalan)**: Petugas dengan progres $> 0.00\%$ tetapi memiliki proyeksi tanggal selesai terjauh (diurutkan berdasarkan estimasi tanggal selesai secara descending).
*   **Penyajian Tabel**:
    *   Wajib disajikan dalam bentuk **tabel** dengan kolom: `No`, `Nama PPL`, `Kecamatan`, `PML Pengawas`, `PJ-Kuda`, `Target`, `Selesai`, `Done %`, dan `Est. Selesai`.
    *   Kolom `Done %` wajib menggunakan emoji status warna (`🟢`, `🟡`, `🔴`).
*   **Prosedur Pengecekan**: Jalankan perintah `python3 scratch/run_worst_projections.py` untuk mendapatkan daftar petugas dengan proyeksi selesai paling lama secara real-time dari Google Sheets.

---

## 🛠️ Standar Kode & Struktur Proyek

*   **Thin Entrypoint**: Berkas `scripts/kb.py` adalah entrypoint CLI tipis. Semua logika bisnis didelegasikan ke package `kb/`.
*   **Isolasi Modul Kegiatan**: Setiap kegiatan yang membutuhkan skrip pemantauan/logika khusus **wajib** dibuatkan sub-package tersendiri di bawah `kb/` (seperti `kb/se_monitor/`) untuk menghindari pencampuran logika bisnis (*spaghetti code*) antar kegiatan.
*   **Epistemological Source**: Penentuan relasi struktural/hierarki petugas dalam kegiatan **wajib** dibaca dari file alokasi resmi kegiatan (seperti `Alokasi Petugas.csv` untuk SE2026). Jangan pernah menebak relasi ini secara mandiri.
*   Batas Ukuran File: Maksimal **500 baris** per berkas Python (diawasi oleh pre-commit hook di `.githooks/pre-commit`). Jaga modul tetap kecil, terfokus, dan modular (di bawah 300 baris).
*   Analisis Repo: Gunakan `python3 ./scripts/dump_tree.py` untuk memantau struktur direktori dan baris kode.
*   **Batasan Modifikasi Workspace (Read-Only)**: Agent di repositori ini (`knowledge-base`) hanya bertanggung jawab untuk mengelola/menulis berkas di dalam workspace `knowledge-base`. Agent diperbolehkan membaca berkas di repositori luar (seperti `sikendis`) untuk analisis dan pelaporan kesalahan, namun dilarang keras melakukan modifikasi atau penulisan langsung di luar workspace. Pekerjaan modifikasi di workspace eksternal didelegasikan ke AI lain atau pengguna sendiri.

## 📄 SOP Penyusunan Metadata Statistik Sektoral (Satu Data Indonesia)

Untuk menyusun metadata kegiatan, indikator, dan variabel yang terstandarisasi Satu Data Indonesia (SDI) pada kegiatan Desa Cantik, ikuti langkah-langkah berikut:

### 🚨 SOP Wajib Konfirmasi User & Anti-Asumsi (Desa/Kelurahan Baru)

**DILARANG KERAS** langsung menggenerasi metadata atau publikasi (DDA/Metadata) untuk desa/kelurahan baru secara terburu-buru tanpa konfirmasi awal. Setiap kali ada desa/kelurahan baru atau pembaruan instrumen, AI Agent **WAJIB** terlebih dahulu melakukan konfirmasi ulang poin-poin berikut ke pengguna:

1. **Status Nomenklatur Administrasi**:
   - Apakah wilayah tersebut berupa **Desa** (Kepala Desa, Dusun, Desa Cantik) atau **Kelurahan** (Lurah, RW, Kelurahan Cantik)? *Dilarang keras berasumsi "Desa" jika statusnya Kelurahan (seperti Pasir Wan Salim).*
2. **Nama Resmi Kegiatan (`Nama Kegiatan`)**:
   - Konfirmasikan nama resmi kegiatan yang disepakati (misal: *"Pendataan Sosial Keluarga Kelurahan Pasir Wan Salim 2026"* vs *"Pendataan Potensi Kewilayahan RT dan Inventarisasi Fasilitas Umum Desa Cantik..."*). Nama kegiatan tidak boleh diseragamkan secara gegabah.
3. **Cakupan & Sheet/Tab Google Sheets yang Digunakan**:
   - Konfirmasikan nama tab eksplisit di Google Sheet (`rt_tab`, `fas_tab`). Jangan berasumsi nama tab seragam di semua link Google Sheet.
   - Konfirmasikan apakah ada pendataan **Fasilitas Umum** atau murni **CAPI Keluarga** saja. Jika suatu desa/kelurahan tidak mengumpulkan Fasilitas Umum (seperti Pasir Wan Salim), tab fasilitas **wajib dikosongkan/diabaikan sepenuhnya** dan dilarang menampilkan header tabel kosong pada output.
4. **Verifikasi Indikator Sektoral (`MS-INDIKATOR`)**:
   - **Aturan Ketat Verifikasi Pembentuk**: Indikator **HANYA BISA DICANTUMKAN** jika seluruh variabel pembentuknya (pembagi & pembilang) benar-benar terbukti ada dan terisi di sheet desa tersebut.
   - Dilarang mencantumkan *Persentase Rumah Layak Huni* jika tidak ada data fisik dinding/atap/lantai/jamban.
   - Dilarang mencantumkan *Rasio Sarana Keagamaan* jika tidak ada pendataan fasilitas umum (`fas_tab` kosong).
   - Dilarang mencantumkan *Persentase Penduduk Lansia* atau *KTP-el* jika variabel pendukungnya tidak dikumpulkan pada instrumen desa/kelurahan bersangkutan.

### 1. Kebutuhan Input
*   **Database Penyelenggaraan**: File Excel database/AppSheet pendataan tingkat RT dan inventarisasi sarana prasarana (contoh: `sbk_appsheet.xlsx`).
*   **Kamus Data**: Daftar variabel, tipe data, definisi operasional, rentang isian, dan konsep terkait.

### 2. Jalankan Perintah CLI Otomatis
Gunakan perintah CLI berikut untuk mengompilasi metadata secara otomatis:
```bash
python scripts/kb.py metadata [nama-desa-kebab]
```
*Pilihan nama desa: `sungai-bakau-kecil`, `pasir-palembang`, `pasir-wan-salim`.*

### 3. 🏗️ Arsitektur Decoupled DTO & Engine (`kb/metadata_generator/`):
- **Pemisahan Kontrak Data (Decoupled DTO)**: Modul renderer ([markdown_renderer.py](file:///home/ihza/Projects/knowledge-base/scripts/kb/metadata_generator/renderers/markdown_renderer.py) & [typst_renderer.py](file:///home/ihza/Projects/knowledge-base/scripts/kb/metadata_generator/renderers/typst_renderer.py)) **hanya menerima objek DTO terisolasi (`DesaMetadataDTO`)** dari `builder.py` sebagai Single Source of Truth.
- **Zero Hardcoding**: `builder.py` menyusun DTO secara universal tanpa percabangan hardcode nama desa di layer renderer.
- **Ketentuan Desain & Layout (PDF Typst)**:
  - **Wrapping Underscore**: Nama variabel di-wrap menggunakan `#let wrap-var(name)` dengan zero-width space (`\u{200b}`) dan font `Courier New` 8pt agar ter-wrap otomatis tanpa overflow.
  - **Penulisan Rumus**: Gunakan format fraksi matematika Typst yang benar (`$ frac(sum L, sum P) $`).
  - **Page Margin**: Margin horizontal `margin: (x: 1.5cm, y: 2cm)` untuk menampung tabel variabel 7-kolom secara presisi.

### 4. Output yang Dihasilkan
Perintah akan secara otomatis menulis dua file:
1.  **Dokumen Markdown**: `kegiatan/desa-cantik/2026/[desa]/metadata-descan-[desa]-2026.md`
2.  **Dokumen PDF**: `kegiatan/desa-cantik/2026/[desa]/metadata-descan-[desa]-2026.pdf` (dan salinan publikasinya di folder `outputs/`).

---

## 📊 SOP Pembuatan Publikasi Desa Dalam Angka (DDA Engine)

Untuk menggenerasikan publikasi **Desa Dalam Angka (DDA)** berstandar BPS 5 Bab (Markdown, HTML bilingual interaktif, dan PDF Siap Cetak A4) untuk desa manapun secara otomatis, gunakan perintah CLI:

```bash
python scripts/kb.py dda [nama-desa-kebab] [--sheet-id SHEET_ID] [--year 2026]
```
*Pilihan nama desa standar: `sungai-bakau-kecil`, `pasir-palembang`, `pasir-wan-salim`.*

### 🏗️ Prinsip Arsitektur Decoupled DTO & Engine (`kb/dda_generator/`):
1. **Pemisahan Kontrak Data (Decoupled DTO)**:
   - Modul renderer layout (`renderers/html_renderer.py`, `markdown_builder.py`) **TIDAK BOLEH** mengolah atau menyaring data mentah secara langsung. Renderer hanya menerima objek DTO terisolasi (`DesaPublicationData`) yang bertindak sebagai kontrak tunggal (*Single Source of Truth*).
   - Seluruh logika pengolahan data (*fetching*, agregasi mikrodata CAPI per rumah tangga ke tingkat RT, kalkulasi indikator demografi, bansos, dan sanitasi) sepenuhnya diisolasi di dalam `fetcher.py` dan `calculator.py`.
2. **Prinsip *Feature Flags / Capabilities Matrix* pada DTO (Zero Hardcode Nama Desa di Renderer)**:
   - **Dilarang Keras** menulis pengkondisian berbasis nama desa eksplisit (seperti `if name_kebab == "pasir-wan-salim":`) di dalam layer renderer (`html_renderer.py`, `md_builder.py`, atau renderer lain).
   - **Solusi Fleksibilitas**: DTO `DesaPublicationData` wajib membawa atribut kapabilitas dataset (`capabilities: DatasetCapabilitiesDTO`), misalnya `has_employment`, `has_msme`, `has_building_materials`, `has_decent_housing`, `has_ktp_el`, `has_public_facilities`, dan `admin_type`. Layer renderer hanya mengecek ketersediaan atribut ini untuk mengaktifkan/mematikan bab, tabel, atau infografis secara universal.
3. **Multi-Renderer Extensibility**:
   - Berkat ketersediaan objek DTO `DesaPublicationData` yang *strongly-typed* (`dataclass`), renderer baru (seperti Typst PDF, React UI, atau Web Dashboard) dapat dibuat atau diganti secara independen tanpa menyentuh atau merusak logika kalkulasi statistik di `calculator.py`.
4. **Ketentuan Pedoman Diseminasi & Tata Naskah BPS**:
   - **Tanpa ISSN, Nomor Katalog, & Nomor Publikasi**: Seluruh publikasi tingkat desa (Desa Dalam Angka) **TIDAK memiliki ISSN, Nomor Katalog, maupun Nomor Publikasi**. Dilarang keras menambahkan elemen ISSN, Nomor Katalog, atau Nomor Publikasi pada templat HTML, Typst, maupun metadata publikasi desa.
   - **Aturan Running Header Halaman Romawi (Frontmatter)**: Sesuai Pedoman Diseminasi Publikasi BPS, running header pada bagian awal/romawi (Halaman ii s.d. ix) **WAJIB dimatikan/suppressed** (`show_header=False`). Running header (Judul Buku di halaman genap dan Nama Bab di halaman ganjil) **HANYA boleh muncul** pada halaman isi utama (Angka Arab: 1, 2, 3...).
   - **Halaman Katalog BPS & Hak Cipta (Halaman ii)**: Halaman 2 memuat Ukuran Buku (A4), Jumlah Halaman (`ix + 35 halaman`), Penanggung Jawab, Penyusun, Penyunting, Penerbit, dan Kotak Klausul Hak Cipta Resmi BPS (tanpa ISSN, Nomor Katalog, atau Nomor Publikasi).

---

## 📑 SOP Permintaan Data & Diseminasi Statistik Desa Cantik (Dual-Channel Delivery)

Setiap penyusunan dokumen Standar Operasional Prosedur (SOP) Permintaan Data untuk desa/kelurahan binaan Desa Cantik (Sungai Bakau Kecil, Pasir Palembang, Pasir Wan Salim, dll.) **WAJIB** menerapkan prinsip dan arsitektur berikut:

### 🚨 Aturan Wajib Non-*By Name By Address* & Bebas Hambatan Birokrasi
1. **Batasan Mutlak Non-*By Name By Address* (UU No. 27/2022 PDP)**:
   - Seluruh permohonan data yang dilayani **HANYA BERUPA DATA AGREGAT / MAKRO** (tingkat RT, Dusun/RW, desa/kelurahan, atau sebaran fasilitas umum).
   - Data mikro perorangan/keluarga (*by name by address*) bersifat rahasia dan **SAMA SEKALI TIDAK DAPAT DIBERIKAN KEPADA PEMOHON MANAPUN**.
2. **Prinsip Pelayanan Cepat (Tanpa Tanda Tangan Kades/Lurah)**:
   - Untuk mempercepat durasi layanan (*quick turnaround* 15 s.d. 30 menit), verifikasi data agregat dan rilis data dilakukan langsung oleh **Petugas Agen Statistik Desa/Kelurahan** tanpa memerlukan disposisi atau tanda tangan basah Kepala Desa / Lurah.
   - Penyerahan berkas berupa lembar rekapitulasi data agregat terverifikasi siap pakai.
3. **Mekanisme Download Langsung di Web**:
   - **Seluruh dokumen SOP Permintaan Data Desa Cantik WAJIB mencantumkan mekanisme download mandiri (*self-service*) langsung di website portal resmi (`https://desa-sm.dvlp.asia/desa-cantik/[slug-desa]`) dan Open Data API, meskipun status fiturnya masih dalam tahap pengembangan/penyusunan.** Dilarang membuat SOP yang murni manual/tatap muka tanpa mencantumkan kanal digital terbuka ini.

### 🏗️ Arsitektur Saluran Layanan Dual-Channel:
1. **Jalur 1 — Layanan Mandiri Digital (*Self-Service Online Download & Open API*) — Instan (0 Menit)**:
   - **Sasaran**: Masyarakat umum, akademisi, mahasiswa, media, dan OPD yang membutuhkan data terbuka (agregat RT, daftar fasilitas umum, publikasi digital, dan infografis).
   - **Kanal Akses**:
     - **Portal Website**: `https://desa-sm.dvlp.asia/desa-cantik/[slug-desa]`
       - Sungai Bakau Kecil: `https://desa-sm.dvlp.asia/desa-cantik/desasungaibakaukecil`
       - Pasir Palembang: `https://desa-sm.dvlp.asia/desa-cantik/desapasirpalembang`
       - Pasir Wan Salim: `https://desa-sm.dvlp.asia/desa-cantik/kelurahanpasirwansalim`
     - **Open Data REST API**: `https://desa-sm.dvlp.asia/desa-cantik/api/[slug]/[sheet]` (format JSON live/cached).
   - **Output**: Dataset Excel (`.xlsx`), Naskah Buku Publikasi PDF Siap Cetak, Monografi Desa, dan Infografis Demografi format HD.
   - **Ketentuan**: Tanpa registrasi berbelit, tanpa surat pengantar, dan tanpa verifikasi manual.
2. **Jalur 2 — Layanan Fasilitasi Cepat (*Offline & WhatsApp*) — ⏱️ 15 s.d. 30 Menit**:
   - **Sasaran**: Instansi pemerintah, akademisi/mahasiswa, atau pemohon data disagregasi agregat khusus yang memerlukan asistensi teknis statistik.
   - **Kanal Akses**: Loket Kantor Desa / Kelurahan atau kontak WhatsApp resmi Agen Statistik Desa.
     - Sungai Bakau Kecil: `+62 815-4928-3541`
     - Pasir Palembang: `+62 857-5171-8089`
     - Pasir Wan Salim: `+62 897-7539-550`
   - **Ketentuan Privasi**: Murni data agregat non-BNBA, langsung diproses oleh Agen Statistik tanpa menunggu tanda tangan Kades/Lurah.

---

## Progress Log
- **2026-08-14**: Menyempurnakan SOP Permintaan Data untuk seluruh desa/kelurahan binaan Desa Cantik 2026 (**Sungai Bakau Kecil**, **Pasir Palembang**, dan **Kelurahan Pasir Wan Salim**) dengan aturan ketat: (1) Hanya melayani data agregat non-*by name by address* (UU No. 27/2022 PDP), (2) Proses Jalur 2 dipercepat menjadi 15 s.d. 30 menit langsung oleh Petugas Agen Statistik tanpa memerlukan tanda tangan basah Kepala Desa / Lurah, (3) Mengintegrasikan nomor kontak WhatsApp resmi per desa/kelurahan (`+62 815-4928-3541` untuk SBK, `+62 857-5171-8089` untuk Pasir Palembang, dan `+62 897-7539-550` untuk Pasir Wan Salim), serta menyematkan diagram alur vektor SVG yang rapi dan siap cetak 2 halaman penuh tanpa header/footer peramban.
- **2026-08-13**: Memperbaiki duplikasi penulisan jabatan Pj. pada tanda tangan Kata Pengantar (`kades_title.upper()`) dan mengembalikan tata letak baku halaman `KONTRIBUTOR DATA / DATA CONTRIBUTORS` (Halaman iii) berstandar tata naskah diseminasi BPS. Mengompilasi ulang seluruh publikasi desa dalam angka (SBK, Pasir Palembang, Pasir Wan Salim) ke format PDF & DOCX.
- **2026-08-10**: Menyelesaikan audit dan perbaikan menyeluruh (*comprehensive overhaul*) pada DDA Engine (`kb/dda_generator/`) sehingga 100% elemen publikasi Desa/Kelurahan Dalam Angka (Statistik Kunci Tabel 0.1, Tabel Bab 3 & Bab 5, Infografis/Grafik Visualisasi, Ulasan Narasi Bilingual, dan Penjelasan Teknis) bersifat dinamis 100% berbasis data CAPI aktual per desa/kelurahan. Menghapus seluruh nilai/pengali sintetis (`* 0.71`, `* 0.09`, `92,33%` default) dan memastikan variabel yang tidak dikumpulkan di suatu desa (seperti KTP-el atau Layak Huni di Pasir Wan Salim) tidak ditampilkan dalam tabel maupun infografis. Menyajikan data aktual CAPI Ketenagakerjaan (Usia Kerja Bekerja 1.094 jiwa), UMKM (126 KK), & BPJS (2.655 jiwa) untuk Kelurahan Pasir Wan Salim, serta Bahan Bangunan (Dinding Tembok 837 unit, Atap Seng 849 unit, Sanitasi BAB 748 KK) & Rumah Layak Huni Aktual (65,90%) untuk Desa Pasir Palembang.
- **2026-08-10**: Mengoreksi dan menyelaraskan metrik metadata serta publikasi Pasir Palembang sesuai standar metodologi CAPI mikrodata: memperbarui `Nama Kegiatan` menjadi **"Pendataan Sosial Keluarga dan Fasilitas Umum Desa Cantik Pasir Palembang 2026"**, memperjelas `Cara Pengumpulan Data` menjadi **"Wawancara langsung (CAPI) pendataan bangunan tempat tinggal biasa per keluarga dan observasi geospasial fasilitas desa menggunakan aplikasi mobile AppSheet"** (tanpa penyebutan agregat RT), serta mengisolasikan pembersihan nilai invalid CAPI (`safe_int` sanitization `-1` menjadi `0`) sehingga total penduduk konsisten di angka **3.679 jiwa**.
- **2026-08-10**: Membakukan **SOP Wajib Konfirmasi User & Anti-Asumsi** pada `GEMINI.md` untuk kompilasi metadata & publikasi desa/kelurahan baru. Merefaktor mesin metadata (`builder.py`, `fetcher.py`, `typst_renderer.py`) untuk: (1) Mengharuskan konfirmasi nama kegiatan, status administrasi (Kelurahan vs Desa), serta tab sheet eksplisit (`rt_tab`, `fas_tab`), (2) Mengisolasi Pasir Wan Salim murni CAPI Keluarga tanpa Fasilitas Umum (`fas_tab` kosong) dan menghapus header tabel kosong dari PDF/Markdown, (3) Melakukan audit ketat pada `MS-INDIKATOR` di mana indikator HANYA dicantumkan jika variabel pembentuknya terbukti ada di sheet desa, (4) Mengubah ukuran font tabel Typst menjadi 7.5pt dan memperluas *zero-width space* (`wrap-var`) ke karakter `_`, `(`, `)`, `/`, `?` sehingga bebas overflow, dan (5) Memperbaiki nomenklatur Pasir Wan Salim 100% konsisten sebagai **Kelurahan Pasir Wan Salim**.
- **2026-08-09**: Membakukan dan merefaktor mesin pembuat metadata menjadi package modular `kb/metadata_generator/` berarsitektur *Decoupled DTO & Engine*. `builder.py` menyusun DTO `DesaMetadataDTO` murni sebagai Single Source of Truth, yang kemudian dikirim ke `markdown_renderer.py` dan `typst_renderer.py` tanpa percabangan hardcode nama desa di layer renderer. Menghapus teks `(Sheet1)` dari judul tabel CAPI, menyempurnakan seluruh opsi isian (*enum*) CAPI AppSheet, serta menggunakan sintaks fraksi matematika Typst (`frac(...)`) yang rapi.
- **2026-08-09**: Membakukan prinsip arsitektur *Decoupled DTO & Engine* pada `kb/dda_generator/` di mana pengolah data (`calculator.py`) mentransformasikan data mentah (baik agregat RT maupun mikrodata CAPI) menjadi DTO `DesaPublicationData` murni sebelum dikirim ke renderer. Menyempurnakan layout HTML & PDF DDA sesuai Pedoman Diseminasi BPS: menambahkan Halaman Katalog BPS & Hak Cipta resmi pada Halaman ii, mematikan running header pada halaman romawi (ii s.d. ix), memastikan ketiadaan ISSN untuk publikasi desa, serta memperbaiki garis titik-titik pembatas (*dots leader*) pada Daftar Tabel.
- **2026-08-09**: Berhasil merefaktor dan menggeneralisasikan mesin pembuat publikasi **Desa Dalam Angka (DDA Engine)** ke dalam package modular `kb/dda_generator/` dan menambahkan subcommand CLI `kb dda [nama-desa-kebab]`. Sistem kini mampu menarik data live Google Sheets/CSV, mengalkulasi seluruh metrik statistik per RT secara dinamis (tanpa hardcode), serta mengompilasi naskah 5 Bab Markdown, HTML bilingual A4, dan PDF Siap Cetak via Headless Chrome untuk desa manapun secara universal.
- **2026-07-10**: Memperbaiki modul data monitoring `data.py` untuk mengikutsertakan kolom tindakan admin kabupaten (`COMPLETED BY Admin Kabupaten` dan `EDITED BY Admin Kabupaten`) ke dalam metrik penyelesaian. Membuat modul baru `completed.py` yang otomatis berjalan di setiap eksekusi `kb se-monitor` untuk mengekspor daftar Sub-SLS yang sudah 100% Approved (total 56 wilayah) ke dalam berkas `kegiatan/sensus-ekonomi-2026/2026/outputs/subsls_selesai.csv`.
- **2026-07-12**: Mengorganisasi surat dinas umum/administratif non-kegiatan statistik (Surat Pembinaan Pelanggaran Disiplin Laporan Perkawinan dan Perceraian B-415/61513/KP.380/2026) di bawah folder baru `kegiatan/kepegawaian/2026/` menggunakan tautan relatif. Verifikasi menunjukkan tenggat waktu (31 Juli 2026) berhasil dipindai dan ditampilkan oleh skrip CLI `kb.py schedule`. Merapikan nama berkas template menjadi `template-laporan-perkawinan-pertama.docx` (kebab-case tanpa spasi) dan mendokumentasikan aturan organisasi berkas administrasi dan template di dalam root `README.md`.
- **2026-07-14**: Melakukan rebase branch lokal `main` ke `origin/main` terbaru. Menyelesaikan konflik merge pada `scripts/kb/se_monitor/data.py` (dengan mempertahankan perbaikan variabel `comp_admin` dkk. agar terhindar dari NameError) serta file CSV/JSON. Mengalihkan kredensial GitHub CLI (`gh`) aktif ke organisasi `ipds6104` dan berhasil melakukan push semua commit lokal ke repositori GitHub.
- **2026-07-14**: Menambahkan modul `cmd_latsar.py` dan subcommand baru `kb latsar` pada skrip CLI `kb.py` untuk mengotomatiskan penarikan serta sinkronisasi jadwal Latsar CPNS Golongan III Angkatan 10 tahun 2026 dari Google Sheets (secara spesifik untuk Kelompok 2 tempat Akma Batrisyia Jazima berada). Menginisialisasi struktur folder kegiatan Latsar di `kegiatan/latsar-cpns/2026/` yang memuat folder data pendukung, log mentoring, rancangan, dan laporan aktualisasi untuk Akma Batrisyia Jazima dan CPNS Kedua.
- **2026-07-14**: Mengimplementasikan perintah `kb sync-sheets` (didukung oleh `google_sheets.py` dan `cmd_sync_sheets.py`) untuk sinkronisasi massal seluruh milestones kegiatan dari basis pengetahuan ke Google Sheets pribadi pengguna. Melakukan konfigurasi OAuth 2.0 Credentials (Desktop App) dan memperbarui `.gitignore`. Menambahkan dokumentasi integrasi Google Sheets (`unified_milestones`) dan panduan pemanfaatan data JSON untuk developer visualisasi pada berkas `README.md`.
- **2026-07-14**: Mengimplementasikan alur otomatisasi harian terpadu OS-Independent melalui perintah `kb auto-update` (menjalankan `git pull`, `latsar`, dan `sync-sheets` secara berurutan). Membuat berkas konfigurasi GitHub Actions di `.github/workflows/sync-sheets.yml` untuk memfasilitasi otomatisasi harian penuh berbasis cloud.
- **2026-07-14**: Berhasil mengonfigurasi GitHub Secrets (`GOOGLE_CREDENTIALS`, `GOOGLE_TOKEN`, dan `SPREADSHEET_ID`) secara langsung ke repositori `ipds6104/knowledge-base` menggunakan GitHub CLI (`gh`) untuk mendukung workflow otomatisasi di cloud.
- **2026-07-14**: Memperbarui status 3 milestone Evaluasi EPSS 2026 ke status 'selesai' dan menambahkan milestone interviu EPSS Pemkab Mempawah pada 15 Juli 2026 berdasarkan berkas undangan resmi. Mengoptimalkan modul `cmd_sync_sheets.py` agar secara dinamis menyertakan semua kunci tambahan dari frontmatter deadlines markdown ke dalam kolom `attributes_json` Google Sheets.
- **2026-07-14**: Menambahkan milestone Penilaian Interviu EPSS Pemkab Kubu Raya oleh BPS Mempawah (selaku Penilai Badan) pada 15 Juli 2026 pukul 13.30 WIB beserta tautan Google Slides bahan tayang paparan.
- **2026-07-14**: Menyalin dokumen keputusan Bupati Mempawah terkait Susunan Keanggotaan Tim Penilai Internal (TPI) EPSS Kabupaten Mempawah 2026 ke berkas `sk-tpi-mempawah-2026.md` dan menautkannya ke README utama kegiatan EPSS.
- **2026-07-14**: Menyepakati batasan kerja Agent di mana Agent basis pengetahuan hanya bersifat Read-Only untuk repositori eksternal (seperti `sikendis`), melaporkan diagnosis kesalahan ke pengguna, dan menyerahkan penulisan/modifikasinya kepada AI khusus repositori bersangkutan.
- **2026-07-14**: Menambahkan modul `cmd_chat.py` dan subcommand baru `kb chat` untuk mengurai berkas zip ekspor chat WhatsApp, menyaring tautan bersama, melakukan pencarian kontekstual, dan mengekstrak jadwal/milestone penting untuk menyokong proses pemeliharaan data.
- **2026-07-14**: Memindahkan data pegawai dari root (`Data_Pegawai_2026-07-14.xlsx`) ke `data/pegawai/Data_Pegawai.csv` (hanya kolom Nama, Email, Jabatan, Panggilan — tanpa NIP/data sensitif). Mengimplementasikan modul `user_identity.py` dengan mekanisme deteksi pengguna aktif 2-lapis (cascade: `KB_USER_EMAIL` di `.env` → `git config user.email`). Menambahkan subcommand `kb whoami` dan file template `.env.example` untuk memudahkan setup di laptop baru.
- **2026-07-18**: Melakukan sinkronisasi repositori lokal `knowledge-base` dengan `git pull --rebase` ke `origin/main` terbaru, menjalankan workflow `kb auto-update` untuk memproses pembaruan status jadwal Latsar CPNS Kelompok 2, serta menganalisis dan mendokumentasikan aturan bisnis dan rekap kinerja PML Sensus Ekonomi 2026 per 15 Juli 2026 (hasil: ~36%) dan per kondisi real-time saat ini (hasil: 32.39%).
- **2026-07-18**: Membuat kegiatan baru `evaluasi-sakip-dan-sinergi` periode `2026` via CLI `kb create`, serta mendokumentasikan panduan pelaporan capaian kinerja Triwulan II 2026 secara komprehensif (aturan Sinergi, kertas kerja Excel, notulen rapat, timeline, alur data) berdasarkan berkas transkrip YouTube `internalisasi_sinergi_youtube.md` dan mengintegrasikan catatan koordinasi internal serta capaian indikator kunci (EPSS & PEKPPP) dari chat WhatsApp tim SAKIP, serta aturan tindak lanjut LHE & Renstra hasil koordinasi BPS se-Kalbar.
- **2026-07-18**: Merestrukturisasi penyimpanan grup WhatsApp koordinasi umum/berkelanjutan ke direktori terpusat `data/chats/`, memperbarui logika pencarian berkas di CLI `scripts/kb/cmd_chat.py`, membuat README pendukung konteks grup, serta mendokumentasikan best practices penataan grup WhatsApp (single vs multi-kegiatan) pada root README.md, menautkan relative links obrolan WhatsApp pada README.md kegiatan Sensus Ekonomi 2026 dan EPSS 2026, menganalisis dan mengekstrak info taktis (timeline ekstensi penilaian, prosedur Simbatik, insiden Data Center) dari chat log EPSS, memperbarui aturan NDA FASIH-DATA, konfirmasi paket data, struktur database (schema/tables), panduan anomali & UK, serta riwayat rilis template/validasi aplikasi pada Sensus Ekonomi 2026, membakukan aturan wajib memicu sync-sheets/auto-update setiap kali ada perubahan jadwal, menyusun panduan penanganan kendala teknis terpadu (troubleshooting guide) petugas lapangan, serta mendokumentasikan salinan Surat Dinas BPS Pusat No. B-69/07000/PR.100/2026 tentang penanganan missing values, anomali, dan ketidakwajaran indikator pada Sensus Ekonomi 2026.
- **2026-07-20**: Memperbarui berkas [README.md](file:///c:/projects/knowledge-base/kegiatan/evaluasi-sakip-dan-sinergi/2026/README.md) pada kegiatan SAKIP/SINERGI untuk mencakup aturan baru pengukuran kinerja Triwulan II 2026 (persyaratan direct entry per IKU PK di Sinergi, kewajiban upload berkas pembanding sebagai mitigasi risiko data hilang, serta rincian daftar kegiatan RO Prioritas Nasional, Prioritas Presiden, dan Isu Strategis untuk ditambahkan ke Notulen) dengan batas akhir 22 Juli 2026. Memicu sinkronisasi data jadwal ke Google Sheets menggunakan `kb sync-sheets`.
- **2026-07-20**: Mendokumentasikan pengumuman resmi Direktorat SIS dan 10 klausul Non-Disclosure Agreement (NDA) untuk pembagian data dan aktivasi akses FASIH-DATA BPS RI pada Sensus Ekonomi 2026 ke dalam berkas baru [nda-fasih-data-se2026.md](file:///c:/projects/knowledge-base/kegiatan/sensus-ekonomi-2026/2026/docs/nda-fasih-data-se2026.md) serta memperbarui tautan rujukannya pada [README.md](file:///c:/projects/knowledge-base/kegiatan/sensus-ekonomi-2026/2026/README.md).
- **2026-07-20**: Membuat kegiatan baru `kecamatan-dalam-angka` periode `2026` via CLI `kb create` berdasarkan Surat Dinas BPS Provinsi Kalbar No. B-632/61000/KS.200/2026 tentang penyusunan publikasi Kecamatan Dalam Angka (KCDA) 2026. Mendokumentasikan batas upload (23 September 2026) dan rilis resmi (28 September 2026) untuk 9 kecamatan di Kabupaten Mempawah, melengkapi daftar 24 tabel wajib, serta memicu sinkronisasi data jadwal ke Google Sheets.
- **2026-07-20**: Membaca berkas Excel `Daftar Perubahan Template DDA Kecamatan 2026.xlsx` di root via skrip Python otomatis dan mengonversinya menjadi dokumen markdown lengkap di [daftar-perubahan-dda-2026.md](file:///c:/projects/knowledge-base/kegiatan/kecamatan-dalam-angka/2026/daftar-perubahan-dda-2026.md), serta menambahkan tautan rujukan tersebut pada [README.md](file:///c:/projects/knowledge-base/kegiatan/kecamatan-dalam-angka/2026/README.md). Memindahkan berkas Excel asli ke folder kegiatan dengan nama kebab-case `daftar-perubahan-template-dda-kecamatan-2026.xlsx` untuk menjaga kerapian struktur direktori.
- **2026-07-20**: Membaca data acuan monitoring KCDA 2025 dari Google Sheets untuk memetakan alokasi PIC dan nomor publikasi estimasi KCDA 2026 bagi 9 kecamatan di Kabupaten Mempawah, serta mendokumentasikannya ke dalam [README.md](file:///c:/projects/knowledge-base/kegiatan/kecamatan-dalam-angka/2026/README.md).
- **2026-07-20**: Memperbarui berkas [README.md](file:///c:/projects/knowledge-base/kegiatan/kecamatan-dalam-angka/2026/README.md) pada kegiatan KCDA 2026 untuk mendokumentasikan target unggah internal (H-3 ARC atau 20 September 2026) dan merinci 10 tahapan kerja penyusunan publikasi (inisiasi Drive oleh Sukma, templating, Perjadin camat, peer review, dll.).
- **2026-07-20**: Menyusun linimasa detail kerja KCDA 2026 dengan menetapkan target penentuan PIC pada 3 Agustus 2026 dan menyinkronkan seluruh 6 milestones baru KCDA ke Google Sheets utama.
- **2026-07-20**: Menganalisis progres kerja PML Sensus Ekonomi 2026 untuk pencapaian target 40% per Kabupaten berdasarkan formula standar (Approve+Reject+Revoke+Edited By Admin+Reject By Admin) menggunakan alokasi total Kalbar (sheet 6100) dan realisasi. Membuat artifact laporan detail [pml_progress_report.md](file:///C:/Users/Admin/.gemini/antigravity-ide/brain/8204cedc-a531-4262-b816-b87235d1de06/pml_progress_report.md) yang menyajikan data klasemen Kalbar dan rincian PML Mempawah.
- **2026-07-20**: Membakukan proses pengecekan target PML 40% dengan mengintegrasikan opsi `--pml-40` pada sub-command `kb se-monitor` (mengimplementasikan modul baru [view_pml_40.py](file:///c:/projects/knowledge-base/scripts/kb/se_monitor/view_pml_40.py) dan memodifikasi [kb.py](file:///c:/projects/knowledge-base/scripts/kb.py) serta [__init__.py](file:///c:/projects/knowledge-base/scripts/kb/se_monitor/__init__.py)).
- **2026-07-20**: Mendokumentasikan progres Pemutakhiran Keluarga Kabupaten Mempawah dan merumuskan kerangka kerja cerdas untuk deteksi moral hazard (shortcut data) menggunakan pendekatan Z-score statistik, uji konsistensi spasial kecamatan, dan korelasi keluarga baru. Menambahkan bagian analisis ini serta daftar 12 PPL anomali teratas ke dalam berkas [README.md](file:///c:/projects/knowledge-base/kegiatan/sensus-ekonomi-2026/2026/README.md) Sensus Ekonomi 2026.
- **2026-07-20**: Melakukan analisis anomali terintegrasi pada lembar "Usaha/Perusahaan" dan "Usaha Keluarga" Google Sheets SE 2026 Mempawah. Menemukan pola bias non-aktif ekstrem (Z-Score $> 1.5\sigma$) dan mengidentifikasi anomali kritis berupa konsentrasi PPL anomali di bawah pengawasan PML Haris Rosi (4 PPL anomali) dan PPL Selvia (96.32% non-aktif). Mendokumentasikan temuan ini ke [README.md](file:///c:/projects/knowledge-base/kegiatan/sensus-ekonomi-2026/2026/README.md).
- **2026-07-20**: Memperbarui dan menyatukan seluruh proses deteksi anomali (Keluarga, Usaha/Perusahaan, Usaha Keluarga) serta menambahkan visualisasi PPL Terlambat (Proyeksi > 15 Agustus) lengkap dengan kolom nama PJ-Kuda pada modul [view_anomaly.py](file:///c:/projects/knowledge-base/scripts/kb/se_monitor/view_anomaly.py) dan melakukan push perubahan ke GitHub.
- **2026-07-20**: Memperbaiki typo *hardcoded* nama PJ-Kuda untuk PML Haris Rosi dari Andi Noviantoni menjadi Arini Faurizah pada berkas [view_anomaly.py](file:///c:/projects/knowledge-base/scripts/kb/se_monitor/view_anomaly.py) dan melakukan push ke GitHub.
- **2026-07-22**: Membuat dokumen [panduan-sql-lab-fasih-se2026.md](file:///home/ihza/Projects/knowledge-base/kegiatan/sensus-ekonomi-2026/2026/docs/panduan-sql-lab-fasih-se2026.md) yang merinci mekanisme integrasi Superset SQL Lab API, limitasi teknis Superset (`SELECT *` dilarang, max 1000 baris, max 25 kolom, client_id 10-char unik, rate limit 300 req/hari), alur login Playwright SSL BPS, serta kamus data 12 tabel Superset SE2026.
- **2026-08-13**: Membakukan dan merekayasa ulang arsitektur penarikan data SQLLab SE2026 dengan penemuan 3 temuan kritis: (1) **Limit Kapasitas Query 9.000 Baris** (ditegaskan bahwa 1 SQL query kini mereturn hingga 9.000 baris sehingga 126.976 assignment Mempawah ter-cover dalam 15 chunk), (2) **Zero-Pruning Server-Side Multi-Block CONCAT JSON Packaging** via [smart_json_packer.py](file:///home/ihza/Projects/knowledge-base/scripts/smart_json_packer.py) (mengemas 599+ kolom metadata dari 12 tabel menjadi 15 blok JSON output per query sehingga 100% kolom ditarik tanpa pruning dalam 5 SQL request total), dan (3) **Hasil Uji Paralelisme Empiris** (eksekusi sekuensial Pool=1 Worker terbukti 100% stabil & lebih cepat 39.8s vs paralel 48.6s karena batasan session lock server Superset).
- **2026-07-25**: Mendokumentasikan dinamika obrolan WhatsApp Sakernas Agustus 2026 dan irisan pendataan CAPI SE2026 ke dalam berkas [README.md](file:///home/ihza/Projects/knowledge-base/kegiatan/sakernas/2026-08/README.md) kegiatan Sakernas Agustus 2026, mencakup petunjuk teknis perbaikan assignment/sync FASIH SM, SOP mitigasi *respondent burden* (pendampingan penguasa wilayah RT/Kades, pemanfaatan data awal SE2026 untuk updating, pemahaman konsep keberadaan keluarga), pelaporan kasus penolakan wilayah via Form OneDrive Pimpinan, serta akar masalah sosiologis persepsi masyarakat.
- **2026-07-25**: Mengambil dan menyalin berkas dokumentasi Kamus Data FASIH (`data-dictionary-se2026.md`), Template Kuesioner (`template-kuesioner-se2026.md`), dan Superset SQL Crawler (`superset-sql-crawler-se2026.md`) dari repositori `fasih-sync-monitoring/docs/` ke dalam folder kegiatan [sensus-ekonomi-2026/2026](file:///home/ihza/Projects/knowledge-base/kegiatan/sensus-ekonomi-2026/2026/) serta menautkannya pada `README.md` kegiatan.
- **2026-07-26**: Mengoperasionalkan arahan Rakornas SE2026 Surabaya (26 Juli 2026), membuat utilitas CLI `kb se-schedule` untuk evaluasi irisan jadwal & penjadwalan query SQL Lab, mendokumentasikan limitasi data status OPEN pada replikasi OLTP FASIH, serta merestrukturisasi folder `kegiatan/sensus-ekonomi-2026/2026/` ke dalam subfolder terstruktur (`master_data/`, `outputs/`, `docs/`, `assets/`) dengan refactoring 18 skrip Python dan tautan markdown secara presisi. Push sukses ke GitHub repository `ipds6104/knowledge-base`.
- **2026-07-29**: Mengintegrasikan antarmuka monorepo `antigravity-repo-explorer` (Vue 3, PrimeVue v4, Rust Agent Daemon) untuk akses eksplorasi basis pengetahuan terpadu (*Unified Personal & Team Workspace Architecture*), otomasi penarikan prelist irisan Sakernas 2026-08 via `extract_sakernas_intersect.py`, dan penegakan *Path Jail Guard* serta *Secrets Exclusion Dual-Layer*.
- **2026-08-06**: Mengintegrasikan kegiatan baru `desa-cantik` periode `2026` via CLI `kb create`. Melakukan restrukturisasi folder kegiatan Desa Cantik 2026, memindahkan berkas ekspor chat WhatsApp Desa Cantik ke `kegiatan/desa-cantik/2026/`, serta membuat file README detail untuk main kegiatan dan 3 desa binaan (Pasir Palembang, Pasir Wan Salim, Sungai Bakau Kecil) yang merinci 28 bukti dukung LKE per desa. Membuat 3 berkas template prototype website interaktif premium (`pasir-palembang.html`, `pasir-wan-salim.html`, `sungai-bakau-kecil.html`) di bawah `assets/websites/` yang memuat visualisasi bar chart perkembangan data 3 tahun terakhir (LK Row 97) dan formulir permintaan data interaktif (LK Row 92) untuk bahan bukti dukung. Menyusun modul CLI baru `kb metadata` dan menetapkan SOP standar (SDI/BPS) untuk otomatisasi kompilasi metadata kegiatan, variabel, dan indikator secara rapi ke format PDF via Typst tanpa terjadi overlap teks atau overflow kolom.
- **2026-08-08**: Mendokumentasikan dan membakukan aturan Halaman Kosong (Blank Page) & Rekto-Verso BPS Edisi 2023 Revisi 2026 pada pedoman publikasi [pedoman-penyusunan-publikasi-bps.md](file:///home/ihza/Projects/knowledge-base/docs/pedoman-penyusunan-publikasi-bps.md) (aturan total Front Matter wajib genap dan setiap awal bab wajib bernomor ganjil/rekto). Menerapkan struktur Halaman Kosong ini secara presisi pada skrip generator publikasi Desa Sungai Bakau Kecil Dalam Angka 2026 (`scratch/generator.py`) dan menyinkronkan penomoran Daftar Isi (TOC) & Daftar Tabel (LOT).
- **2026-08-09**: Memperbarui dan mengabstraksi penomoran tabel publikasi DDA Engine menjadi format 2-tingkat (`1.1`, `1.2`, `2.1` s.d. `5.1`) serta mengintegrasikan data nama Ketua RT resmi BPS (`Alokasi Petugas.csv`) ke modul DTO `calculator.py` sehingga Kolom (2) pada Tabel 1.2 terisi 100% lengkap. Mengisikan Google Sheet ID resmi Pasir Wan Salim (`1XJ8ywTVfDQqeOpgLcDSEsayA3B7k_PvT9HqUcihrMNw`) dan mengimplementasikan mekanisme *Smart Validation Filtering* di `calculator.py` (`has_content` check) untuk secara otomatis memfilter entri kosong/non-respon dari kalkulasi agregasi statistik, sembari menjaga sistem tetap fleksibel 100% sehingga apabila petugas mengunggah isian baru di masa mendatang, engine akan secara otomatis mengkalkulasi ulang data publikasi secara real-time. Memperkaya DTO `metadata_generator` (`builder.py`) dengan daftar variabel CAPI mikrodata lengkap (termasuk Pasir Wan Salim) serta enum isian terstandarisasi Satu Data Indonesia (SDI/BPS) berbasis skema AppSheet. Membakukan pembedaan nomenklatur **Kelurahan vs Desa** secara otomatis pada `config.py`, `calculator.py`, `html_renderer.py`, dan `md_builder.py` di mana **Pasir Wan Salim** secara tepat diklasifikasikan sebagai **Kelurahan** (menggunakan nomenklatur *Lurah*, *Pemerintah Kelurahan*, *Kelurahan Pasir Wan Salim Dalam Angka*, serta pembagian sub-wilayah **8 Rukun Warga (RW 01 s.d. RW 08)** pada infografis Bab 1).
- **2026-08-10**: Mengoreksi dan menyelaraskan metrik metadata serta publikasi Pasir Palembang sesuai standar metodologi CAPI mikrodata: memperbarui `Nama Kegiatan` menjadi **"Pendataan Sosial Keluarga dan Fasilitas Umum Desa Cantik Pasir Palembang 2026"**, memperjelas `Cara Pengumpulan Data` menjadi **"Wawancara langsung (CAPI) pendataan bangunan tempat tinggal biasa per keluarga dan observasi geospasial fasilitas desa menggunakan aplikasi mobile AppSheet"** (tanpa penyebutan agregat RT), serta mengisolasikan pembersihan nilai invalid CAPI (`safe_int` sanitization `-1` menjadi `0`) sehingga total penduduk konsisten di angka **3.679 jiwa**.
- **2026-08-10**: Membakukan **SOP Wajib Konfirmasi User & Anti-Asumsi** pada `GEMINI.md` untuk kompilasi metadata & publikasi desa/kelurahan baru. Merefaktor mesin metadata (`builder.py`, `fetcher.py`, `typst_renderer.py`) untuk: (1) Mengharuskan konfirmasi nama kegiatan, status administrasi (Kelurahan vs Desa), serta tab sheet eksplisit (`rt_tab`, `fas_tab`), (2) Mengisolasi Pasir Wan Salim murni CAPI Keluarga tanpa Fasilitas Umum (`fas_tab` kosong) dan menghapus header tabel kosong dari PDF/Markdown, (3) Melakukan audit ketat pada `MS-INDIKATOR` di mana indikator HANYA dicantumkan jika variabel pembentuknya terbukti ada di sheet desa, (4) Mengubah ukuran font tabel Typst menjadi 7.5pt dan memperluas *zero-width space* (`wrap-var`) ke karakter `_`, `(`, `)`, `/`, `?` sehingga bebas overflow, dan (5) Memperbaiki nomenklatur Pasir Wan Salim 100% konsisten sebagai **Kelurahan Pasir Wan Salim**.
- **2026-08-12**: Menyelesaikan perbaikan tata letak publikasi DDA Engine (`kb/dda_generator/renderers/html_renderer.py`) sesuai standar Pedoman BPS: (1) Mengoreksi perataan badge nomor bab menjadi *flex-center* di tengah atas halaman rekto, (2) Memposisikan nomor halaman (*footer*) BPS 100% konsisten dengan aturan Halaman Ganjil (ODD) di kanan bawah dan Halaman Genap (EVEN) di kiri bawah, (3) Mengabaikan running header pada seluruh halaman romawi/frontmatter (Halaman ii s.d. ix), (4) Mengharuskan running header muncul konsisten di halaman Arab (Halaman 1 s.d. akhir), (5) Memasukkan penandatangan resmi (Lurah Pasir Wan Salim: H. Mulyadi, S.H.I; Pj. Kades Sungai Bakau Kecil: Agus Junaidi; Kades Pasir Palembang: Kades Pasir Palembang) pada Kata Pengantar & Katalog Halaman ii, (6) Menyelaraskan skema warna utama BPS Orange (`#eb8a3c` / `#0b3c5d`), dan (7) Mengurutkan urutan eksekusi penomoran halaman sehingga jumlah halaman romawi (`ix`) dan jumlah halaman Arab (`{tot_arabic_pages}`) pada Halaman ii, Daftar Isi (TOC), serta Daftar Tabel (LOT) terhubung 100% dinamis dan presisi secara matematis.
