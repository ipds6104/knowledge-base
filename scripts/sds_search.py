#!/usr/bin/env python3
"""Utilitas Pencarian Standar Data Statistik Nasional (SDSN) BPS.

Mencari variabel, konsep, dan klasifikasi statistik baku dari data/sds/.
"""

import sys
import json
import argparse
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "sds"


def load_json(filename):
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"Error: Berkas {filepath} tidak ditemukan.", file=sys.stderr)
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def search_sds(query, limit=10):
    data = load_json("standar_data.json")
    q = query.lower()
    results = []
    for item in data:
        nama = item.get("nama", "").lower()
        definisi = item.get("definisi", "").lower()
        kode = item.get("kode", "")
        konsep_list = [c.get("konsep", {}).get("nama", "").lower() for c in item.get("detailKonsep", [])]
        klas_list = [k.get("klasifikasi", {}).get("nama", "").lower() for k in item.get("detailKlasifikasi", [])]

        score = 0
        if q == nama or q == kode:
            score += 100
        elif q in nama:
            score += 50
        elif any(q in k for k in konsep_list):
            score += 30
        elif any(q in kl for kl in klas_list):
            score += 20
        elif q in definisi:
            score += 10

        if score > 0:
            results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:limit]]


def search_konsep(query, limit=10):
    data = load_json("konsep.json")
    q = query.lower()
    results = []
    for item in data:
        nama = item.get("nama", "").lower()
        definisi = item.get("definisi", "").lower()
        kode = item.get("kode", "").lower()
        if q in nama or q in definisi or q in kode:
            results.append(item)
    return results[:limit]


def search_klasifikasi(query, limit=10):
    data = load_json("klasifikasi.json")
    q = query.lower()
    results = []
    for item in data:
        nama = item.get("nama", "").lower()
        definisi = item.get("definisi", "").lower()
        kode = item.get("kode", "").lower()
        if q in nama or q in definisi or q in kode:
            results.append(item)
    return results[:limit]


def main():
    parser = argparse.ArgumentParser(
        description="Pencarian Cepat Standar Data Statistik Nasional (SDSN) BPS (Kepka 996/2025)"
    )
    parser.add_argument("query", help="Kata kunci pencarian (misal: 'stunting', 'jalan', 'sampah', 'asn')")
    parser.add_argument("--type", "-t", choices=["sds", "konsep", "klasifikasi", "all"], default="sds",
                        help="Tipe entitas yang dicari (default: sds)")
    parser.add_argument("--limit", "-n", type=int, default=5, help="Batas jumlah hasil (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output dalam format JSON mentah")

    args = parser.parse_args()

    if args.type == "sds" or args.type == "all":
        sds_results = search_sds(args.query, args.limit)
        if args.json and args.type == "sds":
            print(json.dumps(sds_results, indent=2, ensure_ascii=False))
            return

        print(f"\n🔍 Ditemukan {len(sds_results)} Standar Data Statistik untuk '{args.query}':")
        print("=" * 80)
        for i, item in enumerate(sds_results, 1):
            kode = item.get("kode")
            nama = item.get("nama").upper()
            satuan = item.get("satuan")
            ukuran = item.get("ukuran")
            definisi = item.get("definisi")
            konsep = ", ".join([c.get("konsep", {}).get("nama", "") for c in item.get("detailKonsep", [])])
            klas = ", ".join([k.get("klasifikasi", {}).get("nama", "") for k in item.get("detailKlasifikasi", [])])

            print(f"[{i}] KODE SDSN: {kode} — {nama}")
            print(f"    • Definisi    : {definisi}")
            print(f"    • Satuan      : {satuan} | Ukuran: {ukuran}")
            print(f"    • Konsep      : {konsep or '-'}")
            print(f"    • Klasifikasi : {klas or '-'}")
            print("-" * 80)

    if args.type in ["konsep", "all"]:
        konsep_res = search_konsep(args.query, args.limit)
        if args.json and args.type == "konsep":
            print(json.dumps(konsep_res, indent=2, ensure_ascii=False))
            return
        print(f"\n📖 Ditemukan {len(konsep_res)} Konsep Baku untuk '{args.query}':")
        print("=" * 80)
        for i, item in enumerate(konsep_res, 1):
            print(f"[{i}] [{item.get('kode')}] {item.get('nama').upper()}")
            print(f"    • Definisi : {item.get('definisi')}")
            print("-" * 80)

    if args.type in ["klasifikasi", "all"]:
        klas_res = search_klasifikasi(args.query, args.limit)
        if args.json and args.type == "klasifikasi":
            print(json.dumps(klas_res, indent=2, ensure_ascii=False))
            return
        print(f"\n🏷️  Ditemukan {len(klas_res)} Klasifikasi Baku untuk '{args.query}':")
        print("=" * 80)
        for i, item in enumerate(klas_res, 1):
            print(f"[{i}] [{item.get('kode')}] {item.get('nama').upper()}")
            print(f"    • Definisi : {item.get('definisi')}")
            kategori = item.get("detailKategori", [])
            if kategori:
                kategori_str = ", ".join([f"{k.get('kode').strip()}: {k.get('label')}" for k in kategori[:6]])
                print(f"    • Kategori : {kategori_str}")
            print("-" * 80)


if __name__ == "__main__":
    main()

