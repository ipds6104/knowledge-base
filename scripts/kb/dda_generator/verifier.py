"""Deterministic PDF Verification Module for BPS Desa Dalam Angka (DDA).

Extracts and deterministically validates statistical metrics from the compiled PDF
against the live Google Sheet / AppSheet data ground truth.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        pymupdf = None

from .config import get_desa_config
from .fetcher import fetch_desa_data
from .calculator import calculate_desa_metrics, build_capabilities_dto


def parse_indonesian_number(val_str: str) -> Optional[float]:
    """Mengonversi format angka lokal Indonesia (1.234,56 / 3.074 / 104,25) ke float/int."""
    if not val_str or val_str.strip() in ("-", "", "None", "null"):
        return None
    cleaned = val_str.strip().replace(".", "").replace(",", ".")
    try:
        val = float(cleaned)
        return int(val) if val.is_integer() else val
    except ValueError:
        return None


def extract_keystats_from_pdf(pdf_path: str) -> Tuple[Optional[int], List[Dict[str, Any]]]:
    """Mengekstrak baris tabel Statistik Kunci (Tabel 0.1) dari berkas PDF.
    
    Returns:
        (page_number_1_indexed, list_of_row_dicts)
    """
    if pymupdf is None:
        raise RuntimeError("Library pymupdf tidak terpasang. Jalankan 'pip install pymupdf'.")

    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"Berkas PDF tidak ditemukan: {pdf_path}")

    doc = pymupdf.open(str(pdf_file))
    keystat_page_idx = None

    for i, page in enumerate(doc):
        txt = page.get_text()
        if "Tabel 0.1" in txt or "Table Key Statistics" in txt:
            keystat_page_idx = i
            break

    if keystat_page_idx is None:
        return None, []

    page = doc[keystat_page_idx]
    lines = [l.strip() for l in page.get_text().split("\n") if l.strip()]

    try:
        start_idx = lines.index("(3)") + 1
    except ValueError:
        start_idx = 0

    end_idx = len(lines)
    for i in range(start_idx, len(lines)):
        if lines[i].startswith("Catatan") or lines[i].startswith("Sumber"):
            end_idx = i
            break

    table_lines = lines[start_idx:end_idx]
    section_headers = [
        "DEMOGRAFI DAN KEPENDUDUKAN / DEMOGRAPHICS AND POPULATION",
        "KETENAGAKERJAAN, UMKM & SOSIAL / EMPLOYMENT, MSME & SOCIAL",
        "SOSIAL DAN KESEJAHTERAAN / SOCIAL AND WELFARE",
        "PERUMAHAN DAN LINGKUNGAN / HOUSING AND ENVIRONMENT",
    ]
    tokens = [l for l in table_lines if l not in section_headers]

    rows = []
    i = 0
    while i < len(tokens):
        label = tokens[i]
        i += 1
        unit_parts = []
        val_str = ""

        # Kasus khusus unit '-' seperti Sex Ratio
        if i < len(tokens) and tokens[i] == "-":
            unit = "-"
            i += 1
            if i < len(tokens):
                val_str = tokens[i]
                i += 1
        else:
            while i < len(tokens):
                tok = tokens[i]
                if tok == "%":
                    unit_parts.append(tok)
                    i += 1
                elif re.match(r"^[0-9]+([.,][0-9]+)*$", tok) or tok == "-":
                    val_str = tok
                    i += 1
                    break
                else:
                    unit_parts.append(tok)
                    i += 1
            unit = " ".join(unit_parts)

        rows.append({
            "label": label,
            "unit": unit,
            "raw_value": val_str,
            "parsed_value": parse_indonesian_number(val_str),
        })

    return keystat_page_idx + 1, rows


def extract_structural_info(pdf_path: str) -> Dict[str, Any]:
    """Mengekstrak informasi struktur dan tata naskah publikasi dari PDF."""
    if pymupdf is None:
        raise RuntimeError("Library pymupdf tidak terpasang.")

    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)

    has_cover = False
    has_preface = False
    has_toc = False
    has_tech_notes = False
    has_abbreviations = False
    chapter_pages = {}

    for i, page in enumerate(doc):
        txt = page.get_text()
        page_num = i + 1
        if i == 0 and "DALAM ANGKA" in txt.upper():
            has_cover = True
        if "KATA PENGANTAR" in txt.upper():
            has_preface = True
        if "DAFTAR ISI" in txt.upper():
            has_toc = True
        if "PENJELASAN UMUM" in txt.upper() or "EXPLANATORY NOTES" in txt.upper():
            has_tech_notes = True
        if "DAFTAR SINGKATAN" in txt.upper() or "LIST OF ABBREVIATIONS" in txt.upper():
            has_abbreviations = True
        
        for ch_num in range(1, 6):
            if f"BAB {ch_num}" in txt.upper() or f"CHAPTER {ch_num}" in txt.upper():
                if ch_num not in chapter_pages:
                    chapter_pages[ch_num] = page_num

    return {
        "total_pages": total_pages,
        "has_cover": has_cover,
        "has_preface": has_preface,
        "has_toc": has_toc,
        "has_tech_notes": has_tech_notes,
        "has_abbreviations": has_abbreviations,
        "chapter_pages": chapter_pages,
    }


def map_expected_metrics(metrics: dict, caps: Any) -> Dict[str, Tuple[str, Any]]:
    """Memetakan metrik hasil kalkulasi ke rincian baris Tabel 0.1 berdasarkan kapabilitas."""
    expected = {
        "Penduduk / Population": ("tot_pop", metrics.get("tot_pop")),
        "Laki-laki / Male": ("tot_l", metrics.get("tot_l")),
        "Perempuan / Female": ("tot_p", metrics.get("tot_p")),
        "Rasio Jenis Kelamin / Sex Ratio": ("tot_sr", round(metrics.get("tot_sr", 0.0), 2) if metrics.get("tot_sr") is not None else None),
        "Kepala Keluarga / Households": ("tot_kk", metrics.get("tot_kk")),
    }

    if caps.has_employment:
        expected.update({
            "Usia Kerja Bekerja / Employed Working Age": ("tot_bekerja", metrics.get("tot_bekerja")),
            "Rumah Tangga UMKM / MSME Households": ("tot_umkm", metrics.get("tot_umkm")),
            "Peserta BPJS Kesehatan / BPJS Health Participants": ("tot_bpjs", metrics.get("tot_bpjs")),
            "Keluarga Penerima Bansos (PKH/BPNT) / Assistance Recipients": ("tot_bansos", metrics.get("tot_bansos")),
            "Bumbung Rumah (Hunian) / Residential Buildings": ("tot_bumbung", metrics.get("tot_bumbung")),
            "Kepadatan Hunian Rata-rata / Housing Density": ("tot_kepadatan", round(metrics.get("tot_kepadatan", 0.0), 2) if metrics.get("tot_kepadatan") is not None else None),
            "Sanitasi BAB Sendiri / Private Toilet Sanitation": ("tot_bab_sendiri", metrics.get("tot_bab_sendiri")),
        })
    elif caps.has_building_materials:
        expected.update({
            "Keluarga Penerima Bansos (PKH/BPNT/BLT) / Assistance Recipients": ("tot_bansos", metrics.get("tot_bansos")),
            "Penerima BPJS PBI / BPJS PBI Insurance Recipients": ("tot_bpjs", None),  # Non-PBI / strip
            "Bumbung Rumah (Hunian) / Residential Buildings": ("tot_bumbung", metrics.get("tot_bumbung")),
            "Rumah Layak Huni / Decent Housing": ("tot_layak", metrics.get("tot_layak")),
            "Persentase Rumah Layak Huni / Decent Housing Rate": ("tot_layak_pct", round(metrics.get("tot_layak_pct", 0.0), 2) if metrics.get("tot_layak_pct") is not None else None),
        })
    else:
        expected.update({
            "Memiliki KTP-el / ID Card Owners": ("tot_ktp", metrics.get("tot_ktp")),
            "Persentase KTP-el / ID Card Ownership Rate": ("tot_ktp_pct", round(metrics.get("tot_ktp_pct", 0.0), 2) if metrics.get("tot_ktp_pct") is not None else None),
            "Keluarga Penerima Bansos (PKH/BPNT/BLT) / Assistance Recipients": ("tot_bansos", metrics.get("tot_bansos")),
            "Bumbung Rumah (Hunian) / Residential Buildings": ("tot_bumbung", metrics.get("tot_bumbung")),
            "Kepadatan Hunian Rata-rata / Housing Density": ("tot_kepadatan", round(metrics.get("tot_kepadatan", 0.0), 2) if metrics.get("tot_kepadatan") is not None else None),
        })

    return expected


def verify_desa_publication(
    name_kebab: str,
    pdf_path: Optional[str] = None,
    sheet_id: Optional[str] = None,
    year: int = 2026,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Melakukan verifikasi deterministik penuh atas angka-angka publikasi PDF terhadap Google Sheet live."""
    config = get_desa_config(name_kebab, sheet_id=sheet_id, year=year)

    if pdf_path is None:
        prefix = "publikasi-kelurahan" if config.get("is_kelurahan") else "publikasi-desa"
        pdf_path = f"kegiatan/desa-cantik/{year}/{config['name_kebab']}/{prefix}-{config['name_kebab']}-dalam-angka-{year}.pdf"

    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        # Coba cek di outputs/
        alt_path = Path("outputs") / pdf_file.name
        if alt_path.exists():
            pdf_file = alt_path
        else:
            raise FileNotFoundError(f"PDF publikasi tidak ditemukan di {pdf_path} atau {alt_path}")

    # Ingest & Calculate Ground Truth
    rt_data, fas_data = fetch_desa_data(config)
    if not rt_data:
        raise RuntimeError("Gagal memuat dataset RT dari Google Sheet / cache lokal.")

    metrics = calculate_desa_metrics(rt_data, fas_raw_list=fas_data, pub_config=config)
    caps = build_capabilities_dto(metrics, config=config)

    # Extract Key Stats & Structural Data from PDF
    keystat_page, extracted_rows = extract_keystats_from_pdf(str(pdf_file))
    structural_info = extract_structural_info(str(pdf_file))

    # Match items
    expected_map = map_expected_metrics(metrics, caps)
    actual_map = {r["label"]: r for r in extracted_rows}

    checks = []
    all_matched = True

    for label, (metric_key, exp_val) in expected_map.items():
        actual_entry = actual_map.get(label)
        if not actual_entry:
            # Fuzzy match label prefix
            for k, v in actual_map.items():
                if label.split("/")[0].strip().lower() == k.split("/")[0].strip().lower():
                    actual_entry = v
                    break

        if actual_entry:
            act_val = actual_entry["parsed_value"]
            act_raw = actual_entry["raw_value"]
            unit = actual_entry["unit"]
        else:
            act_val = None
            act_raw = "NOT_FOUND"
            unit = "-"

        # Bandingkan nilai (toleransi float 0.01)
        matched = False
        if exp_val is None and (act_val is None or act_raw in ("-", "")):
            matched = True
        elif exp_val is not None and act_val is not None:
            if isinstance(exp_val, float) or isinstance(act_val, float):
                matched = abs(float(exp_val) - float(act_val)) < 0.02
            else:
                matched = int(exp_val) == int(act_val)

        if not matched:
            all_matched = False

        checks.append({
            "label": label,
            "metric_key": metric_key,
            "unit": unit,
            "expected": exp_val,
            "actual_raw": act_raw,
            "actual_parsed": act_val,
            "matched": matched,
        })

    passed_count = sum(1 for c in checks if c["matched"])
    failed_count = len(checks) - passed_count

    result = {
        "village": config["name_title"],
        "name_kebab": config["name_kebab"],
        "pdf_path": str(pdf_file),
        "total_pages": structural_info["total_pages"],
        "keystat_page": keystat_page,
        "structural_info": structural_info,
        "total_checks": len(checks),
        "passed_checks": passed_count,
        "failed_checks": failed_count,
        "all_matched": all_matched,
        "checks": checks,
    }

    if verbose:
        print_verification_report(result)

    return result


