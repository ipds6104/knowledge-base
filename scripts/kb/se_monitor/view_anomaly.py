"""kb/se_monitor/view_anomaly.py - Tampilkan analisis deteksi moral hazard / anomali PPL (Keluarga, Perusahaan, & Usaha Keluarga) serta proyeksi keterlambatan."""

import csv
import sys
import urllib.request
import datetime
from pathlib import Path
from ..colors import Colors
from .data import download_sheet, get_sls_metrics, compute_timeline, TARGET_DATE
from .hierarchy import build_hierarchy

# Paths
ALOKASI_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/Alokasi Petugas.csv")
FAMILY_CACHE_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/Pemutakhiran_Keluarga.csv")
USAHA_PERUSAHAAN_CACHE = Path("kegiatan/sensus-ekonomi-2026/2026/Usaha_Perusahaan.csv")
USAHA_KELUARGA_CACHE = Path("kegiatan/sensus-ekonomi-2026/2026/Usaha_Keluarga.csv")

def download_sheet_with_progress(url: str, dest_path: Path, label: str):
    print(f"{Colors.BLUE}Mengunduh data {label} dari Google Sheets...{Colors.ENDC}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            csv_text = response.read().decode('utf-8-sig')
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(csv_text, encoding='utf-8')
        print(f"{Colors.GREEN}Sukses memperbarui berkas cache {label}.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.WARNING}Peringatan: Gagal memperbarui data {label} ({e}). Menggunakan cache lokal jika ada.{Colors.ENDC}")

def clean_int(val):
    if not val:
        return 0
    val_str = str(val).strip().replace(',', '').replace('.', '')
    if val_str == '-' or not val_str:
        return 0
    try:
        return int(val_str)
    except ValueError:
        return 0

def print_anomaly() -> None:
    """Mencetak analisis deteksi moral hazard dan PPL anomali di Kabupaten Mempawah (Keluarga & Usaha)."""
    # 1. Unduh sheet yang diperlukan jika belum ada
    if not FAMILY_CACHE_PATH.exists():
        download_sheet_with_progress(
            "https://docs.google.com/spreadsheets/d/1QWwKu8VMg3jwTW6q1SShMBzS10jkBy6Y4wEd7IDWzb0/export?format=csv&gid=51144941",
            FAMILY_CACHE_PATH, "Pemutakhiran Keluarga"
        )
    if not USAHA_PERUSAHAAN_CACHE.exists():
        download_sheet_with_progress(
            "https://docs.google.com/spreadsheets/d/1QWwKu8VMg3jwTW6q1SShMBzS10jkBy6Y4wEd7IDWzb0/export?format=csv&gid=492418760",
            USAHA_PERUSAHAAN_CACHE, "Usaha/Perusahaan"
        )
    if not USAHA_KELUARGA_CACHE.exists():
        download_sheet_with_progress(
            "https://docs.google.com/spreadsheets/d/1QWwKu8VMg3jwTW6q1SShMBzS10jkBy6Y4wEd7IDWzb0/export?format=csv&gid=1367738322",
            USAHA_KELUARGA_CACHE, "Usaha Keluarga"
        )

    # Validasi berkas
    if not FAMILY_CACHE_PATH.exists() or not USAHA_PERUSAHAAN_CACHE.exists() or not USAHA_KELUARGA_CACHE.exists():
        print(f"{Colors.FAIL}Error: Beberapa berkas monitoring tidak tersedia di cache lokal.{Colors.ENDC}")
        return

    # Bangun hierarki dan ambil realisasi
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()
    sheet_map, csv_text, data_source_info = download_sheet()
    elapsed_days, total_days, expected_pct = compute_timeline()

    if not has_alokasi:
        print(f"{Colors.FAIL}Error: Berkas alokasi petugas tidak ditemukan.{Colors.ENDC}")
        return

    # Ambil lookup alokasi
    alokasi_map = {}      # idsubsls (16 chars) -> {ppl, pml, pj, nmkec}
    alokasi_map_sls = {}  # idsls (14 chars) -> {ppl, pml, pj, nmkec}
    try:
        with open(ALOKASI_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                idsubsls = row.get("idsubsls", "").strip()
                idsls = row.get("idsls", "").strip()
                ppl = row.get("PPL", "").strip().upper()
                pml = row.get("PML", "").strip().upper()
                pj = row.get("Pj-Kuda", "").strip().upper()
                nmkec = row.get("nmkec", "").strip().upper()
                if idsubsls:
                    info = {"ppl": ppl, "pml": pml, "pj": pj, "nmkec": nmkec}
                    alokasi_map[idsubsls] = info
                    if idsls:
                        alokasi_map_sls[idsls] = info
    except Exception as e:
        print(f"{Colors.FAIL}Error saat membaca alokasi petugas: {e}{Colors.ENDC}")
        return

    # ==========================================================================
    # BAGIAN 1: ANOMALI PEMUTAKHIRAN KELUARGA
    # ==========================================================================
    ppl_family = {}
    try:
        with open(FAMILY_CACHE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            row_count = 0
            for row in reader:
                row_count += 1
                if row_count < 4 or not row or len(row) < 14 or row_count in [4, 5]:
                    continue
                code = row[0].strip()
                if not code or len(code) != 16 or code.startswith("61040000"):
                    continue
                
                prelist = clean_int(row[2])
                td_ditemukan = clean_int(row[12])
                
                info = alokasi_map.get(code, {"ppl": "UNKNOWN", "pml": "UNKNOWN", "pj": "UNKNOWN", "nmkec": "UNKNOWN"})
                ppl = info["ppl"]
                if ppl == "UNKNOWN":
                    continue
                    
                if ppl not in ppl_family:
                    ppl_family[ppl] = {
                        "ppl": ppl, "pml": info["pml"], "pj": info["pj"], "nmkec": info["nmkec"],
                        "prelist": 0, "td_ditemukan": 0
                    }
                ppl_family[ppl]["prelist"] += prelist
                ppl_family[ppl]["td_ditemukan"] += td_ditemukan
    except Exception as e:
        print(f"{Colors.FAIL}Error saat membaca pemutakhiran keluarga: {e}{Colors.ENDC}")
        return

    # ==========================================================================
    # BAGIAN 2: ANOMALI USAHA/PERUSAHAAN
    # ==========================================================================
    ppl_perusahaan = {}
    try:
        with open(USAHA_PERUSAHAAN_CACHE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            row_count = 0
            for row in reader:
                row_count += 1
                if row_count < 6 or not row or len(row) < 13:
                    continue
                code = row[0].strip()
                if not code or len(code) != 14 or not code.isdigit():
                    continue
                
                prelist_usaha = clean_int(row[2])
                td_ditemukan = clean_int(row[9])
                
                info = alokasi_map_sls.get(code, {"ppl": "UNKNOWN", "pml": "UNKNOWN", "pj": "UNKNOWN", "nmkec": "UNKNOWN"})
                ppl = info["ppl"]
                if ppl == "UNKNOWN":
                    continue
                    
                if ppl not in ppl_perusahaan:
                    ppl_perusahaan[ppl] = {
                        "ppl": ppl, "pml": info["pml"], "pj": info["pj"], "nmkec": info["nmkec"],
                        "prelist": 0, "td_ditemukan": 0
                    }
                ppl_perusahaan[ppl]["prelist"] += prelist_usaha
                ppl_perusahaan[ppl]["td_ditemukan"] += td_ditemukan
    except Exception as e:
        print(f"{Colors.FAIL}Error saat membaca usaha perusahaan: {e}{Colors.ENDC}")
        return

    # ==========================================================================
    # BAGIAN 3: ANOMALI USAHA KELUARGA
    # ==========================================================================
    ppl_keluarga = {}
    try:
        with open(USAHA_KELUARGA_CACHE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            row_count = 0
            for row in reader:
                row_count += 1
                if row_count < 6 or not row or len(row) < 7:
                    continue
                code = row[0].strip()
                if not code or len(code) != 14 or not code.isdigit():
                    continue
                
                ditemukan = clean_int(row[2])
                tutup = clean_int(row[3])
                ganda = clean_int(row[4])
                td_ditemukan = clean_int(row[5])
                baru = clean_int(row[6])
                
                info = alokasi_map_sls.get(code, {"ppl": "UNKNOWN", "pml": "UNKNOWN", "pj": "UNKNOWN", "nmkec": "UNKNOWN"})
                ppl = info["ppl"]
                if ppl == "UNKNOWN":
                    continue
                    
                if ppl not in ppl_keluarga:
                    ppl_keluarga[ppl] = {
                        "ppl": ppl, "pml": info["pml"], "pj": info["pj"], "nmkec": info["nmkec"],
                        "ditemukan": 0, "tutup": 0, "ganda": 0, "td_ditemukan": 0, "baru": 0
                    }
                ppl_keluarga[ppl]["ditemukan"] += ditemukan
                ppl_keluarga[ppl]["tutup"] += tutup
                ppl_keluarga[ppl]["ganda"] += ganda
                ppl_keluarga[ppl]["td_ditemukan"] += td_ditemukan
                ppl_keluarga[ppl]["baru"] += baru
    except Exception as e:
        print(f"{Colors.FAIL}Error saat membaca usaha keluarga: {e}{Colors.ENDC}")
        return

    # ==========================================================================
    # BAGIAN 4: PROYEKSI KETERLAMBATAN PPL (KUANTITAS)
    # ==========================================================================
    ppl_projections = []
    today = datetime.date.today()
    for pj_name, pmls in pj_kuda_groups.items():
        for pml_name, ppls in pmls.items():
            for ppl_name, sls_list in ppls.items():
                total_target = 0
                total_completed = 0
                for idsubsls in sls_list:
                    info = sls_info.get(idsubsls, {})
                    idsls = info.get("idsls")
                    m = get_sls_metrics(sheet_map, idsls, idsubsls)
                    total_target += m["target"]
                    total_completed += m["completed"]
                
                if total_target == 0:
                    continue
                    
                done_pct = (total_completed / total_target * 100)
                
                # Hitung estimasi selesai
                est_str = "-"
                is_late = False
                if done_pct >= 100.0:
                    est_str = "Selesai"
                elif done_pct > 0.0 and elapsed_days > 0:
                    daily_speed = done_pct / elapsed_days
                    rem_days = (100.0 - done_pct) / daily_speed
                    est_date = today + datetime.timedelta(days=rem_days)
                    est_str = est_date.strftime("%d %b %Y")
                    if est_date > TARGET_DATE:
                        is_late = True
                else:
                    est_str = "Belum Mulai"
                    is_late = True
                    
                if is_late:
                    ppl_projections.append({
                        "ppl": ppl_name,
                        "pml": pml_name,
                        "pj": pj_name,
                        "target": total_target,
                        "done_pct": done_pct,
                        "est_selesai": est_str
                    })

    import numpy as np
    sep = "-" * 135

    # ----------------- PRINT TABLE 1: KELUARGA -----------------
    family_list = []
    for ppl, s in ppl_family.items():
        pre = s["prelist"]
        if pre < 50:
            continue
        pct = (s["td_ditemukan"] / pre * 100)
        family_list.append({
            "ppl": ppl, "pml": s["pml"], "pj": s["pj"], "nmkec": s["nmkec"], "prelist": pre,
            "td_ditemukan": s["td_ditemukan"], "pct": pct
        })
    pct_f_vals = [x["pct"] for x in family_list]
    avg_f = np.mean(pct_f_vals) if pct_f_vals else 0
    std_f = np.std(pct_f_vals) if pct_f_vals else 0

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== DETEKSI ANOMALI PEMUTAKHIRAN KELUARGA (POTENSI MORAL HAZARD) ==={Colors.ENDC}")
    print(f"Rata-rata Keluarga Td Ditemukan (Mean) : {avg_f:.2f}% | Standar Deviasi (StdDev): {std_f:.2f}%")
    print(f"Batas Anomali Kritis (Mean + 2.0xStdDev): {avg_f + 2*std_f:.2f}%")
    print(sep)
    print(f" {'No':<3} | {'Nama PPL':<25} | {'Kecamatan':<15} | {'PML Pengawas':<25} | {'PJ-Kuda':<25} | {'Prelist':<7} | {'% Td Ditemukan':<15}")
    print(sep)
    
    idx = 1
    for p in sorted(family_list, key=lambda x: x["pct"], reverse=True):
        if p["pct"] > (avg_f + 1.5 * std_f):
            color = Colors.FAIL if p["pct"] > (avg_f + 2.0 * std_f) else Colors.WARNING
            print(f" {idx:<3} | {p['ppl']:<25} | {p['nmkec']:<15} | {p['pml']:<25} | {p['pj']:<25} | {p['prelist']:<7} | {color}{p['pct']:>13.2f}%{Colors.ENDC}")
            idx += 1
    print(sep)

    # ----------------- PRINT TABLE 2: PERUSAHAAN -----------------
    perusahaan_list = []
    for ppl, s in ppl_perusahaan.items():
        pre = s["prelist"]
        if pre < 10:
            continue
        pct = (s["td_ditemukan"] / pre * 100)
        perusahaan_list.append({
            "ppl": ppl, "pml": s["pml"], "pj": s["pj"], "nmkec": s["nmkec"], "prelist": pre,
            "td_ditemukan": s["td_ditemukan"], "pct": pct
        })
    pct_p_vals = [x["pct"] for x in perusahaan_list]
    avg_p = np.mean(pct_p_vals) if pct_p_vals else 0
    std_p = np.std(pct_p_vals) if pct_p_vals else 0

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== DETEKSI ANOMALI USAHA/PERUSAHAAN (KONTRAKTOR/MITRA) ==={Colors.ENDC}")
    print(f"Rata-rata Usaha Td Ditemukan (Mean)    : {avg_p:.2f}% | Standar Deviasi (StdDev): {std_p:.2f}%")
    print(f"Batas Anomali Kritis (Mean + 1.5xStdDev): {avg_p + 1.5*std_p:.2f}%")
    print(sep)
    print(f" {'No':<3} | {'Nama PPL':<25} | {'Kecamatan':<15} | {'PML Pengawas':<25} | {'PJ-Kuda':<25} | {'Prelist':<7} | {'% Td Ditemukan':<15}")
    print(sep)
    
    idx = 1
    for p in sorted(perusahaan_list, key=lambda x: x["pct"], reverse=True):
        if p["pct"] > (avg_p + 1.5 * std_p):
            color = Colors.FAIL if p["pct"] > (avg_p + 2.0 * std_p) else Colors.WARNING
            print(f" {idx:<3} | {p['ppl']:<25} | {p['nmkec']:<15} | {p['pml']:<25} | {p['pj']:<25} | {p['prelist']:<7} | {color}{p['pct']:>13.2f}%{Colors.ENDC}")
            idx += 1
    print(sep)

    # ----------------- PRINT TABLE 3: USAHA KELUARGA -----------------
    keluarga_list = []
    for ppl, s in ppl_keluarga.items():
        total_listed = s["ditemukan"] + s["tutup"] + s["ganda"] + s["td_ditemukan"] + s["baru"]
        if total_listed < 30:
            continue
        inactive = s["tutup"] + s["td_ditemukan"]
        pct_inactive = (inactive / total_listed * 100)
        keluarga_list.append({
            "ppl": ppl, "pml": s["pml"], "pj": s["pj"], "nmkec": s["nmkec"], "total": total_listed,
            "tutup_td": inactive, "pct_inactive": pct_inactive
        })
    pct_k_vals = [x["pct_inactive"] for x in keluarga_list]
    avg_k = np.mean(pct_k_vals) if pct_k_vals else 0
    std_k = np.std(pct_k_vals) if pct_k_vals else 0

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== DETEKSI ANOMALI USAHA KELUARGA (SEKTOR RUMAH TANGGA) ==={Colors.ENDC}")
    print(f"Rata-rata Usaha Non-Aktif (Mean)       : {avg_k:.2f}% | Standar Deviasi (StdDev): {std_k:.2f}%")
    print(f"Batas Anomali Kritis (Mean + 1.5xStdDev): {avg_k + 1.5*std_k:.2f}%")
    print(sep)
    print(f" {'No':<3} | {'Nama PPL':<25} | {'Kecamatan':<15} | {'PML Pengawas':<25} | {'PJ-Kuda':<25} | {'Total Usaha':<11} | {'% Non-Aktif':<12}")
    print(sep)
    
    idx = 1
    for p in sorted(keluarga_list, key=lambda x: x["pct_inactive"], reverse=True):
        if p["pct_inactive"] > (avg_k + 1.5 * std_k):
            color = Colors.FAIL if p["pct_inactive"] > (avg_k + 2.0 * std_k) else Colors.WARNING
            print(f" {idx:<3} | {p['ppl']:<25} | {p['nmkec']:<15} | {p['pml']:<25} | {p['pj']:<25} | {p['total']:<11} | {color}{p['pct_inactive']:>10.2f}%{Colors.ENDC}")
            idx += 1
    print(sep)

    # ----------------- PRINT TABLE 4: KETERLAMBATAN PPL -----------------
    print(f"\n{Colors.BOLD}{Colors.HEADER}=== PPL DENGAN RISIKO KETERLAMBATAN TINGGI (PROYEKSI SELESAI > 15 AGUSTUS) ==={Colors.ENDC}")
    print(sep)
    print(f" {'No':<3} | {'Nama PPL':<25} | {'PML Pengawas':<25} | {'PJ-Kuda':<25} | {'Target':<7} | {'Done %':<8} | {'Proyeksi Selesai':<15}")
    print(sep)
    
    idx = 1
    # Urutkan berdasarkan done_pct asc (yang paling lambat jalannya)
    for p in sorted(ppl_projections, key=lambda x: x["done_pct"]):
        color = Colors.FAIL
        print(f" {idx:<3} | {p['ppl']:<25} | {p['pml']:<25} | {p['pj']:<25} | {p['target']:<7} | {color}{p['done_pct']:>6.2f}%{Colors.ENDC} | {color}{p['est_selesai']:<15}{Colors.ENDC}")
        idx += 1
    print(sep)
    
    # Cetak Sorotan Pola PML
    print(f"\n{Colors.BOLD}[INFO] TEMUAN POLA PENGAWASAN:{Colors.ENDC}")
    print(f" * Ditemukan konsentrasi anomali tinggi pada kelompok PML {Colors.BOLD}HARIS ROSI{Colors.ENDC} (PJ-Kuda: {Colors.BOLD}ARINI FAURIZAH{Colors.ENDC} / Sungai Pinyuh).")
    print(f"   Sebanyak 4 PPL di bawah pengawasannya memiliki persentase usaha keluarga non-aktif (Tutup/Tidak Ditemukan) ekstrem.")
    print(f" * PPL {Colors.BOLD}SELVIA{Colors.ENDC} (Kec. Toho, PML Handoko Tuah S., PJ-Kuda: {Colors.BOLD}LISTIO JATI NANDHIKO{Colors.ENDC}) mencatat persentase non-aktif tertinggi ({Colors.FAIL}96.32%{Colors.ENDC}).")
    print()
