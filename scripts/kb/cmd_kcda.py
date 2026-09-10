"""CLI Handler Subcommand 'kb kcda' for Kecamatan Dalam Angka (KCDA) 2026 Engine."""

import os
import sys
import json
import glob
from pathlib import Path
from .kcda_audit import run_kcda_audit, download_all_kcda_tables
from .kcda_generator.compiler import compile_kecamatan, compile_all_kcda
from .kcda_generator.uploader import upload_kcda_drafts
from .kcda_generator.config import KCDA_KECAMATAN_CONFIG

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
        choices=["audit", "sync", "report", "build"],
        help="Aksi: 'audit' (evaluasi kesiapan data), 'sync' (unduh ulang tabel dari Sheets), 'build' (kompilasi naskah Typst/PDF)",
    )
    parser.add_argument(
        "--kecamatan", "-k",
        default=None,
        help="Nama spesifik kecamatan (contoh: 'jongkat', 'mempawah-hilir', 'sungai-pinyuh')",
    )
    parser.add_argument(
        "--upload", "-u",
        action="store_true",
        help="Unggah draf PDF yang dihasilkan langsung ke Google Drive subfolder '3. Draft Publikasi'",
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
    elif action == "build":
        if args.kecamatan:
            slug = args.kecamatan.lower().strip()
            # Handle user typing 'Mempawah Hilir' instead of 'mempawah-hilir'
            slug = slug.replace("kecamatan ", "").replace(" ", "-")
            if slug not in KCDA_KECAMATAN_CONFIG:
                for k, v in KCDA_KECAMATAN_CONFIG.items():
                    if slug in k:
                        slug = k
                        break
            print(f"🚀 Memulai kompilasi KCDA 2026 untuk: {slug}...")
            res = compile_kecamatan(slug)
            print(f"✅ Selesai: {res['pdf_path']} ({res['pages']} hal, {res['file_size_kb']} KB, {res['duration_sec']}s)")
            if args.upload:
                upload_kcda_drafts([res])
        else:
            results = compile_all_kcda()
            if args.upload:
                upload_kcda_drafts(results)
