#!/usr/bin/env python3
"""
generate_surat_kcda.py
======================
Script otomasi pembuatan Surat Dinas Resmi BPS Kabupaten Mempawah untuk
permintaan dan konfirmasi data acuan (baseline) tabel KCDA 2026 bagi
9 kecamatan di Kabupaten Mempawah, serta pengunggahan otomatis ke Google Drive.

Revisi per instruksi Kak Sukma (17 September 2026 - Tahap 2):
1. Petunjuk pengisian diarahkan langsung ke Google Sheets (bukan di berkas cetak).
2. Shortlink resmi s.bps.go.id/kcda26-<kecamatan> per kecamatan, di-highlight biru khas URL.
3. Header lampiran surat & halaman di bagian atas dihapus.
4. Kolom 'Keterangan' pada tabel PNS dihapus.
5. Border merah hanya pada garis luar/samping (outer border) membingkai area isian,
   bukan garis tebal merah per sel (persis seperti tampilan di Google Sheets).
6. Nomor surat resmi B-1091 s.d. B-1100, narahubung mengalir (Sukma Andini 082234120921),
   tanpa tembusan, tanda tangan Kepala BPS Munawir, S.E., M.M.

Penggunaan:
    python3 scripts/generate_surat_kcda.py [--kecamatan <slug|all>] [--upload] [--share <anyone|user|none>]
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

REPO_ROOT = Path("/app/workspaces/bps-mempawah")
DATA_DIR = REPO_ROOT / "data" / "kcda-2026"
CACHE_FILE = DATA_DIR / "gsheet_cache.json"
RAW_TABLES_DIR = DATA_DIR / "raw_tables"
ASSETS_DIR = REPO_ROOT / "kegiatan" / "kecamatan-dalam-angka" / "2026" / "assets"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "kegiatan" / "kecamatan-dalam-angka" / "2026" / "outputs" / "surat"
DEFAULT_GDRIVE_FOLDER_ID = "1zBq1esGJOndJS1XMXvOVQj6UOL5-7lvr"

# Pemetaan nomor surat dinas resmi BPS Kabupaten Mempawah per kecamatan
NOMOR_SURAT_MAP = {
    "mempawah-timur": "B-1091/61046/HM.310/2026",
    "mempawah-hilir": "B-1092/61046/HM.310/2026",
    "sungai-pinyuh": "B-1093/61046/HM.310/2026",
    "sungai-kunyit": "B-1094/61046/HM.310/2026",
    "segedong": "B-1095/61046/HM.310/2026",
    "toho": "B-1097/61046/HM.310/2026",
    "jongkat": "B-1098/61046/HM.310/2026",
    "anjongan": "B-1099/61046/HM.310/2026",
    "sadaniang": "B-1100/61046/HM.310/2026",
}

# Pemetaan tautan singkat s.bps.go.id resmi per kecamatan
SHORTLINK_MAP = {
    "sadaniang": "https://s.bps.go.id/kcda26-sadaniang",
    "anjongan": "https://s.bps.go.id/kcda26-anjongan",
    "jongkat": "https://s.bps.go.id/kcda26-jongkat",
    "toho": "https://s.bps.go.id/kcda26-toho",
    "segedong": "https://s.bps.go.id/kcda26-segedong",
    "sungai-kunyit": "https://s.bps.go.id/kcda26-kunyit",
    "sungai-pinyuh": "https://s.bps.go.id/kcda26-pinyuh",
    "mempawah-hilir": "https://s.bps.go.id/kcda26-mphilir",
    "mempawah-timur": "https://s.bps.go.id/kcda26-mptimur",
}

KECAMATAN_CONFIG = {
    "mempawah-timur": {
        "nama_resmi": "Kecamatan Mempawah Timur",
        "slug": "mempawah-timur",
        "kode_wilayah": "6104051",
        "ibukota_kecamatan": "Antibar",
        "tab_name": "Mempawah Timur",
        "sheet_id": "1rIf9ZuTD2kK4BOysQ__kh_e5ZtWmopttM5GrEYrZd9g",
        "desa_list": [
            "Pasir Wan Salim", "Sungai Bakau Kecil", "Pasir Panjang", "Pasir Palembang",
            "Pulau Pedalaman", "Antibar", "Sejegi", "Parit Banjar"
        ]
    },
    "mempawah-hilir": {
        "nama_resmi": "Kecamatan Mempawah Hilir",
        "slug": "mempawah-hilir",
        "kode_wilayah": "6104050",
        "ibukota_kecamatan": "Tanjung",
        "tab_name": "Mempawah Hilir",
        "sheet_id": "1VB3k9opurqMccOdBMC4uKoP9UBiMOkzCroJEl7zriq4",
        "desa_list": [
            "Tanjung", "Kuala Secapah", "Tengah", "Terusan",
            "Pasir", "Penibung", "Sengkubang", "Malikian"
        ]
    },
    "sungai-pinyuh": {
        "nama_resmi": "Kecamatan Sungai Pinyuh",
        "slug": "sungai-pinyuh",
        "kode_wilayah": "6104040",
        "ibukota_kecamatan": "Sungai Pinyuh",
        "tab_name": "Sungai Pinyuh",
        "sheet_id": "1lEUFr2BTPtnuBPHje2MLAg4hZONO_dQE-BAGad6X9UA",
        "desa_list": [
            "Sungai Purun Kecil", "Peniraman", "Nusapati", "Galang",
            "Sungai Rasau", "Sungai Pinyuh", "Sungai Batang", "Sungai Bakau Besar Laut",
            "Sungai Bakau Besar Darat"
        ]
    },
    "sungai-kunyit": {
        "nama_resmi": "Kecamatan Sungai Kunyit",
        "slug": "sungai-kunyit",
        "kode_wilayah": "6104060",
        "ibukota_kecamatan": "Sungai Kunyit Laut",
        "tab_name": "Sungai Kunyit",
        "sheet_id": "1rj5c7TUhK1NvVDWaubXQrrr97661Hdw4Q_DHoOx7r00",
        "desa_list": [
            "Semudun", "Semparong Parit Raden", "Mendalok", "Sungai Dungun",
            "Sungai Limau", "Sungai Kunyit Laut", "Sungai Kunyit Dalam", "Sungai Kunyit Hulu",
            "Bukit Batu", "Sungai Bundung Laut", "Sungai Duri I", "Sungai Duri II"
        ]
    },
    "segedong": {
        "nama_resmi": "Kecamatan Segedong",
        "slug": "segedong",
        "kode_wilayah": "6104030",
        "ibukota_kecamatan": "Parit Bugis",
        "tab_name": "Segedong",
        "sheet_id": "1Z-1MqJtT8mIXwdWjeSiFLdso52ECJCsBBYPi-5Cd-3c",
        "desa_list": [
            "Peniti Dalam I", "Sungai Burung", "Sungai Purun Besar",
            "Parit Bugis", "Peniti Besar", "Peniti Dalam II"
        ]
    },
    "toho": {
        "nama_resmi": "Kecamatan Toho",
        "slug": "toho",
        "kode_wilayah": "6104070",
        "ibukota_kecamatan": "Toho",
        "tab_name": "Toho",
        "sheet_id": "15VShKwCXs-T5W7UmS1Cw1D3H2CAJiZLEJ3MjXOKfCbk",
        "desa_list": [
            "Sambora", "Benuang", "Pak Utan", "Sepang",
            "Pak Laheng", "Terap", "Kecurit", "Toho Ilir"
        ]
    },
    "jongkat": {
        "nama_resmi": "Kecamatan Jongkat",
        "slug": "jongkat",
        "kode_wilayah": "6104020",
        "ibukota_kecamatan": "Jungkat",
        "tab_name": "Jongkat",
        "sheet_id": "13hrB-jznRqBceBglwYZWL3tO464oPKpBmP6okwpCfLg",
        "desa_list": [
            "Sungai Nipah", "Jungkat", "Wajok Hilir", "Wajok Hulu", "Peniti Luar"
        ]
    },
    "anjongan": {
        "nama_resmi": "Kecamatan Anjongan",
        "slug": "anjongan",
        "kode_wilayah": "6104041",
        "ibukota_kecamatan": "Anjungan Melancar",
        "tab_name": "Anjongan",
        "sheet_id": "1iofOq1dSkm2F6FhKAKxRTYJH0hAyXmsJjC8briYcji0",
        "desa_list": [
            "Anjungan Melancar", "Anjungan Dalam", "Pak Bulu", "Dema", "Kepayang"
        ]
    },
    "sadaniang": {
        "nama_resmi": "Kecamatan Sadaniang",
        "slug": "sadaniang",
        "kode_wilayah": "6104080",
        "ibukota_kecamatan": "Pentek",
        "tab_name": "Sadaniang",
        "sheet_id": "1jXSyjVD121WCUhy4cU1glzFDrBlHdi68itDhvEa-IHU",
        "desa_list": [
            "Pentek", "Sekabuk", "Bum-Bun", "Amawang", "Ansiap", "Suak Barangan"
        ]
    }
}

KECAMATAN_WITH_DUSUN = {
    "mempawah-timur",
    "sungai-kunyit",
    "segedong",
    "toho",
    "jongkat",
    "anjongan",
    "sadaniang"
}

def escape_typst(val: Any) -> str:
    """Membersihkan dan meng-escape karakter khusus Typst."""
    if val is None:
        return ""
    text = str(val).strip()
    if not text:
        return ""
    text = text.replace("\r\n", " ").replace("\n", " ")
    text = text.replace("\\", "\\\\")
    for ch in ["@", "#", "$", "[", "]"]:
        text = text.replace(ch, f"\\{ch}")
    return text

def load_cached_gsheet_data() -> Dict[str, Any]:
    """Memuat data tabel hasil ekstraksi langsung dari Google Sheets."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Gagal membaca gsheet_cache.json: {e}")
    return {}

