"""Headless Chrome PDF Compilation Engine for DDA Publication Generator."""

import subprocess
import sys
from pathlib import Path


def compile_html_to_pdf(html_path: Path, pdf_path: Path) -> Path:
    """Mengompilasi berkas HTML ke PDF A4 Siap Cetak menggunakan Headless Chrome."""
    print(f"Mengompilasi PDF via Headless Chrome: {html_path} -> {pdf_path}...")

    chrome_candidates = [
        "google-chrome-stable",
        "google-chrome",
        "chromium-browser",
        "chromium",
    ]

    chrome_cmd = None
    for cand in chrome_candidates:
        try:
            res = subprocess.run(
                ["which", cand], capture_output=True, text=True, check=False
            )
            if res.returncode == 0 and res.stdout.strip():
                chrome_cmd = res.stdout.strip()
                break
        except Exception:
            continue

    if not chrome_cmd:
        print(
            "WARNING: Headless Chrome/Chromium tidak ditemukan pada PATH. Tidak dapat membuat PDF.",
            file=sys.stderr,
        )
        return None

    abs_html = html_path.resolve()
    abs_pdf = pdf_path.resolve()

    cmd = [
        chrome_cmd,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={abs_pdf}",
        f"file://{abs_html}",
    ]

    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode == 0 and abs_pdf.exists():
        print(f"PDF berhasil dibuat: {abs_pdf}")
        # Copy to outputs/ directory
        outputs_dir = Path("outputs")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        out_copy = outputs_dir / pdf_path.name
        with open(abs_pdf, "rb") as sf, open(out_copy, "wb") as df:
            df.write(sf.read())
        print(f"Salinan PDF disimpan di: {out_copy}")
        return abs_pdf
    else:
        print(f"Gagal mengompilasi PDF: {res.stderr}", file=sys.stderr)
        return None
