"""
Frontmatter Anatomy and Roman Numbering Compliance Rule.
Single Responsibility: Verifies sequence of preliminary pages and Roman numbering suppression/recto-verso alignment.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class FrontmatterSequenceRule(AuditRule):
    """Memverifikasi urutan anatomi prelims dan penomoran romawi kecil sesuai standar BPS."""

    @property
    def rule_id(self) -> str:
        return "R02_FRONTMATTER_ANATOMY"

    @property
    def name(self) -> str:
        return "Urutan Anatomi Prelims & Penomoran Romawi Rekto-Verso"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.1.3 Poin 1-3 (Hal. 46) & Subbab 4.3 (Hal. 75)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        if len(pages) < 8:
            return violations

        # P3: Judul Utama (Rekto/Kanan) - Nomor fisik disembunyikan
        p3 = pages[2]
        if not p3.is_recto:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=3,
                    message="Halaman Judul Utama (Hal. i) harus berada pada lembar Rekto (muka kanan/ganjil).",
                    pedoman_ref=self.pedoman_ref,
                )
            )
        if p3.footer_blocks:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=3,
                    message="Nomor halaman fisik tidak boleh dicetak pada Halaman Judul Utama (Hal. i).",
                    pedoman_ref=self.pedoman_ref,
                    measured_value=p3.footer_blocks[0].text,
                    expected_value="Tanpa nomor fisik",
                )
            )

        # P4: Katalog & Hak Cipta (Verso/Kiri) - Nomor fisik disembunyikan
        p4 = pages[3]
        if not p4.is_verso:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=4,
                    message="Halaman Katalog & Hak Cipta (Hal. ii) harus berada pada lembar Verso (muka kiri/genap).",
                    pedoman_ref=self.pedoman_ref,
                )
            )
        if p4.footer_blocks:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=4,
                    message="Nomor halaman fisik tidak boleh dicetak pada Halaman Katalog (Hal. ii).",
                    pedoman_ref=self.pedoman_ref,
                    measured_value=p4.footer_blocks[0].text,
                    expected_value="Tanpa nomor fisik",
                )
            )

        # P5 & P6: Tim Penyusun (iii) & Kontributor (iv) - Nomor fisik disembunyikan
        for p_idx, page_label in [(4, "Tim Penyusun (Hal. iii)"), (5, "Kontributor Data (Hal. iv)")]:
            p = pages[p_idx]
            if p.footer_blocks:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=p.page_number,
                        message=f"Nomor halaman fisik tidak boleh dicetak pada {page_label}.",
                        pedoman_ref=self.pedoman_ref,
                        measured_value=p.footer_blocks[0].text,
                        expected_value="Tanpa nomor fisik",
                    )
                )

        # P7: Kata Pengantar (Rekto/Kanan) - Nomor romawi 'v' di Kanan Bawah
        p7 = pages[6]
        if not p7.is_recto:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=7,
                    message="Kata Pengantar (Hal. v) harus mulai pada lembar Rekto (muka kanan/ganjil).",
                    pedoman_ref=self.pedoman_ref,
                )
            )
        if not p7.footer_blocks or "v" not in p7.footer_blocks[-1].text.lower():
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=7,
                    message="Kata Pengantar harus memuat penomoran romawi fisik 'v' pada footer.",
                    pedoman_ref=self.pedoman_ref,
                    measured_value="Tidak ada nomor 'v'" if not p7.footer_blocks else p7.footer_blocks[-1].text,
                    expected_value="Nomor romawi 'v'",
                )
            )
        elif p7.footer_blocks:
            # Check alignment on right (x0 > 10 cm on A5 14.8 cm width)
            f_block = p7.footer_blocks[-1]
            if f_block.x0 < 10.0:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=7,
                        message="Nomor halaman romawi ganjil ('v') harus rata kanan pada lembar Rekto.",
                        pedoman_ref=self.pedoman_ref,
                        measured_value=f"x0 = {f_block.x0:.2f} cm",
                        expected_value="x0 >= 10.0 cm (rata kanan)",
                    )
                )

        # P8: Preface (Verso/Kiri) - Nomor romawi 'vi' di Kiri Bawah
        p8 = pages[7]
        if not p8.is_verso:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=8,
                    message="Preface (Hal. vi) harus berada pada lembar Verso (muka kiri/genap).",
                    pedoman_ref=self.pedoman_ref,
                )
            )
        if not p8.footer_blocks or "vi" not in p8.footer_blocks[-1].text.lower():
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=8,
                    message="Preface harus memuat penomoran romawi fisik 'vi' pada footer.",
                    pedoman_ref=self.pedoman_ref,
                    measured_value="Tidak ada nomor 'vi'" if not p8.footer_blocks else p8.footer_blocks[-1].text,
                    expected_value="Nomor romawi 'vi'",
                )
            )
        elif p8.footer_blocks:
            # Check alignment on left (x0 < 4.0 cm on A5)
            f_block = p8.footer_blocks[-1]
            if f_block.x0 > 4.0:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=8,
                        message="Nomor halaman romawi genap ('vi') harus rata kiri pada lembar Verso.",
                        pedoman_ref=self.pedoman_ref,
                        measured_value=f"x0 = {f_block.x0:.2f} cm",
                        expected_value="x0 <= 4.0 cm (rata kiri)",
                    )
                )

        return violations
