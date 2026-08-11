"""Automated Headless Chrome PDF & DOCX Compiler Module for PODES Generator."""

import subprocess
from pathlib import Path


def compile_podes_pdf(html_path: Path, config: dict) -> Path:
    """Mengompilasi berkas HTML ke PDF A4 via Headless Chrome dan DOCX via pdf2docx."""
    name_kebab = config["name_kebab"]
    year = config.get("year", 2026)

    out_dir = Path("kegiatan") / "desa-cantik" / str(year) / name_kebab
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"publikasi-potensi-{name_kebab}-{year}.pdf"

    cmd = [
        "google-chrome-stable",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        str(html_path),
    ]

    print(f"Mengompilasi PDF PODES via Headless Chrome: {html_path} -> {pdf_path}...")
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode == 0:
        print(f"PDF PODES berhasil dibuat: {pdf_path}")
        outputs_dir = Path("outputs")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        copy_pdf_path = outputs_dir / f"publikasi-potensi-{name_kebab}-{year}.pdf"
        subprocess.run(["cp", str(pdf_path), str(copy_pdf_path)])
        print(f"Salinan PDF PODES disimpan di: {copy_pdf_path}")

        # Compile DOCX from PDF
        try:
            from pdf2docx import Converter
            docx_filename = f"publikasi-potensi-{name_kebab}-{year}.docx"
            docx_path = out_dir / docx_filename
            copy_docx_path = outputs_dir / docx_filename

            print(f"Mengompilasi DOCX dari PDF PODES...")
            cv = Converter(str(pdf_path))
            cv.convert(str(docx_path), start=0, end=None)
            cv.close()

            subprocess.run(["cp", str(docx_path), str(copy_docx_path)])
            print(f"DOCX PODES berhasil dibuat: {docx_path} & {copy_docx_path}")
        except Exception as err:
            print(f"Peringatan: Gagal mengompilasi DOCX PODES: {err}")

        return pdf_path
    else:
        print(f"Gagal mengompilasi PDF PODES: {res.stderr}")
        raise RuntimeError(f"Chrome Headless compilation failed: {res.stderr}")
