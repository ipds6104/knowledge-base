"""kb/se_monitor/view_anomaly.py — Tampilkan analisis deteksi moral hazard / anomali PPL."""

import csv
import sys
import urllib.request
from pathlib import Path
from ..colors import Colors

# Paths
ALOKASI_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/Alokasi Petugas.csv")
FAMILY_CACHE_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/Pemutakhiran_Keluarga.csv")

def download_family_sheet():
    url = "https://docs.google.com/spreadsheets/d/1QWwKu8VMg3jwTW6q1SShMBzS10jkBy6Y4wEd7IDWzb0/export?format=csv&gid=51144941"
    print(f"{Colors.BLUE}Mengunduh data Pemutakhiran Keluarga dari Google Sheets...{Colors.ENDC}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            csv_text = response.read().decode('utf-8-sig')
        FAMILY_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        FAMILY_CACHE_PATH.write_text(csv_text, encoding='utf-8')
        print(f"{Colors.GREEN}Sukses memperbarui berkas pemutakhiran keluarga.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.WARNING}Peringatan: Gagal memperbarui data Pemutakhiran Keluarga ({e}). Menggunakan cache lokal jika ada.{Colors.ENDC}")

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
    """Mencetak analisis deteksi moral hazard dan daftar PPL anomali di Kabupaten Mempawah."""
    if not FAMILY_CACHE_PATH.exists():
        download_family_sheet()

    if not FAMILY_CACHE_PATH.exists():
        print(f"{Colors.FAIL}Error: Berkas pemutakhiran keluarga tidak tersedia.{Colors.ENDC}")
        return

    if not ALOKASI_PATH.exists():
        print(f"{Colors.FAIL}Error: Berkas alokasi petugas tidak ditemukan.{Colors.ENDC}")
        return

    # Read Alokasi
    alokasi_map = {} # idsubsls -> {ppl, pml, pj, nmkec}
    try:
        with open(ALOKASI_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                idsubsls = row.get("idsubsls", "").strip()
                ppl = row.get("PPL", "").strip().upper()
                pml = row.get("PML", "").strip().upper()
                pj = row.get("Pj-Kuda", "").strip().upper()
                nmkec = row.get("nmkec", "").strip().upper()
                if idsubsls:
                    alokasi_map[idsubsls] = {"ppl": ppl, "pml": pml, "pj": pj, "nmkec": nmkec}
    except Exception as e:
        print(f"{Colors.FAIL}Error saat membaca alokasi petugas: {e}{Colors.ENDC}")
        return

    # Read Family Sheet
    ppl_stats = {} # ppl -> {target, ditemukan, baru, meninggal, td_eligible, td_ditemukan, nmkec, pml}
    try:
        with open(FAMILY_CACHE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            row_count = 0
            for row in reader:
                row_count += 1
                if row_count < 4:
                    continue
                if not row or len(row) < 14:
                    continue
                if row_count == 4 or row_count == 5:
                    continue
                    
                code = row[0].strip()
                if not code or len(code) != 16 or code.startswith("61040000"):
                    continue
                    
                prelist = clean_int(row[2])
                ditemukan = clean_int(row[3])
                baru = clean_int(row[5])
                meninggal = clean_int(row[6])
                td_eligible = clean_int(row[8])
                td_ditemui = clean_int(row[10])
                td_ditemukan = clean_int(row[12])
                
                info = alokasi_map.get(code, {"ppl": "UNKNOWN", "pml": "UNKNOWN", "pj": "UNKNOWN", "nmkec": "UNKNOWN"})
                ppl = info["ppl"]
                pml = info["pml"]
                nmkec = info["nmkec"]
                
                if ppl == "UNKNOWN":
                    continue
                    
                if ppl not in ppl_stats:
                    ppl_stats[ppl] = {
                        "ppl": ppl,
                        "pml": pml,
                        "nmkec": nmkec,
                        "prelist": 0,
                        "ditemukan": 0,
                        "baru": 0,
                        "meninggal": 0,
                        "td_eligible": 0,
                        "td_ditemui": 0,
                        "td_ditemukan": 0
                    }
                    
                ppl_stats[ppl]["prelist"] += prelist
                ppl_stats[ppl]["ditemukan"] += ditemukan
                ppl_stats[ppl]["baru"] += baru
                ppl_stats[ppl]["meninggal"] += meninggal
                ppl_stats[ppl]["td_eligible"] += td_eligible
                ppl_stats[ppl]["td_ditemui"] += td_ditemui
                ppl_stats[ppl]["td_ditemukan"] += td_ditemukan
    except Exception as e:
        print(f"{Colors.FAIL}Error saat membaca pemutakhiran keluarga: {e}{Colors.ENDC}")
        return

    # Calculate percentages and metrics
    ppl_list = []
    for ppl, s in ppl_stats.items():
        prelist = s["prelist"]
        if prelist == 0:
            continue
        pct_td_ditemukan = (s["td_ditemukan"] / prelist * 100)
        pct_meninggal = (s["meninggal"] / prelist * 100)
        pct_ditemukan = (s["ditemukan"] / prelist * 100)
        
        ppl_list.append({
            "ppl": ppl,
            "pml": s["pml"],
            "nmkec": s["nmkec"],
            "prelist": prelist,
            "ditemukan": s["ditemukan"],
            "baru": s["baru"],
            "meninggal": s["meninggal"],
            "td_ditemukan": s["td_ditemukan"],
            "pct_td_ditemukan": pct_td_ditemukan,
            "pct_meninggal": pct_meninggal,
            "pct_ditemukan": pct_ditemukan
        })

    # Analyze distributions
    pct_td_list = [p["pct_td_ditemukan"] for p in ppl_list if p["prelist"] >= 50]
    
    if not pct_td_list:
        print(f"{Colors.WARNING}Peringatan: Tidak ada data PPL dengan beban prelist >= 50 untuk dihitung deviasinya.{Colors.ENDC}")
        return
        
    import numpy as np
    avg_td = np.mean(pct_td_list)
    std_td = np.std(pct_td_list)
    
    # Render outputs
    print(f"\n{Colors.BOLD}{Colors.HEADER}=== DETEKSI ANOMALI PEMUTAKHIRAN KELUARGA (POTENSI MORAL HAZARD) ==={Colors.ENDC}")
    print(f"Rata-rata Kab. Mempawah (μ)       : {Colors.BOLD}{avg_td:.2f}%{Colors.ENDC}")
    print(f"Standar Deviasi (σ)               : {Colors.BOLD}{std_td:.2f}%{Colors.ENDC}")
    print(f"Batas Anomali Ringan (μ + 1.5σ)   : {Colors.WARNING}{avg_td + 1.5*std_td:.2f}%{Colors.ENDC}")
    print(f"Batas Anomali Kritis (μ + 2.0σ)   : {Colors.FAIL}{avg_td + 2*std_td:.2f}%{Colors.ENDC}")
    
    sep = "-" * 115
    print(sep)
    print(f" {'No':<3} | {'Nama PPL':<25} | {'Kecamatan':<15} | {'PML Pengawas':<25} | {'Prelist':<7} | {'Td Ditemukan':<12} | {'% Td Ditemukan':<15}")
    print(sep)
    
    sorted_ppl = sorted(ppl_list, key=lambda x: x["pct_td_ditemukan"], reverse=True)
    idx = 1
    for p in sorted_ppl:
        if p["prelist"] < 50:
            continue
        
        pct = p["pct_td_ditemukan"]
        # Filter outliers
        if pct > (avg_td + 1.5 * std_td):
            if pct > (avg_td + 2.0 * std_td):
                color = Colors.FAIL
            else:
                color = Colors.WARNING
                
            print(f" {idx:<3} | {p['ppl']:<25} | {p['nmkec']:<15} | {p['pml']:<25} | {p['prelist']:<7} | {p['td_ditemukan']:<12} | {color}{pct:>13.2f}%{Colors.ENDC}")
            idx += 1
            
    print(sep)
    print(f" * Catatan: Deviasi tinggi (> 1.5σ) mengindikasikan rasio 'Tidak Ditemukan' yang tidak wajar.")
    print(f"   PML bersangkutan direkomendasikan melakukan kroscek lapangan acak (sampling revisit).")
    print()
