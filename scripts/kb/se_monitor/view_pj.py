"""kb/se_monitor/view_pj.py — Tampilkan breakdown detail tim PJ tertentu (default view)."""

import sys

from ..colors import Colors
from .data import get_target_status, get_est_completion


def print_pj(
    target_pj_name: str,
    pj_summaries: list,
    pj_kuda_groups: dict,
    aggregate_fn,
    kab_avg_completed: float,
    kab_avg_worked: float,
    kab_avg_approval: float,
    elapsed_days: int,
    total_days: int,
    expected_pct: float,
    data_source_info: str,
) -> None:
    """Cetak breakdown detail tim PJ-Kuda tertentu beserta diagnosis."""
    target_pj = next(
        (p for p in pj_summaries if p["pj"].lower() == target_pj_name.lower()),
        None,
    )

    if not target_pj:
        print(f"{Colors.FAIL}Error: PJ-Kuda '{target_pj_name}' tidak ditemukan.{Colors.ENDC}")
        print("Nama PJ-Kuda yang tersedia:")
        for p in sorted(pj_summaries, key=lambda x: x["pj"]):
            print(f" - {p['pj']}")
        sys.exit(1)

    rank = pj_summaries.index(target_pj) + 1
    pj_pct = target_pj["completed_rate"] * 100

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== STATUS MONITORING PJ-KUDA: {target_pj['pj']} ==={Colors.ENDC}")
    print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
    print(f"Peringkat Kabupaten : {Colors.BOLD}{rank} dari {len(pj_summaries)}{Colors.ENDC}")
    print(f"Target Total        : {target_pj['target']} unit sensus (SLS: {target_pj['sls_count']})")
    print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
    print(
        f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} "
        f"(Hari ke-{elapsed_days} dari {total_days} hari lapangan)"
    )
    print(f"Status Target       : {get_target_status(pj_pct, expected_pct)}")
    print(f"Estimasi PPL Selesai (Worked): {get_est_completion(target_pj['worked_rate'] * 100, elapsed_days)}")
    print(f"Estimasi PML Selesai (Done)  : {get_est_completion(pj_pct, elapsed_days)}")
    print("-" * 55)

    def _cmp(label, team_val, kab_val):
        color = Colors.GREEN if team_val >= kab_val else Colors.WARNING
        print(f"{label:<19}: {color}{team_val*100:>6.2f}%{Colors.ENDC} (Kabupaten: {kab_val*100:.2f}%)")

    _cmp("Worked Rate",    target_pj["worked_rate"],    kab_avg_worked)
    _cmp("Completed Rate", target_pj["completed_rate"], kab_avg_completed)
    _cmp("Approval Rate",  target_pj["approval_rate"],  kab_avg_approval)

    pmls = pj_kuda_groups.get(target_pj["pj"], {})
    warnings = []

    for pml, ppls in pmls.items():
        pml_sls = []
        for _, sls_list in ppls.items():
            pml_sls.extend(sls_list)
        pml_agg = aggregate_fn(pml_sls)

        pml_done_color = Colors.GREEN if pml_agg["completed_rate"] >= kab_avg_completed else Colors.WARNING
        pml_app_color = (
            Colors.GREEN if pml_agg["approval_rate"] >= 0.7
            else (Colors.FAIL if pml_agg["approval_rate"] < 0.2 and pml_agg["submitted"] > 0
                  else Colors.WARNING)
        )

        print(f"\n{Colors.BOLD}▶ PML: {pml}{Colors.ENDC} (SLS: {pml_agg['sls_count']}, Target: {pml_agg['target']})")
        print(
            f"  └─ Progres: {pml_done_color}{pml_agg['completed_rate']*100:.2f}%{Colors.ENDC} "
            f"Selesai, Approval: {pml_app_color}{pml_agg['approval_rate']*100:.2f}%{Colors.ENDC}"
        )
        sep = "  " + "-" * 88
        print(sep)
        print(
            f"  {'Nama PPL':<25} | {'SLS':<3} | {'Target':<6} | {'Open':<5} "
            f"| {'Draft':<5} | {'Submit':<6} | {'Approve':<7} | {'Done %':<8}"
        )
        print(sep)

        ppl_list = []
        for ppl, sls_list in ppls.items():
            ppl_agg = aggregate_fn(sls_list)
            ppl_agg["name"] = ppl
            ppl_list.append(ppl_agg)
        ppl_list.sort(key=lambda x: x["completed_rate"])

        for ppl in ppl_list:
            done_color = (
                Colors.GREEN if ppl["completed_rate"] >= 0.1
                else (Colors.FAIL if ppl["completed_rate"] < 0.03 else Colors.WARNING)
            )
            print(
                f"  {ppl['name']:<25} | {ppl['sls_count']:<3} | {ppl['target']:<6} "
                f"| {ppl['open']:<5} | {ppl['draft']:<5} | {ppl['submitted']:<6} "
                f"| {ppl['approved']:<7} | {done_color}{ppl['completed_rate']*100:>6.2f}%{Colors.ENDC}"
            )
            if ppl["completed_rate"] < 0.03:
                warnings.append(
                    f"PPL {Colors.BOLD}{ppl['name']}{Colors.ENDC} di bawah PML {pml} "
                    f"lambat memulai pencacahan ({ppl['completed_rate']*100:.2f}% Selesai, {ppl['open']} Open)"
                )

        if pml_agg["approval_rate"] < 0.2 and pml_agg["submitted"] > 5:
            warnings.append(
                f"PML {Colors.BOLD}{pml}{Colors.ENDC} menumpuk pekerjaan PPL "
                f"({Colors.FAIL}Approval Rate: {pml_agg['approval_rate']*100:.2f}%{Colors.ENDC}, "
                f"{pml_agg['submitted']} kiriman menunggu persetujuan)"
            )

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== DIAGNOSIS & TINDAKAN KOREKTIF ==={Colors.ENDC}")
    if warnings:
        for w in warnings:
            print(f" ⚠️  {w}")
    else:
        print(f" {Colors.GREEN}✔ Semua progres tim berjalan sehat sesuai dengan standar rata-rata kabupaten.{Colors.ENDC}")
    print()
