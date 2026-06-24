import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.kb.colors import Colors
from scripts.kb.se_monitor.data import (
    download_sheet,
    aggregate_metrics,
    compute_timeline,
    get_est_completion,
    TARGET_DATE
)
from scripts.kb.se_monitor.hierarchy import build_hierarchy

def main():
    # 1. Download data & hierarchy
    sheet_map, _, _ = download_sheet()
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()

    if not has_alokasi:
        print("Error: Alokasi Petugas tidak ditemukan.")
        return

    # 2. Get elapsed days
    elapsed_days, _, expected_pct = compute_timeline()
    today = datetime.now().date()

    # 3. Aggregate metrics per PPL
    ppl_list = []
    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            for ppl, sls_list in ppls.items():
                ppl_m = aggregate_metrics(sls_list, sls_info, sheet_map)
                done_pct = ppl_m["completed_rate"] * 100
                
                # Hitung tanggal estimasi selesai objek date untuk pengurutan
                if elapsed_days > 0 and done_pct > 0:
                    daily_speed = done_pct / elapsed_days
                    days_needed = (100.0 - done_pct) / daily_speed
                    est_date = today + timedelta(days=days_needed)
                else:
                    est_date = None  # Tdk Terproyeksi

                ppl_list.append({
                    "name": ppl,
                    "pml": pml,
                    "pj": pj,
                    "target": ppl_m["target"],
                    "completed": ppl_m["completed"],
                    "done_pct": done_pct,
                    "est_date": est_date,
                })

    # 4. Sorting logic:
    # - Terproyeksi == None (Belum Mulai) diletakkan paling atas, diurutkan berdasarkan target terbesar
    # - Terproyeksi != None diurutkan berdasarkan est_date secara descending (paling lambat/jauh)
    # Group 0: None, sorted by target desc
    # Group 1: Has date, sorted descending by date
    ppl_list.sort(key=lambda x: (0, -x["target"]) if x["est_date"] is None else (1, -x["est_date"].toordinal()))

    # 5. Print results in a clean table
    print(f"\n==================== PPL DENGAN PROYEKSI SELESAI PALING LAMBAT ====================")
    print(f"Hari Lapangan Berjalan: {elapsed_days} hari | Progress Ideal Hari Ini: {expected_pct:.2f}%")
    print(f"Batas Target Internal : 15 Agustus 2026")
    print("-" * 125)
    print(f"{'No':<3} | {'Nama PPL':<25} | {'PML Pengawas':<20} | {'PJ-Kuda':<15} | {'Target':<6} | {'Selesai':<8} | {'Done %':<8} | {'Est. Selesai':<15}")
    print("-" * 125)

    for idx, p in enumerate(ppl_list[:15], 1):
        if p["est_date"] is None:
            est_str = f"{Colors.FAIL}Tdk Terproyeksi{Colors.ENDC}"
        else:
            date_str = p["est_date"].strftime("%d %b %Y")
            color = Colors.GREEN if p["est_date"] <= TARGET_DATE else (Colors.WARNING if p["est_date"] <= datetime.strptime("2026-08-31", "%Y-%m-%d").date() else Colors.FAIL)
            est_str = f"{color}{date_str}{Colors.ENDC}"

        done_color = Colors.GREEN if p["done_pct"] >= expected_pct * 0.70 else (Colors.FAIL if p["done_pct"] < expected_pct * 0.25 else Colors.WARNING)
        
        # Strip color code to align
        visible_est = est_str.replace(Colors.GREEN, '').replace(Colors.WARNING, '').replace(Colors.FAIL, '').replace(Colors.ENDC, '')
        padding = 15 - len(visible_est)
        est_padded = est_str + " " * padding

        print(f"{idx:<3} | {p['name']:<25} | {p['pml']:<20} | {p['pj'].split()[0]:<15} | {p['target']:<6} | {p['completed']:<8} | {done_color}{p['done_pct']:>6.2f}%{Colors.ENDC} | {est_padded}")

if __name__ == "__main__":
    main()
