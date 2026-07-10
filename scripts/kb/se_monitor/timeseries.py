"""kb/se_monitor/timeseries.py — Modul untuk menganalisis tren data harian dari arsip."""

import os
from pathlib import Path
from datetime import datetime

from ..colors import Colors
from .data import _parse_sheet_csv, aggregate_metrics
from .hierarchy import build_hierarchy

ARCHIVE_DIR = Path("kegiatan/sensus-ekonomi-2026/2026/archive")

def get_ppl_trend(ppl_name_query: str) -> None:
    """Mencari tren harian untuk PPL tertentu berdasarkan arsip."""
    if not ARCHIVE_DIR.exists():
        print(f"{Colors.FAIL}Error: Direktori arsip belum tersedia di {ARCHIVE_DIR}{Colors.ENDC}")
        return

    # Bangun hierarki sekali
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()
    if not has_alokasi:
        print(f"{Colors.FAIL}Error: Alokasi petugas tidak ditemukan.{Colors.ENDC}")
        return

    # Cari target PPL dan daftar SLS-nya
    target_ppl = None
    target_sls_list = []
    target_pml = None
    target_pj = None

    for pj_name, pmls in pj_kuda_groups.items():
        for pml_name, ppls in pmls.items():
            for ppl_name, sls_list in ppls.items():
                if ppl_name_query.lower() in ppl_name.lower():
                    target_ppl = ppl_name
                    target_sls_list = sls_list
                    target_pml = pml_name
                    target_pj = pj_name
                    break
            if target_ppl: break
        if target_ppl: break

    if not target_ppl:
        print(f"{Colors.WARNING}Peringatan: PPL dengan nama '{ppl_name_query}' tidak ditemukan.{Colors.ENDC}")
        return

    print(f"\n{Colors.BOLD}{Colors.CYAN}=== TREN HARIAN PPL: {target_ppl} ==={Colors.ENDC}")
    print(f"PML Pengawas: {target_pml}")
    print(f"PJ Kuda     : {target_pj}")
    print(f"{'-'*75}")
    print(f"{'Tanggal':<12} | {'Target':<6} | {'Worked':<8} | {'Done %':<8} | {'Pending (Draft)':<15}")
    print(f"{'-'*75}")

    # Kumpulkan semua subdirektori YYYY-MM-DD
    folders = []
    for item in ARCHIVE_DIR.iterdir():
        if item.is_dir():
            try:
                dt = datetime.strptime(item.name, "%Y-%m-%d")
                folders.append((dt, item))
            except ValueError:
                pass

    folders.sort(key=lambda x: x[0])

    if not folders:
        print("Belum ada data arsip harian.")
        return

    for dt, folder_path in folders:
        csv_path = folder_path / "Realisasi - 6104.csv"
        if not csv_path.exists():
            continue
            
        try:
            csv_text = csv_path.read_text(encoding='utf-8')
            sheet_map = _parse_sheet_csv(csv_text)
            
            # Hitung metrics untuk hari tersebut
            m = aggregate_metrics(target_sls_list, sls_info, sheet_map)
            
            date_str = dt.strftime("%d %b %Y")
            worked = m["worked"]
            completed = m["completed"]
            draft = worked - completed
            target = m["target"]
            done_pct = (completed / target * 100) if target > 0 else 0.0
            
            # Formatting baris tren
            done_color = Colors.GREEN if done_pct >= 40.0 else (Colors.WARNING if done_pct >= 10.0 else Colors.FAIL)
            print(f"{date_str:<12} | {target:<6} | {worked:<8} | {done_color}{done_pct:>5.2f}%{Colors.ENDC}   | {draft:<15}")
        except Exception as e:
            print(f"{date_str:<12} | Error membaca arsip: {e}")

    print(f"{'-'*75}\n")

def print_trend_main(args) -> None:
    if args.trend:
        get_ppl_trend(args.trend)
