"""
CLI Command Module: kb sqllab
Menangani penarikan data SQL Lab Superset SE2026, analisis 2-view (Early Warning vs Siap Cetak PDF),
serta penyiapan berkas verifikasi RT.
"""

import json
import os
import sys
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SE26_DIR = os.path.join(BASE_DIR, "kegiatan", "sensus-ekonomi-2026", "2026")
SQLLAB_DIR = os.path.join(SE26_DIR, "sqllab_monitoring")
CSV_DIR = os.path.join(SQLLAB_DIR, "csv")
PDF_DIR = os.path.join(SQLLAB_DIR, "pdf_siap_cetak")
CACHE_DIR = os.path.join(SQLLAB_DIR, "cache")

for d in [SQLLAB_DIR, CSV_DIR, PDF_DIR, CACHE_DIR]:
    os.makedirs(d, exist_ok=True)

CACHE_FILE = os.path.join(CACHE_DIR, "monitoring_sqllab_cache.json")
SUBSLS_SELESAI_CSV = os.path.join(CSV_DIR, "subsls_selesai.csv")
SUBSLS_SELESAI_ROOT_CSV = os.path.join(SE26_DIR, "subsls_selesai.csv")
FASIH_SYNC_DIR = "/home/ihza/Projects/fasih-sync-monitoring"


def run_node_sqllab_query(sql):
    """Menjalankan query SQL ke Superset BPS via execute-query.js di fasih-sync-monitoring."""
    if not os.path.exists(FASIH_SYNC_DIR):
        print(f"❌ Error: Repositori fasih-sync-monitoring tidak ditemukan di {FASIH_SYNC_DIR}")
        return None

    cmd = ["node", "src/execute-query.js", sql]
    try:
        res = subprocess.run(cmd, cwd=FASIH_SYNC_DIR, capture_output=True, text=True, check=True)
        stdout = res.stdout
        # Find JSON array starting with '[' and ending with ']'
        # Look for the last matching pair or JSON block
        lines = stdout.splitlines()
        json_lines = []
        in_json = False
        for line in lines:
            if line.strip().startswith("[") and not in_json and ("{" in line or line.strip() == "["):
                in_json = True
                json_lines.append(line)
            elif in_json:
                json_lines.append(line)
                if line.strip() == "]" or line.strip().endswith("]"):
                    break
        
        if json_lines:
            json_str = "\n".join(json_lines)
            return json.loads(json_str)
        else:
            # Fallback to rfind / find
            start_idx = stdout.find("[\n")
            end_idx = stdout.rfind("\n]")
            if start_idx != -1 and end_idx != -1:
                json_str = stdout[start_idx:end_idx + 2]
                return json.loads(json_str)
            print("⚠️ Gagal mengekstrak output JSON dari runner Node.js.")
            print(stdout)
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Error eksekusi SQL Lab via Node.js (Exit {e.returncode}):")
        print(e.stderr or e.stdout)
        return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def cmd_sqllab_pull(args):
    """Subcommand: kb sqllab pull — Penarikan massal data agregat SLS Mempawah dari SQL Lab BPS."""
    print("🔄 [SQL Lab Pull] Menarik data agregat real-time SLS Kabupaten Mempawah (6104)...")

    # Query agregasi SLS memuat data submitted & external_done (Mengecualikan status DRAFT)
    sql = """
    SELECT 
      level_6_full_code,
      MAX(level_5_full_code) AS level_5_full_code,
      MAX(level_3_name) AS kecamatan,
      MAX(level_5_name) AS nama_sls,
      COUNT(assignment_id) AS total_target,
      COUNT(CASE WHEN external_done = '1' THEN 1 END) AS total_external_done,
      COUNT(CASE WHEN assignment_status_alias = 'SUBMITTED BY Pencacah' THEN 1 END) AS submitted_pencacah,
      COUNT(CASE WHEN assignment_status_alias = 'APPROVED BY Pengawas' THEN 1 END) AS approved_pengawas,
      COUNT(CASE WHEN assignment_status_alias IN ('COMPLETED BY Admin Kabupaten', 'EDITED BY Admin Kabupaten') THEN 1 END) AS completed_admin,
      COUNT(CASE WHEN (data9 = '2. Tidak' OR data9 LIKE '%Tidak Ditemukan%') AND assignment_status_alias != 'DRAFT' THEN 1 END) AS tidak_ditemukan_total,
      COUNT(CASE WHEN (data9 = '2. Tidak' OR data9 LIKE '%Tidak Ditemukan%') AND external_done = '1' THEN 1 END) AS tidak_ditemukan_approved,
      COUNT(CASE WHEN (data9 = '2. Tidak' OR data9 LIKE '%Tidak Ditemukan%') AND assignment_status_alias = 'SUBMITTED BY Pencacah' THEN 1 END) AS tidak_ditemukan_submitted
    FROM base_table_assignment
    WHERE level_2_full_code = '6104'
    GROUP BY level_6_full_code
    ORDER BY level_6_full_code ASC
    LIMIT 1000 OFFSET 0;
    """

    data = run_node_sqllab_query(sql)
    if data is not None:
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "total_subsls": len(data),
            "rows": data
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
        print(f"✅ [Sukses] Data agregat {len(data)} Sub-SLS Mempawah berhasil ditarik dan disimpan ke {CACHE_FILE}")
    else:
        print("❌ Penarikan data SQL Lab gagal. Periksa koneksi VPN / SSO.")


