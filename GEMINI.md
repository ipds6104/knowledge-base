# BPS Kabupaten Mempawah Knowledge Base - AI Agent Guidelines (GEMINI.md)

Dokumen ini berisi pedoman perilaku persisten, standar teknis, dan SOP operasional bagi AI agent (Gemini, Antigravity, dll.) yang bekerja di repositori ini.

---

## 📋 SOP Monitoring Harian (Sensus Ekonomi 2026)

Setiap pagi dan sore, apabila pengguna menanyakan:
> **"oke di mana posisi kita hari ini untuk SE 2026 dan apakah ada yang perlu diintervensi agar on target?"** (atau varian serupa)

Agen AI **wajib** secara otomatis memproses alur evaluasi berikut:
1.  **Tarik Data Terbaru**: Jalankan `./scripts/kb.py se-monitor -r` untuk mendapatkan laporan 6-seksi yang baku.
2.  **Sajikan Laporan 6-Seksi**: Tampilkan laporan secara utuh kepada pengguna (termasuk status target harian, posisi makro Kalbar & Mempawah, delta perbandingan, daftar intervensi kritis, rekomendasi taktis Ketua SE, dan rekomendasi aksi cepat PJ-Kuda).

---

## ⚙️ Logika Bisnis & Batas Kritis Dinamis (Dynamic Thresholds)

Agen AI wajib mematuhi formula kalkulasi berikut yang telah terstandardisasi di dalam kode:

### 1. Deteksi PPL Terlambat Terkritis
Batas progres PPL lambat dihitung secara **dinamis** terhadap target ideal hari ini (`expected_pct`):
$$\text{ppl\_threshold} = \text{max}(3.00\%, \frac{\text{expected\_pct}}{100} \times 0.25)$$
*   Petugas disaring jika memiliki `target > 200` dan `completed_rate < ppl_threshold`.

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

*   **Thin Entrypoint**: Berkas `scripts/kb.py` adalah entrypoint CLI tipis. Semua logika bisnis didelegasikan ke package `kb/` dan sub-package `kb/se_monitor/`.
*   **Epistemological Source**: Penentuan relasi struktural PJ-Kuda $\rightarrow$ PML $\rightarrow$ PPL **wajib** diimpor dari `kb/se_monitor/hierarchy.py` yang mem-parse `Alokasi Petugas.csv`. Jangan pernah menebak relasi ini secara mandiri.
*   **Batas Ukuran File**: Maksimal **500 baris** per berkas Python (diawasi oleh pre-commit hook di `.githooks/pre-commit`). Jaga modul tetap kecil, terfokus, dan modular (di bawah 300 baris).
*   **Analisis Repo**: Gunakan `python3 ./scripts/dump_tree.py` untuk memantau struktur direktori dan baris kode.
