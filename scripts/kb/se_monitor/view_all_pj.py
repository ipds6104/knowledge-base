"""kb/se_monitor/view_all_pj.py — Tampilkan peringkat PJ-Kuda (--all-pj)."""

from ..colors import Colors
from .data import get_target_status


def print_all_pj(
    pj_summaries: list,
    kab_avg_completed: float,
    elapsed_days: int,
    total_days: int,
    expected_pct: float,
    data_source_info: str,
    target_pj_name: str,
) -> None:
    """Cetak tabel peringkat seluruh PJ-Kuda Kabupaten Mempawah."""
    kab_pct = kab_avg_completed * 100

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== PERINGKAT PROGRES PJ-KUDA KAB. MEMPAWAH ==={Colors.ENDC}")
    print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
    print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
    print(
        f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} "
        f"(Hari ke-{elapsed_days} dari {total_days})"
    )
    print(f"Status Kab. Mempawah: {get_target_status(kab_pct, expected_pct)}")

    sep = "-" * 88
    print(sep)
    print(
        f"{'No':<3} | {'Nama PJ-Kuda':<28} | {'SLS':<4} | {'Target':<6} "
        f"| {'Worked %':<10} | {'Done %':<10} | {'Approved %':<10}"
    )
    print(sep)

    for idx, pj in enumerate(pj_summaries, 1):
        is_me = pj["pj"].lower() == target_pj_name.lower()
        row_c = Colors.BOLD + Colors.CYAN if is_me else ""
        end_c = Colors.ENDC if is_me else ""
        print(
            f"{row_c}{idx:<3} | {pj['pj']:<28} | {pj['sls_count']:<4} | {pj['target']:<6} "
            f"| {pj['worked_rate']*100:>8.2f}% | {pj['completed_rate']*100:>8.2f}% "
            f"| {pj['approval_rate']*100:>8.2f}%{end_c}"
        )

    print(sep)
