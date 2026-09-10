"""cli.py — Standalone CLI entrypoint for Slide-to-Markdown converter."""

import argparse
import sys
from pathlib import Path

# Setup path agar modul bisa diimpor saat dijalankan langsung
current_dir = Path(__file__).parent.resolve()
scripts_dir = current_dir.parent.parent.resolve()
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from kb.colors import Colors
from kb.slide_converter import create_slide_converter
from kb.utils import load_env


def main():
    parser = argparse.ArgumentParser(
        description="Konversi slide presentasi PDF ke Markdown terstruktur (dengan diagram Mermaid & tabel visual).",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("pdf", type=str, help="Path ke berkas PDF slide presentasi")
    parser.add_argument(
        "output",
        type=str,
        nargs="?",
        default=None,
        help="Path berkas output Markdown (.md). Default: nama_file_sama.md",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model AI Vision yang digunakan (default: Top-Tools-Ai)",
    )

    args = parser.parse_args()
    pdf_path = Path(args.pdf).resolve()

    if not pdf_path.exists():
        print(f"{Colors.FAIL}Error: Berkas PDF '{pdf_path}' tidak ditemukan.{Colors.ENDC}")
        sys.exit(1)

    output_path = Path(args.output).resolve() if args.output else pdf_path.with_suffix(".md")

    config = load_env()
    if args.model:
        config["TOP_TOOLS_AI_MODEL"] = args.model

    converter = create_slide_converter(config)

    def on_progress(current: int, total: int, message: str):
        pct = int((current / total) * 100)
        print(f"{Colors.BLUE}[{pct:3d}%] Slide {current}/{total}: {message}{Colors.ENDC}")

    print(f"{Colors.HEADER}=== Slide to Markdown Converter (Hexagonal Architecture) ==={Colors.ENDC}")
    print(f"Berkas Sumber : {pdf_path}")
    print(f"Berkas Target : {output_path}")
    print(f"Engine AI     : Top Tools AI Vision\n")

    try:
        result = converter.convert(
            pdf_path=pdf_path,
            output_path=output_path,
            on_progress=on_progress,
        )
        print(f"\n{Colors.GREEN}✓ Selesai! Berhasil mengonversi {result.total_slides} slide.{Colors.ENDC}")
        print(f"{Colors.GREEN}✓ Hasil disimpan di: {result.output_path}{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}✗ Terjadi kesalahan saat konversi: {e}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
