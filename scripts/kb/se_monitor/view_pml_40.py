"""kb/se_monitor/view_pml_40.py — Tampilkan progres PML >= 40% per Kabupaten dan detail Mempawah."""

import csv
import sys
import urllib.request
from pathlib import Path
from ..colors import Colors

# Paths
REALISASI_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/Realisasi - 6104.csv")
ALOKASI_6100_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/Alokasi_6100.csv")

def download_alokasi_6100():
    url = "https://docs.google.com/spreadsheets/d/1JNwyb7TsPmSsGl3o1zNTSc-3wzFwIr_t3HPz_a1CVVQ/export?format=csv&gid=1206035192"
    print(f"{Colors.BLUE}Mengunduh Alokasi 6100 Kalbar dari Google Sheets...{Colors.ENDC}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            csv_text = response.read().decode('utf-8-sig')
        ALOKASI_6100_PATH.parent.mkdir(parents=True, exist_ok=True)
        ALOKASI_6100_PATH.write_text(csv_text, encoding='utf-8')
        print(f"{Colors.GREEN}Sukses memperbarui berkas alokasi 6100.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.WARNING}Peringatan: Gagal memperbarui alokasi 6100 ({e}). Menggunakan cache lokal jika ada.{Colors.ENDC}")

def print_pml_40() -> None:
    """Mencetak ringkasan PML >= 40% per Kabupaten dan detail PML Mempawah."""
    if not ALOKASI_6100_PATH.exists():
        download_alokasi_6100()
        
    if not ALOKASI_6100_PATH.exists():
        print(f"{Colors.FAIL}Error: Berkas alokasi 6100 tidak tersedia.{Colors.ENDC}")
        return

    if not REALISASI_PATH.exists():
        print(f"{Colors.FAIL}Error: Berkas realisasi {REALISASI_PATH} tidak ditemukan.{Colors.ENDC}")
        return

    # Read Alokasi 6100
    alokasi_map = {} # idsubsls -> (nmkab, PML)
    try:
        with open(ALOKASI_6100_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                idsubsls = row.get("idsubsls", "").strip()
                nmkab = row.get("nmkab", "").strip().upper()
                pml = row.get("PML", "").strip().upper()
                if idsubsls:
                    alokasi_map[idsubsls] = (nmkab, pml)
    except Exception as e:
        print(f"{Colors.FAIL}Error saat membaca berkas alokasi 6100: {e}{Colors.ENDC}")
        return

    # Read Realisasi
    pml_stats = {} # (kab, pml) -> {target, progress}
    try:
        with open(REALISASI_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                subsls = row.get("Kode Wilayah (Sub-SLS)", "").strip()
                kab = row.get("Kab/Kota", "").strip().upper()
                
                pml = "UNKNOWN"
                if subsls in alokasi_map:
                    kab_alok, pml_alok = alokasi_map[subsls]
                    if kab_alok:
                        kab = kab_alok
                    if pml_alok:
                        pml = pml_alok
                
                # Saring PML yang tidak valid atau reference error dari Google Sheets
                if not kab or pml in ["", "-", "UNKNOWN", "#REF!"]:
                    continue
                    
                target = int(row.get("Total Target", 0) or 0)
                app = int(row.get("APPROVED BY Pengawas", 0) or 0)
                rej = int(row.get("REJECTED BY Pengawas", 0) or 0)
                rev = int(row.get("REVOKED BY Pengawas", 0) or 0)
                edit_adm = int(row.get("EDITED BY Admin Kabupaten", 0) or 0)
                rej_adm = int(row.get("REJECTED BY Admin Kabupaten", 0) or 0)
                
                pml_prog = app + rej + rev + edit_adm + rej_adm
                
                key = (kab, pml)
                if key not in pml_stats:
                    pml_stats[key] = {"target": 0, "progress": 0}
                    
                pml_stats[key]["target"] += target
                pml_stats[key]["progress"] += pml_prog
    except Exception as e:
        print(f"{Colors.FAIL}Error saat membaca berkas realisasi: {e}{Colors.ENDC}")
        return

    # Group by Kabupaten
    kab_pmls = {} # kab -> list of (pml, target, progress, pct)
    for (kab, pml), stats in pml_stats.items():
        t = stats["target"]
        p = stats["progress"]
        pct = (p / t * 100) if t > 0 else 0.0
        kab_pmls.setdefault(kab, [])
        kab_pmls[kab].append((pml, t, p, pct))

    # Print Table 1: Summary per Kabupaten
    print(f"\n{Colors.BOLD}{Colors.HEADER}=== PERSENTASE PML YANG MEMENUHI 40% PER KABUPATEN (PROV. KALBAR) ==={Colors.ENDC}")
    sep = "-" * 80
    print(sep)
    print(f" {'No':<3} | {'Kabupaten/Kota':<20} | {'Total PML':<10} | {'PML >= 40%':<12} | {'% PML >= 40%':<14} | {'Status':<12}")
    print(sep)
    
    sorted_kabs = sorted(kab_pmls.keys())
    total_pmls_all = 0
    total_meet_all = 0
    
    kab_rows = []
    for kab in sorted_kabs:
        pmls = kab_pmls[kab]
        meet_40 = [p for p in pmls if p[3] >= 40.0]
        count_all = len(pmls)
        count_meet = len(meet_40)
        pct_meet = (count_meet / count_all * 100) if count_all > 0 else 0.0
        
        total_pmls_all += count_all
        total_meet_all += count_meet
        
        if pct_meet >= 40.0:
            status_color = Colors.GREEN
            status_txt = "🟢 AMAN"
        elif pct_meet >= 25.0:
            status_color = Colors.WARNING
            status_txt = "🟡 WARNING"
        else:
            status_color = Colors.FAIL
            status_txt = "🔴 BEHIND"
            
        kab_rows.append((kab, count_all, count_meet, pct_meet, status_color, status_txt))
        
    # Urutkan berdasarkan persentase PML >= 40% desc
    kab_rows.sort(key=lambda x: x[3], reverse=True)
    
    for idx, (kab, count_all, count_meet, pct_meet, status_color, status_txt) in enumerate(kab_rows, 1):
        print(f" {idx:<3} | {kab:<20} | {count_all:<10} | {count_meet:<12} | {status_color}{pct_meet:>12.2f}%{Colors.ENDC} | {status_color}{status_txt:<12}{Colors.ENDC}")
        
    print(sep)
    pct_meet_all = (total_meet_all / total_pmls_all * 100) if total_pmls_all > 0 else 0.0
    tot_color = Colors.GREEN if pct_meet_all >= 40.0 else (Colors.WARNING if pct_meet_all >= 25.0 else Colors.FAIL)
    print(f" {'TOTAL PROVINSI KALBAR':<26} | {total_pmls_all:<10} | {total_meet_all:<12} | {tot_color}{pct_meet_all:>12.2f}%{Colors.ENDC} | {tot_color}{'🔴 BEHIND' if pct_meet_all < 40.0 else '🟢 AMAN':<12}{Colors.ENDC}")
    print(sep)

    # Print Table 2: Detailed PML Mempawah
    print(f"\n{Colors.BOLD}{Colors.HEADER}=== RINCIAN KINERJA PML KABUPATEN MEMPAWAH ==={Colors.ENDC}")
    sep_detail = "-" * 85
    print(sep_detail)
    print(f" {'No':<3} | {'Nama PML':<30} | {'Target':<7} | {'Progress':<8} | {'Persentase':<10} | {'Status >= 40%':<12}")
    print(sep_detail)
    
    mempawah_pmls = sorted(kab_pmls.get("MEMPAWAH", []), key=lambda x: x[3], reverse=True)
    for idx, (pml, target, progress, pct) in enumerate(mempawah_pmls, 1):
        if pct >= 40.0:
            status_color = Colors.GREEN
            status_txt = "🟢 YES"
        else:
            status_color = Colors.FAIL
            status_txt = "🔴 NO"
        print(f" {idx:<3} | {pml:<30} | {target:<7} | {progress:<8} | {status_color}{pct:>9.2f}%{Colors.ENDC} | {status_color}{status_txt:<12}{Colors.ENDC}")
    print(sep_detail)
    print()
