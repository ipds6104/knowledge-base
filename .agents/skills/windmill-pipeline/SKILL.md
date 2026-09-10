---
name: windmill-pipeline
description: Workflow-as-Code dan otomasi pipeline data terjadwal (cron) menggunakan platform Windmill (Rust Engine, 20+ bahasa, typed scripts, flow DAG, schedules).
---

# Agentic Workflow: Otomasi & Pipeline Data Berbasis Windmill

Skill ini memandu AI Agent dalam merancang, mengimplementasikan, menguji, dan mendeploy alur kerja otomasi data (*Workflows-as-Code*) serta penjadwalan berkala (*Cron Schedules*) menggunakan **Windmill** di lingkungan BPS Kabupaten Mempawah.

---

## 🎯 Kapan Menggunakan Windmill? (Mandat Kebijakan)

Gunakan Windmill sebagai **pilihan utama pertama** untuk:
1. **Pipeline ETL / Sinkronisasi Terjadwal**: Menarik data dari Google Sheets, Portal SDI, Web BPS, atau API eksternal secara harian/mingguan.
2. **Rekapitulasi & Monitoring Berkala**: Memicu perhitungan agregasi statistik atau pengecekan target progres (misal: SE 2026, KCDA 2026, Desa Cantik).
3. **Pemberitahuan & Alerting Otomatis**: Mengirim laporan atau notifikasi telegram/whatsapp/email secara terjadwal.
4. **Alur Multi-Langkah (DAG)**: Langkah A (fetch) $\rightarrow$ Langkah B (transform) $\rightarrow$ Langkah C (load/notify).

> [!WARNING]
> **Larangan Mutlak**: DILARANG membuat daemon `nohup`, background loop `sleep` manual di terminal, atau cron OS lokal yang tidak terlacak untuk kebutuhan pipeline data instansi. Gunakan penjadwalan deklaratif Windmill.

---

## 🏗️ 5-Step Agentic Workflow Pembuatan Pipeline

### 1. Desain Skrip Mandiri (Typed Scripts)
Tentukan bahasa yang paling tepat:
- **Python 3 (`uv`)**: Pemrosesan data statistik, manipulasi pandas/polars, integrasi API.
- **TypeScript Bun (`.ts`)**: Agregasi data cepat, validasi JSON, formatting.
- **Bash (`.sh`)**: Eksekusi CLI Linux, transfer file, backup arsip.

Pastikan fungsi memiliki type annotation lengkap agar form input UI terbentuk otomatis di web Windmill:
```python
def main(target_wilayah: str, limit: int = 100) -> dict:
    ...
```

### 2. Pengujian Skrip Lokal (`wmill script preview`)
Sebelum diunggah ke server, uji coba eksekusi skrip secara lokal:
```bash
wmill script preview f/mempawah/my_script.py -d '{"target_wilayah": "Jongkat", "limit": 50}'
```

### 3. Perakitan Alur Kerja (*Flow DAG*)
Jika pipeline memiliki lebih dari satu langkah, rangkai modul-modul skrip di dalam folder `.flow/` dengan berkas `flow.yaml`:
- Hubungkan input langkah berikutnya ke output langkah sebelumnya menggunakan notasi `results.<step_id>`.
- Tambahkan penanganan error atau fallback module jika diperlukan.

Uji coba flow secara lokal:
```bash
wmill flow preview f/mempawah/my_flow.flow -d '{"param1": "val1"}'
```

### 4. Konfigurasi Jadwal Cron 6-Field (`*.schedule.yaml`)
Tentukan waktu eksekusi menggunakan cron 6-field (detik, menit, jam, hari, bulan, hari-minggu) dengan timezone `Asia/Jakarta`:
```yaml
schedule: 0 0 8 * * * # Pukul 08:00 WIB setiap hari
timezone: Asia/Jakarta
enabled: true
script_path: f/mempawah/my_flow
is_flow: true
args: {}
summary: "Daily Morning Data Sync"
no_flow_overlap: true
```

### 5. Deployment ke Server Windmill
Unggah dan aktifkan alur kerja di server resmi:
```bash
# Push skrip atau flow
wmill flow push f/mempawah/my_flow.flow/flow.yaml f/mempawah/my_flow
# Push dan aktifkan jadwal cron
wmill schedule push f/mempawah/my_flow.schedule.yaml f/mempawah/my_flow_cron
wmill schedule enable f/mempawah/my_flow_cron
```

---

## 📚 Rujukan Lengkap
Baca pedoman arsitektur dan cheatsheet lengkap di:
👉 **[docs/windmill-handbook.md](file:///home/ihza/Projects/knowledge-base/docs/windmill-handbook.md)**.
