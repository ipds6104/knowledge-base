# BPS Kabupaten Mempawah Knowledge Base - AI Agent Guidelines (GEMINI.md)

Dokumen ini berisi pedoman perilaku persisten, standar teknis, dan SOP operasional bagi AI agent (Gemini, Antigravity, dll.) yang bekerja di repositori ini. Repositori ini menampung multi-kegiatan statistik BPS (Sensus, Survei, Evaluasi) di berbagai periode waktu.

---

## 📋 SOP Monitoring & Evaluasi Multi-Kegiatan

Setiap kali pengguna menanyakan status progres, evaluasi, atau intervensi harian (misal: *"bagaimana progres kita hari ini?"* atau *"apa yang perlu diintervensi?"*):

1.  **Deteksi Konteks Kegiatan**: Identifikasi kegiatan mana yang dimaksud oleh pengguna (misal: *Sensus Ekonomi 2026*, *Sakernas*, *Susenas*, dll.) beserta periode aktifnya.
2.  **Rujuk README Kegiatan**: Buka dan baca berkas `README.md` di dalam folder kegiatan terkait (misal: `kegiatan/sensus-ekonomi-2026/2026/README.md`) untuk mencari tahu apakah ada SOP monitoring terstandardisasi atau perintah CLI khusus yang wajib dijalankan.
3.  **SOP Khusus Sensus Ekonomi 2026 (Aktif Juni-Agustus 2026)**:
    *   Jika pengguna menanyakan: *"oke di mana posisi kita hari ini untuk SE 2026 dan apakah ada yang perlu diintervensi agar on target?"* (atau variannya).
    *   **Wajib** secara otomatis menjalankan `./scripts/kb.py se-monitor -r` dan menyajikan laporan 6-seksi baku secara utuh.
4.  **Format Analisis Ad-Hoc PML-PPL (SE 2026)**:
    *   Apabila pengguna meminta pemeriksaan detail kinerja PML tertentu, asisten AI **wajib** menyajikan laporan dalam dua tabel standar (Tabel 1: Klasemen Makro PML vs Rata-rata/Lainnya, Tabel 2: Detail PPL di bawah PML tersebut diurutkan berdasarkan `Done %` terkecil) beserta diagnosis bottleneck dan rekomendasi tindakan taktis.

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

### 3. Deteksi PML Bottleneck (Antrean Kritis)
PML dianggap menumpuk verifikasi berkas (*bottleneck*) jika:
*   Berkas masuk dalam antrean (`submitted`) $> 20$ dokumen.
*   Tingkat pemeriksaan/kelulusan berkas (`approval_rate`) $< 20.00\%$ ($0.20$).

---

## 🛠️ Standar Kode & Struktur Proyek

*   **Thin Entrypoint**: Berkas `scripts/kb.py` adalah entrypoint CLI tipis. Semua logika bisnis didelegasikan ke package `kb/`.
*   **Isolasi Modul Kegiatan**: Setiap kegiatan yang membutuhkan skrip pemantauan/logika khusus **wajib** dibuatkan sub-package tersendiri di bawah `kb/` (seperti `kb/se_monitor/`) untuk menghindari pencampuran logika bisnis (*spaghetti code*) antar kegiatan.
*   **Epistemological Source**: Penentuan relasi struktural/hierarki petugas dalam kegiatan **wajib** dibaca dari file alokasi resmi kegiatan (seperti `Alokasi Petugas.csv` untuk SE2026). Jangan pernah menebak relasi ini secara mandiri.
*   **Batas Ukuran File**: Maksimal **500 baris** per berkas Python (diawasi oleh pre-commit hook di `.githooks/pre-commit`). Jaga modul tetap kecil, terfokus, dan modular (di bawah 300 baris).
*   **Analisis Repo**: Gunakan `python3 ./scripts/dump_tree.py` untuk memantau struktur direktori dan baris kode.
