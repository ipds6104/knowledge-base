# Windmill Automation & Pipeline Handbook (BPS Mempawah Knowledge Base)

Dokumen ini merupakan pedoman teknis baku, arsitektur sistem, dan panduan operasional implementasi otomasi alur kerja (*Workflows-as-Code*) dan penjadwalan data (*Cron Pipelines*) berbasis **Windmill** di lingkungan repositori Knowledge Base BPS Kabupaten Mempawah.

---

## 📌 I. Mengapa Windmill? (Arsitektur & Keunggulan)

Windmill bukan sekadar alternatif *task scheduler* atau *cron job* biasa, melainkan **Developer Platform & Automation Engine** generasi modern berperforma tinggi:

1. **Bare-Metal Performance (Rust Engine)**:
   - Worker dan orchestrator dibangun menggunakan bahasa **Rust**, jauh lebih ringan, cepat, dan hemat memori dibandingkan engine berbasis NodeJS (n8n) atau Python Celery (Airflow).
2. **Polyglot & Multi-Language (20+ Bahasa)**:
   - Mendukung Python 3 dengan package manager super cepat `uv` (bebas import PyPI apa pun tanpa rebuild container).
   - TypeScript/JavaScript dengan runtime ultra cepat `Bun` (default, cold-start ~0 ms) dan `Deno`.
   - Bash, Shell Linux murni, Go, Rust, PHP, PowerShell, R, Java, C#, DuckDB, dan SQL murni.
3. **Workflow-as-Code (WAC) & Visual DAG**:
   - Seluruh alur data, percabangan logika (*if-else*), perulangan (*loops*), dan penanganan kegagalan (*try-catch failure handlers*) dikelola secara deklaratif dalam format kode YAML/Python/TS yang dapat di-versi di Git.
4. **Auto-Generated UI & Type Validation**:
   - Setiap kali membuat skrip dengan signature typed (contoh: `def main(sheet_id: str, dry_run: bool = False):`), Windmill secara otomatis menggenerasikan formulir input UI di peramban tanpa perlu membuat frontend.
5. **Durable Execution & Concurrency Protection**:
   - Mendukung `no_flow_overlap: true` untuk mencegah penumpukan eksekusi pipeline jika tugas sebelumnya masih berjalan.
   - Mendukung *human-in-the-loop approvals* dan *durable sleep* tanpa mengonsumsi CPU/RAM worker selama masa tunggu.

---

## ⚙️ II. Konfigurasi Lingkungan & Server Windmill

### 1. Endpoint & Workspace Resmi
- **Base URL**: `https://wind.dvlpid.my.id`
- **Workspace**: `admins`
- **Username**: `ihza2karunia`
- **CLI Executable**: `wmill` (terpasang di path lingkungan pengguna)

### 2. Konfigurasi Workspace via CLI
Jika perlu menghubungkan workspace atau mengonfigurasi perangkat baru:
```bash
wmill workspace add Admins admins https://wind.dvlpid.my.id --token <WINDMILL_API_TOKEN>
wmill workspace use Admins
```

Verifikasi status koneksi:
```bash
wmill --version
wmill workspace list
```

---

## ⏱️ III. Standar Penjadwalan (Scheduler / Cron)

Windmill menggunakan format **6-field cron** standar (termasuk satuan detik):

```text
 ┌───────────── detik (0-59)
 │ ┌───────────── menit (0-59)
 │ │ ┌───────────── jam (0-23)
 │ │ │ ┌───────────── hari dalam bulan (1-31)
 │ │ │ │ ┌───────────── bulan (1-12)
 │ │ │ │ │ ┌───────────── hari dalam minggu (0-6, 0=Minggu)
 │ │ │ │ │ │
 * * * * * *
```