# ==============================================================================
# PEMBANGUN TABEL LAMPIRAN SESUAI GSHEET (DENGAN BORDER MERAH PADA ISIAN)
# ==============================================================================

def render_table_2_1_2(slug: str, gdata: Dict[str, Any]) -> str:
    """
    Tabel 2.1.2: Nama Camat yang Pernah dan Masih Menjabat.
    Menampilkan daftar camat acuan, dan baris isian camat baru dengan border merah di samping/luar.
    """
    rows = gdata.get(slug, {}).get("Tabel 2.1.2", [])
    
    camat_items = []
    has_camat_baru_row = False
    
    for r in rows[3:]:
        if not r or not any(r):
            continue
        no_str = r[0].strip() if len(r) > 0 else ""
        nama_str = r[1].strip() if len(r) > 1 else ""
        periode_str = r[2].strip() if len(r) > 2 else ""
        
        if "camat baru" in nama_str.lower():
            has_camat_baru_row = True
            camat_items.append((no_str or "+", nama_str, periode_str, True))
        elif nama_str:
            camat_items.append((no_str or str(len(camat_items) + 1), nama_str, periode_str, False))
            
    if not has_camat_baru_row:
        next_no = str(len(camat_items) + 1)
        camat_items.append((next_no, "Camat Baru (jika ada pergantian jabatan)", "2024 -- sekarang", True))

    total_rows = len(camat_items)
    last_row_idx = total_rows

    content = []
    content.append("#v(8pt)")
    content.append("== Tabel 1: Nama-Nama Camat yang Pernah dan Masih Menjabat")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Publikasi KCDA BPS]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (32pt, 1.9fr, 1.2fr),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, center),")
    content.append(f"""  stroke: (col, row) => {{
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let top_b = if row == 0 {{ 0.8pt + black }} else if row == {last_row_idx} {{ red_b }} else {{ norm }}
    let bot_b = if row == 0 {{ 1.2pt + black }} else if row == {last_row_idx} {{ red_b }} else {{ norm }}
    let left_b = if row == {last_row_idx} and col == 0 {{ red_b }} else {{ norm }}
    let right_b = if row == {last_row_idx} and col == 2 {{ red_b }} else {{ norm }}
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  }},""")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  table.header(")
    content.append("    [*No*], [*Nama-Nama Camat*], [*Periode Jabatan*]")
    content.append("  ),")

    for no, nama, periode, is_new in camat_items:
        if is_new:
            content.append(f"  [{escape_typst(no)}], [*Camat Baru* #text(size: 7.5pt, fill: rgb(\"#DC2626\"))[\ (Tuliskan nama camat baru di sini jika ada pergantian jabatan)]], [{escape_typst(periode)}],")
        else:
            content.append(f"  [{escape_typst(no)}], [{escape_typst(nama)}], [{escape_typst(periode)}],")

    content.append(")")
    return "\n".join(content)

def render_table_2_1_3(slug: str, gdata: Dict[str, Any]) -> str:
    """
    Tabel 2.1.3: Nama-Nama Kepala Desa / Lurah.
    Kolom ke-4 adalah isian kondisi 2026/terkini dengan garis tepi merah di sekeliling kolom.
    """
    rows = gdata.get(slug, {}).get("Tabel 2.1.3", [])
    
    kades_items = []
    for r in rows[3:]:
        if not r or not any(r):
            continue
        no_str = r[0].strip() if len(r) > 0 else ""
        desa_str = r[1].strip() if len(r) > 1 else ""
        kades_acuan = r[2].strip() if len(r) > 2 else "-"
        if desa_str:
            kades_items.append((no_str or str(len(kades_items) + 1), desa_str, kades_acuan))

    last_row_idx = len(kades_items)

    content = []
    content.append("#v(8pt)")
    content.append("== Tabel 2: Nama-Nama Kepala Desa / Lurah")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Pemerintah Desa]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (30pt, 1.2fr, 1.4fr, 1.5fr),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, left, left),")
    content.append(f"""  stroke: (col, row) => {{
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let left_b = if col == 3 {{ red_b }} else {{ norm }}
    let right_b = if col == 3 {{ red_b }} else {{ norm }}
    let top_b = if row == 0 {{ if col == 3 {{ red_b }} else {{ 0.8pt + black }} }} else {{ norm }}
    let bot_b = if row == 0 {{ 1.2pt + black }} else if row == {last_row_idx} {{ if col == 3 {{ red_b }} else {{ norm }} }} else {{ norm }}
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  }},""")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  table.header(")
    content.append("    [*No*], [*Desa / Kelurahan*], [*Nama Kades / Lurah (Kondisi 2025)*], [*Nama Kades / Lurah (Kondisi 2026 / Terkini)*]")
    content.append("  ),")

    for no, desa, kades in kades_items:
        content.append(f"  [{escape_typst(no)}], [{escape_typst(desa)}], [{escape_typst(kades)}], [],")

    content.append(")")
    return "\n".join(content)

def render_table_2_1_4(slug: str, gdata: Dict[str, Any]) -> str:
    """
    Tabel 2.1.4: Nama-Nama Kepala Dusun (hanya kecamatan yang memiliki dusun).
    Kolom ke-5 adalah isian kondisi 2026/terkini dengan garis tepi merah di sekeliling kolom.
    """
    rows = gdata.get(slug, {}).get("Tabel 2.1.4", [])
    
    dusun_items = []
    for r in rows[3:]:
        if not r or not any(r):
            continue
        no_str = r[0].strip() if len(r) > 0 else ""
        desa_str = r[1].strip() if len(r) > 1 else ""
        dusun_str = r[2].strip() if len(r) > 2 else ""
        kadus_acuan = r[3].strip() if len(r) > 3 else "-"
        if dusun_str or desa_str or kadus_acuan != "-":
            dusun_items.append((no_str, desa_str, dusun_str, kadus_acuan))

    last_row_idx = len(dusun_items)

    content = []
    content.append("#v(8pt)")
    content.append("== Tabel 3: Nama-Nama Kepala Dusun di Wilayah Kecamatan")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Pemerintah Desa]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (28pt, 1.1fr, 1.1fr, 1.3fr, 1.4fr),")
    content.append("  inset: 4pt,")
    content.append("  align: (center, left, left, left, left),")
    content.append(f"""  stroke: (col, row) => {{
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let left_b = if col == 4 {{ red_b }} else {{ norm }}
    let right_b = if col == 4 {{ red_b }} else {{ norm }}
    let top_b = if row == 0 {{ if col == 4 {{ red_b }} else {{ 0.8pt + black }} }} else {{ norm }}
    let bot_b = if row == 0 {{ 1.2pt + black }} else if row == {last_row_idx} {{ if col == 4 {{ red_b }} else {{ norm }} }} else {{ norm }}
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  }},""")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  table.header(")
    content.append("    [*No*], [*Desa / Kelurahan*], [*Nama Dusun*], [*Nama Kadus (Acuan 2025)*], [*Nama Kadus (Kondisi 2026 / Terkini)*]")
    content.append("  ),")

    for no, desa, dusun, kadus in dusun_items:
        content.append(f"  [{escape_typst(no)}], [{escape_typst(desa)}], [{escape_typst(dusun)}], [{escape_typst(kadus)}], [],")

    content.append(")")
    return "\n".join(content)

def render_table_2_2_1(slug: str, gdata: Dict[str, Any], table_no: int = 4) -> str:
    """
    Tabel 2.2.1: Jumlah PNS Menurut Pemerintah Daerah dan Jenis Kelamin.
    Kolom Keterangan dihapus.
    Area Laki-Laki, Perempuan, Jumlah dibingkai border merah di sekelilingnya (outer border).
    """
    rows = gdata.get(slug, {}).get("Tabel 2.2.1", [])
    
    instansi_items = []
    for r in rows[4:]:
        if not r or not any(r):
            continue
        first_col = r[0].strip()
        if first_col == "2024" or "2024" in first_col:
            break
        if first_col.startswith("-") or "local government" in first_col.lower():
            continue
        inst_clean = first_col.split("\n")[0].strip()
        if inst_clean:
            instansi_items.append(inst_clean)

    last_row_idx = len(instansi_items)

    content = []
    content.append("#v(8pt)")
    content.append(f"== Tabel {table_no}: Jumlah Pegawai Negeri Sipil (PNS) Kantor Camat dan Desa/Kelurahan Tahun 2025")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Badan Kepegawaian dan Pengembangan SDM]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (32pt, 1fr, 75pt, 75pt, 75pt),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, center, center, center),")
    content.append(f"""  stroke: (col, row) => {{
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let left_b = if col == 2 {{ red_b }} else {{ norm }}
    let right_b = if col == 4 {{ red_b }} else {{ norm }}
    let top_b = if row == 0 {{ if col in (2, 3, 4) {{ red_b }} else {{ 0.8pt + black }} }} else {{ norm }}
    let bot_b = if row == 0 {{ 1.2pt + black }} else if row == {last_row_idx} {{ if col in (2, 3, 4) {{ red_b }} else {{ norm }} }} else {{ norm }}
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  }},""")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  table.header(")
    content.append("    [*No*], [*Pemerintah Daerah / Instansi*], [*Laki-Laki*], [*Perempuan*], [*Jumlah*]")
    content.append("  ),")

    idx = 1
    for inst in instansi_items:
        if "jumlah" in inst.lower():
            content.append(f"  table.cell(colspan: 2, align: center)[*Jumlah Total*], [], [], [],")
        else:
            content.append(f"  [{idx}], [{escape_typst(inst)}], [], [], [],")
            idx += 1

    content.append(")")
    return "\n".join(content)

def render_table_2_2_2(slug: str, gdata: Dict[str, Any], table_no: int = 5) -> str:
    """
    Tabel 2.2.2: Jumlah PNS Kantor Camat Menurut Pendidikan dan Jenis Kelamin.
    Kolom Keterangan dihapus.
    Area Laki-Laki, Perempuan, Jumlah dibingkai border merah di sekelilingnya (outer border).
    """
    rows = gdata.get(slug, {}).get("Tabel 2.2.2", [])
    
    pendidikan_items = []
    for r in rows[4:]:
        if not r or not any(r):
            continue
        first_col = r[0].strip()
        if first_col == "2024" or "2024" in first_col:
            break
        if first_col.startswith("-"):
            continue
        pend_clean = first_col.split("\n")[0].strip()
        if pend_clean:
            pendidikan_items.append(pend_clean)

    last_row_idx = len(pendidikan_items)

    content = []
    content.append("#v(8pt)")
    content.append(f"== Tabel {table_no}: Jumlah PNS Kantor Camat Menurut Tingkat Pendidikan dan Jenis Kelamin Tahun 2025")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (32pt, 1fr, 75pt, 75pt, 75pt),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, center, center, center),")
    content.append(f"""  stroke: (col, row) => {{
    let red_b = 1.5pt + rgb("#DC2626")
    let norm = 0.4pt + luma(180)
    let left_b = if col == 2 {{ red_b }} else {{ norm }}
    let right_b = if col == 4 {{ red_b }} else {{ norm }}
    let top_b = if row == 0 {{ if col in (2, 3, 4) {{ red_b }} else {{ 0.8pt + black }} }} else {{ norm }}
    let bot_b = if row == 0 {{ 1.2pt + black }} else if row == {last_row_idx} {{ if col in (2, 3, 4) {{ red_b }} else {{ norm }} }} else {{ norm }}
    (top: top_b, bottom: bot_b, left: left_b, right: right_b)
  }},""")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  table.header(")
    content.append("    [*No*], [*Tingkat Pendidikan*], [*Laki-Laki*], [*Perempuan*], [*Jumlah*]")
    content.append("  ),")

    idx = 1
    for pend in pendidikan_items:
        if "jumlah" in pend.lower():
            content.append(f"  table.cell(colspan: 2, align: center)[*Jumlah Total*], [], [], [],")
        else:
            content.append(f"  [{idx}], [{escape_typst(pend)}], [], [], [],")
            idx += 1

    content.append(")")
    return "\n".join(content)

# ==============================================================================
# PEMBUAT DOKUMEN TYPST LENGKAP PER KECAMATAN
# ==============================================================================

def build_surat_typst(slug: str, gdata: Dict[str, Any]) -> str:
    cfg = KECAMATAN_CONFIG[slug]
    nama_resmi = cfg["nama_resmi"]
    nomor_surat = NOMOR_SURAT_MAP.get(slug, "B-1091/61046/HM.310/2026")
    short_url = SHORTLINK_MAP.get(slug, f"https://s.bps.go.id/kcda26-{slug}")
    has_dusun = slug in KECAMATAN_WITH_DUSUN

    t212_str = render_table_2_1_2(slug, gdata)
    t213_str = render_table_2_1_3(slug, gdata)

    camat_rows_count = len(gdata.get(slug, {}).get("Tabel 2.1.2", []))
    camat_pagebreak = "\n\n#pagebreak()\n\n" if camat_rows_count > 12 else "\n\n"

    if has_dusun:
        t214_str = render_table_2_1_4(slug, gdata)
        t221_str = render_table_2_2_1(slug, gdata, table_no=4)
        t222_str = render_table_2_2_2(slug, gdata, table_no=5)
        dusun_phrase = "kepala dusun, "
        appendix_body = f"{t212_str}{camat_pagebreak}{t213_str}\n\n#pagebreak()\n\n{t214_str}\n\n#pagebreak()\n\n{t221_str}\n\n#v(10pt)\n\n{t222_str}"
    else:
        t221_str = render_table_2_2_1(slug, gdata, table_no=3)
        t222_str = render_table_2_2_2(slug, gdata, table_no=4)
        dusun_phrase = ""
        appendix_body = f"{t212_str}\n\n#pagebreak()\n\n{t213_str}\n\n#v(10pt)\n\n{t221_str}\n\n#v(10pt)\n\n{t222_str}"

    doc = f'''// Surat Dinas Permintaan dan Konfirmasi Data KCDA 2026 BPS Kabupaten Mempawah
// Ditujukan kepada Camat {nama_resmi}

#set page(
  paper: "a4",
  margin: (
    top: 4.8cm,
    bottom: 2.0cm,
    left: 2.0cm,
    right: 2.0cm
  ),
  header: locate(loc => {{
    v(0.8cm)
    grid(
      columns: (58pt, 1fr, 95pt),
      gutter: 10pt,
      align: (center + horizon, left + horizon, right + horizon),
      image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", width: 56pt),
      [
        #text(13.8pt, weight: "bold", style: "italic", font: "Metropolis", fill: black)[BADAN PUSAT STATISTIK] \\
        #text(13.8pt, weight: "bold", style: "italic", font: "Metropolis", fill: black)[KABUPATEN MEMPAWAH] \\
        #v(2.5pt)
        #text(8.2pt, font: "Arial", fill: black)[Jalan Raden Kusno Nomor 59 Mempawah 78912; Telepon (0561) 691049;] \\
        #text(8.2pt, font: "Arial", fill: black)[Laman https://mempawahkab.bps.go.id; Pos-el bps6104\\@bps.go.id.]
      ],
      image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_se2026.png", width: 92pt)
    )
    v(3pt)
    line(length: 100%, stroke: 2.2pt + black)
  }})
)

#set text(font: "Arial", size: 12pt, lang: "id")
#set par(justify: true, leading: 0.65em)

// =============================================================================
// METADATA SURAT DINAS (HALAMAN 1)
// =============================================================================
#v(4pt)
#grid(
  columns: (1fr, 175pt),
  gutter: 8pt,
  [
    #grid(
      columns: (65pt, 8pt, 1fr),
      gutter: 3pt,
      [Nomor], [:], [{nomor_surat}],
      [Sifat], [:], [Biasa],
      [Lampiran], [:], [1 (satu) Berkas],
      [Hal], [:], [*Permintaan dan Konfirmasi Data KCDA 2026*]
    )
  ],
  [
    #align(right)[
      Mempawah, 17 September 2026
    ]
  ]
)

#v(10pt)
Yth. *Camat {nama_resmi}* \\
di Tempat

#v(10pt)
Dengan hormat,

#set par(first-line-indent: 1.8em, leading: 0.65em)
Sehubungan dengan penyusunan Publikasi {nama_resmi} Dalam Angka 2026, kami bermaksud mengajukan permohonan data nama camat, kepala desa/lurah, {dusun_phrase}serta profil kepegawaian aparatur sipil negara di lingkungan Pemerintah {nama_resmi} sesuai format terlampir.

Pengisian data dapat dilakukan secara daring melalui tautan lembar kerja berikut: #link("{short_url}")[#text(fill: rgb("#0055D4"), weight: "bold")[{short_url}]]. Besar harapan kami data tersebut dapat kami terima selambat-lambatnya pada *Senin, 21 September 2026*. Apabila memerlukan koordinasi lebih lanjut, Bapak/Ibu dapat menghubungi narahubung kami, *Sukma Andini, S.Tr.Stat.* (WhatsApp: *082234120921*).

Demikian permohonan ini kami sampaikan. Atas perhatian dan kerja sama Bapak/Ibu, kami ucapkan terima kasih.

#v(18pt)
#set par(first-line-indent: 0pt)
#align(right)[
  #block(width: 220pt, breakable: false)[
    #align(left)[
      Kepala Badan Pusat Statistik \\
      Kabupaten Mempawah, \\
      #v(4pt)
      #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 42pt) \\
      #v(4pt)
      *Munawir*
    ]
  ]
]

// =============================================================================
// HALAMAN LAMPIRAN TABEL KONFIRMASI DATA
// =============================================================================
#pagebreak()

#v(4pt)
#grid(
  columns: (65pt, 8pt, 1fr),
  gutter: 3.5pt,
  [Lampiran 1], [], [],
  [Nomor], [:], [{nomor_surat}],
  [Tanggal], [:], [17 September 2026]
)

#v(8pt)
#align(center)[
  #text(11pt, weight: "bold")[Lembar Konfirmasi dan Pemutakhiran Data Sektoral \\ {nama_resmi} Dalam Angka 2026]
]
#v(6pt)

#rect(fill: rgb("#EFF6FF"), stroke: 0.6pt + rgb("#93C5FD"), radius: 3pt, inset: (x: 10pt, y: 6pt))[
  #text(8.5pt)[
    *Petunjuk Pengisian & Konfirmasi Data:*
    + Periksa data acuan (*baseline*) tahun sebelumnya yang tercantum pada tabel lampiran di bawah ini.
    + Pengisian atau konfirmasi data kondisi terkini dilakukan langsung melalui lembar kerja online (*Google Sheets*) pada tautan: #link("{short_url}")[#text(fill: rgb("#0055D4"), weight: "bold")[{short_url}]].
    + Pada lembar kerja online, pengisian difokuskan pada kolom/sel yang diberi tanda *garis tepi merah (border merah)*.
  ]
]

#set text(size: 8.5pt)
{appendix_body}
'''
    return doc

# ==============================================================================
# FUNGSI KOMPILASI DAN UPLOAD GOOGLE DRIVE
# ==============================================================================

def get_page_count(pdf_path: Path) -> Optional[int]:
    try:
        import re
        content = pdf_path.read_bytes()
        pages = re.findall(rb"/Type\s*/Page[^s]", content)
        if pages:
            return len(pages)
    except Exception:
        pass
    return None

def compile_surat_kecamatan(slug: str, output_dir: Path, gdata: Dict[str, Any]) -> Dict[str, Any]:
    cfg = KECAMATAN_CONFIG.get(slug)
    if not cfg:
        raise ValueError(f"Kecamatan slug '{slug}' tidak valid.")

    t0 = time.time()
    typ_path = output_dir / f"surat-konfirmasi-kcda-2026-{slug}.typ"
    pdf_path = output_dir / f"surat-konfirmasi-kcda-2026-{slug}.pdf"

    doc_typst = build_surat_typst(slug, gdata)
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write(doc_typst)

    typst_bin = "typst"

    cmd = [
        typst_bin, "compile",
        "--root", str(REPO_ROOT),
        "--font-path", str(ASSETS_DIR / "fonts"),
        str(typ_path),
        str(pdf_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Typst compilation failed for {slug}:\n{res.stderr}")

    duration = round(time.time() - t0, 2)
    file_size_kb = round(pdf_path.stat().st_size / 1024, 1)
    pages = get_page_count(pdf_path)

    return {
        "slug": slug,
        "nama_resmi": cfg["nama_resmi"],
        "nomor_surat": NOMOR_SURAT_MAP.get(slug, "-"),
        "short_url": SHORTLINK_MAP.get(slug, "-"),
        "typ_path": str(typ_path),
        "pdf_path": str(pdf_path),
        "file_name": pdf_path.name,
        "file_size_kb": file_size_kb,
        "pages": pages,
        "duration_sec": duration,
        "status": "SUCCESS"
    }

def upload_to_gdrive(file_path: Path, folder_id: str, share: str = "anyone") -> Dict[str, Any]:
    """Mengunggah berkas ke Google Drive via helper CLI gdrive_tool."""
    cmd = [
        "gdrive_tool", "drive-upload",
        "--file", str(file_path),
        "--folder-id", folder_id,
        "--share", share
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Upload failed for {file_path.name}:\n{res.stderr}")

    try:
        data = json.loads(res.stdout)
        return {
            "status": "success",
            "file_id": data.get("id"),
            "file_name": file_path.name,
            "web_view_link": data.get("web_view_link"),
            "shared": data.get("shared", False)
        }
    except Exception as e:
        raise RuntimeError(f"Failed to parse gdrive_tool output: {res.stdout}") from e

def main():
    parser = argparse.ArgumentParser(description="Generator Surat Dinas Konfirmasi KCDA 2026 BPS Kabupaten Mempawah (Revisi Kak Sukma Tahap 2)")
    parser.add_argument("--kecamatan", default="all", help="Slug kecamatan (contoh: 'mempawah-timur') atau 'all'")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Direktori output berkas .typ dan .pdf")
    parser.add_argument("--upload", action="store_true", help="Otomatis unggah PDF yang dihasilkan ke Google Drive")
    parser.add_argument("--folder-id", default=DEFAULT_GDRIVE_FOLDER_ID, help="Folder ID Google Drive tujuan (0. Surat)")
    parser.add_argument("--share", default="anyone", choices=["anyone", "user", "none"], help="Mode sharing link Google Drive")
    
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    gdata = load_cached_gsheet_data()

    target_slugs = list(KECAMATAN_CONFIG.keys()) if args.kecamatan == "all" else [args.kecamatan]

    print("==================================================================")
    print("🏛️  GENERATOR SURAT DINAS PERMINTAAN & KONFIRMASI DATA KCDA 2026")
    print("📋  Revisi Tahap 2: Shortlink s.bps.go.id, Header Dihapus, Outer Border")
    print(f"🎯 Target: {len(target_slugs)} kecamatan ({', '.join(target_slugs)})")
    print(f"📂 Output Dir: {out_dir}")
    print(f"☁️  Google Drive Upload: {'Aktif' if args.upload else 'Nonaktif'}")
    if args.upload:
        print(f"📁 Drive Folder ID: {args.folder_id}")
    print("==================================================================\n")

    compile_results = []
    for slug in target_slugs:
        cfg = KECAMATAN_CONFIG[slug]
        no_surat = NOMOR_SURAT_MAP.get(slug, "-")
        print(f"⚙️  Memproses: {cfg['nama_resmi']} [{no_surat}]...")
        try:
            res = compile_surat_kecamatan(slug, out_dir, gdata)
            print(f"   ✅ Berhasil dikompilasi ({res['pages']} hal, {res['file_size_kb']} KB, {res['duration_sec']} detik)")
            compile_results.append(res)
        except Exception as e:
            print(f"   ❌ Gagal: {e}")
            compile_results.append({
                "slug": slug,
                "nama_resmi": cfg["nama_resmi"],
                "nomor_surat": no_surat,
                "status": "FAILED",
                "error": str(e)
            })

    if args.upload:
        print("\n☁️  Memulai pengunggahan ke Google Drive...")
        for r in compile_results:
            if r.get("status") == "SUCCESS":
                pdf_p = Path(r["pdf_path"])
                print(f"   📤 Mengunggah {pdf_p.name} ke folder {args.folder_id}...")
                try:
                    up_res = upload_to_gdrive(pdf_p, args.folder_id, share=args.share)
                    r["drive_id"] = up_res["file_id"]
                    r["drive_link"] = up_res["web_view_link"]
                    print(f"      🔗 Link Drive: {r['drive_link']}")
                except Exception as e:
                    print(f"      ❌ Gagal unggah: {e}")
                    r["upload_error"] = str(e)

    print("\n==================================================================")
    print("📊 REKAPITULASI PEMBUATAN SURAT DINAS KCDA 2026")
    print("==================================================================")
    for r in compile_results:
        status_icon = "✅" if r.get("status") == "SUCCESS" else "❌"
        line = f"{status_icon} {r['nama_resmi']} ({r.get('nomor_surat', '-')}) : {r.get('pages', 0)} hal, {r.get('file_size_kb', 0)} KB"
        if r.get("short_url"):
            line += f" | {r['short_url']}"
        if r.get("drive_link"):
            line += f"\n   🔗 Drive: {r['drive_link']}"
        print(line)
    print("==================================================================\n")

if __name__ == "__main__":
    main()
