"""service.py — Orchestrator Use Case for Slide-to-Markdown Conversion.

Mengikuti Clean Architecture (Hexagonal Architecture):
Service ini murni bertindak sebagai orkestrator use-case.
Tidak bergantung pada pustaka konkret (PyMuPDF, HTTP client), melainkan
bergantung murni pada Ports (PDFRendererPort, VisionClientPort, MarkdownWriterPort)
yang diinjeksikan secara eksplisit melalui Dependency Injection (DI).
"""

from pathlib import Path
from typing import Callable, Optional

from .domain import ConversionResult, SlidePage
from .ports import MarkdownWriterPort, PDFRendererPort, VisionClientPort

# Tipe callback untuk memonitor progres: (slide_sekarang, total_slide, pesan_status)
ProgressCallback = Callable[[int, int, str], None]


class SlideConverterService:
    """Use case orchestrator yang mengoordinasikan konversi slide PDF ke Markdown."""

    def __init__(
        self,
        renderer: PDFRendererPort,
        vision_client: VisionClientPort,
        writer: MarkdownWriterPort,
    ):
        self.renderer = renderer
        self.vision_client = vision_client
        self.writer = writer

    def convert(
        self,
        pdf_path: Path,
        output_path: Path,
        on_progress: Optional[ProgressCallback] = None,
    ) -> ConversionResult:
        """Mengeksekusi proses konversi dari berkas PDF sumber ke berkas Markdown target."""
        if not pdf_path.exists():
            raise FileNotFoundError(f"Berkas PDF tidak ditemukan: {pdf_path}")

        total_pages = self.renderer.get_page_count(pdf_path)
        if total_pages == 0:
            raise ValueError(f"Berkas PDF kosong (0 halaman): {pdf_path}")

        slides: list[SlidePage] = []

        for page_idx in range(total_pages):
            slide_num = page_idx + 1

            if on_progress:
                on_progress(slide_num, total_pages, f"Merender visual slide {slide_num}...")

            # 1. Render halaman ke citra base64
            img_b64 = self.renderer.render_page_to_base64(pdf_path, page_idx)

            if on_progress:
                on_progress(
                    slide_num,
                    total_pages,
                    f"Menganalisis visual, diagram, & hierarki slide {slide_num}...",
                )

            # 2. Transkripsi visual slide via Vision Client Port
            markdown_content = self.vision_client.transcribe_slide(
                image_base64=img_b64,
                slide_number=slide_num,
                total_slides=total_pages,
            )

            slides.append(
                SlidePage(
                    slide_number=slide_num,
                    raw_markdown=markdown_content,
                )
            )

        # 3. Persistensi hasil ke media penyimpanan via Writer Port
        if on_progress:
            on_progress(total_pages, total_pages, "Menyimpan berkas Markdown akhir...")

        raw_slides = [s.raw_markdown for s in slides]
        self.writer.write(raw_slides, output_path)

        return ConversionResult(
            total_slides=total_pages,
            output_path=output_path,
            slides=slides,
            success=True,
        )