### 1. Contoh Ekspresi Cron Populer
| Kebutuhan Penjadwalan | Ekspresi Cron (6 Field) | Timezone | Keterangan |
| :--- | :--- | :--- | :--- |
| **Setiap Menit** | `0 * * * * *` | `Asia/Jakarta` | Dijalankan tepat pada detik ke-00 setiap menit. |
| **Setiap 15 Menit** | `0 */15 * * * *` | `Asia/Jakarta` | Monitoring cepat berkala. |
| **Setiap Jam** | `0 0 * * * *` | `Asia/Jakarta` | Sinkronisasi data operasional harian. |
| **Setiap Hari (08.00 WIB)** | `0 0 8 * * *` | `Asia/Jakarta` | Laporan briefing pagi (Morning Report). |
| **Setiap Hari (17.00 WIB)** | `0 0 17 * * *` | `Asia/Jakarta` | Rekapitulasi progres sore (Closing Report). |
| **Setiap Senin (07.30 WIB)** | `0 30 7 * * 1` | `Asia/Jakarta` | Evaluasi mingguan. |

### 2. Format File Schedule Deklaratif (`*.schedule.yaml`)
Penjadwalan disimpan dalam file berekstensi `.schedule.yaml` berdampingan dengan skrip atau flow:

```yaml
schedule: 0 0 8 * * *
timezone: Asia/Jakarta
enabled: true
script_path: f/mempawah/sync_google_sheets
is_flow: true
args:
  kegiatan: "kecamatan-dalam-angka-2026"
  mode: "full_sync"
summary: "Sync Harian Data Monitoring KCDA 2026"
description: "Menarik data monitoring 9 kecamatan dari Google Sheets ke penyimpanan lokal setiap jam 08:00 WIB"
no_flow_overlap: true
```

> [!IMPORTANT]
> **Aturan Wajib `no_flow_overlap: true`**:
> Seluruh pipeline ETL atau sinkronisasi data **wajib** menyertakan parameter `no_flow_overlap: true`. Hal ini mencegah terjadinya *race condition*, duplikasi penarikan data, atau kebocoran kuota API saat proses sinkronisasi sebelumnya memakan waktu lebih lama dari interval cron.

---

## 🐍 IV. Standar Penulisan Skrip Pipeline (Typed Scripts)

### 1. Standar Skrip Python (`.py`)
Skrip Python di Windmill berjalan dengan environment `uv`. Tentukan tipe data parameter secara eksplisit pada fungsi `main()`:

```python
# f/mempawah/fetch_sheet_data.py
"""
Summary: Fetch Sheet Data
Description: Menarik data tabular dari Google Sheets menggunakan Google API Client
"""
from typing import Dict, Any
import json

def main(spreadsheet_id: str, sheet_range: str, dry_run: bool = False) -> Dict[str, Any]:
    """
    Fungsi entrypoint Windmill. Parameter fungsi otomatis menjadi form input di UI web.
    """
    print(f"Fetching data from: {spreadsheet_id}, range: {sheet_range}")
    if dry_run:
        return {"status": "dry_run", "rows_count": 0}
    
    # Logika penarikan data...
    data = {"status": "success", "rows_count": 42}
    return data
```

### 2. Standar Skrip TypeScript Bun (`.ts`)
```typescript
// f/mempawah/aggregate_metrics.ts
export async function main(
  inputData: Record<string, any>,
  threshold: number = 75.0
): Promise<{ approved: boolean; score: number }> {
  console.log("Evaluating metrics with threshold:", threshold);
  return {
    approved: inputData.rows_count >= threshold,
    score: inputData.rows_count
  };
}
```

### 3. Standar Skrip Bash (`.sh`)
```bash
#!/bin/bash
# f/mempawah/backup_to_storage.sh
set -euo pipefail

TARGET_DIR="$1"
echo "Backing up artifacts from $TARGET_DIR..."
# Eksekusi rsync / tar / curl...
echo "Backup completed."
```

---

## 🔄 V. Standar Alur Kerja Terpadu (*Flows / OpenFlow*)

Flows menggabungkan beberapa langkah skrip menjadi satu alur pipeline utuh (*DAG*).

### Struktur Direktori Flow
Setiap flow disimpan dalam subdirektori dengan akhiran `.flow/`:
```text
f/mempawah/
├── sync_kcda_pipeline.flow/
│   └── flow.yaml
├── fetch_sheets.py
├── transform_data.py
├── notify_whatsapp.py
└── sync_kcda_pipeline.schedule.yaml
```

