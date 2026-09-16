"""
PDF Geometry Inspector using PyMuPDF.
Single Responsibility: Parses physical PDF pages into PageGeometry models with exact metric coordinates (cm).
"""

from pathlib import Path
from typing import List, Union
from .models import PageGeometry, TextBlock

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        raise ImportError(
            "PyMuPDF tidak ditemukan. Silakan pasang paket 'pymupdf' untuk menjalankan audit PDF."
        )

# Conversion factor: 1 point = 1/72 inch = 2.54 / 72 cm = 0.0352777778 cm
PT_TO_CM = 0.0352777778


class PdfInspector:
    """Extracts geometric layout and coordinate bounding boxes from a PDF file."""

    def __init__(self, pdf_path: Union[str, Path]):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Berkas PDF tidak ditemukan: {self.pdf_path}")

    def inspect_pages(self) -> List[PageGeometry]:
        """Inspects all pages and extracts PageGeometry objects."""
        doc = fitz.open(str(self.pdf_path))
        geometries: List[PageGeometry] = []

        try:
            for page_idx in range(len(doc)):
                page = doc[page_idx]
                rect = page.rect
                width_cm = rect.width * PT_TO_CM
                height_cm = rect.height * PT_TO_CM

                raw_blocks = page.get_text("blocks")
                text_blocks: List[TextBlock] = []

                for b in raw_blocks:
                    # b format: (x0, y0, x1, y1, text, block_no, block_type)
                    content = b[4].strip()
                    if not content:
                        continue

                    x0_cm = b[0] * PT_TO_CM
                    y0_cm = b[1] * PT_TO_CM
                    x1_cm = b[2] * PT_TO_CM
                    y1_cm = b[3] * PT_TO_CM

                    text_blocks.append(
                        TextBlock(
                            text=content,
                            x0=round(x0_cm, 3),
                            y0=round(y0_cm, 3),
                            x1=round(x1_cm, 3),
                            y1=round(y1_cm, 3),
                        )
                    )

                geometries.append(
                    PageGeometry(
                        page_number=page_idx + 1,
                        width_cm=round(width_cm, 2),
                        height_cm=round(height_cm, 2),
                        blocks=text_blocks,
                    )
                )
        finally:
            doc.close()

        return geometries
