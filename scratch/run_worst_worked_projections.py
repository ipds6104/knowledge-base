import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

# Add workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.kb.colors import Colors
from scripts.kb.se_monitor.data import (
    download_sheet,
    aggregate_metrics,
    compute_timeline,
    TARGET_DATE,
    download_alokasi
)
from scripts.kb.se_monitor.hierarchy import build_hierarchy

def main():
    download_alokasi()

    sheet_map, _, _ = download_sheet()
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()

    if not has_alokasi:
        print("Error: Alokasi Petugas tidak ditemukan.")
        return

    elapsed_days, _, expected_pct = compute_timeline()
    today = datetime.now().date()

    ppl_list = []
    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            for ppl, sls_list in ppls.items():
                ppl_m = aggregate_metrics(sls_list, sls_info, sheet_map)
                done_pct = ppl_m["completed_rate"] * 100
                worked_pct = ppl_m["worked_rate"] * 100
                
                # Hitung estimasi selesai berdasarkan worked_rate
                if elapsed_days > 0 and worked_pct > 0:
                    daily_speed = worked_pct / elapsed_days
                    days_needed = (100.0 - worked_pct) / daily_speed
                    est_date = today + timedelta(days=days_needed)
                else:
                    est_date = None

                ppl_list.append({
                    "name": ppl,
                    "pml": pml,
                    "pj": pj,
                    "target": ppl_m["target"],
                    "completed": ppl_m["completed"],
                    "worked": ppl_m["worked"],
                    "worked_pct": worked_pct,
                    "done_pct": done_pct,
                    "est_date": est_date,
                })

    # Sort logic (Worked):
    # - Terproyeksi == None (Belum Mulai Worked) diletakkan paling atas, diurutkan berdasarkan target terbesar
    # - Terproyeksi != None diurutkan berdasarkan est_date secara descending (paling lambat)
    ppl_list.sort(key=lambda x: (0, -x["target"]) if x["est_date"] is None else (1, -x["est_date"].toordinal()))

    print(f"\n==================== 15 PPL DENGAN PROYEKSI SELESAI WORKED TERLAMA ====================")
    print(f"Hari Lapangan Berjalan: {elapsed_days} hari | Progress Ideal Hari Ini: {expected_pct:.2f}%")
    print(f"Batas Target Internal : 15 Agustus 2026")
    sep_line = "-" * 142
    print(sep_line)
    print(f"{'No':<3} | {'Nama PPL':<25} | {'PML Pengawas':<20} | {'PJ-Kuda':<15} | {'Target':<6} | {'Worked':<8} | {'Worked %':<10} | {'Done %':<8} | {'Est. Selesai Worked':<20}")
    print(sep_line)

    for idx, p in enumerate(ppl_list[:15], 1):
        if p["est_date"] is None:
            est_str = f"{Colors.FAIL}Tdk Terproyeksi{Colors.ENDC}"
        else:
            date_str = p["est_date"].strftime("%d %b %Y")
            color = Colors.GREEN if p["est_date"] <= TARGET_DATE else (Colors.WARNING if p["est_date"] <= datetime.strptime("2026-08-31", "%Y-%m-%d").date() else Colors.FAIL)
            est_str = f"{color}{date_str}{Colors.ENDC}"

        done_color = Colors.GREEN if p["done_pct"] >= expected_pct * 0.70 else (Colors.FAIL if p["done_pct"] < expected_pct * 0.25 else Colors.WARNING)
        worked_color = Colors.GREEN if p["worked_pct"] >= expected_pct * 0.70 else (Colors.FAIL if p["worked_pct"] < expected_pct * 0.25 else Colors.WARNING)
        worked_emoji = "🟢" if p["worked_pct"] >= expected_pct * 0.70 else ("🔴" if p["worked_pct"] < expected_pct * 0.25 else "🟡")

        visible_est = re.sub(r'\033\[[0-9;]*m', '', est_str)
        padding = 20 - len(visible_est)
        est_padded = est_str + " " * padding

        print(f"{idx:<3} | {p['name']:<25} | {p['pml']:<20} | {p['pj'].split()[0]:<15} | {p['target']:<6} | {p['worked']:<8} | {worked_color}{worked_emoji} {p['worked_pct']:>6.2f}%{Colors.ENDC} | {done_color}{p['done_pct']:>6.2f}%{Colors.ENDC} | {est_padded}")

if __name__ == "__main__":
    main()
