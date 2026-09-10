"""adapters/writer_local.py — Local File Markdown Writer implementing MarkdownWriterPort.

Tanggung Jawab Tunggal:
Menyimpan teks Markdown hasil konversi ke sistem berkas lokal dengan format baku.
"""

from pathlib import Path

from ..ports import MarkdownWriterPort


class LocalMarkdownWriter(MarkdownWriterPort):
    """Implementasi penulisan berkas Markdown ke media penyimpanan lokal."""

    def __init__(self, delimiter: str = "\n\n---\n\n"):
        self.delimiter = delimiter

    def write(self, slides_content: list[str], output_path: Path) -> None:
        """Menyimpan seluruh teks Markdown slide ke berkas output."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        full_content = self.delimiter.join(s.strip() for s in slides_content if s.strip())
        output_path.write_text(full_content + "\n", encoding="utf-8")
