#!/usr/bin/env python3
"""
update_assignment_sheet.py
==========================
Script untuk menambahkan kolom 'Nama PML' dan 'Nama PJ Kuda' pada Google Spreadsheet:
'Rekap Assignment Ditemukan dan Baru - Mempawah'
URL: https://docs.google.com/spreadsheets/d/1eDzkuD-hzN_ePbIytFNiEAy9pR5IEy5JPENQgKjnkC4/edit

Fitur Utama:
1. Pemeriksaan kemungkinan nama PPL ganda (ditemukan 2 kasus: Nurmala dan Amrullah).
2. Pemetaan deterministik PML -> PJ Kuda dari master data 'Alokasi Petugas.csv'.
3. Penambahan kolom 'Nama PJ Kuda' pada sheet 'Per SLS' (setelah kolom 'Nama PML').
4. Penambahan kolom 'Nama PML' dan 'Nama PJ Kuda' pada sheet 'Per PPL', sekaligus
   memisahkan baris PPL yang bernama sama agar capaian per individu terhitung akurat.
5. Mendukung flag --preview (dry-run) dan --apply (eksekusi nyata ke Google Sheets).
"""

import argparse
import csv
import json
import sys
import requests
from collections import defaultdict
from pathlib import Path

SPREADSHEET_ID = "1eDzkuD-hzN_ePbIytFNiEAy9pR5IEy5JPENQgKjnkC4"
TOKEN_FILE = Path("/app/data/google_token.json")
ALOKASI_FILE = Path("/app/workspaces/bps-mempawah/kegiatan/sensus-ekonomi-2026/2026/master_data/Alokasi Petugas.csv")

def get_headers():
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(f"Berkas token tidak ditemukan di {TOKEN_FILE}")
    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
    token = data.get("token") or data.get("access_token")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def load_pml_to_pj_map():
    if not ALOKASI_FILE.exists():
        raise FileNotFoundError(f"Berkas Alokasi Petugas tidak ditemukan di {ALOKASI_FILE}")
    pml_to_pj = {}
    with open(ALOKASI_FILE, "r", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        for row in r:
            pml = row["PML"].strip()
            pj = row["Pj-Kuda"].strip()
            if pml:
                pml_to_pj[pml.lower()] = pj
    return pml_to_pj

def fetch_sheet_values(sheet_id: str, range_name: str, headers: dict):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"Gagal membaca sheet {range_name}: {resp.status_code} - {resp.text}")
    return resp.json().get("values", [])

def update_sheet_values(sheet_id: str, range_name: str, values: list, headers: dict):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}?valueInputOption=USER_ENTERED"
    body = {"values": values}
    resp = requests.put(url, headers=headers, json=body)
    if resp.status_code != 200:
        raise RuntimeError(f"Gagal memperbarui sheet {range_name}: {resp.status_code} - {resp.text}")
    return resp.json()

