# IPDS BPS Kabupaten Mempawah Knowledge Base

Repositori ini digunakan sebagai basis pengetahuan (knowledge base) terstruktur untuk seluruh kegiatan di Tim IPDS BPS Kabupaten Mempawah. Repositori ini dirancang khusus untuk diakses secara mandiri maupun melalui antarmuka asisten AI (Antigravity).

---

## 📂 Struktur Folder Kegiatan

Setiap kegiatan di periode tertentu memiliki foldernya masing-masing di bawah direktori `kegiatan/`:

```text
kegiatan/
└── [nama-kegiatan-slug]/
    └── [periode]/
        ├── README.md           # Berkas utama berisi metadata & deskripsi kegiatan
        ├── surat_tugas.pdf     # Berkas dokumen asli (PDF)
        └── surat_tugas.md      # Hasil konversi dokumen ke Markdown
```

*   **Nama Kegiatan**: Disuguhkan dalam format slug (lowercase, spasi diganti `-`). Contoh: `sakernas`, `sensus-ekonomi`.
*   **Periode**: Format waktu pelaksanaan. Contoh: `2026-06` (bulanan), `2026-Q2` (triwulanan), `2026` (tahunan).

### 📂 Dokumen Administrasi Umum & Template

Untuk dokumen yang tidak terikat pada survei/sensus spesifik (seperti surat dinas umum, kepegawaian, tata usaha, atau template laporan):

1. **Pengelompokan Kegiatan**:
   * Kelompokkan di bawah nama kategori umum seperti `kepegawaian` (untuk SDM/hukum/disiplin) atau `tata-usaha` (untuk persuratan umum).
   * Gunakan periode tahunan (misalnya `2026`) sebagai folder periode agar terkonsolidasi dengan baik.

2. **Aturan Penamaan File (Naming Conventions)**:
   * **Hindari penggunaan spasi** pada nama berkas untuk mencegah masalah di terminal/Git. Gunakan format kebab-case (`-`) atau snake_case (`_`).
   * **Surat Dinas**: Gunakan format `[Nomor_Surat].md` atau deskripsi singkat, misalnya `B-415_KP.380_2026.md`.
   * **Berkas Template/Lampiran**: Berikan prefiks `template-` di depan nama berkas, misalnya `template-laporan-perkawinan-pertama.docx`.

3. **Referensi Relative Path**:
   * Semua tautan dokumen di dalam `README.md` **wajib menggunakan relative path** (misal `B-415_KP.380_2026.md` atau `template-laporan-perkawinan-pertama.docx`), bukan absolute path, agar tautan tetap bekerja ketika di-clone di komputer lain atau diakses via web Git.

---

## 📝 Format Metadata YAML (`README.md` Kegiatan)

Setiap `README.md` di tingkat folder kegiatan memuat frontmatter YAML sebagai berikut:

```yaml
---
nama: "Sakernas"
kategori: "survey"
rutinitas: "rutin"
frekuensi: "bulanan"
peran: "ketua"
status: "aktif"
deadlines:
  - tanggal: "2026-06-25"
    kegiatan: "Pengumpulan Kuesioner"
    status: "belum"
  - tanggal: "2026-06-30"
    kegiatan: "Entri Data ke Web Sakernas"
    status: "belum"
---
# Sakernas (2026-06)

## Deskripsi Kegiatan
Detail tentang target, sampel, dan cakupan wilayah.

## Catatan Pelaksanaan
Catatan kendala lapangan atau evaluasi.
```

---

## 🛠️ Panduan Penggunaan Skrip CLI `kb.py`

Untuk memudahkan manajemen, pencarian jadwal, dan konversi dokumen, gunakan skrip utilitas `scripts/kb.py`.

### 1. Membuat Kegiatan Baru (`create`)
Membuat folder terstruktur beserta template `README.md` secara otomatis.
```bash
./scripts/kb.py create "[Nama Kegiatan]" "[Periode]" [options]
```
*Pilihan Opsi:*
*   `--kategori {survey,non-survey}` (default: `survey`)
*   `--rutinitas {rutin,non-rutin}` (default: `rutin`)
*   `--frekuensi {bulanan,triwulanan,semesteran,tahunan,10-tahunan,ad-hoc}` (default: `bulanan`)
*   `--peran {ketua,anggota}` (default: `ketua`)

*Contoh:*
```bash
./scripts/kb.py create "Sakernas Agustus" "2026-08" --frekuensi bulanan --peran ketua
```

---

### 2. Menampilkan Daftar Semua Kegiatan (`list`)
Menampilkan seluruh daftar kegiatan yang ada di basis pengetahuan dalam bentuk tabel.
```bash
./scripts/kb.py list
```

