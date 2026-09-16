"""
Chapter Odd Page Start Compliance Rule.
Single Responsibility: Verifies that every chapter start / divider falls on a Recto (odd) page.
"""

import re
from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class ChapterOddStartRule(AuditRule):
    """Memverifikasi bahwa seluruh pembatas/awal bab dimulai pada halaman fisik ganjil (Rekto/Kanan)."""

    @property
    def rule_id(self) -> str:
        return "R12_CHAPTER_ODD_PAGE_START"

    @property
    def name(self) -> str:
        return "Awal Bab Wajib Halaman Ganjil / Rekto"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.1.3 Poin 7 (Hal. 47) & Subbab 4.4.1 (Hal. 88)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []

        for page in pages:
            # Cari deklarasi bab di body/full text
            m = re.search(r'\bBAB\s+([0-9IVXLCDM]+)', page.full_text)
            if m:
                # Periksa apakah halaman fisik genap (Verso/Kiri)
                if page.is_verso:
                    chapter_str = m.group(0).strip()
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            rule_name=self.name,
                            physical_page=page.page_number,
                            message=(
                                f"{chapter_str} dimulai pada halaman fisik genap (Hal. {page.page_number}). "
                                "Pedoman BPS mewajibkan setiap bab dimulai pada halaman ganjil (Rekto/Kanan)."
                            ),
                            pedoman_ref=self.pedoman_ref,
                            severity=Severity.ERROR,
                            measured_value=f"Halaman {page.page_number} (Verso/Genap)",
                            expected_value="Halaman Rekto/Ganjil",
                        )
                    )

        return violations