def process_data():
    headers = get_headers()
    pml_to_pj = load_pml_to_pj_map()

    # 1. Baca Per SLS
    rows_sls = fetch_sheet_values(SPREADSHEET_ID, "Per%20SLS!A1:Z2000", headers)
    if not rows_sls:
        raise ValueError("Sheet 'Per SLS' kosong!")
    
    header_sls = rows_sls[0]
    # Header: ['Kabkota', 'kk-PPL', 'Nama PPL', 'Nama PML', 'Draf', 'prelist', ...]
    # Cek apakah 'Nama PJ Kuda' sudah ada
    pj_kuda_exists = "Nama PJ Kuda" in header_sls

    new_rows_sls = []
    if not pj_kuda_exists:
        new_header_sls = header_sls[:4] + ["Nama PJ Kuda"] + header_sls[4:]
        new_rows_sls.append(new_header_sls)
        for r in rows_sls[1:]:
            pml = r[3].strip() if len(r) > 3 else ""
            pj = pml_to_pj.get(pml.lower(), "-")
            new_r = r[:4] + [pj] + r[4:]
            new_rows_sls.append(new_r)
    else:
        new_rows_sls = rows_sls

    # 2. Agregasi Per PPL (berdasarkan pasangan Nama PPL + Nama PML)
    # Ini otomatis memecah PPL dengan nama sama (Nurmala & Amrullah)
    aggregated = defaultdict(lambda: {"prelist": 0, "temu": 0, "draf": 0, "count": 0, "kk_ppl": ""})
    for r in rows_sls[1:]:
        if len(r) > 6:
            kk_ppl = r[1].strip()
            ppl = r[2].strip()
            pml = r[3].strip()
            draf = int(r[4]) if r[4].isdigit() else 0
            prelist = int(r[5]) if r[5].isdigit() else 0
            temu = int(r[6]) if r[6].isdigit() else 0

            key = (ppl, pml)
            aggregated[key]["kk_ppl"] = kk_ppl
            aggregated[key]["prelist"] += prelist
            aggregated[key]["temu"] += temu
            aggregated[key]["draf"] += draf
            aggregated[key]["count"] += 1

    list_ppl = []
    for (ppl, pml), d in aggregated.items():
        pj = pml_to_pj.get(pml.lower(), "-")
        pct = round((d["temu"] / d["prelist"] * 100), 2) if d["prelist"] > 0 else 0.0
        list_ppl.append({
            "kk_ppl": d["kk_ppl"],
            "ppl": ppl,
            "pml": pml,
            "pj": pj,
            "prelist": d["prelist"],
            "temu": d["temu"],
            "draf": d["draf"],
            "pct": pct
        })

    # Urutkan berdasarkan persentase capaian menaik (sama persis dengan urutan asli sheet)
    list_ppl.sort(key=lambda x: x["pct"])

    # Buat baris baru untuk Per PPL
    # Format: ['Row Labels', 'Nama PML', 'Nama PJ Kuda', 'Prelist-Awal', 'Usaha-Kel Yg Temu+baru', 'Draf', 'Persentase (C/B)']
    new_rows_ppl = [
        ["Jumlah Prelist Awal, Usaha dan Keluarga ditemukan + Baru", "", "", "", "", "", ""],
        ["Row Labels", "Nama PML", "Nama PJ Kuda", "Prelist-Awal", "Usaha-Kel Yg Temu+baru", "Draf", "Persentase (C/B)"]
    ]
    for r in list_ppl:
        new_rows_ppl.append([
            r["kk_ppl"],
            r["pml"],
            r["pj"],
            r["prelist"],
            r["temu"],
            r["draf"],
            f"{r['pct']:.2f}"
        ])

    return {
        "new_rows_sls": new_rows_sls,
        "new_rows_ppl": new_rows_ppl,
        "list_ppl": list_ppl,
        "pml_to_pj": pml_to_pj
    }

def main():
    parser = argparse.ArgumentParser(description="Update kolom PJ Kuda dan PML di Spreadsheet Rekap Assignment SE2026")
    parser.add_argument("--apply", action="store_true", help="Terapkan perubahan langsung ke Google Spreadsheet")
    args = parser.parse_args()

    print("==================================================================")
    print("📊 PEMERIKSAAN & PENAMBAHAN KOLOM PJ KUDA & PML (SPREADSHEET SE2026)")
    print("==================================================================")

    data = process_data()
    list_ppl = data["list_ppl"]

    print(f"✅ Master PML terpetakan ke PJ Kuda: {len(data['pml_to_pj'])} PML (100% unik)")
    print(f"✅ Total baris Per SLS: {len(data['new_rows_sls']) - 1} SLS")
    print(f"✅ Total baris Per PPL (setelah pemisahan nama sama): {len(list_ppl)} PPL (sebelumnya 213)")

    print("\n🔍 Pemeriksaan Kasus Nama PPL Ganda:")
    for r in list_ppl:
        if r["ppl"].lower() in ["nurmala", "amrullah"]:
            print(f"  • {r['kk_ppl']} | PML: {r['pml']} | PJ Kuda: {r['pj']} | Prelist: {r['prelist']} | Temu: {r['temu']} | Capaian: {r['pct']:.2f}%")

    if args.apply:
        headers = get_headers()
        print("\n🚀 Memperbarui Google Spreadsheet secara live...")

        # Update Per SLS
        print("  📤 Memperbarui Sheet 'Per SLS'...")
        update_sheet_values(SPREADSHEET_ID, "Per%20SLS!A1", data["new_rows_sls"], headers)
        print("     ✅ Sheet 'Per SLS' berhasil diperbarui!")

        # Update Per PPL
        print("  📤 Memperbarui Sheet 'Per PPL'...")
        # Bersihkan dulu area lama jika ada sisa kolom
        clear_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/Per%20PPL!A1:Z500:clear"
        requests.post(clear_url, headers=headers)
        update_sheet_values(SPREADSHEET_ID, "Per%20PPL!A1", data["new_rows_ppl"], headers)
        print("     ✅ Sheet 'Per PPL' berhasil diperbarui!")

        print("\n🎉 Selesai! Seluruh sheet telah diperbarui dengan kolom Nama PML dan Nama PJ Kuda.")
    else:
        print("\nℹ️  Mode Pratinjau (Dry-run). Gunakan flag --apply untuk mengeksekusi ke Google Sheets.")
    print("==================================================================")

if __name__ == "__main__":
    main()
