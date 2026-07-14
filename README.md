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

