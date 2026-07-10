import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

# Reconfigure stdout to support UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Add workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.kb.colors import Colors
from scripts.kb.se_monitor.data import (
    download_sheet,
    aggregate_metrics,
    compute_timeline,
    get_est_completion,
    download_alokasi
)
from scripts.kb.se_monitor.hierarchy import build_hierarchy

def main():
    # Download latest alokasi first
    download_alokasi()

    sheet_map, csv_text, data_source_info = download_sheet()
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()

    if not has_alokasi:
        print("Error: Alokasi Petugas tidak ditemukan.")
        return

    # Find all PMLs and compute metrics for ranking
    all_pml_to_sls = {}
    pml_to_pj = {}
    pml_ppl_to_sls = {}
    
    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            pml_to_pj[pml] = pj
            for ppl, sls_list in ppls.items():
                all_pml_to_sls.setdefault(pml, []).extend(sls_list)
                pml_ppl_to_sls.setdefault((pml, ppl), []).extend(sls_list)

    all_pml_metrics = {}
    for pml, sls_list in all_pml_to_sls.items():
        all_pml_metrics[pml] = aggregate_metrics(sls_list, sls_info, sheet_map)

    # Calculate Ranks
    sorted_by_completed = sorted(all_pml_metrics.items(), key=lambda x: x[1]["completed_rate"], reverse=True)
    sorted_by_worked = sorted(all_pml_metrics.items(), key=lambda x: x[1]["worked_rate"], reverse=True)

    completed_ranks = {item[0]: idx + 1 for idx, item in enumerate(sorted_by_completed)}
    worked_ranks = {item[0]: idx + 1 for idx, item in enumerate(sorted_by_worked)}

    # Calculate County Averages
    total_pmls = len(all_pml_metrics)
    avg_target = sum(m["target"] for m in all_pml_metrics.values()) / total_pmls
    avg_completed = sum(m["completed_rate"] for m in all_pml_metrics.values()) / total_pmls
    avg_worked = sum(m["worked_rate"] for m in all_pml_metrics.values()) / total_pmls
    avg_pending = sum(m["submitted"] for m in all_pml_metrics.values()) / total_pmls
    avg_daily_target = sum(m["pml_daily_target"] for m in all_pml_metrics.values()) / total_pmls
    
    all_approved = sum(m["approved"] for m in all_pml_metrics.values())
    all_submitted = sum(m["submitted"] for m in all_pml_metrics.values())
    avg_approval = all_approved / (all_approved + all_submitted) if (all_approved + all_submitted) > 0 else 0.0

    elapsed_days, _, expected_pct = compute_timeline()

    # Target PMLs to analyze
    target_pmls = ["Mulyadi", "Dandy"]
    pml_results = {}

    for pml in target_pmls:
        if pml not in all_pml_metrics:
            print(f"Error: PML {pml} tidak ditemukan.")
            continue
        pml_results[pml] = {
            "metrics": all_pml_metrics[pml],
            "pj": pml_to_pj[pml],
            "completed_rank": completed_ranks[pml],
            "worked_rank": worked_ranks[pml]
        }

    # Print Table 1 comparison
    print("### PML MACRO COMPARISON DATA")
    print(json.dumps({
        "target_pmls": target_pmls,
        "expected_pct": expected_pct,
        "elapsed_days": elapsed_days,
        "averages": {
            "target": avg_target,
            "completed_rate": avg_completed,
            "worked_rate": avg_worked,
            "approval_rate": avg_approval,
            "submitted": avg_pending,
            "pml_daily_target": avg_daily_target
        },
        "pmls": {
            pml: {
                "pj": pml_results[pml]["pj"],
                "target": pml_results[pml]["metrics"]["target"],
                "completed_rate": pml_results[pml]["metrics"]["completed_rate"],
                "completed_rank": pml_results[pml]["completed_rank"],
                "worked_rate": pml_results[pml]["metrics"]["worked_rate"],
                "worked_rank": pml_results[pml]["worked_rank"],
                "approval_rate": pml_results[pml]["metrics"]["approval_rate"],
                "submitted": pml_results[pml]["metrics"]["submitted"],
                "pml_daily_target": pml_results[pml]["metrics"]["pml_daily_target"]
            }
            for pml in target_pmls if pml in pml_results
        }
    }, indent=2))

    # Print Table 2 details for each target PML
    for pml in target_pmls:
        if pml not in pml_results:
            continue
        print(f"\n### PPL DETAILS FOR PML {pml.upper()}")
        ppl_details = []
        for (k_pml, ppl), sls_list in pml_ppl_to_sls.items():
            if k_pml == pml:
                ppl_m = aggregate_metrics(sls_list, sls_info, sheet_map)
                done_pct = ppl_m["completed_rate"] * 100
                draft_pct = ppl_m["draft"] / ppl_m["target"] * 100 if ppl_m["target"] > 0 else 0.0
                worked_pct = ppl_m["worked_rate"] * 100
                
                if elapsed_days > 0 and done_pct > 0:
                    daily_speed = done_pct / elapsed_days
                    days_needed = (100.0 - done_pct) / daily_speed
                    est_date = datetime.now().date() + timedelta(days=days_needed)
                    est_str = est_date.strftime("%d %b %Y")
                else:
                    est_str = "Tdk Terproyeksi"

                ppl_details.append({
                    "name": ppl,
                    "sls_count": ppl_m["sls_count"],
                    "target": ppl_m["target"],
                    "open": ppl_m["open"],
                    "draft": ppl_m["draft"],
                    "draft_pct": draft_pct,
                    "submit": ppl_m["submitted"],
                    "approve": ppl_m["approved"],
                    "daily_tgt": ppl_m["ppl_daily_target"],
                    "worked_pct": worked_pct,
                    "done_pct": done_pct,
                    "est_selesai": est_str
                })
        
        # Sort by done_pct ascending
        ppl_details.sort(key=lambda x: x["done_pct"])
        print(json.dumps(ppl_details, indent=2))

if __name__ == "__main__":
    main()
