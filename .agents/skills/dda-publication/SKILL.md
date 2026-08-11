---
name: dda-publication
description: Agentic workflow untuk membuat, meng-audit data, menyusun ulasan narasi bilingual, dan mengompilasi publikasi Desa Dalam Angka (DDA) berstandar BPS.
---

# Agentic Workflow: Pembuatan & Audit Publikasi Desa Dalam Angka (DDA)

Skill ini memberikan panduan operasional *agentic* bagi AI Agent ketika mengelola, meng-audit, atau mengenerasikan publikasi **Desa Dalam Angka (DDA)** untuk desa manapun di Kabupaten Mempawah (seperti *Sungai Bakau Kecil*, *Pasir Palembang*, *Pasir Wan Salim*, dll.) menggunakan DDA Engine (`kb dda`).

---

## 📋 Alur Kerja Agentic (5-Step Agentic Workflow)

Saat pengguna meminta pembuatan, perbaikan, atau pembuatan ulang publikasi Desa Dalam Angka:

### 1. Ingestion & Data Audit (Pemeriksaan Anomali Lapangan)
Sebelum menggenerasikan publikasi, **selalu periksa kesehatan data** dari Google Sheet / AppSheet:
- **Bumbung Rumah vs KK**: Flag jika `Bumbung = 0` padahal ada KK/Jiwa, atau jika `Bumbung > KK * 2` (terutama jika angka bumbung persis sama dengan Total Jiwa, menandakan input tertukar).
- **Typo Nama Wilayah**: Periksa ejaan nama RT/Dusun (contoh: `SENGGIIRING` vs `SENGGIRING`).
- **KTP-el & Bansos**: Periksa jika `KTP = 0` padahal ada penduduk usia wajib KTP (≥17 thn).
- **Tindakan Agent**: Informasikan temuan anomali atau terapkan aturan sanitasi cerdas sebelum pencetakan.

### 2. Eksekusi Engine CLI (`kb dda`)
Jalankan perintah CLI DDA Engine:
```bash
python scripts/kb.py dda [nama-desa-kebab] [--sheet-id SHEET_ID] [--year 2026]
```
- Mesin akan menarik data live/cache, mengalkulasi seluruh metrik baku per RT, serta membuat naskah Markdown, HTML bilingual A4, dan PDF Siap Cetak.

### 3. Contextual Narrative Synthesis (Ulasan Deskriptif Bilingual)
Pastikan narasi deskriptif pada Bab 1 s.d. Bab 5 ditulis secara kaya, analitis, dan kontekstual berbasis data desa bersangkutan:
- **Demografi (Bab 2)**: Ulas jumlah penduduk, proporsi gender, dan *Sex Ratio*.
- **Pendidikan & Adminduk (Bab 3)**: Ulas tingkat perekaman KTP-el dan konsentrasi anak putus sekolah per RT.
- **Bantuan Sosial (Bab 4)**: Ulas sebaran KPM penerima PKH, BPNT, dan BLT Dana Desa.
- **Perumahan & Lingkungan (Bab 5)**: Ulas total bumbung hunian, kepadatan hunian (jiwa/rumah), dan persentase rumah layak huni (RLH).

### 4. Layout & Page Budget Quality Assurance (Visual QA)
Verifikasi bahwa layout HTML/PDF A4 mematuhi **BPS Publication Layout Rules**:
- **Zero-Overlap Budget**: Maksimal 12 baris data untuk halaman pertama bab (dengan narasi), 13-14 baris untuk *continued table*, dan 12 baris + total untuk halaman akhir.
- **Recto-Verso Headers**: Running header genap di kanan, ganjil di kiri.
- **No Concatenation Artifacts**: Pastikan tidak ada artefak teks sintaks seperti `' + dyn_...`.

### 5. Repository & Knowledge Base Sync
- Simpan output di `kegiatan/desa-cantik/[tahun]/[desa]/` dan salinan PDF di `outputs/`.
- Perbarui `README.md` kegiatan desa terkait dan picu `kb sync-sheets` jika jadwal/milestone diperbarui.

---

## 🔗 Berkas Rujukan (References)

- **Pedoman Layout BPS**: [docs/pedoman-penyusunan-publikasi-bps.md](file:///home/ihza/Projects/knowledge-base/docs/pedoman-penyusunan-publikasi-bps.md)
- **Pedoman Pembuatan Publikasi BPS 2023**: [docs/pedoman-pembuatan-publikasi-bps-2023.md](file:///home/ihza/Projects/knowledge-base/docs/pedoman-pembuatan-publikasi-bps-2023.md)
- **Modul Engine Generator**: [scripts/kb/dda_generator/](file:///home/ihza/Projects/knowledge-base/scripts/kb/dda_generator/)