def print_verification_report(result: Dict[str, Any]):
    """Menampilkan laporan verifikasi deterministik ke terminal."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    v_name = result["village"]
    pdf_path = result["pdf_path"]
    tot_p = result["total_pages"]
    ks_page = result["keystat_page"]

    print("\n" + "=" * 80)
    print(f" {BOLD}LAPORAN VERIFIKASI DETERMINISTIK PUBLIKASI PDF — {v_name.upper()}{RESET}")
    print("=" * 80)
    print(f"📄 Berkas PDF    : {pdf_path}")
    print(f"📖 Total Halaman : {tot_p} halaman")
    print(f"📌 Statistik Kunci: Halaman {ks_page} (Arab 1)")
    print("-" * 80)
    print(f"{'No':<3} | {'Rincian Indikator':<38} | {'Expected (Sheet)':<16} | {'Actual (PDF)':<12} | {'Status'}")
    print("-" * 80)

    for idx, c in enumerate(result["checks"], 1):
        status_str = f"{GREEN}✅ MATCH{RESET}" if c["matched"] else f"{RED}❌ MISMATCH{RESET}"
        exp_str = str(c["expected"]) if c["expected"] is not None else "-"
        act_str = str(c["actual_raw"])
        label_disp = c["label"].split("/")[0].strip()[:36]

        print(f"{idx:<3} | {label_disp:<38} | {exp_str:<16} | {act_str:<12} | {status_str}")

    print("-" * 80)
    if result["all_matched"]:
        print(f"{GREEN}{BOLD}🎉 SEMUA ANGKA STATISTIK KUNCI 100% SESUAI & VALID DENGAN DATA GOOGLE SHEET!{RESET}")
    else:
        print(f"{RED}{BOLD}⚠️ TERDAPAT {result['failed_checks']} ANGKA YANG TIDAK SESUAI ANTARA PDF DAN DATASET!{RESET}")
    print("=" * 80 + "\n")
