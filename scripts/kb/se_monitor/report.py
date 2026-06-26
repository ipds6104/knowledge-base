"""kb/se_monitor/report.py — Laporan 6-seksi baku (--report / -r)."""

from datetime import datetime, timedelta
import re

from ..colors import Colors
from .data import get_target_status, get_est_completion
from .hierarchy import pj_first_name


def print_report(
    prov_agg: dict,
    kab_data: dict,
    kab_list: list,
    pj_summaries: list,
    pj_kuda_groups: dict,
    sls_info: dict,
    aggregate_fn,
    elapsed_days: int,
    total_days: int,
    expected_pct: float,
    target_pj_name: str,
    current_snapshot: dict,
    latest_history: dict | None,
) -> None:
    """Cetak laporan 6-seksi baku SE-2026."""
    now_str = datetime.now().strftime("%d %B %Y, pukul %H:%M WIB")
    prov_pct = prov_agg["done_rate"] * 100
    prov_approved_pct = prov_agg["approved"] / prov_agg["target"] * 100 if prov_agg.get("target", 0) > 0 else 0.0

    # Kalbar rank of Mempawah
    memp_rank  = next((i + 1 for i, (k, _) in enumerate(kab_list) if k == "MEMPAWAH"), "?")
    memp_total = len(kab_list)

    # Mempawah metrics
    memp_m = kab_data.get("MEMPAWAH", {})
    memp_done_pct   = memp_m["completed"] / memp_m["target"] * 100 if memp_m.get("target", 0) > 0 else 0.0
    memp_approved_pct = memp_m["approved"] / memp_m["target"] * 100 if memp_m.get("target", 0) > 0 else 0.0

    # Target PJ metrics
    target_pj_data = next((p for p in pj_summaries if p["pj"].lower() == target_pj_name.lower()), None)

    # Lookup maps built here (sourced only from pj_kuda_groups → Alokasi Petugas.csv)
    pml_to_pj: dict = {}
    ppl_to_sup: dict = {}
    for pj_name, pmls in pj_kuda_groups.items():
        for pml_name, ppls in pmls.items():
            pml_to_pj[pml_name] = pj_name
            for ppl_name in ppls:
                ppl_to_sup[ppl_name] = (pml_name, pj_name)

    # ─── Build PML & PPL metrics dicts ────────────────────────────────────────
    ppl_metrics: dict = {}
    pml_metrics: dict = {}
    for pj_name, pmls in pj_kuda_groups.items():
        for pml_name, ppls in pmls.items():
            pml_sls = []
            for ppl_name, sls_list in ppls.items():
                ppl_metrics[ppl_name] = aggregate_fn(sls_list)
                pml_sls.extend(sls_list)
            pml_metrics[pml_name] = aggregate_fn(pml_sls)

    # ─── Section 1: Target Harian ─────────────────────────────────────────────
    print(f"\n{'='*80}")
    print(f"   LAPORAN PROGRES SE-2026 — {now_str}")
    print(f"{'='*80}")
    print(f"\n{'─'*80}")
    print(f" 📅 1. STATUS TARGET HARIAN (Tenggat: 15 Agustus 2026)")
    print(f"{'─'*80}")
    print(
        f"   Target Progres Ideal Hari Ini : "
        f"{Colors.BOLD}{expected_pct:.2f}%{Colors.ENDC} "
        f"(Hari ke-{elapsed_days} dari {total_days} hari lapangan)"
    )
    print(
        f"   Target Harian Kab. Mempawah   : "
        f"PPL: {Colors.BOLD}{memp_m['ppl_daily_target']:.1f}/hari{Colors.ENDC} (submit), "
        f"PML: {Colors.BOLD}{memp_m['pml_daily_target']:.1f}/hari{Colors.ENDC} (approve)"
    )

    # ─── Section 2: Posisi Makro ──────────────────────────────────────────────
    # Hitung kabupaten terlama di Kalbar
    if kab_list:
        slowest_kab, slowest_m = kab_list[-1]
        slowest_pct = slowest_m["completed_rate"] * 100
        slowest_est = get_est_completion(slowest_pct, elapsed_days)
        visible_slowest_est = re.sub(r'\033\[[0-9;]*m', '', slowest_est)
        prov_worst_str = f"{slowest_kab} ({visible_slowest_est}, progres {slowest_pct:.2f}%)"
    else:
        prov_worst_str = "-"

    # Hitung PPL terlama di Mempawah
    worst_ppl_name = None
    worst_ppl_date = None
    worst_ppl_pct = 0.0
    today_dt = datetime.now().date()
    for ppl_name, m in ppl_metrics.items():
        pct = m["completed_rate"] * 100
        if elapsed_days > 0 and pct > 0:
            daily_speed = pct / elapsed_days
            days_needed = (100.0 - pct) / daily_speed
            est_date = today_dt + timedelta(days=days_needed)
        else:
            est_date = None
            
        if est_date is None:
            if m["target"] > 0 and (worst_ppl_date is not None or worst_ppl_name is None):
                worst_ppl_name = ppl_name
                worst_ppl_date = None
                worst_ppl_pct = pct
        else:
            if worst_ppl_name is None:
                worst_ppl_name = ppl_name
                worst_ppl_date = est_date
                worst_ppl_pct = pct
            elif worst_ppl_date is not None and est_date > worst_ppl_date:
                worst_ppl_name = ppl_name
                worst_ppl_date = est_date
                worst_ppl_pct = pct

    if worst_ppl_name:
        if worst_ppl_date is None:
            memp_worst_str = f"Tdk Terproyeksi ({worst_ppl_name}, progres 0.00%)"
        else:
            date_str = worst_ppl_date.strftime("%d %b %Y")
            memp_worst_str = f"{date_str} ({worst_ppl_name}, progres {worst_ppl_pct:.2f}%)"
    else:
        memp_worst_str = "-"

    print(f"\n{'─'*80}")
    print(f" 📊 2. POSISI MAKRO PROVINSI KALBAR & MEMPAWAH")
    print(f"{'─'*80}")
    print(f"   Progres Kalbar    : {Colors.BOLD}{prov_pct:.2f}%{Colors.ENDC} | Status: {get_target_status(prov_pct, expected_pct)}")
    print(f"     Target Harian Kalbar      : PPL: {prov_agg['ppl_daily_target']:.1f}/hari | PML: {prov_agg['pml_daily_target']:.1f}/hari")
    print(f"     Est. PPL Selesai (Agregat): {get_est_completion(prov_pct, elapsed_days)}")
    print(f"     Est. Kabupaten Terlama    : {prov_worst_str}")
    print(f"     Est. PML Selesai (Agregat): {get_est_completion(prov_approved_pct, elapsed_days)}")
    print(f"   Progres Mempawah  : {Colors.BOLD}{memp_done_pct:.2f}%{Colors.ENDC} | Status: {get_target_status(memp_done_pct, expected_pct)}")
    print(f"     Target Harian Mempawah    : PPL: {memp_m['ppl_daily_target']:.1f}/hari | PML: {memp_m['pml_daily_target']:.1f}/hari")
    print(f"     Est. PPL Selesai (Agregat): {get_est_completion(memp_done_pct, elapsed_days)}")
    print(f"     Est. PPL Selesai Terlama  : {memp_worst_str}")
    print(f"     Est. PML Selesai (Agregat): {get_est_completion(memp_approved_pct, elapsed_days)}")
    print(f"   Peringkat Mempawah: {Colors.BOLD}#{memp_rank} dari {memp_total}{Colors.ENDC} Kab/Kota se-Kalbar")

    # ─── Section 3: Delta ─────────────────────────────────────────────────────
    good_pmls:   list = []
    ppl_diffs_r: list = []

    print(f"\n{'─'*80}")
    print(f" 🔄 3. PERBANDINGAN DENGAN PENGECEKAN TERAKHIR")
    print(f"{'─'*80}")

    if latest_history:
        ts_last = latest_history.get('timestamp', '-')
        print(f"   (Delta sejak pengecekan {ts_last})")

        # Prov delta
        l_prov = latest_history.get("prov", {})
        if l_prov and l_prov.get("target", 0) > 0:
            l_pct = l_prov["completed"] / l_prov["target"] * 100
            diff  = prov_pct - l_pct
            diff_s = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
            c = Colors.GREEN if diff > 0 else Colors.ENDC
            print(f"   Prov. Kalbar  : {l_pct:.2f}% → {Colors.BOLD}{prov_pct:.2f}%{Colors.ENDC} ({c}{diff_s}{Colors.ENDC})")

        # Mempawah delta
        l_memp = latest_history.get("kab", {}).get("MEMPAWAH", {})
        if l_memp and l_memp.get("target", 0) > 0:
            l_pct = l_memp["completed"] / l_memp["target"] * 100
            diff  = memp_done_pct - l_pct
            diff_s = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
            c = Colors.GREEN if diff > 0 else Colors.ENDC
            print(f"   Kab. Mempawah : {l_pct:.2f}% → {Colors.BOLD}{memp_done_pct:.2f}%{Colors.ENDC} ({c}{diff_s}{Colors.ENDC})")

        # PJ delta
        c_pj_snap = current_snapshot.get("pj", {}).get(target_pj_name)
        l_pj_snap = latest_history.get("pj", {}).get(target_pj_name)
        if c_pj_snap and l_pj_snap and l_pj_snap.get("target", 0) > 0:
            l_pct = l_pj_snap["completed"] / l_pj_snap["target"] * 100
            c_pct = c_pj_snap["completed"] / c_pj_snap["target"] * 100
            diff  = c_pct - l_pct
            diff_s = f"+{diff:.2f}%" if diff >= 0 else f"{diff:.2f}%"
            c = Colors.GREEN if diff > 0 else Colors.ENDC
            pj_first = target_pj_name.split()[0]
            print(f"   Tim PJ {pj_first:<8}: {l_pct:.2f}% → {Colors.BOLD}{c_pct:.2f}%{Colors.ENDC} ({c}{diff_s}{Colors.ENDC})")

        # PML pending delta
        c_pmls = current_snapshot.get("pml_pending", {})
        l_pmls = latest_history.get("pml_pending", {})
        pml_diffs: list = []
        for pml, c_val in c_pmls.items():
            c_pend = c_val["pending"] if isinstance(c_val, dict) else c_val
            c_pj_v = c_val["pj"]      if isinstance(c_val, dict) else pml_to_pj.get(pml, "")
            l_val  = l_pmls.get(pml)
            if l_val is None:
                continue
            l_pend = l_val["pending"] if isinstance(l_val, dict) else l_val
            diff = c_pend - l_pend
            if diff != 0:
                pml_diffs.append((pml, c_pend, l_pend, diff, c_pj_v))

        good_pmls = sorted([(p, c, l, d, pj) for p, c, l, d, pj in pml_diffs if d < 0], key=lambda x: x[3])
        bad_pmls  = sorted([(p, c, l, d, pj) for p, c, l, d, pj in pml_diffs if d > 0], key=lambda x: -x[3])

        if good_pmls or bad_pmls:
            print(f"\n   Perubahan Antrean PML (Kinerja Verifikasi):")
            for pml, c_p, l_p, diff, pj_v in good_pmls[:5]:
                pj_lbl = f"PJ {pj_first_name(pj_v)}" if pj_v else "-"
                print(f"   👍 PML {Colors.BOLD}{pml}{Colors.ENDC} ({pj_lbl}): memeriksa {Colors.GREEN}{abs(diff)} berkas{Colors.ENDC} (pending: {l_p} → {c_p})")
            for pml, c_p, l_p, diff, pj_v in bad_pmls[:5]:
                pj_lbl = f"PJ {pj_first_name(pj_v)}" if pj_v else "-"
                print(f"   ⚠️  PML {Colors.BOLD}{pml}{Colors.ENDC} ({pj_lbl}): antrean bertambah {Colors.FAIL}+{diff} berkas{Colors.ENDC} (pending: {l_p} → {c_p})")

        # PPL completed delta
        c_ppls = current_snapshot.get("ppl_completed", {})
        l_ppls = latest_history.get("ppl_completed", {})
        for ppl, c_val in c_ppls.items():
            c_comp  = c_val["completed"] if isinstance(c_val, dict) else c_val
            c_pml_v = c_val.get("pml", "") if isinstance(c_val, dict) else ppl_to_sup.get(ppl, ("", ""))[0]
            c_pj_v  = c_val.get("pj",  "") if isinstance(c_val, dict) else ppl_to_sup.get(ppl, ("", ""))[1]
            l_val = l_ppls.get(ppl)
            if l_val is None:
                continue
            l_comp = l_val["completed"] if isinstance(l_val, dict) else l_val
            diff = c_comp - l_comp
            if diff > 0:
                ppl_diffs_r.append((ppl, c_comp, diff, c_pml_v, c_pj_v))

        ppl_diffs_r.sort(key=lambda x: -x[2])
        if ppl_diffs_r:
            print(f"\n   Kemajuan PPL Teratas:")
            for ppl, c_comp, diff, pml_v, pj_v in ppl_diffs_r[:5]:
                pj_lbl = f"PJ {pj_first_name(pj_v)}" if pj_v else "-"
                team_note = " (tim Anda)" if pj_v.lower() == target_pj_name.lower() else ""
                print(f"   🚀 PPL {Colors.BOLD}{ppl}{Colors.ENDC} (PML {pml_v}, {pj_lbl}){team_note}: +{diff} dokumen (total: {c_comp})")
    else:
        print("   (Belum ada data pengecekan sebelumnya untuk dibandingkan)")

    # ─── Section 4: Intervensi ────────────────────────────────────────────────
    print(f"\n{'─'*80}")
    print(f" 🔍 4. DAFTAR INTERVENSI TAKTIS KABUPATEN MEMPAWAH")
    print(f"{'─'*80}")

    bottleneck = sorted(
        [(n, m, pml_to_pj.get(n, "-")) for n, m in pml_metrics.items()
         if m["submitted"] > 20 and m["approval_rate"] < 0.20],
        key=lambda x: x[1]["approval_rate"],
    )
    ppl_threshold = max(0.03, (expected_pct / 100) * 0.25)
    low_ppls = sorted(
        [(n, m, ppl_to_sup.get(n, ("-", "-"))) for n, m in ppl_metrics.items()
         if m["target"] > 200 and m["completed_rate"] < ppl_threshold],
        key=lambda x: x[1]["completed_rate"],
    )

    print(f"\n   A. PML Bottleneck (Antrean Verifikasi Kritis)")
    for idx, (name, m, pj_v) in enumerate(bottleneck[:7], 1):
        pj_lbl = pj_first_name(pj_v)
        diff_note = ""
        if latest_history:
            l_v = latest_history.get("pml_pending", {}).get(name)
            if l_v is not None:
                l_p = l_v["pending"] if isinstance(l_v, dict) else l_v
                ddiff = m["submitted"] - l_p
                if ddiff != 0:
                    diff_note = f" ({'+' if ddiff > 0 else ''}{ddiff} berkas)"
        flag = f"{Colors.FAIL}*(Naik Kritis){Colors.ENDC} " if diff_note.startswith(" (+") else ""
        print(
            f"   {idx}. {Colors.BOLD}{name}{Colors.ENDC} (PJ: {pj_lbl}) → "
            f"{m['submitted']} berkas pending | Approval: {m['approval_rate']*100:.2f}% | "
            f"Tgt Approve: {m['pml_daily_target']:.1f}/hari{diff_note} {flag}"
        )

    print(f"\n   B. PPL Terlambat Terkritis (Selesai < {ppl_threshold*100:.2f}% & Target > 200)")
    print(f"   {'No':<3} {'Nama PPL':<25} {'Kec':<16} {'Target':<7} {'Worked':<20} {'Done %':<9} {'Tgt/Hari':<10} {'PML':<22} {'PJ'}")
    print(f"   {'-'*145}")
    for idx, (name, m, sup) in enumerate(low_ppls[:10], 1):
        pml_v, pj_v = sup
        worked_pct = m["worked_rate"] * 100
        worked_emoji = "🟢" if worked_pct >= expected_pct * 0.70 else ("🔴" if worked_pct < expected_pct * 0.25 else "🟡")
        sls_list = pj_kuda_groups.get(pj_v, {}).get(pml_v, {}).get(name, [])
        kecs = sorted(list(set(
            sls_info[s].get("kecamatan", "") for s in sls_list if s in sls_info
        )))
        kec_str = "/".join(kecs) if kecs else "-"
        # Format worked text (strip ANSI for width calc)
        worked_raw = f"{worked_emoji} {m['worked']} ({worked_pct:.1f}%)"
        worked_padded = f"{worked_raw:<20}"
        done_pct = m['completed_rate'] * 100
        print(
            f"   {idx:<3} {name:<25} {kec_str:<16} {m['target']:<7} {worked_padded} "
            f"{Colors.FAIL}🔴 {done_pct:>5.2f}%{Colors.ENDC}   "
            f"{m['ppl_daily_target']:>6.1f}/hari  {pml_v:<22} {pj_first_name(pj_v)}"
        )

    # ─── Section 5: Rekomendasi Ketua ─────────────────────────────────────────
    print(f"\n{'─'*80}")
    print(f" 📋 5. REKOMENDASI TAKTIS UNTUK KETUA SE-2026 BPS KAB. MEMPAWAH")
    print(f"{'─'*80}")

    rec = 1
    if bottleneck:
        worst2    = bottleneck[:2]
        names_str = " & ".join(f"{n} (PJ {pj_first_name(pj_v)})" for n, _, pj_v in worst2)
        pend_str  = " & ".join(f"{m['submitted']} pending (Tgt: {m['pml_daily_target']:.1f}/hari)" for _, m, _ in worst2)
        print(
            f"   {rec}. Tegur PML {names_str}: {pend_str} namun approval rate < 5%. "
            "Hubungi PJ-Kuda masing-masing untuk mendesak pembersihan antrean siang ini."
        )
        rec += 1

    if latest_history and good_pmls:
        names_str = ", ".join(f"{n} (PJ {pj_first_name(pj_v)})" for n, _, _, _, pj_v in good_pmls[:3])
        print(f"   {rec}. Apresiasi untuk PML {names_str}: PML ini terbukti responsif membersihkan antrean.")
        rec += 1

    if low_ppls:
        ppl_name, ppl_m, ppl_sup = low_ppls[0]
        pml_v, pj_v = ppl_sup
        print(
            f"   {rec}. PPL terlambat kritis: {Colors.BOLD}{ppl_name}{Colors.ENDC} "
            f"(PML {pml_v}, PJ {pj_first_name(pj_v)}) baru {ppl_m['completed_rate']*100:.2f}% selesai "
            f"(harus submit {Colors.BOLD}{ppl_m['ppl_daily_target']:.1f}/hari{Colors.ENDC}). "
            "Minta PML turun lapangan mendampingi."
        )
        rec += 1

    # ─── Section 6: Rekomendasi PJ ────────────────────────────────────────────
    print(f"\n{'─'*80}")
    pj_first = target_pj_name.split()[0]
    print(f" 💡 6. REKOMENDASI AKSI CEPAT PJ-KUDA (Tim {pj_first})")
    print(f"{'─'*80}")

    my_pmls = pj_kuda_groups.get(target_pj_name, {})
    rec2 = 1

    for pml_name, ppls in my_pmls.items():
        pml_sls = [sls for sls_list in ppls.values() for sls in sls_list]
        pml_m   = aggregate_fn(pml_sls)
        if pml_m["submitted"] > 50 and pml_m["approval_rate"] < 0.5:
            delta_note = ""
            if latest_history:
                l_v = latest_history.get("pml_pending", {}).get(pml_name)
                if l_v is not None:
                    l_p3 = l_v["pending"] if isinstance(l_v, dict) else l_v
                    dd   = pml_m["submitted"] - l_p3
                    if dd != 0:
                        delta_note = f", naik {'+' if dd > 0 else ''}{dd} dari pengecekan terakhir"
            print(
                f"   {rec2}. PML {Colors.BOLD}{pml_name}{Colors.ENDC}: "
                f"{pml_m['submitted']} berkas pending "
                f"(Approval: {pml_m['approval_rate']*100:.2f}%, Tgt Approve: {pml_m['pml_daily_target']:.1f}/hari{delta_note}). "
                f"Segera hubungi {pml_name} untuk mempercepat verifikasi."
            )
            rec2 += 1

    ppl_warn_threshold = max(0.05, (expected_pct / 100) * 0.50)
    my_low_ppls = sorted(
        [(ppl_name, ppl_metrics[ppl_name])
         for pml_name, ppls in my_pmls.items()
         for ppl_name in ppls
         if ppl_name in ppl_metrics
         and ppl_metrics[ppl_name]["target"] > 100
         and ppl_metrics[ppl_name]["completed_rate"] < ppl_warn_threshold],
        key=lambda x: x[1]["completed_rate"],
    )
    for ppl_name, ppl_m in my_low_ppls[:3]:
        pml_v = ppl_to_sup.get(ppl_name, ("-", "-"))[0]
        print(
            f"   {rec2}. PPL {Colors.BOLD}{ppl_name}{Colors.ENDC} (PML {pml_v}): "
            f"baru {ppl_m['completed_rate']*100:.2f}% selesai (harus submit {ppl_m['ppl_daily_target']:.1f}/hari). "
            "Beri semangat atau tanya kendala lapangan."
        )
        rec2 += 1

    if rec2 == 1:
        print(f"   {Colors.GREEN}✔ Semua PML tim berjalan dalam batas normal pagi ini.{Colors.ENDC}")

    print(f"\n{'='*80}\n")
