"""Automated Headless Chrome PDF Compiler Module for DDA Generator."""

import os
import subprocess
from pathlib import Path


def compile_pdf(html_path: Path, config: dict) -> Path:
    """Mengompilasi berkas HTML ke PDF A4 bebas header/footer via Headless Chrome."""
    name_kebab = config["name_kebab"]
    year = config.get("year", 2026)

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"publikasi-desa-{name_kebab}-dalam-angka-{year}.pdf"

    cmd = [
        "google-chrome-stable",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        str(html_path),
    ]

    print(f"Mengompilasi PDF via Headless Chrome: {html_path} -> {pdf_path}...")
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode == 0:
        print(f"PDF berhasil dibuat: {pdf_path}")
        outputs_dir = Path("outputs")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        copy_pdf_path = outputs_dir / f"publikasi-desa-{name_kebab}-dalam-angka-{year}.pdf"
        subprocess.run(["cp", str(pdf_path), str(copy_pdf_path)])
        print(f"Salinan PDF disimpan di: {copy_pdf_path}")
        return pdf_path
    else:
        print(f"Gagal mengompilasi PDF: {res.stderr}")
        raise RuntimeError(f"Chrome Headless compilation failed: {res.stderr}")
