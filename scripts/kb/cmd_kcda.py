"""CLI Handler Subcommand 'kb kcda' for Kecamatan Dalam Angka (KCDA) 2026 Engine."""

import os
import sys
import json
import glob
from pathlib import Path
from .kcda_audit import run_kcda_audit, download_all_kcda_tables


def register_kcda_subparser(subparsers):
    """Mendaftarkan subcommand 'kcda' ke ArgumentParser CLI kb."""
    parser = subparsers.add_parser(
        "kcda",
        help="Pengelolaan, audit kesiapan data, dan kompilasi publikasi Kecamatan Dalam Angka (KCDA) 2026",
    )
    parser.add_argument(
        "action",
        nargs="?",
        default="audit",
        choices=["audit", "sync", "report"],
        help="Aksi: 'audit' (evaluasi kesiapan data 9 kecamatan), 'sync' (unduh ulang 35 tabel dari Google Sheets), 'report' (tampilkan ringkasan)",
    )
    parser.add_argument(
        "--kecamatan", "-k",
        default=None,
        help="Nama spesifik kecamatan (contoh: 'Jongkat', 'Mempawah Hilir')",
    )


def handle_kcda(args):
    """Memproses eksekusi subcommand kcda."""
    action = args.action
    if action == "sync":
        print("🔄 Memulai sinkronisasi 35 nested spreadsheet KCDA 2026...")
        download_all_kcda_tables()
        print("✅ Sinkronisasi selesai. Menjalankan audit...")
        run_kcda_audit(filter_kec=args.kecamatan)
    elif action in ["audit", "report"]:
        run_kcda_audit(filter_kec=args.kecamatan)