---

### 3. Melacak Jadwal & Deadline (`schedule`)
Memindai semua berkas `README.md` dan menampilkan daftar deadline secara kronologis.
```bash
./scripts/kb.py schedule [options]
```
*Pilihan Opsi:*
*   `--week`: Tampilkan deadline minggu ini saja.
*   `--month`: Tampilkan deadline bulan ini saja.
*   `--overdue`: Tampilkan deadline yang terlewat (melewati tanggal hari ini dan statusnya masih `belum`).

*Contoh:*
```bash
./scripts/kb.py schedule --week
```

---

### 4. Konversi Surat PDF ke Markdown (`convert`)
Mengonversi berkas surat tugas/edaran/dokumen berbentuk PDF ke berkas Markdown (`.md`) dengan nama yang sama.
```bash
# Mode Cepat & Offline (Menggunakan pdftotext bawaan poppler)
./scripts/kb.py convert "kegiatan/sakernas/2026-06/surat_tugas.pdf"

# Mode AI Vision (Menggunakan Gemini 3 Flash via Proxy - Presisi Tinggi)
./scripts/kb.py convert "kegiatan/sakernas/2026-06/surat_tugas.pdf" --ai
```
*Catatan Mode AI:* Membutuhkan konfigurasi API Key dan URL Proxy di berkas `.env` pada root repositori.

---

### 5. Monitoring Progres Sensus Ekonomi 2026 (`se-monitor`)
Melakukan penarikan rekapitulasi progres pencacahan secara real-time dari data `progress-pencacah.json` (hasil crawl aplikasi FASIH-SM) dan mencocokkannya dengan alokasi petugas di `Alokasi Petugas.csv`.

*   **Menampilkan Ringkasan Tim Anda (default: Ihza Fikri Zaki Karunia):**
    ```bash
    ./scripts/kb.py se-monitor
    ```
    Skrip akan menampilkan peringkat tim Anda, perbandingan dengan rata-rata kabupaten, kinerja masing-masing PML dan PPL di bawah pengawasan Anda, serta mendeteksi secara otomatis *bottleneck* persetujuan PML atau keterlambatan pencacahan PPL.

*   **Menampilkan Peringkat Seluruh PJ-Kuda Kabupaten Mempawah:**
    ```bash
    ./scripts/kb.py se-monitor --all-pj
    ```

*   **Menampilkan Ringkasan PJ-Kuda Lain:**
    ```bash
    ./scripts/kb.py se-monitor --pj "[Nama PJ-Kuda]"
    ```

---

### 6. Sinkronisasi Google Sheets Terpadu (`sync-sheets`)
Mengunggah dan menyinkronkan seluruh milestones kegiatan lokal di repositori ke Google Sheets pribadi untuk dashboard visualisasi eksternal.
```bash
./scripts/kb.py sync-sheets
```

---

### 7. Otomasi Harian Terpadu (`auto-update`)
Menjalankan seluruh rangkaian otomasi harian secara berurutan dan bebas OS (OS-independent):
1. Melakukan `git pull` untuk memperbarui berkas repositori lokal.
2. Mengunduh jadwal Latsar CPNS terbaru dari Google Sheets Pusdiklat.
3. Mengunggah seluruh milestones terbaru ke Google Sheets pribadi Anda.
```bash
./scripts/kb.py auto-update
```

---

### 8. Analisis Obrolan WhatsApp (`chat`)
Menganalisis berkas ekspor obrolan WhatsApp (`.zip`) yang disimpan di folder kegiatan. Perintah ini mendukung pencarian tautan, pencarian kata kunci, visualisasi keaktifan pengirim, serta deteksi tenggat waktu/jadwal potensial dari obrolan secara instan.
*   **Menampilkan daftar berkas chat WhatsApp yang tersedia:**
    ```bash
    ./scripts/kb.py chat list
    ```
*   **Menampilkan ringkasan statistik obrolan:**
    ```bash
    ./scripts/kb.py chat info [index_atau_nama_file]
    ```
*   **Mengekstrak seluruh tautan/links yang dibagikan:**
    ```bash
    ./scripts/kb.py chat links [index_atau_nama_file]
    ```
*   **Mencari pesan berdasarkan kata kunci:**
    ```bash
    ./scripts/kb.py chat search [index_atau_nama_file] -q "[kata_kunci]"
    ```
*   **Mendeteksi jadwal/milestone potensial dari chat:**
    ```bash
    ./scripts/kb.py chat extract [index_atau_nama_file]
    ```

