"""kb/se_monitor/view_intervention.py — Tampilkan daftar intervensi se-kabupaten (-i)."""

from ..colors import Colors
from .data import get_target_status, get_est_completion


def print_intervention(
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
    """Cetak daftar PPL terlambat dan PML bottleneck se-kabupaten."""
    kab_pct = kab_avg_completed * 100

    # Build supervisor lookups & metrics
    ppl_to_supervisors: dict = {}
    pml_to_pj: dict = {}
    ppl_metrics: dict = {}
    pml_metrics: dict = {}

    for pj, pmls in pj_kuda_groups.items():
        for pml, ppls in pmls.items():
            pml_to_pj[pml] = pj
            pml_sls = []
            for ppl, sls_list in ppls.items():
                ppl_to_supervisors[ppl] = (pml, pj)
                ppl_metrics[ppl] = aggregate_fn(sls_list)
                pml_sls.extend(sls_list)
            pml_metrics[pml] = aggregate_fn(pml_sls)

    # PPL terlambat: completed < ppl_threshold dan target > 200
    # Batas kritis PPL: max(3.0%, 25% dari target ideal harian)
    ppl_threshold = max(0.03, (expected_pct / 100) * 0.25)
    low_ppls = [
        (name, m) for name, m in ppl_metrics.items()
        if m["target"] > 200 and m["completed_rate"] < ppl_threshold
    ]
    low_ppls.sort(key=lambda x: x[1]["completed_rate"])

    # PML bottleneck: pending > 20 dan approval < 20%
    bottleneck_pmls = [
        (name, m) for name, m in pml_metrics.items()
        if m["submitted"] > 20 and m["approval_rate"] < 0.20
    ]
    bottleneck_pmls.sort(key=lambda x: x[1]["approval_rate"])

    print(f"\n{Colors.BOLD}{Colors.HEADER}=== LAPORAN INTERVENSI PROGRES SE-2026 KAB. MEMPAWAH ==={Colors.ENDC}")
    print(f"Sumber Data         : {Colors.BOLD}{data_source_info}{Colors.ENDC}")
    print(f"Target Deadline     : {Colors.BOLD}15 Agustus 2026{Colors.ENDC} (Tenggat Internal)")
    print(
        f"Expected Progress   : {Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} "
        f"(Hari ke-{elapsed_days} dari {total_days})"
    )
    print(f"Status Kab. Mempawah: {get_target_status(kab_pct, expected_pct)}")
    print(f"Estimasi PPL Selesai (Worked): {get_est_completion(kab_avg_worked * 100, elapsed_days)}")
    print(f"Estimasi PML Selesai (Done)  : {get_est_completion(kab_pct, elapsed_days)}")
    sep = "-" * 115
    print(sep)
    print(
        f"Rata-rata Kabupaten : Worked={kab_avg_worked*100:.2f}%, "
        f"Completed={kab_avg_completed*100:.2f}%, Approval={kab_avg_approval*100:.2f}%"
    )

    # Tabel PPL terlambat
    print(f"\n{Colors.BOLD}{Colors.FAIL}1. DAFTAR PPL TERLAMBAT (Progres Selesai < {ppl_threshold*100:.2f}% & Target > 200){Colors.ENDC}")
    print(sep)
    print(f"{'No':<3} | {'Nama PPL':<25} | {'Target':<6} | {'Selesai':<8} | {'Open':<5} | {'Nama PML':<20} | {'PJ-Kuda':<25}")
    print(sep)
    for idx, (name, m) in enumerate(low_ppls, 1):
        pml, pj = ppl_to_supervisors[name]
        print(
            f"{idx:<3} | {name:<25} | {m['target']:<6} | {m['completed_rate']*100:>6.2f}% "
            f"| {m['open']:<5} | {pml:<20} | {pj:<25}"
        )
    print(sep)

    # Tabel PML bottleneck
    print(f"\n{Colors.BOLD}{Colors.WARNING}2. DAFTAR PML BOTTLENECK (Pending > 20 & Approval Rate < 20.00%){Colors.ENDC}")
    sep2 = "-" * 105
    print(sep2)
    print(f"{'No':<3} | {'Nama PML':<20} | {'Pending':<8} | {'Approved':<8} | {'Approval %':<10} | {'PJ-Kuda':<25}")
    print(sep2)
    for idx, (name, m) in enumerate(bottleneck_pmls, 1):
        pj = pml_to_pj[name]
        print(
            f"{idx:<3} | {name:<20} | {m['submitted']:<8} | {m['approved']:<8} "
            f"| {m['approval_rate']*100:>8.2f}% | {pj:<25}"
        )
    print(sep2)

    print(f"\n{Colors.BOLD}{Colors.CYAN}💡 PEDOMAN INTERVENSI PROFESIONAL PJ-KUDA & PML MITRA:{Colors.ENDC}")
    print(" 1. Hubungi PML Bottleneck: Tekankan agar PML memverifikasi berkas yang masuk minimal 2 kali sehari.")
    print("    Ingatkan bahwa PML Mitra wajib menjaga ritme kerja agar PPL tidak terhambat.")
    print(" 2. Hubungi PML dari PPL Terlambat: Tugaskan PML untuk mendampingi PPL tersebut ke lapangan.")
    print("    Identifikasi masalah: apakah ada penolakan usaha, kendala HP/aplikasi, atau masalah personal.")
    print(" 3. Lakukan Tactical Visit: Jika ada penolakan responden besar, PJ-Kuda harus turun bersama PML.")
    print()
