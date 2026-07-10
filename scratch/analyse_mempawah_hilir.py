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
    get_est_completion,
    download_alokasi
)
from scripts.kb.se_monitor.hierarchy import build_hierarchy

def main():
    # Reconfigure stdout to support UTF-8 on Windows
    sys.stdout.reconfigure(encoding='utf-8')
    # Download latest alokasi first
    download_alokasi()

    sheet_map, csv_text, data_source_info = download_sheet()
    pj_kuda_groups, sls_info, has_alokasi = build_hierarchy()

    if not has_alokasi:
        print("Error: Alokasi Petugas tidak ditemukan.")
        return

    # Mempawah Hilir PML list (based on finding)
    mempawah_hilir_pmls = ["Abang Handri", "Nelly Nalita", "Wandi Syafari", "Zaini"]
    
    # Map PPL to SLS for each PML in Mempawah Hilir
    pml_to_sls = {pml: [] for pml in mempawah_hilir_pmls}
    pml_ppl_to_sls = {} # (pml, ppl): list of sls
    pml_to_pj = {}

    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            if pml in mempawah_hilir_pmls:
                pml_to_pj[pml] = pj
                for ppl, sls_list in ppls.items():
                    # Check if the SLS belongs to Mempawah Hilir
                    # Wait, let's filter SLS lists to only include SLS that belong to Mempawah Hilir
                    mh_sls_list = [idsls for idsls in sls_list if sls_info.get(idsls, {}).get("kecamatan", "").strip().upper() == "MEMPAWAH HILIR"]
                    if mh_sls_list:
                        pml_to_sls[pml].extend(mh_sls_list)
                        pml_ppl_to_sls.setdefault((pml, ppl), []).extend(mh_sls_list)

    # Calculate metrics for Mempawah Hilir PMLs
    pml_metrics = {}
    for pml in mempawah_hilir_pmls:
        pml_metrics[pml] = aggregate_metrics(pml_to_sls[pml], sls_info, sheet_map)

    # Calculate county averages
    all_pml_to_sls = {}
    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            for ppl, sls_list in ppls.items():
                all_pml_to_sls.setdefault(pml, []).extend(sls_list)
    
    all_pml_metrics = []
    for pml, sls_list in all_pml_to_sls.items():
        all_pml_metrics.append(aggregate_metrics(sls_list, sls_info, sheet_map))

    total_pmls = len(all_pml_metrics)
    avg_target = sum(m["target"] for m in all_pml_metrics) / total_pmls
    avg_completed = sum(m["completed_rate"] for m in all_pml_metrics) / total_pmls
    avg_worked = sum(m["worked_rate"] for m in all_pml_metrics) / total_pmls
    avg_pending = sum(m["submitted"] for m in all_pml_metrics) / total_pmls
    avg_daily_target = sum(m["pml_daily_target"] for m in all_pml_metrics) / total_pmls
    
    all_approved = sum(m["approved"] for m in all_pml_metrics)
    all_submitted = sum(m["submitted"] for m in all_pml_metrics)
    avg_approval = all_approved / (all_approved + all_submitted) if (all_approved + all_submitted) > 0 else 0.0

    elapsed_days, _, expected_pct = compute_timeline()

    # Let's print Table 1
    print("\nTABEL 1: PERBANDINGAN MAKRO KINERJA PML KECAMATAN MEMPAWAH HILIR")
    print("-" * 150)
    print(f"{'Dimensi Perbandingan':<25} | {'Abang Handri':<18} | {'Nelly Nalita':<18} | {'Wandi Syafari':<18} | {'Zaini':<18} | {'Rata-rata Kabupaten':<25}")
    print("-" * 150)
    
    def print_row(label, key, is_pct=False, is_daily=False, is_plain_int=False):
        vals = []
        for pml in mempawah_hilir_pmls:
            m = pml_metrics[pml]
            val = m[key]
            if is_pct:
                vals.append(f"{val*100:.2f}%")
            elif is_daily:
                vals.append(f"{val:.1f}/hari")
            elif is_plain_int:
                vals.append(f"{val}")
            else:
                vals.append(f"{val}")
        
        # average
        if key == "target":
            avg_val = f"{avg_target:.1f}"
        elif key == "completed_rate":
            avg_val = f"{avg_completed*100:.2f}%"
        elif key == "worked_rate":
            avg_val = f"{avg_worked*100:.2f}%"
        elif key == "approval_rate":
            avg_val = f"{avg_approval*100:.2f}%"
        elif key == "submitted":
            avg_val = f"{avg_pending:.1f}"
        elif key == "pml_daily_target":
            avg_val = f"{avg_daily_target:.1f}/hari"
        else:
            avg_val = "-"
        print(f"{label:<25} | {vals[0]:<18} | {vals[1]:<18} | {vals[2]:<18} | {vals[3]:<18} | {avg_val:<25}")

    print_row("Target Unit Sensus", "target", is_plain_int=True)
    print_row("Completed Rate (Done %)", "completed_rate", is_pct=True)
    print_row("Worked Rate (Mulai %)", "worked_rate", is_pct=True)
    print_row("Approval Rate (%)", "approval_rate", is_pct=True)
    print_row("Antrean Pending (Sub)", "submitted", is_plain_int=True)
    print_row("Target Harian (App/Hr)", "pml_daily_target", is_daily=True)
    
    # Bottleneck status row
    bottleneck_strs = []
    for pml in mempawah_hilir_pmls:
        m = pml_metrics[pml]
        is_bn = m["submitted"] > 20 and m["approval_rate"] < 0.20
        bottleneck_strs.append(f"{Colors.FAIL}🔴 BOTTLENECK{Colors.ENDC}" if is_bn else f"{Colors.GREEN}🟢 AMAN{Colors.ENDC}")
    print(f"{'Status Bottleneck':<25} | {bottleneck_strs[0]:<18} | {bottleneck_strs[1]:<18} | {bottleneck_strs[2]:<18} | {bottleneck_strs[3]:<18} | -")
    print("-" * 150)

    # Print Table 2 for each PML
    for pml in mempawah_hilir_pmls:
        print(f"\nTABEL 2: DETAIL KINERJA PPL DI BAWAH PML {pml.upper()} (PJ: {pml_to_pj[pml].split()[0]})")
        print("-" * 155)
        print(f"{'Nama PPL':<25} | {'SLS':<5} | {'Target':<6} | {'OPEN':<5} | {'DRAFT':<5} | {'DRAFT %':<8} | {'SUBMIT':<6} | {'APPROVE':<7} | {'Tgt Submit/Hr':<13} | {'Worked %':<10} | {'Done %':<8} | {'Est. Selesai'}")
        print("-" * 155)
        
        # Collect PPLs under this PML
        ppl_details = []
        for (k_pml, ppl), sls_list in pml_ppl_to_sls.items():
            if k_pml == pml:
                ppl_m = aggregate_metrics(sls_list, sls_info, sheet_map)
                done_pct = ppl_m["completed_rate"] * 100
                draft_pct = ppl_m["draft"] / ppl_m["target"] * 100 if ppl_m["target"] > 0 else 0.0
                worked_pct = ppl_m["worked_rate"] * 100
                
                # Hitung est selesai
                if elapsed_days > 0 and done_pct > 0:
                    daily_speed = done_pct / elapsed_days
                    days_needed = (100.0 - done_pct) / daily_speed
                    est_date = datetime.now().date() + timedelta(days=days_needed)
                    est_str = est_date.strftime("%d %b %Y")
                else:
                    est_str = "Tdk Terproyeksi"
                
                ppl_details.append({
                    "name": ppl,
                    "sls": ppl_m["sls_count"],
                    "target": ppl_m["target"],
                    "open": ppl_m["open"],
                    "draft": ppl_m["draft"],
                    "draft_pct": draft_pct,
                    "worked_pct": worked_pct,
                    "submit": ppl_m["submitted"],
                    "approve": ppl_m["approved"],
                    "daily_tgt": ppl_m["ppl_daily_target"],
                    "done_pct": done_pct,
                    "est_str": est_str
                })
        
        # Sort by done_pct ascending
        ppl_details.sort(key=lambda x: x["done_pct"])
        for p in ppl_details:
            done_col = Colors.GREEN if p["done_pct"] >= expected_pct * 0.70 else (Colors.FAIL if p["done_pct"] < expected_pct * 0.25 else Colors.WARNING)
            emoji = "🟢" if p["done_pct"] >= expected_pct * 0.70 else ("🔴" if p["done_pct"] < expected_pct * 0.25 else "🟡")
            
            worked_col = Colors.GREEN if p["worked_pct"] >= expected_pct * 0.70 else (Colors.FAIL if p["worked_pct"] < expected_pct * 0.25 else Colors.WARNING)
            worked_emoji = "🟢" if p["worked_pct"] >= expected_pct * 0.70 else ("🔴" if p["worked_pct"] < expected_pct * 0.25 else "🟡")
            
            # Format Est. Selesai color
            if p["est_str"] == "Tdk Terproyeksi":
                est_col = Colors.FAIL
            else:
                est_dt = datetime.strptime(p["est_str"], "%d %b %Y").date()
                from scripts.kb.se_monitor.data import TARGET_DATE, SOFT_DEADLINE
                est_col = Colors.GREEN if est_dt <= TARGET_DATE else (Colors.WARNING if est_dt <= SOFT_DEADLINE else Colors.FAIL)
            
            print(f"{p['name']:<25} | {p['sls']:<5} | {p['target']:<6} | {p['open']:<5} | {p['draft']:<5} | {p['draft_pct']:>6.2f}% | {p['submit']:<6} | {p['approve']:<7} | {p['daily_tgt']:>13.1f} | {worked_col}{worked_emoji} {p['worked_pct']:>5.2f}%{Colors.ENDC} | {done_col}{emoji} {p['done_pct']:>5.2f}%{Colors.ENDC} | {est_col}{p['est_str']}{Colors.ENDC}")
        print("-" * 155)

if __name__ == "__main__":
    main()