---

## ⚙️ Alur Otomatisasi Harian (Bebas OS)

Untuk menjaga agar data di Google Sheets selalu sinkron tanpa interaksi manual:

### 1. Otomatisasi Cloud (GitHub Actions)
Pembaruan berjalan otomatis di cloud GitHub setiap hari pukul 00:00 UTC (07:00 WIB) dan setiap kali ada `push` ke branch `main`.

**Cara Mengonfigurasi Kredensial di GitHub:**
1. Masuk ke halaman repositori Anda di GitHub.
2. Buka menu **Settings** > **Secrets and variables** > **Actions**.
3. Tambahkan 3 Secret baru berikut:
   * **`GOOGLE_CREDENTIALS`** : Isi dengan seluruh konten teks dari file `credentials.json` lokal Anda.
   * **`GOOGLE_TOKEN`** : Isi dengan seluruh konten teks dari file `token.json` lokal Anda.
   * **`SPREADSHEET_ID`** : Isi dengan ID Spreadsheet target (`1OXmqaEgWczJ3um8zwRJfqjOp6Zklc_eSvvW687L57Y4`).

### 2. Otomatisasi Lokal (Cron / Task Scheduler)
* **Linux / macOS (Cron):**
  Buka konfigurasi cron dengan `crontab -e` dan tambahkan perintah berikut agar berjalan otomatis setiap pagi pukul 07:00:
  ```text
  0 7 * * * cd /path/to/knowledge-base && python3 scripts/kb.py auto-update
  ```
* **Windows (Task Scheduler):**
  Buat tugas baru (*Basic Task*) pada aplikasi *Task Scheduler* Windows untuk menjalankan `python` dengan parameter `scripts/kb.py auto-update` setiap pagi.

---

## 📊 Integrasi Google Sheets Terpadu (`unified_milestones`)

Repositori ini bertindak sebagai **Data Writer** yang memperbarui database Google Sheets secara massal, sementara aplikasi dashboard eksternal bertindak sebagai **Data Reader/Consumer** yang merender visualisasi.

### 1. Struktur Skema Data (Tabel Milestones)
Tab `unified_milestones` memiliki kolom baku sebagai berikut:

| Nama Kolom | Deskripsi | Contoh Nilai |
| :--- | :--- | :--- |
| `activity_id` | Slug nama kegiatan. Berguna untuk ID filter. | `latsar-cpns-2026`, `sakernas-agustus-2026` |
| `kategori` | Klasifikasi makro kegiatan. | `survey`, `non-survey`, `kepegawaian` |
| `tanggal` | Format tanggal ISO baku. | `2026-07-30` (Format: `YYYY-MM-DD`) |
| `kegiatan` | Deskripsi atau nama tenggat waktu kegiatan. | `Kelompok 2: Sync Seminar Rancangan` |
| `status` | Status penyelesaian otomatis berdasarkan hari ini. | `selesai`, `belum`, `overdue` |
| `pic` | Kode peran penanggung jawab utama. | `ketua`, `anggota` |
| `attributes_json` | Metadata kustom kegiatan dalam format string JSON. | `{"activity_name": "Latsar CPNS 2026", "kelompok": 2}` |

### 2. Cara Memanfaatkan Data (Panduan Developer Visualisasi)

Bagi pengembang repositori visualisasi, data dari sheet ini dapat dimanfaatkan untuk membuat antarmuka interaktif:
*   **Visualisasi Kalender Grid:**
    Petakan baris berdasarkan kolom `tanggal`. Gunakan kolom `status` untuk mewarnai indikator (Hijau untuk `selesai`, Kuning untuk `belum`, Merah untuk `overdue`).
*   **Pemfilteran Lintas Kegiatan:**
    Sediakan tombol dropdown berbasis `activity_id` untuk menampilkan kalender satu kegiatan spesifik, atau dropdown berbasis `kategori` untuk memisahkan kalender Survei Statistik vs Kalender Non-Survei.
*   **Penguraian Atribut Kustom (`attributes_json`):**
    Uraikan (*parse*) string JSON di kolom terakhir untuk menampilkan komponen UI kontekstual:
    *   **Untuk Kasus Latsar:** Baca properti `kelompok` (misal: `{"kelompok": 2}`) untuk menyaring dan merender hanya jadwal Latsar milik Kelompok 2 tempat Akma berada.
    *   **Untuk Kasus Kepegawaian:** Baca properti `nomor_surat` (misal: `{"nomor_surat": "B-415"}`) untuk menampilkan nomor surat dinas terkait di pop-over detail kalender.


