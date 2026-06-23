"""kb/se_monitor/data.py — Download Google Sheets, parsing, dan agregasi metrik."""

import csv
import io
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

from ..colors import Colors

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1JNwyb7TsPmSsGl3o1zNTSc-3wzFwIr_t3HPz_a1CVVQ/"
    "export?format=csv&gid=1834012774"
)
CACHE_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/Realisasi - 6104.csv")

START_DATE  = datetime.strptime("2026-06-15", "%Y-%m-%d").date()
TARGET_DATE = datetime.strptime("2026-08-15", "%Y-%m-%d").date()
SOFT_DEADLINE = datetime.strptime("2026-08-31", "%Y-%m-%d").date()


# ─── Download & Parse ─────────────────────────────────────────────────────────

def download_sheet(
    url: str = SHEET_URL,
    cache_path: Path = CACHE_PATH,
) -> tuple[dict, str, str]:
    """Unduh data dari Google Sheets atau fallback ke cache lokal.

    Returns:
        sheet_map:       {kode_subsls: {field: value}}
        csv_text:        raw CSV string (digunakan untuk agregasi provinsi)
        data_source_info: deskripsi sumber data
    """
    sheet_map: dict = {}
    csv_text = ""
    data_source_info = ""

    try:
        print(f"{Colors.BLUE}Mengunduh progres terbaru dari Google Sheets...{Colors.ENDC}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            csv_text = response.read().decode('utf-8')

        sheet_map = _parse_sheet_csv(csv_text)

        try:
            cache_path.write_text(csv_text, encoding='utf-8')
            data_source_info = "Google Sheets (Real-time)"
        except Exception as cache_err:
            print(
                f"{Colors.WARNING}Peringatan: Gagal menyimpan cache lokal: "
                f"{cache_err}{Colors.ENDC}"
            )
            data_source_info = "Google Sheets (Real-time, Gagal Cache)"

    except Exception as e:
        print(
            f"{Colors.WARNING}Peringatan: Gagal mengunduh dari Google Sheets ({e}). "
            f"Mencoba membaca cache lokal...{Colors.ENDC}"
        )
        if cache_path.exists():
            try:
                csv_text = cache_path.read_text(encoding='utf-8')
                sheet_map = _parse_sheet_csv(csv_text)
                data_source_info = "Cache Lokal (Realisasi - 6104.csv)"
            except Exception as read_err:
                print(f"{Colors.FAIL}Error: Gagal membaca cache lokal: {read_err}{Colors.ENDC}")

        if not sheet_map:
            print(
                f"{Colors.FAIL}Error: Tidak ada data progres dari Google Sheets "
                f"maupun cache lokal.{Colors.ENDC}"
            )
            print("Pastikan komputer Anda terhubung ke internet untuk penarikan data pertama kali.")
            sys.exit(1)

    return sheet_map, csv_text, data_source_info


def _parse_sheet_csv(csv_text: str) -> dict:
    """Parse raw CSV Google Sheets menjadi sheet_map {kode: {field: int}}."""
    sheet_map: dict = {}
    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        code = row.get("Kode Wilayah (Sub-SLS)", "").strip()
        if code:
            sheet_map[code] = {
                "Total Target":             int(row.get("Total Target", 0) or 0),
                "OPEN":                     int(row.get("OPEN", 0) or 0),
                "DRAFT":                    int(row.get("DRAFT", 0) or 0),
                "SUBMITTED BY Pencacah":    int(row.get("SUBMITTED BY Pencacah", 0) or 0),
                "APPROVED BY Pengawas":     int(row.get("APPROVED BY Pengawas", 0) or 0),
                "SUBMITTED RESPONDENT":     int(row.get("SUBMITTED RESPONDENT", 0) or 0),
                "REJECTED BY Pengawas":     int(row.get("REJECTED BY Pengawas", 0) or 0),
            }
    return sheet_map


# ─── Metrik SLS & Agregasi ────────────────────────────────────────────────────

def get_sls_metrics(sheet_map: dict, idsls: str, idsubsls: str) -> dict:
    """Ambil metrik untuk satu SLS dari sheet_map."""
    row = sheet_map.get(idsubsls)
    if not row:
        for k in sheet_map:
            if k.startswith(idsls):
                row = sheet_map[k]
                break

    if not row:
        return {
            "target": 0, "open": 0, "draft": 0, "submitted": 0,
            "approved": 0, "resp_submitted": 0, "rejected": 0,
            "completed": 0, "worked": 0,
        }

    submitted = row["SUBMITTED BY Pencacah"]
    approved  = row["APPROVED BY Pengawas"]
    resp_sub  = row["SUBMITTED RESPONDENT"]
    draft     = row["DRAFT"]
    completed = submitted + approved + resp_sub
    worked    = completed + draft

    return {
        "target":        row["Total Target"],
        "open":          row["OPEN"],
        "draft":         draft,
        "submitted":     submitted,
        "approved":      approved,
        "resp_submitted": resp_sub,
        "rejected":      row["REJECTED BY Pengawas"],
        "completed":     completed,
        "worked":        worked,
    }


def aggregate_metrics(sls_list: list, sls_info: dict, sheet_map: dict) -> dict:
    """Agregasikan metrik untuk sekumpulan SLS."""
    agg = {
        "target": 0, "open": 0, "draft": 0, "submitted": 0,
        "approved": 0, "resp_submitted": 0, "rejected": 0,
        "completed": 0, "worked": 0, "sls_count": len(sls_list),
    }
    for idsls in sls_list:
        idsubsls = sls_info[idsls]["idsubsls"]
        m = get_sls_metrics(sheet_map, idsls, idsubsls)
        for k in agg:
            if k != "sls_count":
                agg[k] += m[k]

    t = agg["target"]
    agg["completed_rate"] = agg["completed"] / t if t > 0 else 0.0
    agg["worked_rate"]    = agg["worked"]    / t if t > 0 else 0.0
    sub_plus_app = agg["approved"] + agg["submitted"]
    agg["approval_rate"]  = agg["approved"] / sub_plus_app if sub_plus_app > 0 else 0.0
    return agg


# ─── Kalbar Provinsi Aggregation ─────────────────────────────────────────────

def compute_kab_stats(csv_text: str) -> tuple[dict, list, dict]:
    """Hitung statistik per Kabupaten/Kota dari csv_text (baris-baris Realisasi).

    Returns:
        kab_data:  {kab_name: {target, completed, worked, approved, submitted, ...}}
        kab_list:  sorted list of (kab_name, metrics) by completed_rate desc
        prov_agg:  aggregated province metrics dict
    """
    kab_data: dict = {}
    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        kab = row.get("Kab/Kota", "").strip()
        if not kab:
            continue
        target      = int(row.get("Total Target", 0) or 0)
        draft       = int(row.get("DRAFT", 0) or 0)
        submitted   = int(row.get("SUBMITTED BY Pencacah", 0) or 0)
        approved    = int(row.get("APPROVED BY Pengawas", 0) or 0)
        resp_sub    = int(row.get("SUBMITTED RESPONDENT", 0) or 0)
        completed   = submitted + approved + resp_sub
        worked      = completed + draft

        kab_data.setdefault(kab, {
            "target": 0, "open": 0, "draft": 0, "submitted": 0,
            "approved": 0, "completed": 0, "worked": 0,
        })
        kab_data[kab]["target"]    += target
        kab_data[kab]["draft"]     += draft
        kab_data[kab]["submitted"] += submitted
        kab_data[kab]["approved"]  += approved
        kab_data[kab]["completed"] += completed
        kab_data[kab]["worked"]    += worked

    kab_list = []
    for kab, m in kab_data.items():
        if m["target"] == 0:
            continue
        m["completed_rate"] = m["completed"] / m["target"]
        m["worked_rate"]    = m["worked"]    / m["target"]
        sub_app = m["approved"] + m["submitted"]
        m["approval_rate"]  = m["approved"] / sub_app if sub_app > 0 else 0.0
        kab_list.append((kab, m))

    kab_list.sort(key=lambda x: x[1]["completed_rate"], reverse=True)

    prov_agg = {
        "target":    sum(m["target"]    for m in kab_data.values()),
        "completed": sum(m["completed"] for m in kab_data.values()),
        "worked":    sum(m["worked"]    for m in kab_data.values()),
        "approved":  sum(m["approved"]  for m in kab_data.values()),
        "submitted": sum(m["submitted"] for m in kab_data.values()),
    }
    t = prov_agg["target"]
    prov_agg["done_rate"]     = prov_agg["completed"] / t if t > 0 else 0.0
    prov_agg["worked_rate"]   = prov_agg["worked"]    / t if t > 0 else 0.0
    sa = prov_agg["approved"] + prov_agg["submitted"]
    prov_agg["approval_rate"] = prov_agg["approved"]  / sa if sa > 0 else 0.0

    return kab_data, kab_list, prov_agg


# ─── Timeline Helpers ─────────────────────────────────────────────────────────

def compute_timeline() -> tuple[int, int, float]:
    """Hitung elapsed_days, total_days, expected_pct berdasarkan tanggal hari ini."""
    today = datetime.now().date()
    total_days   = (TARGET_DATE - START_DATE).days
    elapsed_days = (today - START_DATE).days
    bounded      = max(0, min(total_days, elapsed_days))
    expected_pct = (bounded / total_days * 100) if total_days > 0 else 100.0
    return elapsed_days, total_days, expected_pct


def get_target_status(actual_pct: float, expected_pct: float) -> str:
    """Kembalikan string status berwarna berdasarkan perbandingan aktual vs target."""
    if actual_pct >= expected_pct:
        return f"{Colors.GREEN}🟢 ON TARGET{Colors.ENDC}"
    elif actual_pct >= expected_pct - 2.0 or actual_pct >= expected_pct * 0.85:
        return f"{Colors.WARNING}🟡 WARNING (Slightly Behind){Colors.ENDC}"
    else:
        return f"{Colors.FAIL}🔴 BEHIND TARGET{Colors.ENDC}"


def get_est_completion(actual_pct: float, elapsed_days: int) -> str:
    """Estimasi tanggal selesai berdasarkan kecepatan saat ini."""
    today = datetime.now().date()
    if elapsed_days > 0 and actual_pct > 0:
        daily_speed = actual_pct / elapsed_days
        est_date    = today + timedelta(days=(100.0 - actual_pct) / daily_speed)
        date_str    = est_date.strftime("%d %b %Y")
        if est_date <= TARGET_DATE:
            color = Colors.GREEN
        elif est_date <= SOFT_DEADLINE:
            color = Colors.WARNING
        else:
            color = Colors.FAIL
        return f"{color}{date_str}{Colors.ENDC}"
    return f"{Colors.FAIL}Tidak Terprediksi (Belum Ada Progres){Colors.ENDC}"
