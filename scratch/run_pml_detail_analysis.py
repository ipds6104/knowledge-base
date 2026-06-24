import sys
import json
from pathlib import Path
from datetime import datetime

# Add the workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.kb.colors import Colors
from scripts.kb.se_monitor.data import (
    download_sheet,
    get_sls_metrics,
    aggregate_metrics,
    get_remaining_days,
    compute_timeline,
    get_est_completion
)
from scripts.kb.se_monitor.hierarchy import build_hierarchy, build_lookup_maps

def main():
    # 1. Download sheet and build hierarchy
    sheet_map, csv_text, data_source_info = download_sheet()
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()
    
    if not has_alokasi:
        print("Error: Alokasi Petugas.csv tidak ditemukan.")
        return

    # 2. Map SLS lists for each PML and each PPL
    pml_to_sls = {}
    pml_ppl_to_sls = {} # key: (pml, ppl)
    pml_to_pj = {}

    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            pml_to_pj[pml] = pj
            for ppl, sls_list in ppls.items():
                pml_to_sls.setdefault(pml, []).extend(sls_list)
                pml_ppl_to_sls.setdefault((pml, ppl), []).extend(sls_list)

    # 3. Calculate metrics for all PMLs
    pml_metrics = {}
    for pml, sls_list in pml_to_sls.items():
        pml_metrics[pml] = aggregate_metrics(sls_list, sls_info, sheet_map)

    # Ranks & Averages
    total_pmls = len(pml_metrics)
    sorted_by_completed = sorted(pml_metrics.items(), key=lambda x: x[1]["completed_rate"], reverse=True)
    sorted_by_worked = sorted(pml_metrics.items(), key=lambda x: x[1]["worked_rate"], reverse=True)

    completed_ranks = {item[0]: idx + 1 for idx, item in enumerate(sorted_by_completed)}
    worked_ranks = {item[0]: idx + 1 for idx, item in enumerate(sorted_by_worked)}

    avg_target = sum(m["target"] for m in pml_metrics.values()) / total_pmls
    avg_completed_rate = sum(m["completed_rate"] for m in pml_metrics.values()) / total_pmls
    avg_worked_rate = sum(m["worked_rate"] for m in pml_metrics.values()) / total_pmls
    
    all_approved = sum(m["approved"] for m in pml_metrics.values())
    all_submitted = sum(m["submitted"] for m in pml_metrics.values())
    avg_approval_rate = all_approved / (all_approved + all_submitted) if (all_approved + all_submitted) > 0 else 0.0
    avg_pending = sum(m["submitted"] for m in pml_metrics.values()) / total_pmls
    avg_daily_target = sum(m["pml_daily_target"] for m in pml_metrics.values()) / total_pmls

    elapsed_days, _, expected_pct = compute_timeline()

    # Dynamic threshold for PPL status
    # ppl_threshold = max(3.00, expected_pct * 0.25)
    # green_threshold = max(10.00, expected_pct * 0.70)
    def get_status_color(completed_rate_pct):
        val = completed_rate_pct
        red_limit = max(3.00, expected_pct * 0.25)
        green_limit = max(10.00, expected_pct * 0.70)
        if val >= green_limit:
            return "🟢"
        elif val < red_limit:
            return "🔴"
        else:
            return "🟡"

    for target_pml in ["Prabowo", "Jamaluddin"]:
        if target_pml not in pml_metrics:
            print(f"\nError: PML '{target_pml}' tidak ditemukan.")
            continue
        
        m = pml_metrics[target_pml]
        pj = pml_to_pj[target_pml]
        
        # Bottleneck Status
        is_bottleneck = m["submitted"] > 20 and m["approval_rate"] < 0.20
        status_bottleneck = "🔴 BOTTLENECK KRITIS" if is_bottleneck else "🟢 AMAN / AKTIF"
        if not is_bottleneck and m["submitted"] > 20:
            status_bottleneck = "🟡 WARNING (Antrean Tinggi)"

        print(f"\n==================== DETAIL PML: {target_pml} ====================")
        print(f"PJ-Kuda: {pj}")
        print(f"Target Unit: {m['target']}")
        print(f"Completed Rate: {m['completed_rate']*100:.2f}% (Rank: #{completed_ranks[target_pml]})")
        print(f"Worked Rate: {m['worked_rate']*100:.2f}% (Rank: #{worked_ranks[target_pml]})")
        print(f"Approval Rate: {m['approval_rate']*100:.2f}%")
        print(f"Pending Queue (Submitted): {m['submitted']}")
        print(f"PML Daily Target: {m['pml_daily_target']:.1f} / hari")
        print(f"Status Bottleneck: {status_bottleneck}")
        
        print("\nDetail PPL:")
        ppl_details = []
        for (pml, ppl), sls_list in pml_ppl_to_sls.items():
            if pml == target_pml:
                ppl_m = aggregate_metrics(sls_list, sls_info, sheet_map)
                done_pct = ppl_m["completed_rate"] * 100
                color = get_status_color(done_pct)
                
                # Hitung estimasi selesai
                est_val = get_est_completion(done_pct, elapsed_days)
                if "Tidak Terprediksi" in est_val or done_pct == 0:
                    est_val = f"{Colors.FAIL}Tdk Terproyeksi{Colors.ENDC}"

                ppl_details.append({
                    "name": ppl,
                    "sls": ppl_m["sls_count"],
                    "target": ppl_m["target"],
                    "open": ppl_m["open"],
                    "draft": ppl_m["draft"],
                    "submit": ppl_m["submitted"],
                    "approve": ppl_m["approved"],
                    "daily_tgt": ppl_m["ppl_daily_target"],
                    "done_pct": done_pct,
                    "color": color,
                    "est_selesai": est_val
                })
        
        # Sort by done_pct ascending
        ppl_details.sort(key=lambda x: x["done_pct"])
        for p in ppl_details:
            print(f" - {p['name']} | SLS: {p['sls']} | Target: {p['target']} | Open: {p['open']} | Draft: {p['draft']} | Submit: {p['submit']} | Approve: {p['approve']} | Tgt Submit: {p['daily_tgt']:.1f}/hari | Done: {p['done_pct']:.2f}% ({p['color']}) | Est. Selesai: {p['est_selesai']}")

    # Output averages for Table 1
    print("\n==================== RATA-RATA KABUPATEN ====================")
    print(f"Avg Target: {avg_target:.1f}")
    print(f"Avg Completed Rate: {avg_completed_rate*100:.2f}%")
    print(f"Avg Worked Rate: {avg_worked_rate*100:.2f}%")
    print(f"Avg Approval Rate: {avg_approval_rate*100:.2f}%")
    print(f"Avg Pending: {avg_pending:.1f}")
    print(f"Avg Daily Target (Approve): {avg_daily_target:.1f}")
    print(f"Expected Ideal %: {expected_pct:.2f}%")

if __name__ == "__main__":
    main()
