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

ALOKASI_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1JNwyb7TsPmSsGl3o1zNTSc-3wzFwIr_t3HPz_a1CVVQ/"
    "export?format=csv&gid=191266181"
)
ALOKASI_CACHE_PATH = Path("kegiatan/sensus-ekonomi-2026/2026/Alokasi Petugas.csv")

START_DATE  = datetime.strptime("2026-06-15", "%Y-%m-%d").date()
TARGET_DATE = datetime.strptime("2026-08-15", "%Y-%m-%d").date()
SOFT_DEADLINE = datetime.strptime("2026-08-31", "%Y-%m-%d").date()


# ─── Download & Parse ─────────────────────────────────────────────────────────

def download_alokasi(
    url: str = ALOKASI_URL,
    cache_path: Path = ALOKASI_CACHE_PATH,
) -> bool:
    """Unduh data alokasi petugas terbaru dari Google Sheets."""
    try:
        print(f"{Colors.BLUE}Mengunduh alokasi petugas terbaru dari Google Sheets...{Colors.ENDC}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            csv_text = response.read().decode('utf-8-sig')

        # Verifikasi kolom penting sebelum menulis
        reader = csv.reader(io.StringIO(csv_text))
        header = next(reader)
        required = ['idsls', 'idsubsls', 'Pj-Kuda', 'PML', 'PPL', 'nmsls']
        missing = [col for col in required if col not in header]
        if missing:
            print(f"{Colors.FAIL}Error: Berkas alokasi di spreadsheet kekurangan kolom wajib: {missing}{Colors.ENDC}")
            return False

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(csv_text, encoding='utf-8')

        # Arsip harian
        archive_dir = cache_path.parent / "archive" / datetime.now().strftime("%Y-%m-%d")
        archive_dir.mkdir(parents=True, exist_ok=True)
        (archive_dir / cache_path.name).write_text(csv_text, encoding='utf-8')
        print(f"{Colors.GREEN}Sukses memperbarui berkas alokasi petugas.{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.WARNING}Peringatan: Gagal memperbarui alokasi petugas dari Google Sheets ({e}). Menggunakan cache lokal.{Colors.ENDC}")
        return False


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
        with urllib.request.urlopen(req, timeout=30) as response:
            csv_text = response.read().decode('utf-8')

        sheet_map = _parse_sheet_csv(csv_text)

        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(csv_text, encoding='utf-8')
            
            # Arsip harian
            archive_dir = cache_path.parent / "archive" / datetime.now().strftime("%Y-%m-%d")
            archive_dir.mkdir(parents=True, exist_ok=True)
            (archive_dir / cache_path.name).write_text(csv_text, encoding='utf-8')
            
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


def get_csv_reader(csv_text: str) -> csv.DictReader:
    """Helper untuk mendapatkan DictReader, otomatis mengisi fieldnames jika header hilang."""
    lines = csv_text.splitlines()
    if not lines:
        return csv.DictReader(io.StringIO(csv_text))
    
    first_line = lines[0]
    is_header = "Kode Wilayah" in first_line or "Kab/Kota" in first_line
    
    if is_header:
        return csv.DictReader(io.StringIO(csv_text))
    else:
        fieldnames = [
            "No", "Kab/Kota", "Kode Wilayah (Sub-SLS)", "Username Petugas", "Email Petugas", "Role",
            "Total Target", "DRAFT", "OPEN", "SUBMITTED RESPONDENT", "SUBMITTED BY Pencacah",
            "APPROVED BY Pengawas", "REJECTED BY Pengawas", "REVOKED BY Pengawas", 
            "COMPLETED BY Admin Kabupaten", "EDITED BY Admin Kabupaten", "EDITED BY Pengawas", 
            "REJECTED BY Admin Kabupaten", "REVOKED BY Admin Kabupaten", "Total Submit PPL",
            "Total Submit Seluruh SLS per Petugas", "empty_col5", "Target", "Persentase_Done",
            "empty_col6", "empty_col7", "Ranking", "Status Target"
        ]
        return csv.DictReader(io.StringIO(csv_text), fieldnames=fieldnames)


def is_status_col(col_name: str) -> bool:
    """Cek apakah nama kolom merupakan kolom status pendataan FASIH."""
    c = col_name.upper()
    keywords = {"DRAFT", "OPEN", "SUBMITTED", "APPROVED", "REJECTED", "REVOKED", "EDITED", "COMPLETED"}
    return any(kw in c for kw in keywords)


def is_approved_status(col_name: str) -> bool:
    """Cek apakah nama kolom status merupakan berkas yang disetujui (Approved)."""
    c = col_name.upper()
    return "APPROVED" in c or "COMPLETED BY" in c or "EDITED BY ADMIN" in c


def _parse_sheet_csv(csv_text: str) -> dict:
    """Parse raw CSV Google Sheets menjadi sheet_map {kode: {field: int}} secara dinamis."""
    sheet_map: dict = {}
    reader = get_csv_reader(csv_text)
    
    # Identifikasi kolom status secara dinamis
    ignore_cols = {
        "No", "Kab/Kota", "Kode Wilayah (Sub-SLS)", "Username Petugas", "Email Petugas", "Role",
        "Total Target", "Total Submit PPL", "Total Submit Seluruh SLS per Petugas", "Target",
        "Persentase_Done", "Ranking", "Status Target"
    }
    fieldnames = reader.fieldnames or []
    status_cols = [
        col for col in fieldnames 
        if col and col not in ignore_cols and not col.startswith("empty_") and is_status_col(col)
    ]
    
    for row in reader:
        code = row.get("Kode Wilayah (Sub-SLS)", "").strip()
        if not code or code == "Kode Wilayah (Sub-SLS)":
            continue
            
        raw_statuses = {}
        for col in status_cols:
            raw_statuses[col] = int(row.get(col, 0) or 0)
            
        entry = {
            "Total Target": int(row.get("Total Target", 0) or 0),
            "raw_statuses": raw_statuses
        }
        
        # Sediakan mapping flat di root untuk backward-compatibility
        for col, val in raw_statuses.items():
            entry[col] = val
            
        sheet_map[code] = entry
    return sheet_map


# ─── Metrik SLS & Agregasi ────────────────────────────────────────────────────

def get_sls_metrics(sheet_map: dict, idsls: str, idsubsls: str) -> dict:
    """Ambil metrik untuk satu SLS dari sheet_map secara dinamis."""
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
            "revoked": 0, "edited": 0, "completed": 0, "worked": 0,
            "comp_admin": 0, "edit_admin": 0, "rej_admin": 0, "rev_admin": 0,
        }

    raw_statuses = row.get("raw_statuses")
    if raw_statuses is None:
        ignore_keys = {"Total Target", "open", "worked", "completed", "target"}
        raw_statuses = {
            k: v for k, v in row.items() 
            if k not in ignore_keys and isinstance(v, (int, float))
        }

    submitted = raw_statuses.get("SUBMITTED BY Pencacah", 0)
    approved_orig = raw_statuses.get("APPROVED BY Pengawas", 0)
    resp_sub  = raw_statuses.get("SUBMITTED RESPONDENT", 0)
    draft     = raw_statuses.get("DRAFT", 0)
    rejected  = raw_statuses.get("REJECTED BY Pengawas", 0)
    revoked   = raw_statuses.get("REVOKED BY Pengawas", 0)
    edited    = raw_statuses.get("EDITED BY Pengawas", 0)
    comp_admin = raw_statuses.get("COMPLETED BY Admin Kabupaten", 0)
    edit_admin = raw_statuses.get("EDITED BY Admin Kabupaten", 0)
    rej_admin  = raw_statuses.get("REJECTED BY Admin Kabupaten", 0)
    rev_admin  = raw_statuses.get("REVOKED BY Admin Kabupaten", 0)

    completed = sum(val for col, val in raw_statuses.items() if col.upper() not in {"DRAFT", "OPEN"})
    worked    = completed + draft
    approved  = sum(val for col, val in raw_statuses.items() if is_approved_status(col))

    return {
        "target":        row.get("Total Target", 0),
        "open":          raw_statuses.get("OPEN", 0),
        "draft":         draft,
        "submitted":     submitted,
        "approved":      approved,
        "resp_submitted": resp_sub,
        "rejected":      rejected,
        "revoked":       revoked,
        "edited":        edited,
        "completed":     completed,
        "worked":        worked,
        "comp_admin":    comp_admin,
        "edit_admin":    edit_admin,
        "rej_admin":     rej_admin,
        "rev_admin":     rev_admin,
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
    
    rem_days = get_remaining_days()
    agg["ppl_daily_target"] = max(0.0, (agg["target"] - agg["completed"]) / rem_days)
    agg["pml_daily_target"] = max(0.0, (agg["target"] - agg["approved"]) / rem_days)
    return agg


# ─── Kalbar Provinsi Aggregation ─────────────────────────────────────────────

def compute_kab_stats(csv_text: str) -> tuple[dict, list, dict]:
    """Hitung statistik per Kabupaten/Kota dari csv_text (baris-baris Realisasi) secara dinamis.

    Returns:
        kab_data:  {kab_name: {target, completed, worked, approved, submitted, ...}}
        kab_list:  sorted list of (kab_name, metrics) by completed_rate desc
        prov_agg:  aggregated province metrics dict
    """
    kab_data: dict = {}
    reader = get_csv_reader(csv_text)
    
    ignore_cols = {
        "No", "Kab/Kota", "Kode Wilayah (Sub-SLS)", "Username Petugas", "Email Petugas", "Role",
        "Total Target", "Total Submit PPL", "Total Submit Seluruh SLS per Petugas", "Target",
        "Persentase_Done", "Ranking", "Status Target"
    }
    fieldnames = reader.fieldnames or []
    status_cols = [
        col for col in fieldnames 
        if col and col not in ignore_cols and not col.startswith("empty_") and is_status_col(col)
    ]

    for row in reader:
        kab = row.get("Kab/Kota", "").strip()
        if not kab or kab == "Kab/Kota":
            continue
            
        target = int(row.get("Total Target", 0) or 0)
        
        raw_statuses = {}
        for col in status_cols:
            raw_statuses[col] = int(row.get(col, 0) or 0)

        draft     = raw_statuses.get("DRAFT", 0)
        submitted = raw_statuses.get("SUBMITTED BY Pencacah", 0)
        completed = sum(val for col, val in raw_statuses.items() if col.upper() not in {"DRAFT", "OPEN"})
        worked    = completed + draft
        approved  = sum(val for col, val in raw_statuses.items() if is_approved_status(col))

        kab_data.setdefault(kab, {
            "target": 0, "open": 0, "draft": 0, "submitted": 0,
            "approved": 0, "rejected": 0, "revoked": 0, "edited": 0,
            "completed": 0, "worked": 0,
        })
        kab_data[kab]["target"]    += target
        kab_data[kab]["draft"]     += draft
        kab_data[kab]["submitted"] += submitted
        kab_data[kab]["approved"]  += approved
        kab_data[kab]["rejected"]  += raw_statuses.get("REJECTED BY Pengawas", 0)
        kab_data[kab]["revoked"]   += raw_statuses.get("REVOKED BY Pengawas", 0)
        kab_data[kab]["edited"]    += raw_statuses.get("EDITED BY Pengawas", 0)
        kab_data[kab]["completed"] += completed
        kab_data[kab]["worked"]    += worked

    rem_days = get_remaining_days()
    kab_list = []
    for kab, m in kab_data.items():
        if m["target"] == 0:
            continue
        m["completed_rate"] = m["completed"] / m["target"]
        m["worked_rate"]    = m["worked"]    / m["target"]
        sub_app = m["approved"] + m["submitted"]
        m["approval_rate"]  = m["approved"] / sub_app if sub_app > 0 else 0.0
        m["ppl_daily_target"] = max(0.0, (m["target"] - m["completed"]) / rem_days)
        m["pml_daily_target"] = max(0.0, (m["target"] - m["approved"]) / rem_days)
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
    prov_agg["ppl_daily_target"] = max(0.0, (prov_agg["target"] - prov_agg["completed"]) / rem_days)
    prov_agg["pml_daily_target"] = max(0.0, (prov_agg["target"] - prov_agg["approved"]) / rem_days)

    return kab_data, kab_list, prov_agg


# ─── Timeline Helpers ─────────────────────────────────────────────────────────

def get_remaining_days() -> int:
    """Hitung sisa hari lapangan secara dinamis terhadap tanggal target internal 15 Agustus 2026."""
    today = datetime.now().date()
    return max(1, (TARGET_DATE - today).days)


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