### Contoh File `flow.yaml`:
```yaml
summary: "Pipeline Sinkronisasi & Monitoring KCDA 2026"
description: "Pipeline hulu-ke-hilir: Penarikan Google Sheets -> Agregasi Metrik -> Notifikasi Status"
value:
  modules:
    - id: a
      summary: "Tarik Data Google Sheets"
      value:
        type: script
        path: f/mempawah/fetch_sheets
        args:
          spreadsheet_id: "1vVNdy6uOlMWrvXdD0ZZzoRKik85oMKAhAX7rvqFci18"
          sheet_range: "Monitoring!A1:Z100"
    - id: b
      summary: "Transformasi & Validasi Data"
      value:
        type: script
        path: f/mempawah/transform_data
        args:
          raw_data: "results.a"
    - id: c
      summary: "Kirim Notifikasi Rekapitulasi"
      value:
        type: script
        path: f/mempawah/notify_whatsapp
        args:
          payload: "results.b"
```

---

## 🛠️ VI. Windmill CLI Cheatsheet (`wmill`)

| Kategori | Perintah CLI | Penjelasan |
| :--- | :--- | :--- |
| **Workspace** | `wmill workspace list` | Melihat daftar workspace aktif dan URL remote. |
| | `wmill workspace use <name>` | Beralih ke workspace yang dipilih. |
| **Script** | `wmill script list f/<folder>` | Melihat daftar skrip pada folder tertentu. |
| | `wmill script preview <path> -d '<json_args>'` | Menjalankan skrip secara lokal tanpa deploy ke server. |
| | `wmill script push <file_path> <remote_path>` | Mengunggah/memperbarui skrip ke server Windmill. |
| **Flow** | `wmill flow list` | Melihat daftar alur kerja (flows). |
| | `wmill flow preview <flow_dir> -d '<json_args>'` | Menjalankan flow secara lokal untuk pengujian. |
| | `wmill flow push <flow_yaml> <remote_path>` | Mengunggah/memperbarui flow ke server. |
| **Schedule** | `wmill schedule list` | Melihat daftar cron schedule yang aktif beserta intervalnya. |
| | `wmill schedule enable <path>` | Mengaktifkan pemicu jadwal cron. |
| | `wmill schedule disable <path>` | Menghentikan sementara (pause) jadwal cron. |
| | `wmill schedule push <yaml_path> <path>` | Mengunggah konfigurasi cron baru ke server. |
| **Sync** | `wmill sync push` | Mendorong seluruh folder lokal yang berubah ke server Windmill. |
| | `wmill sync pull` | Menarik perubahan terbaru dari server Windmill ke repositori lokal. |
| | `wmill generate-metadata` | Memperbarui hash dependency dan schema form UI pada `wmill-lock.yaml`. |

---

## 🚨 VII. SOP Penegakan (Enforcement Policy di Knowledge Base)

Setiap agen AI atau pengembang di repositori `knowledge-base` **wajib** mematuhi aturan berikut:

1. **Mandat Windmill-First untuk Otomasi & Pipeline**:
   - Seluruh pipeline data hulu-ke-hilir (penarikan data rutin dari API/Sheets, transformasi data bertingkat, rekapitulasi terjadwal, dan pemicuan berkala) **WAJIB MENGGUNAKAN WINDMILL**.
2. **Larangan Cron/Daemon Liar Lokal**:
   - **DILARANG KERAS** membuat script background liar di terminal lokal (seperti loop `while true; do ... sleep 3600; done` atau daemon `nohup` tak terlacak) untuk alur kerja yang membutuhkan keandalan (*durability*) dan penjadwalan. Seluruh tugas terjadwal harus dideklarasikan sebagai file `.schedule.yaml` di Windmill.
3. **Pengecualian Use-Case**:
   - Penggunaan skrip lokal non-Windmill hanya diperkenankan untuk:
     - Perintah ad-hoc interaktif sekali jalan (misal: `python scripts/kb.py whoami` atau `pdf-search`).
     - Script debugging lokal atau run test unit cepat di terminal developer.
4. **Living Knowledge Updates**:
   - Bila terdapat penambahan credential/resource baru atau flow baru, dokumentasikan perubahannya pada log repositori dan perbarui handbook ini.
