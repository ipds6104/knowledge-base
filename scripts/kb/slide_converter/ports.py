"""ports.py — Interface-First Contracts for Slide-to-Markdown Converter.

Mengikuti prinsip Hexagonal Architecture (Ports & Adapters):
Mendefinisikan kontrak interface (Ports) sebelum implementasi konkret (Adapters).
"""

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class PDFRendererPort(Protocol):
    """Port untuk merender halaman berkas PDF menjadi representasi gambar."""

    def get_page_count(self, pdf_path: Path) -> int:
        """Mengambil jumlah total halaman dalam berkas PDF."""
        ...

    def render_page_to_base64(self, pdf_path: Path, page_index: int, dpi: int = 200) -> str:
        """Merender satu halaman tertentu (0-indexed) ke dalam string gambar base64 (PNG)."""
        ...


@runtime_checkable
class VisionClientPort(Protocol):
    """Port untuk berkomunikasi dengan model AI Multimodal / Vision."""

    def transcribe_slide(
        self,
        image_base64: str,
        slide_number: int,
        total_slides: int,
    ) -> str:
        """Mengirim gambar slide ke model AI dan mengembalikan teks Markdown hasil interpretasi."""
        ...


@runtime_checkable
class MarkdownWriterPort(Protocol):
    """Port untuk persistensi hasil konversi teks Markdown dan aset pendukung."""

    def write(self, slides_content: list[str], output_path: Path) -> None:
        """Menyimpan seluruh teks Markdown slide ke berkas output."""
        ...
