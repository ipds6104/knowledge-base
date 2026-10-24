import { chromium } from "patchright";
import { writeFileSync, mkdirSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = resolve(__dirname, "../scratch/raw_podes_json");
mkdirSync(OUT_DIR, { recursive: true });

const ALL_RAW_CHARTS = [
  // --- KATEGORI 1: ASET FASILITAS & SARANA PRASARANA RIIL (DASHBOARD 518) ---
  { id: 12076, key: "raw_aset_pendidikan_negeri", name: "Aset Pendidikan Negeri", ds: 6439, limit: 10000 },
  { id: 12077, key: "raw_aset_pendidikan_swasta", name: "Aset Pendidikan Swasta", ds: 6441, limit: 10000 },
  { id: 12080, key: "raw_aset_kesehatan", name: "Aset Kesehatan", ds: 6442, limit: 10000 },
  { id: 12082, key: "raw_aset_perbankan", name: "Aset Perbankan", ds: 6444, limit: 10000 },
  { id: 12083, key: "raw_aset_ekonomi_pasar", name: "Aset Ekonomi & Pasar", ds: 6446, limit: 10000 },

  // --- KATEGORI 2: TABULASI FASILITAS & POTENSI DESA (DASHBOARD 578) ---
  { id: 11891, key: "raw_tabulasi_desa_master", name: "Tabulasi Status Desa R301", ds: 6343, limit: 1000 },
  { id: 11900, key: "raw_tabulasi_kewilayahan_blok3", name: "Tabulasi Kewilayahan Blok 3", ds: 6343, limit: 1000 },
  { id: 11903, key: "raw_tabulasi_pendidikan_tk_ra", name: "Tabulasi Pendidikan TK RA", ds: 6343, limit: 1000 },
  { id: 11906, key: "raw_tabulasi_pendidikan_sd_mi", name: "Tabulasi Pendidikan SD MI", ds: 6343, limit: 1000 },
  { id: 11909, key: "raw_tabulasi_pendidikan_smp_mts", name: "Tabulasi Pendidikan SMP MTs", ds: 6343, limit: 1000 },
  { id: 11912, key: "raw_tabulasi_pendidikan_sma_smk", name: "Tabulasi Pendidikan SMA SMK MA", ds: 6343, limit: 1000 },
  { id: 11915, key: "raw_tabulasi_pendidikan_ptn", name: "Tabulasi Pendidikan PTN", ds: 6343, limit: 1000 },
  { id: 12336, key: "raw_tabulasi_pendidikan_daycare", name: "Tabulasi Daycare", ds: 6343, limit: 1000 },
  { id: 11918, key: "raw_tabulasi_kesehatan_rs_balai", name: "Tabulasi Kesehatan RS Balai", ds: 6343, limit: 1000 },
  { id: 11921, key: "raw_tabulasi_kesehatan_puskesmas", name: "Tabulasi Kesehatan Puskesmas", ds: 6343, limit: 1000 },
  { id: 11924, key: "raw_tabulasi_kesehatan_klinik_praktek", name: "Tabulasi Kesehatan Klinik Praktek", ds: 6343, limit: 1000 },
  { id: 11927, key: "raw_tabulasi_kesehatan_poskes_apotek", name: "Tabulasi Kesehatan Poskes Apotek", ds: 6343, limit: 1000 },
  { id: 11930, key: "raw_tabulasi_ekonomi_pasar_swalayan", name: "Tabulasi Ekonomi Pasar Swalayan", ds: 6343, limit: 1000 },
  { id: 11933, key: "raw_tabulasi_ekonomi_restoran_toko", name: "Tabulasi Ekonomi Restoran Toko", ds: 6343, limit: 1000 },
  { id: 11936, key: "raw_tabulasi_ekonomi_bank", name: "Tabulasi Ekonomi Bank BPR", ds: 6343, limit: 1000 },
  { id: 11897, key: "raw_tabulasi_wilayah_laut_pesisir", name: "Tabulasi Wilayah Laut Pesisir", ds: 6343, limit: 1000 },
  { id: 11939, key: "raw_tabulasi_blok7_lainnya", name: "Tabulasi Blok 7", ds: 6343, limit: 1000 },
  { id: 11943, key: "raw_tabulasi_penduduk_dtsen", name: "Tabulasi Penduduk DTSEN", ds: 6343, limit: 1000 },

  // --- KATEGORI 3: INDEKS KESULITAN GEOGRAFIS (IKG) (DASHBOARD 582) ---
  { id: 11963, key: "raw_ikg_desa_total", name: "IKG Desa Total", ds: 6345, limit: 1000 },
  { id: 11966, key: "raw_ikg_pelayanan_dasar_desa", name: "IKG Pelayanan Dasar", ds: 6345, limit: 1000 },
  { id: 11969, key: "raw_ikg_infrastruktur_desa", name: "IKG Infrastruktur", ds: 6345, limit: 1000 },
  { id: 11972, key: "raw_ikg_aksesibilitas_desa", name: "IKG Aksesibilitas", ds: 6345, limit: 1000 },

  // --- KATEGORI 4: MONITORING PROGRES LAPANGAN (DASHBOARD 571) ---
  { id: 11621, key: "raw_monitoring_desa", name: "Monitoring Progres Desa", ds: 6256, limit: 1000 },
  { id: 11620, key: "raw_monitoring_kecamatan", name: "Monitoring Progres Kecamatan", ds: 6256, limit: 1000 },
  { id: 11619, key: "raw_monitoring_kabupaten", name: "Monitoring Progres Kabupaten", ds: 6256, limit: 1000 },
  { id: 12377, key: "raw_monitoring_pcl", name: "Monitoring Progres PCL", ds: 6602, limit: 1000 }
];

async function pullAllRawData() {
  console.log(`🚀 Memulai Ekstraksi ${ALL_RAW_CHARTS.length} Tabel Raw PODES 2026...`);

  const browser = await chromium.launch({
    headless: true,
    executablePath: "/usr/bin/google-chrome-stable",
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });
  const context = await browser.newContext({
    storageState: resolve(__dirname, "../data/cookies/fasih-dashboard-arinif-storage.json")
  });
  const page = await context.newPage();
  await page.goto("https://fasih-dashboard.bps.go.id/superset/welcome/", { waitUntil: "networkidle", timeout: 45000 });

  const summary = [];

  for (let i = 0; i < ALL_RAW_CHARTS.length; i++) {
    const item = ALL_RAW_CHARTS[i];
    process.stdout.write(`[${i + 1}/${ALL_RAW_CHARTS.length}] Menarik ${item.key} (ID: ${item.id})... `);

    try {
      const data = await page.evaluate(async ({ id, ds, limit }) => {
        // Ambil params chart
        const rChart = await fetch(`https://fasih-dashboard.bps.go.id/api/v1/chart/${id}`);
        const jChart = await rChart.json();
        const p = JSON.parse(jChart.result.params || "{}");

        // Tentukan columns & metrics
        const columns = p.all_columns && p.all_columns.length > 0 ? p.all_columns : (p.groupby || []);
        const metrics = p.metrics || [];

        const payload = {
          datasource: { id: ds, type: "table" },
          queries: [{
            columns: columns,
            metrics: metrics,
            row_limit: limit
          }]
        };

        const rData = await fetch("https://fasih-dashboard.bps.go.id/api/v1/chart/data", {
          method: "POST",
          headers: { "content-type": "application/json", "accept": "application/json" },
          body: JSON.stringify(payload)
        });
        const jData = await rData.json();

        return {
          chart_id: id,
          slice_name: jChart.result.slice_name,
          colnames: jData.result ? jData.result[0].colnames : [],
          coltypes: jData.result ? jData.result[0].coltypes : [],
          rowcount: jData.result ? jData.result[0].rowcount : 0,
          data: jData.result ? jData.result[0].data : []
        };
      }, item);

      const filePath = resolve(OUT_DIR, `${item.key}.json`);
      writeFileSync(filePath, JSON.stringify(data, null, 2), "utf-8");

      console.log(`✅ ${data.rowcount} baris, ${data.colnames.length} kolom`);
      summary.push({
        key: item.key,
        name: item.name,
        chart_id: item.id,
        rows: data.rowcount,
        cols: data.colnames.length
      });
    } catch (err) {
      console.log(`❌ ERROR: ${err.message}`);
    }
  }

  await browser.close();

  // Simpan manifest summary
  writeFileSync(resolve(OUT_DIR, "_manifest.json"), JSON.stringify(summary, null, 2), "utf-8");
  console.log(`\n🎉 Selesai! Seluruh ${summary.length} dataset mentah disimpan di ${OUT_DIR}`);
}

pullAllRawData().catch(console.error);
