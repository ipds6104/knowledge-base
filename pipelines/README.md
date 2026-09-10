# BPS Mempawah Pipelines (Windmill Workflows-as-Code)

Direktori ini menampung seluruh skrip otomasi (*scripts*), alur kerja (*flows*), dan penjadwalan (*cron schedules*) berbasis **Windmill** untuk operasional data hulu-ke-hilir di lingkungan BPS Kabupaten Mempawah.

---

## 📂 Struktur Direktori

```text
pipelines/
├── wmill.yaml             # Konfigurasi sync workspace Windmill & shared codebases
├── wmill-lock.yaml        # Lockfile dependencies & content hash
├── README.md              # Dokumentasi & panduan teknis
└── f/
    ├── shared/            # Library bersama (BPS formatters, alert helpers)
    │   ├── bps_formatters.py
    │   └── alert_formatter.py
    └── mempawah_kcda/     # Domain Kecamatan Dalam Angka 2026
        ├── monitor_kcda_2026.py
        └── monitor_kcda_2026.schedule.yaml
```

---

## 🚀 Cara Kerja & Perintah Cepat

1. **Uji Coba Skrip Lokal (Preview)**:
   ```bash
   wmill script preview f/mempawah_kcda/monitor_kcda_2026.py -d '{"current_date_override": "2026-09-10"}'
   ```

2. **Push Skrip Tunggal ke Server**:
   ```bash
   wmill script push f/mempawah_kcda/monitor_kcda_2026.py
   ```

3. **Push & Aktifkan Jadwal Cron**:
   ```bash
   wmill schedule push f/mempawah_kcda/monitor_kcda_2026.schedule.yaml f/mempawah_kcda/monitor_kcda_2026_daily
   wmill schedule enable f/mempawah_kcda/monitor_kcda_2026_daily
   ```

4. **Sinkronisasi Metadata Schema Form UI**:
   ```bash
   wmill generate-metadata
   ```

5. **Sinkronisasi Seluruh Pipeline ke Server**:
   ```bash
   wmill sync push
   ```

Rujukan teknis lengkap: [docs/windmill-handbook.md](../../docs/windmill-handbook.md).
