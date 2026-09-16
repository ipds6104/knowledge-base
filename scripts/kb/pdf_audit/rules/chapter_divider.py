"""
Chapter Divider Compliance Rule.
Single Responsibility: Verifies that chapter opener pages contain NO running header and NO running footer.
"""

import re
from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class ChapterDividerRule(AuditRule):
    """Memverifikasi bahwa lembar pembatas bab (Bab 1 s.d. Bab 7) bebas running title dan nomor fisik."""

    @property
    def rule_id(self) -> str:
        return "R03_CHAPTER_DIVIDER_CLEAN"

    @property
    def name(self) -> str:
        return "Suppresi Header & Footer pada Halaman Pembatas Bab"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.1.3 Poin 9 & Subbab 4.4.1 (Hal. 47, 88)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        bab_pattern = re.compile(r"BAB\s+[1-7]:", re.IGNORECASE)

        for page in pages:
            # Check if this page contains a chapter divider heading
            is_divider_page = False
            for block in page.blocks:
                if bab_pattern.search(block.text):
                    is_divider_page = True
                    break

            if not is_divider_page:
                continue

            # 1. Check for forbidden running header (y <= 1.4 cm)
            if page.header_blocks:
                header_text = " | ".join(b.text.replace("\n", " ") for b in page.header_blocks)
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=page.page_number,
                        message=f"Halaman pembatas bab dilarang memuat kepala halaman (running head).",
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value=f"Ditemukan header: '{header_text[:40]}'",
                        expected_value="Tanpa kepala halaman (running head)",
                    )
                )

            # 2. Check for forbidden running footer (y >= 19.4 cm)
            if page.footer_blocks:
                footer_text = " | ".join(b.text.replace("\n", " ") for b in page.footer_blocks)
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=page.page_number,
                        message=f"Halaman pembatas bab dilarang memuat nomor halaman fisik atau kaki halaman.",
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value=f"Ditemukan footer: '{footer_text[:40]}'",
                        expected_value="Tanpa kaki halaman / nomor fisik",
                    )
                )

            # 3. Check that chapter divider always starts on Rekto (Odd/Kanan)
            if not page.is_recto:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=page.page_number,
                        message="Halaman pembatas bab harus selalu berada pada lembar Rekto (muka kanan/halaman ganjil).",
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value=f"Halaman genap (Verso)",
                        expected_value="Halaman ganjil (Rekto)",
                    )
                )

        return violations
