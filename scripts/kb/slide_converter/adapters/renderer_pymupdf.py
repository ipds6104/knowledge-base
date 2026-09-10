"""adapters/renderer_pymupdf.py — PyMuPDF Adapter implementing PDFRendererPort.

Tanggung Jawab Tunggal:
Merender halaman berkas PDF menjadi citra gambar base64 beresolusi tinggi menggunakan PyMuPDF (fitz).
"""

import base64
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz  # Fallback nama modul lama
    except ImportError:
        fitz = None

from ..ports import PDFRendererPort


class PyMuPDFRenderer(PDFRendererPort):
    """Implementasi konkrit perender PDF berbasis PyMuPDF."""

    def __init__(self, default_dpi: int = 200):
        if fitz is None:
            raise ImportError(
                "Library 'pymupdf' belum terpasang. Jalankan: pip install pymupdf"
            )
        self.default_dpi = default_dpi

    def get_page_count(self, pdf_path: Path) -> int:
        """Mengambil jumlah total halaman dalam PDF."""
        doc = fitz.open(str(pdf_path))
        try:
            return len(doc)
        finally:
            doc.close()

    def render_page_to_base64(self, pdf_path: Path, page_index: int, dpi: int = None) -> str:
        """Merender satu halaman slide tertentu ke string base64 PNG."""
        effective_dpi = dpi or self.default_dpi
        doc = fitz.open(str(pdf_path))
        try:
            if page_index < 0 or page_index >= len(doc):
                raise IndexError(
                    f"Indeks halaman {page_index} di luar jangkauan (total: {len(doc)})."
                )
            page = doc.load_page(page_index)
            pixmap = page.get_pixmap(dpi=effective_dpi)
            img_bytes = pixmap.tobytes("png")
            return base64.b64encode(img_bytes).decode("utf-8")
        finally:
            doc.close()
