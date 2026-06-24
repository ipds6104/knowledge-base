# BPS Kabupaten Mempawah Knowledge Base - AI Agent Guidelines (GEMINI.md)

Dokumen ini berisi pedoman perilaku persisten, standar teknis, dan SOP operasional bagi AI agent (Gemini, Antigravity, dll.) yang bekerja di repositori ini. Repositori ini menampung multi-kegiatan statistik BPS (Sensus, Survei, Evaluasi) di berbagai periode waktu.

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
    *   Wajib disajikan dalam bentuk **tabel** dengan kolom: `No`, `Nama PPL`, `PML Pengawas`, `PJ-Kuda`, `Target`, `Selesai`, `Done %`, dan `Est. Selesai`.
    *   Kolom `Done %` wajib menggunakan emoji status warna (`🟢`, `🟡`, `🔴`).
*   **Prosedur Pengecekan**: Jalankan perintah `python3 scratch/run_worst_projections.py` untuk mendapatkan daftar petugas dengan proyeksi selesai paling lama secara real-time dari Google Sheets.

---

## 🛠️ Standar Kode & Struktur Proyek

*   **Thin Entrypoint**: Berkas `scripts/kb.py` adalah entrypoint CLI tipis. Semua logika bisnis didelegasikan ke package `kb/`.
*   **Isolasi Modul Kegiatan**: Setiap kegiatan yang membutuhkan skrip pemantauan/logika khusus **wajib** dibuatkan sub-package tersendiri di bawah `kb/` (seperti `kb/se_monitor/`) untuk menghindari pencampuran logika bisnis (*spaghetti code*) antar kegiatan.
*   **Epistemological Source**: Penentuan relasi struktural/hierarki petugas dalam kegiatan **wajib** dibaca dari file alokasi resmi kegiatan (seperti `Alokasi Petugas.csv` untuk SE2026). Jangan pernah menebak relasi ini secara mandiri.
*   **Batas Ukuran File**: Maksimal **500 baris** per berkas Python (diawasi oleh pre-commit hook di `.githooks/pre-commit`). Jaga modul tetap kecil, terfokus, dan modular (di bawah 300 baris).
*   **Analisis Repo**: Gunakan `python3 ./scripts/dump_tree.py` untuk memantau struktur direktori dan baris kode.
