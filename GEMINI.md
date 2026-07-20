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

---

## Progress Log
- **2026-07-10**: Memperbaiki modul data monitoring `data.py` untuk mengikutsertakan kolom tindakan admin kabupaten (`COMPLETED BY Admin Kabupaten` dan `EDITED BY Admin Kabupaten`) ke dalam metrik penyelesaian. Membuat modul baru `completed.py` yang otomatis berjalan di setiap eksekusi `kb se-monitor` untuk mengekspor daftar Sub-SLS yang sudah 100% Approved (total 56 wilayah) ke dalam berkas `kegiatan/sensus-ekonomi-2026/2026/subsls_selesai.csv`.
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
- **2026-07-20**: Mendokumentasikan pengumuman resmi Direktorat SIS dan 10 klausul Non-Disclosure Agreement (NDA) untuk pembagian data dan aktivasi akses FASIH-DATA BPS RI pada Sensus Ekonomi 2026 ke dalam berkas baru [nda-fasih-data-se2026.md](file:///c:/projects/knowledge-base/kegiatan/sensus-ekonomi-2026/2026/nda-fasih-data-se2026.md) serta memperbarui tautan rujukannya pada [README.md](file:///c:/projects/knowledge-base/kegiatan/sensus-ekonomi-2026/2026/README.md).
- **2026-07-20**: Membuat kegiatan baru `kecamatan-dalam-angka` periode `2026` via CLI `kb create` berdasarkan Surat Dinas BPS Provinsi Kalbar No. B-632/61000/KS.200/2026 tentang penyusunan publikasi Kecamatan Dalam Angka (KCDA) 2026 dengan batas akhir rilis 28 September 2026 (jumlah tabel wajib: 24 tabel, link template: https://linktr.ee/kcda2026_file). Memicu sinkronisasi data jadwal ke Google Sheets.