def cmd_sqllab_pull_microdata(args):
    """Subcommand: kb sqllab pull-microdata — Penarikan massal microdata Usaha & Keluarga Tidak Ditemukan (Chunking 1.000 baris, Non-Draft)."""
    import csv

    print("🔄 [SQL Lab Pull Microdata] Memulai penarikan massal microdata 'Tidak Ditemukan' (Non-Draft)...")
    chunk_size = 1000

    # 1. Tarik Data Penugasan Lapangan Tidak Ditemukan (base_table_assignment)
    print("\n📦 [1/2] Menarik data base_table_assignment (Non-Draft Tidak Ditemukan)...")
    all_assignment_rows = []
    offset = 0

    while True:
        print(f"   → Fetching chunk offset {offset} (Limit {chunk_size})...")
        sql = f"""
        SELECT 
          assignment_id,
          assignment_status_alias,
          assignment_date_modified,
          code_identity,
          level_1_full_code,
          level_2_full_code,
          level_2_name,
          level_3_name,
          level_4_name,
          level_5_full_code,
          level_6_full_code,
          level_6_name,
          data1,
          data2,
          data9,
          current_user_username,
          current_user_survey_role_name
        FROM base_table_assignment
        WHERE level_2_full_code = '6104'
          AND (data9 = '2. Tidak' OR data9 LIKE '%Tidak Ditemukan%')
          AND assignment_status_alias != 'DRAFT'
        ORDER BY level_6_full_code ASC, assignment_id ASC
        LIMIT {chunk_size} OFFSET {offset};
        """
        chunk = run_node_sqllab_query(sql)
        if not chunk:
            break
        all_assignment_rows.extend(chunk)
        print(f"     ✓ Diterima {len(chunk)} baris (Total akumulasi: {len(all_assignment_rows)})")
        if len(chunk) < chunk_size:
            break
        offset += chunk_size

    # Simpan ke CSV microdata
    assign_csv_list = [
        os.path.join(CSV_DIR, "microdata_tidak_ditemukan_6104_latest.csv"),
        os.path.join(SE26_DIR, "microdata_tidak_ditemukan_6104_latest.csv")
    ]
    if all_assignment_rows:
        fieldnames = list(all_assignment_rows[0].keys())
        for assign_csv in assign_csv_list:
            with open(assign_csv, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_assignment_rows)
        print(f"✅ [Sukses] {len(all_assignment_rows)} baris microdata berhasil diekspor ke {assign_csv_list[0]}")

    # 2. Tarik Data Kuesioner Usaha Tidak Ditemukan (se2026_nested)
    print("\n🏢 [2/2] Menarik data kuesioner se2026_nested Usaha Tidak Ditemukan...")
    all_usaha_rows = []
    offset = 0

    while True:
        print(f"   → Fetching chunk offset {offset} (Limit {chunk_size})...")
        sql = f"""
        SELECT 
          assignment_id,
          level_2_name,
          level_3_name,
          level_4_name,
          level_5_full_code,
          level_6_full_code,
          level_5_name AS nama_sls,
          nama_usaha,
          nama_komersial,
          alamat_usaha,
          keberadaan_usaha_label,
          keberadaan_usaha_value,
          kbli_value,
          kbli_label
        FROM se2026_nested
        WHERE level_2_full_code = '6104'
          AND (keberadaan_usaha_label LIKE '%Tidak Ditemukan%' OR keberadaan_usaha_value = '00')
        ORDER BY level_6_full_code ASC, assignment_id ASC
        LIMIT {chunk_size} OFFSET {offset};
        """
        chunk = run_node_sqllab_query(sql)
        if not chunk:
            break
        all_usaha_rows.extend(chunk)
        print(f"     ✓ Diterima {len(chunk)} baris (Total akumulasi: {len(all_usaha_rows)})")
        if len(chunk) < chunk_size:
            break
        offset += chunk_size

    usaha_csv_list = [
        os.path.join(CSV_DIR, "usaha_tidak_ditemukan_6104_latest.csv"),
        os.path.join(SE26_DIR, "usaha_tidak_ditemukan_6104_latest.csv")
    ]
    if all_usaha_rows:
        fieldnames = list(all_usaha_rows[0].keys())
        for usaha_csv in usaha_csv_list:
            with open(usaha_csv, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_usaha_rows)
        print(f"✅ [Sukses] {len(all_usaha_rows)} baris kuesioner usaha berhasil diekspor ke {usaha_csv_list[0]}")

    print(f"\n🎉 [Selesai] Penarikan microdata selesai tanpa melanggar batas 1.000 baris server!")


