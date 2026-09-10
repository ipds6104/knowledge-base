#!/usr/bin/env python3
"""CLI Utility for Deterministic Verification of DDA Publication PDFs.

Usage:
    python scripts/verify_dda_pdf.py [nama-desa-kebab] [--pdf path/to/file.pdf] [--sheet-id ID] [--year 2026]
"""

import sys
import argparse
from pathlib import Path

# Insert scripts/ directory into sys.path
scripts_dir = Path(__file__).parent.resolve()
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from kb.dda_generator.verifier import verify_desa_publication


def main():
    parser = argparse.ArgumentParser(
        description="Verifikasi deterministik angka publikasi Desa Dalam Angka (PDF) terhadap Google Sheet."
    )
    parser.add_argument(
        "nama_desa",
        nargs="?",
        default="pasir-wan-salim",
        help="Nama desa dalam format kebab (contoh: 'pasir-wan-salim', 'sungai-bakau-kecil', 'pasir-palembang'). Default: pasir-wan-salim"
    )
    parser.add_argument(
        "--pdf",
        type=str,
        default=None,
        help="Path manual ke berkas PDF jika berbeda dari default."
    )
    parser.add_argument(
        "--sheet-id",
        type=str,
        default=None,
        help="Google Sheet ID override (opsional)."
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2026,
        help="Tahun publikasi (default: 2026)."
    )

    args = parser.parse_args()

    try:
        res = verify_desa_publication(
            name_kebab=args.nama_desa,
            pdf_path=args.pdf,
            sheet_id=args.sheet_id,
            year=args.year,
            verbose=True
        )
        if not res["all_matched"]:
            sys.exit(1)
        sys.exit(0)
    except Exception as e:
        print(f"Error saat verifikasi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
