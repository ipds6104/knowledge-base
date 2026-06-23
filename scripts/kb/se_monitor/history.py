"""kb/se_monitor/history.py — Manajemen snapshot monitoring_history.json."""

import json
from datetime import datetime
from pathlib import Path

from ..colors import Colors

HISTORY_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/monitoring_history.json")
MAX_HISTORY  = 100


def load_history(path: Path = HISTORY_PATH) -> list:
    """Baca riwayat snapshot dari file JSON. Kembalikan list kosong jika gagal."""
    if path.exists():
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                return json.load(fh)
        except Exception as he:
            print(f"{Colors.WARNING}Peringatan: Gagal membaca riwayat ({he}){Colors.ENDC}")
    return []


def save_history(history_list: list, path: Path = HISTORY_PATH) -> None:
    """Simpan riwayat snapshot ke file JSON."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(history_list, fh, indent=2, ensure_ascii=False)
    except Exception as se:
        print(f"{Colors.WARNING}Peringatan: Gagal menyimpan riwayat ({se}){Colors.ENDC}")


def build_snapshot(
    prov_agg: dict,
    kab_data: dict,
    pj_summaries: list,
    pj_kuda_groups: dict,
    aggregate_fn,          # callable: aggregate_metrics(sls_list) -> dict
) -> dict:
    """Bangun snapshot saat ini dari data yang sudah diagregasi.

    PJ dan PML info dalam snapshot WAJIB berasal dari pj_kuda_groups
    (yang sudah dibangun dari Alokasi Petugas.csv oleh hierarchy.py).
    """
    snapshot = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prov": {
            "completed": prov_agg["completed"],
            "worked":    prov_agg["worked"],
            "target":    prov_agg["target"],
            "approved":  prov_agg["approved"],
            "submitted": prov_agg["submitted"],
        },
        "kab": {},
    }

    for kab, m in kab_data.items():
        snapshot["kab"][kab] = {
            "completed": m["completed"],
            "worked":    m["worked"],
            "target":    m["target"],
            "approved":  m["approved"],
            "submitted": m["submitted"],
        }

    if pj_summaries:
        snapshot["pj"] = {}
        for p in pj_summaries:
            snapshot["pj"][p["pj"]] = {
                "completed": p["completed"],
                "worked":    p["worked"],
                "target":    p["target"],
                "approved":  p["approved"],
                "submitted": p["submitted"],
            }

        snapshot["pml_pending"]   = {}
        snapshot["ppl_completed"] = {}

        for pj_name, pmls in pj_kuda_groups.items():
            for pml_name, ppls in pmls.items():
                pml_sls = []
                for ppl_name, sls_list in ppls.items():
                    ppl_agg = aggregate_fn(sls_list)
                    # PML & PJ sourced from hierarchy (epistemologically valid)
                    snapshot["ppl_completed"][ppl_name] = {
                        "completed": ppl_agg["completed"],
                        "pml": pml_name,
                        "pj":  pj_name,
                    }
                    pml_sls.extend(sls_list)
                pml_agg = aggregate_fn(pml_sls)
                snapshot["pml_pending"][pml_name] = {
                    "pending": pml_agg["submitted"],
                    "pj":      pj_name,
                }

    return snapshot


def should_save(current: dict, latest: dict | None) -> bool:
    """Cek apakah ada perubahan data yang perlu disimpan."""
    if not latest:
        return True
    l_prov = latest.get("prov", {})
    c_prov = current["prov"]
    if (l_prov.get("completed") == c_prov["completed"]
            and l_prov.get("worked") == c_prov["worked"]):
        l_pml = latest.get("pml_pending", {})
        c_pml = current.get("pml_pending", {})
        if l_pml == c_pml:
            return False
    return True


def update_history(history_list: list, snapshot: dict) -> list:
    """Tambahkan snapshot ke history dan trim ke MAX_HISTORY entri terakhir."""
    history_list.append(snapshot)
    if len(history_list) > MAX_HISTORY:
        history_list = history_list[-MAX_HISTORY:]
    return history_list