def cmd_sqllab_pull_completed_subsls(args):
    """Subcommand: kb sqllab pull-completed — Menarik daftar Sub-SLS yang 100% Selesai dari SQL Lab dan mengespor ke CSV."""
    import csv

    print("🔄 [SQL Lab Pull Completed] Menarik daftar Sub-SLS yang 100% Selesai (done_listing / external_done 100%)...")
    
    # Load Alokasi Petugas untuk pengayaan PPL, PML, PJ-Kuda
    alokasi = {}
    alokasi_file = os.path.join(SE26_DIR, "Alokasi Petugas.csv")
    if os.path.exists(alokasi_file):
        with open(alokasi_file, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                code = r.get("idsubsls", "").strip()
                if code:
                    alokasi[code] = r

    sql = """
    SELECT 
      level_6_full_code,
      MAX(level_5_full_code) AS level_5_full_code,
      MAX(level_3_name) AS kecamatan,
      MAX(level_4_name) AS desa,
      MAX(level_5_name) AS nama_sls,
      COUNT(assignment_id) AS total_target,
      COUNT(CASE WHEN external_done = '1' THEN 1 END) AS total_external_done,
      COUNT(CASE WHEN assignment_status_alias = 'APPROVED BY Pengawas' THEN 1 END) AS approved_pengawas,
      COUNT(CASE WHEN assignment_status_alias IN ('COMPLETED BY Admin Kabupaten', 'EDITED BY Admin Kabupaten') THEN 1 END) AS completed_admin,
      COUNT(CASE WHEN (data9 = '2. Tidak' OR data9 LIKE '%Tidak Ditemukan%') AND assignment_status_alias != 'DRAFT' THEN 1 END) AS tidak_ditemukan_total
    FROM base_table_assignment
    WHERE level_2_full_code = '6104'
    GROUP BY level_6_full_code
    HAVING COUNT(assignment_id) = COUNT(CASE WHEN external_done = '1' THEN 1 END)
    ORDER BY level_6_full_code ASC
    LIMIT 1000 OFFSET 0;
    """

    data = run_node_sqllab_query(sql)
    if not data:
        print("❌ Penarikan data Sub-SLS selesai gagal. Periksa koneksi VPN / SSO.")
        return

    csv_rows = []
    for r in data:
        code = r.get("level_6_full_code", "")
        al_info = alokasi.get(code, {})
        
        row_dict = {
            "Kode Wilayah (Sub-SLS)": code,
            "Nama SLS": r.get("nama_sls", ""),
            "Kecamatan": r.get("kecamatan", ""),
            "Desa": r.get("desa", ""),
            "PPL Pencacah": al_info.get("PPL", "-"),
            "PML Pengawas": al_info.get("PML", "-"),
            "PJ-Kuda": al_info.get("Pj-Kuda", "-"),
            "Target Unit": r.get("total_target", 0),
            "Total Approved (External Done)": r.get("total_external_done", 0),
            "PML Approved": r.get("approved_pengawas", 0),
            "Admin Completed": r.get("completed_admin", 0),
            "Jumlah Tidak Ditemukan": r.get("tidak_ditemukan_total", 0),
            "Status Selesai": "🟢 100% Final (Done Listing)"
        }
        csv_rows.append(row_dict)

    # Ekspor ke subsls_selesai.csv & subsls_selesai_sqllab_latest.csv
    out_files = [
        SUBSLS_SELESAI_CSV,
        os.path.join(SE26_DIR, "subsls_selesai_sqllab_latest.csv")
    ]

    fieldnames = list(csv_rows[0].keys())
    for out_fp in out_files:
        with open(out_fp, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)

    print(f"✅ [Sukses] {len(csv_rows)} Sub-SLS 100% Selesai berhasil ditarik real-time dari SQL Lab BPS!")
    print(f"📁 Diperbarui di: {SUBSLS_SELESAI_CSV}")




def load_cache_data():
    """Load cached SQL Lab data if exists."""
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Gagal memuat cache data: {e}")
        return None


def cmd_sqllab_report(args):
    """Subcommand: kb sqllab report — Menyajikan 2 view laporan (Early Warning vs Siap Cetak)."""
    cache = load_cache_data()
    if not cache:
        print("⚠️ Cache data belum ada. Menjalankan penarikan data 'kb sqllab pull' terlebih dahulu...")
        cmd_sqllab_pull(args)
        cache = load_cache_data()
        if not cache:
            print("❌ Gagal memuat data. Batalkan laporan.")
            return

    rows = cache.get("rows", [])
    updated_at = cache.get("timestamp", "Unknown")
    min_not_found = getattr(args, "min_not_found", 5)

    print(f"\n==========================================================================================")
    print(f"📊 LAPORAN DUA-VIEW ANOMALI SLS 'TIDAK DITEMUKAN' SENSUS EKONOMI 2026 (MEMPAWAH 6104)")
    print(f"   Diperbarui: {updated_at} | Total Sub-SLS: {len(rows)}")
    print(f"==========================================================================================\n")

    # VIEW 1: EARLY WARNING (Semua dokumen Submit & Approved)
    # Termasuk dokumen yang masih SUBMITTED BY Pencacah agar terlihat awal oleh Kepala BPS & Ketim SE
    sorted_early_warning = sorted(rows, key=lambda x: int(x.get("tidak_ditemukan_total", 0)), reverse=True)
    early_warning_list = [r for r in sorted_early_warning if int(r.get("tidak_ditemukan_total", 0)) > 0]

    print(f"🚨 VIEW 1: EARLY WARNING - RANKING SLS TIDAK DITEMUKAN TERBANYAK (ALL SUBMISSIONS)")
    print(f"   (Tujuan: Monitoring Dini Kepala BPS & Ketua Tim SE — Mengikutsertakan Status Submitted & Approved)")
    print(f"------------------------------------------------------------------------------------------")
    print(f"| No | Kode Sub-SLS     | Kecamatan     | Nama SLS / RT           | Target | Total Tdk Ditemukan | Approved | Submitted | Progres % | Status Selesai |")
    print(f"------------------------------------------------------------------------------------------")

    for i, r in enumerate(early_warning_list[:20], 1):
        code = r.get("level_6_full_code", "")
        kec = r.get("kecamatan", "")[:13]
        nmsls = r.get("nama_sls", "")[:23]
        target = int(r.get("total_target", 0))
        tdk_total = int(r.get("tidak_ditemukan_total", 0))
        tdk_appr = int(r.get("tidak_ditemukan_approved", 0))
        tdk_sub = int(r.get("tidak_ditemukan_submitted", 0))
        ext_done = int(r.get("total_external_done", 0))
        
        pct = (ext_done / target * 100) if target > 0 else 0.0
        status_str = "🟢 100% Final" if ext_done >= target else f"🟡 {pct:.1f}% Jalan"

        print(f"| {i:<2} | {code} | {kec:<13} | {nmsls:<23} | {target:<6} | {tdk_total:<19} | {tdk_appr:<8} | {tdk_sub:<9} | {pct:>8.1f}% | {status_str:<14} |")

    print(f"------------------------------------------------------------------------------------------\n")

    # Ekspor seluruh peringkat ke CSV subsls_tidak_ditemukan_ranking.csv
    import csv
    alokasi = {}
    alokasi_file = os.path.join(SE26_DIR, "Alokasi Petugas.csv")
    if os.path.exists(alokasi_file):
        with open(alokasi_file, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                code = r.get("idsubsls", "").strip()
                if code:
                    alokasi[code] = r

    ranking_csv_rows = []
    for rank, r in enumerate(early_warning_list, 1):
        code = r.get("level_6_full_code", "")
        al_info = alokasi.get(code, {})
        target = int(r.get("total_target", 0))
        ext_done = int(r.get("total_external_done", 0))
        pct = (ext_done / target * 100) if target > 0 else 0.0
        status_str = "🟢 100% Final" if ext_done >= target else f"🟡 {pct:.1f}% Jalan"

        ranking_csv_rows.append({
            "Peringkat Anomali": rank,
            "Kode Sub-SLS": code,
            "Kecamatan": r.get("kecamatan", ""),
            "Desa": r.get("desa", al_info.get("nmdesa", "")),
            "Nama SLS / RT": r.get("nama_sls", ""),
            "PPL Pencacah": al_info.get("PPL", "-"),
            "PML Pengawas": al_info.get("PML", "-"),
            "PJ-Kuda": al_info.get("Pj-Kuda", "-"),
            "Target Unit": target,
            "Total Tidak Ditemukan (Non-Draft)": int(r.get("tidak_ditemukan_total", 0)),
            "Tidak Ditemukan Approved": int(r.get("tidak_ditemukan_approved", 0)),
            "Tidak Ditemukan Submitted": int(r.get("tidak_ditemukan_submitted", 0)),
            "Total Approved (External Done)": ext_done,
            "Progres %": round(pct, 1),
            "Status SLS": status_str
        })

    out_ranking_csv_list = [
        os.path.join(CSV_DIR, "subsls_tidak_ditemukan_ranking.csv"),
        os.path.join(SE26_DIR, "subsls_tidak_ditemukan_ranking.csv")
    ]
    if ranking_csv_rows:
        fieldnames = list(ranking_csv_rows[0].keys())
        for out_csv in out_ranking_csv_list:
            with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(ranking_csv_rows)
        print(f"💾 [Ekspor CSV] {len(ranking_csv_rows)} Sub-SLS peringkat Tidak Ditemukan berhasil disimpan ke:")
        print(f"   📁 {out_ranking_csv_list[0]}")

        # Sinkronkan otomatis ke Google Sheets
        try:
            print("   → Delta Sync PDF ke Google Drive...")
            res_pdf = subprocess.run(["node", "scripts/upload_pdf_gdrive_delta.js"], cwd=BASE_DIR, capture_output=True, text=True)
            if res_pdf.returncode == 0:
                print("   🟢 [GDrive Delta Upload] Link PDF berhasil disinkronkan!")
            else:
                print(f"   ⚠️ Delta Upload PDF melempar error: {res_pdf.stderr}")

            print("   → Sinkronisasi otomatis ke Google Sheets tab 'Ranking SLS Tidak Ditemukan'...")
            res = subprocess.run(["node", "src/update-gsheet-ranking.js"], cwd=FASIH_SYNC_DIR, capture_output=True, text=True)
            if res.returncode == 0:
                print("   🟢 [Google Sheets Sync] Tab 'Ranking SLS Tidak Ditemukan' berhasil diperbarui!\n")
            else:
                print(f"   ⚠️ Sinkronisasi Google Sheets melempar error: {res.stderr}\n")
        except Exception as e:
            print(f"   ⚠️ Exception sinkronisasi Google Sheets: {e}\n")

    # VIEW 2: SIAP CETAK PDF (Khusus SLS Selesai 100%)
    ready_for_print = [
        r for r in rows 
        if int(r.get("total_external_done", 0)) >= int(r.get("total_target", 1))
        and int(r.get("tidak_ditemukan_total", 0)) >= min_not_found
    ]
    sorted_print = sorted(ready_for_print, key=lambda x: int(x.get("tidak_ditemukan_total", 0)), reverse=True)

    print(f"📄 VIEW 2: SLS SIAP CETAK PDF VERIFIKASI RT (KHUSUS SLS 100% SELESAI & TDK DITEMUKAN >= {min_not_found})")
    print(f"   (Tujuan: Cetak Dokumen Pengesahan Kades/RT — Dijamin Final, Bebas Risiko Cetak Ulang)")
    print(f"------------------------------------------------------------------------------------------")
    print(f"| No | Kode Sub-SLS     | Kecamatan     | Nama SLS / RT           | Target | Total Tdk Ditemukan | Status Selesai | Cetak PDF Ready |")
    print(f"------------------------------------------------------------------------------------------")

    if not sorted_print:
        print(f"|  - Tidak ada SLS yang memenuhi syarat 100% Selesai dan Tidak Ditemukan >= {min_not_found}.                      |")
    else:
        for i, r in enumerate(sorted_print, 1):
            code = r.get("level_6_full_code", "")
            kec = r.get("kecamatan", "")[:13]
            nmsls = r.get("nama_sls", "")[:23]
            target = int(r.get("total_target", 0))
            tdk_total = int(r.get("tidak_ditemukan_total", 0))

            print(f"| {i:<2} | {code} | {kec:<13} | {nmsls:<23} | {target:<6} | {tdk_total:<19} | 🟢 100% Approved | READY TO PRINT  |")

    print(f"------------------------------------------------------------------------------------------\n")


def cmd_sqllab_print_prep(args):
    """Subcommand: kb sqllab print-prep — Memicu generasi PDF verifikasi RT untuk SLS Siap Cetak."""
    min_not_found = getattr(args, "min_not_found", 5)
    print(f"🖨️ [Print Prep] Memulai penyiapan PDF Lembar Verifikasi RT untuk SLS 100% Selesai (Tdk Ditemukan >= {min_not_found})...")

    # Jalankan generate_all_rt_pdf.py dengan parameter
    completed_dir = PDF_DIR
    cmd = [sys.executable, "scripts/generate_all_rt_pdf.py", "--only-completed", "--min-not-found", str(min_not_found), "--output-dir", completed_dir]
    try:
        res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
        print(res.stdout)
        if res.returncode == 0:
            print("✅ Penyiapan PDF Lembar Verifikasi RT berhasil dilaksanakan.")
        else:
            print(f"⚠️ Peringatan: Script melempar exit code {res.returncode}")
            print(res.stderr)
    except Exception as e:
        print(f"❌ Exception saat menjalankan generator PDF: {e}")


def cmd_sqllab_sync(args):
    """Subcommand: kb sqllab sync — Workflow Otomatis Penuh: Tarik Agregat, Microdata, Sub-SLS Selesai, Cetak PDF, & Laporan 2-View."""
    print("==========================================================================================")
    print("🚀 [SQL LAB AUTOMATED SYNC WORKFLOW] MEMULAI REFRESH DATA PENUH SENSUS EKONOMI 2026")
    print("==========================================================================================\n")

    # Step 1: Tarik Agregat Sub-SLS
    print("📌 [STEP 1/5] Penarikan Data Agregat Sub-SLS Mempawah...")
    cmd_sqllab_pull(args)

    # Step 2: Tarik Massal Microdata (Non-Draft)
    print("\n📌 [STEP 2/5] Penarikan Massal Microdata Responden & Kuesioner Usaha (Non-Draft)...")
    cmd_sqllab_pull_microdata(args)

    # Step 3: Tarik Daftar Sub-SLS 100% Selesai
    print("\n📌 [STEP 3/5] Penarikan Daftar Sub-SLS 100% Selesai (Done Listing)...")
    cmd_sqllab_pull_completed_subsls(args)

    # Step 4: Generasi PDF Lembar Verifikasi RT (SLS Selesai 100%)
    print("\n📌 [STEP 4/5] Generasi PDF Lembar Verifikasi RT ke Folder pdf_verifikasi_rt_completed/...")
    cmd_sqllab_print_prep(args)

    # Step 5: Sajikan Laporan 2-View Baku
    print("\n📌 [STEP 5/5] Menyajikan Laporan 2-View Terbaru...")
    cmd_sqllab_report(args)

    print("\n==========================================================================================")
    print("🎉 [WORKFLOW SYNC SELESAI] Data Real-Time Berhasil Diperbarui & Siap Digunakan!")
    print("==========================================================================================\n")

