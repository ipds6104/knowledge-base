"""CLI Handler Subcommand 'kb podes' for Potensi Desa (PODES) Publication Engine."""

import sys
from typing import List
from .podes_generator import generate_podes_publication, PODES_VILLAGE_CONFIGS
from .cmd_gdrive_mirror import run_gdrive_mirror


def register_podes_subparser(subparsers):
    """Mendaftarkan subcommand 'podes' ke ArgumentParser CLI kb."""
    parser = subparsers.add_parser(
        "podes",
        help="Mengompilasi Publikasi Potensi Desa/Kelurahan (PODES 2025/2026) berstandar BPS",
    )
    parser.add_argument(
        "desa_name",
        nargs="?",
        default=None,
        help="Nama desa/kelurahan dalam format kebab-case (misal: pasir-palembang, sungai-bakau-kecil, pasir-wan-salim)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Menggenerasikan publikasi PODES untuk seluruh desa/kelurahan di registri secara kolektif",
    )
    parser.add_argument(
        "--no-drive",
        action="store_true",
        help="Mematikan fungsi auto-upload ke Google Drive",
    )


def handle_podes(args):
    """Memproses eksekusi kompilasi publikasi Potensi Desa."""
    targets: List[str] = []

    if args.all:
        targets = list(PODES_VILLAGE_CONFIGS.keys())
    elif args.desa_name:
        key = args.desa_name.lower().strip()
        if key not in PODES_VILLAGE_CONFIGS:
            print(f"❌ Error: Nama desa '{args.desa_name}' tidak terdaftar di registri PODES.")
            print(f"   Daftar desa valid: {', '.join(PODES_VILLAGE_CONFIGS.keys())}")
            sys.exit(1)
        targets = [key]
    else:
        print("❌ Error: Harap tentukan nama desa (contoh: `kb podes pasir-palembang`) atau gunakan `--all`.")
        sys.exit(1)

    results = []
    for t in targets:
        print(f"\n=======================================================")
        print(f"  BPS PODES GENERATOR ENGINE — DESA {t.upper()}")
        print(f"=======================================================")
        res = generate_podes_publication(t)
        results.append(res)

        print(f"\n=======================================================")
        print(f"  SUKSES! PUBLIKASI POTENSI DESA BERHASIL DIBUAT")
        print(f"=======================================================")
        print(f"  1. Markdown : {res['md']}")
        print(f"  2. HTML     : {res['html']}")
        print(f"  3. PDF      : {res['pdf']}")

    if not args.no_drive:
        print("\n🚀 Memulai auto-upload publikasi PODES ke Google Drive...")
        class DriveArgs:
            source_path = "kegiatan/desa-cantik"
            folder_id = None
            dry_run = False
            force = False
        run_gdrive_mirror(DriveArgs())

