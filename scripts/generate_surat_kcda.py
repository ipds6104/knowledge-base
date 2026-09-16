#!/usr/bin/env python3
"""
generate_surat_kcda.py
======================
Script otomasi pembuatan Surat Dinas Resmi BPS Kabupaten Mempawah untuk
permintaan dan konfirmasi data acuan (baseline) 9 tabel KCDA 2026 bagi
9 kecamatan di Kabupaten Mempawah, serta pengunggahan otomatis ke Google Drive.

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
from typing import Dict, Any, List, Optional, Tuple

REPO_ROOT = Path("/app/workspaces/bps-mempawah")
DATA_DIR = REPO_ROOT / "data" / "kcda-2026" / "raw_tables"
ASSETS_DIR = REPO_ROOT / "kegiatan" / "kecamatan-dalam-angka" / "2026" / "assets"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "kegiatan" / "kecamatan-dalam-angka" / "2026" / "outputs" / "surat"
DEFAULT_GDRIVE_FOLDER_ID = "1zBq1esGJOndJS1XMXvOVQj6UOL5-7lvr"

KECAMATAN_CONFIG = {
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

TABLE_FILES = {
    "1.2": "tabel_1_2_jarak_ke_ibukota_kecamatan_dan.json",
    "1.3": "tabel_1_3_batas_administrasi_kecamatan_x.json",
    "1.4": "tabel_1_4_jarak_kantor_camat_xxx_dengan.json",
    "2.1.1": "tabel_2_1_1_jumlah_rukun_warga__rw__dan_ru.json",
    "2.1.2": "tabel_2_1_2_nama_nama_camat_yang_pernah_ma.json",
    "2.1.3": "tabel_2_1_3_nama_nama_kepala_desa_di_kecam.json",
    "2.1.4": "tabel_2_1_4_nama_nama_kepala_dusun_di_keca.json",
    "2.2.1": "tabel_2_2_1_jumlah_pegawai_negeri_sipil_me.json",
    "2.2.2": "tabel_2_2_2_jumlah_pegawai_negeri_sipil_pe.json"
}

def escape_typst(val: Any) -> str:
    """Membersihkan dan meng-escape karakter khusus Typst."""
    if val is None:
        return ""
    text = str(val).strip()
    if not text:
        return ""
    # Ganti newline dengan spasi atau break
    text = text.replace("\r\n", " ").replace("\n", " ")
    # Escape backslash
    text = text.replace("\\", "\\\\")
    # Escape typst markup characters
    for ch in ["@", "#", "$", "[", "]"]:
        text = text.replace(ch, f"\\{ch}")
    return text

def clean_cell(val: Any) -> str:
    """Membersihkan sel tabel dan membungkusnya dalam format Typst."""
    t = escape_typst(val)
    return f"[{t}]"

def load_raw_table(code: str) -> Dict[str, Any]:
    file_path = DATA_DIR / TABLE_FILES[code]
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_tab_data(json_data: Dict[str, Any], tab_name: str) -> List[List[str]]:
    tabs = json_data.get("tabs", {})
    if tab_name in tabs:
        return tabs[tab_name].get("rows", [])
    
    # Fuzzy match
    norm = tab_name.lower().replace("mempawah", "m").replace("mampawah", "m")
    for k, v in tabs.items():
        k_norm = k.lower().replace("mempawah", "m").replace("mampawah", "m")
        if k_norm == norm or tab_name.lower() in k.lower():
            return v.get("rows", [])
    return []

# ==============================================================================
# PEMBANGUN TABEL LAMPIRAN DALAM TYPST
# ==============================================================================

def render_table_1_3(raw_data: Dict[str, Any], tab_name: str) -> str:
    """Tabel 1.3: Batas Administrasi Kecamatan"""
    rows = get_tab_data(raw_data, tab_name)
    content = []
    content.append("#v(8pt)")
    content.append("== Tabel 1: Batas Administrasi Kecamatan Menurut Arah Mata Angin")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Publikasi KCDA Acuan]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (32pt, 95pt, 1.4fr, 1.4fr),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, left, left),")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else if y == 1 { (bottom: 0.8pt + black) } else { 0.4pt + luma(180) },")
    content.append("  table.header(")
    content.append("    [*No*], [*Arah Mata Angin*], [*Berbatasan dengan (Acuan)*], [*Koreksi / Kondisi Terkini*]")
    content.append("  ),")

    # Ambil baris data (skip row 0: '2025', row 1: header, row 2: '(1) (2)...')
    data_rows = [r for r in rows if len(r) >= 3 and r[0] not in ["2025", "No", "(1)"]]
    for idx, r in enumerate(data_rows, 1):
        arah = r[1].split("\n")[0].split("/")[0].strip()
        batas = r[2].split("\n")[0].split("/")[0].strip()
        content.append(f"  [{idx}], [{escape_typst(arah)}], [{escape_typst(batas)}], [],")
    content.append(")")
    return "\n".join(content)

def render_table_1_4(raw_data: Dict[str, Any], tab_name: str, nama_resmi: str) -> str:
    """Tabel 1.4: Jarak Kantor Camat ke Tempat Penting"""
    rows = get_tab_data(raw_data, tab_name)
    content = []
    content.append("#v(10pt)")
    content.append(f"== Tabel 2: Jarak Kantor Camat {escape_typst(nama_resmi)} ke Tempat Penting Lainnya (km)")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Publikasi KCDA Acuan]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (32pt, 1.8fr, 90pt, 1.2fr),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, center, left),")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },")
    content.append("  table.header(")
    content.append("    [*No*], [*Nama Kota / Tempat Penting*], [*Jarak Acuan (km)*], [*Koreksi Jarak (km)*]")
    content.append("  ),")

    data_rows = [r for r in rows if len(r) >= 3 and r[0] not in ["2025", "No", "(1)"]]
    for idx, r in enumerate(data_rows, 1):
        tempat = r[1].split("\n")[0].strip()
        jarak = r[2].split("\n")[0].strip()
        content.append(f"  [{idx}], [{escape_typst(tempat)}], [{escape_typst(jarak)}], [],")
    content.append(")")
    return "\n".join(content)

def render_table_1_2(raw_data: Dict[str, Any], tab_name: str) -> str:
    """Tabel 1.2: Jarak Desa ke Ibukota Kecamatan dan Kabupaten"""
    rows = get_tab_data(raw_data, tab_name)
    content = []
    content.append("#v(10pt)")
    content.append("== Tabel 3: Jarak ke Ibukota Kecamatan dan Ibukota Kabupaten Menurut Desa/Kelurahan (km)")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / KCDA Acuan]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (30pt, 1.2fr, 75pt, 75pt, 80pt, 80pt),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, center, center, center, center),")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },")
    content.append("  table.header(")
    content.append("    [*No*], [*Desa / Kelurahan*], [*Jarak ke Kec (km)*], [*Jarak ke Kab (km)*], [*Koreksi Kec (km)*], [*Koreksi Kab (km)*]")
    content.append("  ),")

    data_rows = [r for r in rows if len(r) >= 3 and r[0] not in ["2025", "Desa/Kelurahan\n Village/Subdistric", "(1)"]]
    for idx, r in enumerate(data_rows, 1):
        desa = r[0].split("\n")[0].strip()
        d_kec = r[1].split("\n")[0].strip() if len(r) > 1 else "-"
        d_kab = r[2].split("\n")[0].strip() if len(r) > 2 else "-"
        content.append(f"  [{idx}], [{escape_typst(desa)}], [{escape_typst(d_kec)}], [{escape_typst(d_kab)}], [], [],")
    content.append(")")
    return "\n".join(content)

def render_table_2_1_1(raw_data: Dict[str, Any], tab_name: str) -> str:
    """Tabel 2.1.1: Jumlah RW dan RT Menurut Desa/Kelurahan"""
    rows = get_tab_data(raw_data, tab_name)
    content = []
    content.append("#v(10pt)")
    content.append("== Tabel 4: Jumlah Dusun, Rukun Warga (RW), dan Rukun Tetangga (RT) Menurut Desa/Kelurahan")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Desa]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (28pt, 1.2fr, 48pt, 48pt, 48pt, 48pt, 48pt, 48pt),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, center, center, center, center, center, center),")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },")
    content.append("  table.header(")
    content.append("    [*No*], [*Desa/Kelurahan*], [*Dusun (Acuan)*], [*RW (Acuan)*], [*RT (Acuan)*], [*Koreksi Dusun*], [*Koreksi RW*], [*Koreksi RT*]")
    content.append("  ),")

    data_rows = [r for r in rows if len(r) >= 4 and r[0] not in ["2025", "Desa/Kelurahan\n Village/Subdistric", "(1)"]]
    for idx, r in enumerate(data_rows, 1):
        desa = r[0].split("\n")[0].strip()
        dusun = r[1].split("\n")[0].strip() if len(r) > 1 else "-"
        rw = r[2].split("\n")[0].strip() if len(r) > 2 else "-"
        rt = r[3].split("\n")[0].strip() if len(r) > 3 else "-"
        content.append(f"  [{idx}], [{escape_typst(desa)}], [{escape_typst(dusun)}], [{escape_typst(rw)}], [{escape_typst(rt)}], [], [], [],")
    content.append(")")
    return "\n".join(content)

def render_table_2_1_2(raw_data: Dict[str, Any], tab_name: str) -> str:
    """Tabel 2.1.2: Nama Camat yang Pernah/Masih Menjabat"""
    rows = get_tab_data(raw_data, tab_name)
    content = []
    content.append("#v(10pt)")
    content.append("== Tabel 1: Nama-Nama Camat yang Pernah dan Masih Menjabat")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Publikasi KCDA]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (30pt, 1.4fr, 110pt, 1.2fr),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, center, left),")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },")
    content.append("  table.header(")
    content.append("    [*No*], [*Nama-Nama Camat*], [*Periode Jabatan (Acuan)*], [*Koreksi / Perubahan Nama / Status*]")
    content.append("  ),")

    data_rows = [r for r in rows if len(r) >= 3 and r[0] not in ["2025", "No", "(1)"]]
    for idx, r in enumerate(data_rows, 1):
        nama = r[1].split("\n")[0].strip()
        periode = r[2].split("\n")[0].strip() if len(r) > 2 else "-"
        content.append(f"  [{idx}], [{escape_typst(nama)}], [{escape_typst(periode)}], [],")
    
    # Tambahkan baris kosong untuk entri camat baru jika ada pergantian
    content.append(f"  [+], [#text(style: \"italic\", fill: luma(100))[Camat Baru (jika ada)]], [], [],")
    content.append(")")
    return "\n".join(content)

def render_table_2_1_3(raw_data: Dict[str, Any], tab_name: str, desa_list: List[str] = None) -> str:
    """Tabel 2.1.3: Nama-Nama Kepala Desa di Kecamatan"""
    rows = get_tab_data(raw_data, tab_name)
    content = []
    content.append("#v(10pt)")
    content.append("== Tabel 2: Nama-Nama Kepala Desa / Lurah")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Pemerintah Desa]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (30pt, 1.1fr, 1.4fr, 1.4fr),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, left, left),")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },")
    content.append("  table.header(")
    content.append("    [*No*], [*Desa / Kelurahan*], [*Nama Kepala Desa / Lurah (Acuan)*], [*Nama Kepala Desa / Pj Terkini*]")
    content.append("  ),")

    # Ambil data kades dari acuan jika tersedia
    kades_map = {}
    for r in rows:
        if len(r) >= 3 and r[0] not in ["2025", "No", "(1)"]:
            d_name = r[1].split("\n")[0].strip()
            k_name = r[2].split("\n")[0].strip() if len(r) > 2 else "-"
            kades_map[d_name.lower()] = k_name

    if desa_list:
        for idx, desa in enumerate(desa_list, 1):
            kades = kades_map.get(desa.lower(), "-")
            content.append(f"  [{idx}], [{escape_typst(desa)}], [{escape_typst(kades)}], [],")
    else:
        data_rows = [r for r in rows if len(r) >= 2 and r[0] not in ["2025", "No", "(1)"] and not r[1].strip().lower().startswith("kecamatan")]
        for idx, r in enumerate(data_rows, 1):
            desa = r[1].split("\n")[0].strip()
            kades = r[2].split("\n")[0].strip() if len(r) > 2 else "-"
            content.append(f"  [{idx}], [{escape_typst(desa)}], [{escape_typst(kades)}], [],")
    content.append(")")
    return "\n".join(content)

def render_table_2_1_4(raw_data: Dict[str, Any], tab_name: str, desa_list: List[str]) -> str:
    """Tabel 2.1.4: Nama-Nama Kepala Dusun di Kecamatan"""
    rows = get_tab_data(raw_data, tab_name)
    content = []
    content.append("#v(10pt)")
    content.append("== Tabel 3: Nama-Nama Kepala Dusun di Wilayah Kecamatan")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Pemerintah Desa]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (30pt, 1.2fr, 1.2fr, 1.5fr),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, left, left),")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },")
    content.append("  table.header(")
    content.append("    [*No*], [*Desa / Kelurahan*], [*Nama Dusun*], [*Nama Kepala Dusun (Kadus)*]")
    content.append("  ),")

    # Filter data valid jika ada
    valid_rows = [r for r in rows if len(r) >= 4 and r[0] not in ["No", "(1)"] and any(len(c.strip()) > 0 for c in r[1:])]
    if valid_rows:
        for idx, r in enumerate(valid_rows, 1):
            desa = r[1].split("\n")[0].strip()
            dusun = r[2].split("\n")[0].strip()
            kadus = r[3].split("\n")[0].strip()
            content.append(f"  [{idx}], [{escape_typst(desa)}], [{escape_typst(dusun)}], [{escape_typst(kadus)}],")
    else:
        # Jika belum ada data nama kadus, sajikan baris berdasar desa_list dengan kolom kosong
        row_num = 1
        for d in desa_list:
            content.append(f"  [{row_num}], [{escape_typst(d)}], [], [],")
            row_num += 1
            content.append(f"  [{row_num}], [{escape_typst(d)}], [], [],")
            row_num += 1
    content.append(")")
    return "\n".join(content)

def render_table_2_2_1(raw_data: Dict[str, Any], tab_name: str, table_no: int = 4) -> str:
    """Tabel 2.2.1: Jumlah PNS Menurut Pemerintah Daerah dan Jenis Kelamin"""
    rows = get_tab_data(raw_data, tab_name)
    content = []
    content.append("#v(10pt)")
    content.append(f"== Tabel {table_no}: Jumlah Pegawai Negeri Sipil (PNS) Kantor Camat dan Desa/Kelurahan")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat / Badan Kepegawaian dan Pengembangan SDM]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (30pt, 1.6fr, 65pt, 65pt, 65pt, 1fr),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, center, center, center, left),")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },")
    content.append("  table.header(")
    content.append("    [*No*], [*Pemerintah Daerah / Kantor*], [*Laki-Laki*], [*Perempuan*], [*Jumlah*], [*Keterangan / Non-PNS*]")
    content.append("  ),")

    data_rows = [r for r in rows if len(r) >= 1 and r[0] not in ["2025", "Pemerintah Daerah\nLocal Government", "Pemerintah Daerah\n Local Government"]]
    for idx, r in enumerate(data_rows, 1):
        instansi = r[0].split("\n")[0].strip()
        l_val = r[1].split("\n")[0].strip() if len(r) > 1 and r[1].strip() else ""
        p_val = r[2].split("\n")[0].strip() if len(r) > 2 and r[2].strip() else ""
        j_val = r[3].split("\n")[0].strip() if len(r) > 3 and r[3].strip() else ""
        content.append(f"  [{idx}], [{escape_typst(instansi)}], [{escape_typst(l_val)}], [{escape_typst(p_val)}], [{escape_typst(j_val)}], [],")
    content.append(")")
    return "\n".join(content)

def render_table_2_2_2(raw_data: Dict[str, Any], tab_name: str, table_no: int = 5) -> str:
    """Tabel 2.2.2: Jumlah PNS Kantor Camat Menurut Pendidikan dan Jenis Kelamin"""
    rows = get_tab_data(raw_data, tab_name)
    content = []
    content.append("#v(10pt)")
    content.append(f"== Tabel {table_no}: Jumlah PNS Kantor Camat Menurut Tingkat Pendidikan dan Jenis Kelamin")
    content.append("#text(7.5pt, fill: rgb(\"#4B5563\"))[Sumber: Kantor Camat]")
    content.append("#v(4pt)")
    content.append("#table(")
    content.append("  columns: (30pt, 1.6fr, 70pt, 70pt, 70pt, 1fr),")
    content.append("  inset: 4.5pt,")
    content.append("  align: (center, left, center, center, center, left),")
    content.append("  fill: (col, row) => if row == 0 { rgb(\"#F3F4F6\") } else { none },")
    content.append("  stroke: (x, y) => if y == 0 { (bottom: 1.2pt + black, top: 0.8pt + black) } else { 0.4pt + luma(180) },")
    content.append("  table.header(")
    content.append("    [*No*], [*Tingkat Pendidikan*], [*Laki-Laki*], [*Perempuan*], [*Jumlah*], [*Keterangan*]")
    content.append("  ),")

    data_rows = [r for r in rows if len(r) >= 1 and r[0] not in ["2025", "Tingkat Pendidikan\n Educational Level"]]
    for idx, r in enumerate(data_rows, 1):
        pendidikan = r[0].split("\n")[0].strip()
        l_val = r[1].split("\n")[0].strip() if len(r) > 1 and r[1].strip() else ""
        p_val = r[2].split("\n")[0].strip() if len(r) > 2 and r[2].strip() else ""
        j_val = r[3].split("\n")[0].strip() if len(r) > 3 and r[3].strip() else ""
        if "jumlah" in pendidikan.lower():
            content.append(f"  table.cell(colspan: 2, align: center)[*Jumlah Total*], [{escape_typst(l_val)}], [{escape_typst(p_val)}], [{escape_typst(j_val)}], [],")
        else:
            content.append(f"  [{idx}], [{escape_typst(pendidikan)}], [{escape_typst(l_val)}], [{escape_typst(p_val)}], [{escape_typst(j_val)}], [],")
    content.append(")")
    return "\n".join(content)

# ==============================================================================
# PEMBUAT DOKUMEN TYPST LENGKAP PER KECAMATAN
# ==============================================================================

KECAMATAN_WITH_DUSUN = {
    "toho",
    "segedong",
    "sadaniang",
    "anjongan",
    "jongkat",
    "sungai-kunyit",
    "mempawah-timur"
}

def build_surat_typst(slug: str) -> str:
    cfg = KECAMATAN_CONFIG[slug]
    nama_resmi = cfg["nama_resmi"]
    tab_name = cfg["tab_name"]
    ibukota = cfg["ibukota_kecamatan"]
    desa_list = cfg["desa_list"]

    has_dusun = slug in KECAMATAN_WITH_DUSUN

    # Load hanya tabel konfirmasi yang dibutuhkan
    d212 = load_raw_table("2.1.2")
    d213 = load_raw_table("2.1.3")
    d221 = load_raw_table("2.2.1")
    d222 = load_raw_table("2.2.2")

    t212_str = render_table_2_1_2(d212, tab_name)
    t213_str = render_table_2_1_3(d213, tab_name, desa_list)

    if has_dusun:
        d214 = load_raw_table("2.1.4")
        t214_str = render_table_2_1_4(d214, tab_name, desa_list)
        t221_str = render_table_2_2_1(d221, tab_name, table_no=4)
        t222_str = render_table_2_2_2(d222, tab_name, table_no=5)
        dusun_phrase = "kepala dusun, "
        appendix_body = f"{t212_str}\n\n{t213_str}\n\n#pagebreak()\n\n{t214_str}\n\n#pagebreak()\n\n{t221_str}\n\n{t222_str}"
    else:
        t214_str = ""
        t221_str = render_table_2_2_1(d221, tab_name, table_no=3)
        t222_str = render_table_2_2_2(d222, tab_name, table_no=4)
        dusun_phrase = ""
        appendix_body = f"{t212_str}\n\n{t213_str}\n\n#pagebreak()\n\n{t221_str}\n\n{t222_str}"

    sheet_id = cfg.get("sheet_id", "")
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}" if sheet_id else "https://drive.google.com/drive/folders/1eWA-e-esicQ6Jdq6ouviVb76XrB-F0SQ"

    doc = f'''// Surat Dinas Permintaan dan Konfirmasi Data KCDA 2026 BPS Kabupaten Mempawah
// Ditujukan kepada Camat {nama_resmi}

#set page(
  paper: "a4",
  margin: (
    top: 2.2cm,
    bottom: 2.2cm,
    left: 2.2cm,
    right: 2.2cm
  ),
  header: context {{
    let page_num = counter(page).get().first()
    if page_num > 1 {{
      grid(
        columns: (1fr, auto),
        align: (left, right),
        text(7pt, fill: rgb("#4B5563"), font: "Myriad Pro")[Lampiran Surat Konfirmasi Data KCDA 2026 | BPS Kabupaten Mempawah - {nama_resmi}],
        text(7pt, fill: rgb("#4B5563"), font: "Myriad Pro")[Halaman #page_num]
      )
      line(length: 100%, stroke: 0.3pt + luma(180))
    }}
  }},
  footer: context {{
    let page_num = counter(page).get().first()
    if page_num == 1 {{
      align(center, text(7pt, fill: luma(120), font: "Myriad Pro")[BPS Kabupaten Mempawah — Menghasilkan Data Statistik Berkualitas untuk Indonesia Maju])
    }}
  }}
)

#set text(font: ("Myriad Pro", "Metropolis"), size: 9.5pt, lang: "id")
#set par(justify: true, leading: 0.6em)

// =============================================================================
// KOP SURAT RESMI BPS KABUPATEN MEMPAWAH
// =============================================================================
#grid(
  columns: (65pt, 1fr),
  gutter: 12pt,
  align: (center + horizon, center + horizon),
  image("/kegiatan/kecamatan-dalam-angka/2026/assets/logo_bps.png", width: 56pt),
  [
    #text(13.5pt, weight: "bold", font: "Metropolis", fill: rgb("#0F294A"))[BADAN PUSAT STATISTIK KABUPATEN MEMPAWAH] \\
    #v(1pt)
    #text(8.5pt, fill: rgb("#1F2937"))[Jl. Raden Kusno No. 1, Mempawah 79511] \\
    #text(8pt, fill: rgb("#374151"))[Telepon: (0561) 691030 | Pos-el: bps6104\\@bps.go.id | Laman: https://mempawahkab.bps.go.id]
  ]
)
#v(4pt)
#line(length: 100%, stroke: 1.8pt + rgb("#0F294A"))
#v(-5.5pt)
#line(length: 100%, stroke: 0.6pt + rgb("#0F294A"))
#v(12pt)

// =============================================================================
// METADATA SURAT DINAS
// =============================================================================
#grid(
  columns: (1fr, 150pt),
  gutter: 10pt,
  [
    #grid(
      columns: (60pt, 8pt, 1fr),
      gutter: 3pt,
      [Nomor], [:], [B-155/61040/VS.100/09/2026],
      [Sifat], [:], [Biasa],
      [Lampiran], [:], [1 (satu) Berkas],
      [Hal], [:], [*Permintaan dan Konfirmasi Data Kecamatan Dalam Angka (KCDA) 2026*]
    )
  ],
  [
    #align(right)[
      Mempawah, 16 September 2026
    ]
  ]
)

#v(10pt)
Yth. *Camat {nama_resmi}* \\
di Tempat

#v(10pt)
Dengan hormat,

#set par(first-line-indent: 1.8em, leading: 0.65em)
Dalam rangka pelaksanaan amanat Undang-Undang Nomor 16 Tahun 1997 tentang Statistik dan Peraturan Presiden Nomor 39 Tahun 2019 tentang Satu Data Indonesia, Badan Pusat Statistik (BPS) Kabupaten Mempawah saat ini sedang menyusun publikasi statistik tahunan *"{nama_resmi} Dalam Angka 2026"*. Publikasi ini menyajikan data statistik sektoral komprehensif tingkat kecamatan dan desa/kelurahan yang menjadi rujukan penting bagi perencanaan, pemantauan, serta evaluasi program pembangunan di Kabupaten Mempawah.

Sehubungan dengan hal tersebut, bersama ini kami sampaikan lembar data acuan (*baseline*) tahun sebelumnya sebagaimana terlampir, yang mencakup data pejabat camat, kepala desa/lurah, {dusun_phrase}serta profil kepegawaian aparatur sipil negara di lingkungan {nama_resmi}.

Guna menjamin akurasi dan kemutakhiran data publikasi edisi 2026, kami sangat mengharapkan bantuan dan kerja sama Bapak/Ibu Camat beserta jajaran untuk dapat melakukan pemeriksaan, verifikasi, serta pengisian koreksi data mutakhir pada kolom konfirmasi yang telah disediakan.

Berkas konfirmasi data yang telah diverifikasi kiranya dapat disampaikan kembali kepada BPS Kabupaten Mempawah selambat-lambatnya pada hari *Senin, 21 September 2026*. Apabila memerlukan informasi teknis lebih lanjut atau untuk konfirmasi pemutakhiran data secara langsung, Bapak/Ibu dapat menghubungi narahubung kami:

#set par(first-line-indent: 0pt)
#align(center)[
  #rect(fill: rgb("#F8FAFC"), stroke: 0.8pt + rgb("#CBD5E1"), radius: 4pt, inset: (x: 14pt, y: 8pt))[
    #text(9pt)[
      *Sukma (Sukma Andini, S.Tr.Stat.)* \\
      Staf Fungsi Integrasi Pengolahan dan Diseminasi Statistik (IPDS) BPS Kabupaten Mempawah \\
      WhatsApp / Kontak: *0812-5853-2420* (+62 812-5853-2420) \\
      #v(2pt)
      Lembar Kerja Pengisian Data (Google Sheets): \\
      #link("{sheet_url}")[#text(size: 8pt, fill: rgb("#1D4ED8"), weight: "bold")[{sheet_url}]]
    ]
  ]
]

#set par(first-line-indent: 1.8em)
Demikian permohonan ini kami sampaikan. Atas perhatian, dukungan, dan kerja sama yang baik dari Bapak/Ibu Camat demi terwujudnya data statistik daerah yang berkualitas dan akuntabel, kami ucapkan terima kasih.

#v(12pt)
#set par(first-line-indent: 0pt)
#grid(
  columns: (1fr, 210pt),
  gutter: 10pt,
  [],
  [
    #align(left)[
      Kepala Badan Pusat Statistik \\
      Kabupaten Mempawah, \\
      #v(2pt)
      #image("/kegiatan/kecamatan-dalam-angka/2026/assets/ttd_kepala_bps.png", height: 42pt) \\
      #v(2pt)
      *MUNAWIR, S.E., M.M.* \\
      Pembina Tk. I (IV/b)
    ]
  ]
)

#v(8pt)
#text(8pt, fill: rgb("#374151"))[
  *Tembusan Yth:* \\
  1. Bupati Mempawah (sebagai laporan) \\
  2. Arsip BPS Kabupaten Mempawah
]

// =============================================================================
// HALAMAN LAMPIRAN TABEL KONFIRMASI DATA
// =============================================================================
#pagebreak()

#align(center)[
  #text(11pt, weight: "bold", font: "Metropolis")[LAMPIRAN SURAT DINAS KEPALA BPS KABUPATEN MEMPAWAH] \\
  #text(9pt)[Nomor: B-155/61040/VS.100/09/2026 | Tanggal: 16 September 2026] \\
  #v(2pt)
  #text(10pt, weight: "bold", fill: rgb("#0F294A"))[LEMBAR KONFIRMASI DAN PEMUTAKHIRAN DATA SEKTORAL \\ {nama_resmi.upper()} DALAM ANGKA 2026]
]
#v(6pt)

#rect(fill: rgb("#EFF6FF"), stroke: 0.6pt + rgb("#93C5FD"), radius: 3pt, inset: (x: 10pt, y: 7pt))[
  #text(8pt)[
    *Petunjuk Pengisian & Konfirmasi Data:*
    + Periksa data acuan (*baseline*) tahun sebelumnya yang tercantum pada tabel lampiran di bawah ini sebagai gambaran data yang perlu dikonfirmasi.
    + Pengisian perbaikan atau konfirmasi kondisi terkini dapat dilakukan langsung secara digital melalui tautan Google Spreadsheet kecamatan yang telah disediakan di atas.
    + Apabila terdapat perubahan nama, pemekaran wilayah, atau pergantian pejabat terkini, silakan perbarui pada lembar kerja online atau hubungi narahubung kami.
  ]
]

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

def compile_surat_kecamatan(slug: str, output_dir: Path) -> Dict[str, Any]:
    cfg = KECAMATAN_CONFIG.get(slug)
    if not cfg:
        raise ValueError(f"Kecamatan slug '{slug}' tidak valid.")

    t0 = time.time()
    typ_path = output_dir / f"surat-konfirmasi-kcda-2026-{slug}.typ"
    pdf_path = output_dir / f"surat-konfirmasi-kcda-2026-{slug}.pdf"

    # Buat konten Typst
    doc_typst = build_surat_typst(slug)
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write(doc_typst)

    # Kompilasi Typst ke PDF
    cmd = [
        "typst", "compile",
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
    parser = argparse.ArgumentParser(description="Generator Surat Dinas Konfirmasi KCDA 2026 BPS Kabupaten Mempawah")
    parser.add_argument("--kecamatan", default="all", help="Slug kecamatan (contoh: 'mempawah-hilir') atau 'all'")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Direktori output berkas .typ dan .pdf")
    parser.add_argument("--upload", action="store_true", help="Otomatis unggah PDF yang dihasilkan ke Google Drive")
    parser.add_argument("--folder-id", default=DEFAULT_GDRIVE_FOLDER_ID, help="Folder ID Google Drive tujuan")
    parser.add_argument("--share", default="anyone", choices=["anyone", "user", "none"], help="Mode sharing link Google Drive")
    
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    target_slugs = list(KECAMATAN_CONFIG.keys()) if args.kecamatan == "all" else [args.kecamatan]

    print("==================================================================")
    print("🏛️  GENERATOR SURAT DINAS PERMINTAAN & KONFIRMASI DATA KCDA 2026")
    print(f"🎯 Target: {len(target_slugs)} kecamatan ({', '.join(target_slugs)})")
    print(f"📂 Output Dir: {out_dir}")
    print(f"☁️  Google Drive Upload: {'Aktif' if args.upload else 'Nonaktif'}")
    if args.upload:
        print(f"📁 Drive Folder ID: {args.folder_id}")
    print("==================================================================\n")

    compile_results = []
    for slug in target_slugs:
        cfg = KECAMATAN_CONFIG[slug]
        print(f"⚙️  Memproses: {cfg['nama_resmi']} ({slug})...")
        try:
            res = compile_surat_kecamatan(slug, out_dir)
            print(f"   ✅ Berhasil dikompilasi ({res['pages']} hal, {res['file_size_kb']} KB, {res['duration_sec']} detik)")
            compile_results.append(res)
        except Exception as e:
            print(f"   ❌ Gagal: {e}")
            compile_results.append({
                "slug": slug,
                "nama_resmi": cfg["nama_resmi"],
                "status": "FAILED",
                "error": str(e)
            })

    # Upload ke Google Drive bila flag diaktifkan
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
        line = f"{status_icon} {r['nama_resmi']}: {r.get('pages', 0)} hal, {r.get('file_size_kb', 0)} KB"
        if r.get("drive_link"):
            line += f" -> {r['drive_link']}"
        print(line)
    print("==================================================================\n")

if __name__ == "__main__":
    main()
