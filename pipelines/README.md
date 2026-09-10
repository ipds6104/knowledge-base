# BPS Mempawah Pipelines (Windmill Workflows-as-Code)

Direktori ini menampung seluruh skrip otomasi (*scripts*), alur kerja (*flows*), dan penjadwalan (*cron schedules*) berbasis **Windmill** untuk operasional data hulu-ke-hilir di lingkungan BPS Kabupaten Mempawah.

---

## 📂 Struktur Direktori

```text
pipelines/
├── wmill.yaml             # Konfigurasi sync workspace Windmill
├── README.md              # Dokumentasi & panduan
└── f/
    └── mempawah/          # Folder utama untuk alur kerja BPS Mempawah
        ├── sync_kcda_2026.py
        ├── sync_se2026_monitoring.py
        └── ...
```

---

## 🚀 Cara Kerja & Perintah Cepat

1. **Uji Coba Skrip Lokal**:
   ```bash
   wmill script preview f/mempawah/[nama_script].py -d '{"arg1": "val1"}'
   ```

2. **Push Skrip Tunggal**:
   ```bash
   wmill script push f/mempawah/[nama_script].py f/mempawah/[nama_script]
   ```

3. **Push Jadwal Cron**:
   ```bash
   wmill schedule push f/mempawah/[nama_schedule].schedule.yaml f/mempawah/[nama_schedule]
   wmill schedule enable f/mempawah/[nama_schedule]
   ```

4. **Sinkronisasi Seluruh Pipeline ke Server**:
   ```bash
   wmill sync push
   ```

Rujukan teknis lengkap: [docs/windmill-handbook.md](../../docs/windmill-handbook.md).
