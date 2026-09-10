"""Compiler module for KCDA 2026 Typst documents."""

import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from .config import KCDA_KECAMATAN_CONFIG
from .builder import build_kcda_typst

def get_page_count(pdf_path: str) -> Optional[int]:
    """Mendapatkan jumlah halaman PDF menggunakan pdfinfo jika tersedia."""
    try:
        res = subprocess.run(["pdfinfo", pdf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        for line in res.stdout.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":")[1].strip())
    except Exception:
        pass
    return None

def compile_kecamatan(slug: str, output_dir: str = "kegiatan/kecamatan-dalam-angka/2026/outputs") -> Dict[str, Any]:
    """Mengompilasi naskah Typst untuk satu kecamatan."""
    cfg = KCDA_KECAMATAN_CONFIG.get(slug)
    if not cfg:
        raise ValueError(f"Kecamatan slug '{slug}' tidak ditemukan.")

    t0 = time.time()
    out_base = Path(output_dir) / slug
    out_base.mkdir(parents=True, exist_ok=True)

    typ_path = out_base / f"kcda-2026-{slug}.typ"
    pdf_path = out_base / f"kcda-2026-{slug}.pdf"

    # Generate Typst content
    typst_code = build_kcda_typst(slug)
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write(typst_code)

    # Compile via typst CLI
    cmd = ["typst", "compile", str(typ_path), str(pdf_path)]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Typst compilation failed for {slug}:\n{res.stderr}")

    duration = round(time.time() - t0, 2)
    file_size_kb = round(os.path.getsize(pdf_path) / 1024, 1)
    pages = get_page_count(str(pdf_path))

    return {
        "slug": slug,
        "nama_resmi": cfg["nama_resmi"],
        "no_publikasi": cfg["no_publikasi"],
        "typ_path": str(typ_path),
        "pdf_path": str(pdf_path),
        "file_size_kb": file_size_kb,
        "pages": pages,
        "duration_sec": duration,
        "status": "SUCCESS"
    }

def compile_all_kcda(output_dir: str = "kegiatan/kecamatan-dalam-angka/2026/outputs") -> List[Dict[str, Any]]:
    """Mengompilasi seluruh 9 kecamatan secara batch."""
    results = []
    print(f"🚀 Memulai kompilasi publikasi KCDA 2026 untuk 9 kecamatan...")
    for slug in KCDA_KECAMATAN_CONFIG.keys():
        print(f"   ⚙️  Mengompilasi: {KCDA_KECAMATAN_CONFIG[slug]['nama_resmi']} ({slug})...")
        try:
            res = compile_kecamatan(slug, output_dir)
            print(f"      ✅ Selesai ({res['pages']} halaman, {res['file_size_kb']} KB, {res['duration_sec']}s)")
            results.append(res)
        except Exception as e:
            print(f"      ❌ Gagal: {e}")
            results.append({
                "slug": slug,
                "nama_resmi": KCDA_KECAMATAN_CONFIG[slug]["nama_resmi"],
                "status": "FAILED",
                "error": str(e)
            })
    return results
