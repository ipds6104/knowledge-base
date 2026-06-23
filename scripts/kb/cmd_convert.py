"""kb/cmd_convert.py — Implementasi perintah `kb convert` (PDF → Markdown)."""

import base64
import glob
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from .colors import Colors
from .utils import load_env


def cmd_convert(args) -> None:
    """Konversi dokumen PDF ke Markdown menggunakan AI Vision atau pdftotext."""
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"{Colors.FAIL}Error: Berkas PDF tidak ditemukan di {pdf_path}{Colors.ENDC}")
        sys.exit(1)

    output_md = pdf_path.with_suffix('.md')

    if args.ai:
        _convert_ai(pdf_path, output_md)
    else:
        _convert_pdftotext(pdf_path, output_md)

    print(f"{Colors.GREEN}Sukses! Hasil konversi disimpan di: {output_md}{Colors.ENDC}")


# ─── Private helpers ──────────────────────────────────────────────────────────

def _convert_pdftotext(pdf_path: Path, output_md: Path) -> None:
    """Konversi cepat menggunakan pdftotext (tanpa AI)."""
    print(f"{Colors.BLUE}Memulai konversi cepat PDF menggunakan pdftotext...{Colors.ENDC}")
    try:
        subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), str(output_md)],
            check=True,
        )
    except subprocess.SubprocessError as e:
        print(f"{Colors.FAIL}Error: pdftotext gagal melakukan konversi: {e}{Colors.ENDC}")
        sys.exit(1)


def _convert_ai(pdf_path: Path, output_md: Path) -> None:
    """Konversi presisi tinggi menggunakan AI Vision (Gemini Proxy)."""
    print(f"{Colors.BLUE}Memulai konversi PDF menggunakan AI Vision (Gemini Proxy)...{Colors.ENDC}")

    config = load_env()
    api_url = config.get("AI_PROXY_URL")
    api_key = config.get("AI_API_KEY")
    model = config.get("AI_MODEL", "gemini-3-flash")

    if not api_url or not api_key:
        print(
            f"{Colors.FAIL}Error: API proxy tidak terkonfigurasi. "
            f"Pastikan berkas .env terisi dengan benar.{Colors.ENDC}"
        )
        sys.exit(1)

    print(f"Menggunakan Model: {model}")

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Mengekstrak halaman PDF menjadi gambar di folder temp...")
        prefix = os.path.join(tmpdir, "page")

        try:
            subprocess.run(
                ["pdftoppm", "-png", "-r", "150", str(pdf_path), prefix],
                check=True,
            )
        except subprocess.SubprocessError as e:
            print(f"{Colors.FAIL}Error saat mengekstrak halaman PDF: {e}{Colors.ENDC}")
            sys.exit(1)

        image_files = sorted(glob.glob(os.path.join(tmpdir, "page-*.png")))
        if not image_files:
            print(f"{Colors.FAIL}Error: Tidak ada gambar halaman yang berhasil diekstrak.{Colors.ENDC}")
            sys.exit(1)

        print(f"Ditemukan {len(image_files)} halaman untuk diproses.")

        markdown_pages = []
        for idx, img_path in enumerate(image_files, 1):
            print(f"Memproses halaman {idx} dari {len(image_files)}...")
            with open(img_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Convert this document page image to Markdown format. "
                                    "Preserve layout, headings, lists, tables (using pipe tables), "
                                    "and exact text. Do not include code block wrappers like "
                                    "```markdown in the output, just raw markdown."
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                            },
                        ],
                    }
                ],
                "temperature": 0.1,
            }

            req = urllib.request.Request(
                api_url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                method="POST",
            )

            try:
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    text = res_data["choices"][0]["message"]["content"]
                    markdown_pages.append(text)
            except urllib.error.URLError as e:
                print(f"{Colors.FAIL}API Error di Halaman {idx}: {e}{Colors.ENDC}")
                sys.exit(1)
            except Exception as e:
                print(f"{Colors.FAIL}Error tidak dikenal di Halaman {idx}: {e}{Colors.ENDC}")
                sys.exit(1)

        full_markdown = "\n\n<!-- PAGE BREAK -->\n\n".join(markdown_pages)
        output_md.write_text(full_markdown, encoding='utf-8')
