"""
Flyleaf Compliance Rule.
Single Responsibility: Verifies physical page 2 (flyleaf / balik kover luar) is 100% empty.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class FlyleafRule(AuditRule):
    """Memverifikasi bahwa Halaman 2 (balik kover depan) adalah halaman kosong pelindung."""

    @property
    def rule_id(self) -> str:
        return "R01_FLYLEAF_BLANK"

    @property
    def name(self) -> str:
        return "Halaman Kosong Pelindung (Flyleaf) di Balik Kover Luar"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.1.2 Poin 6 (Hal. 45)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        if len(pages) < 2:
            return violations

        page2 = pages[1]  # 0-indexed index 1 is Physical Page 2
        if not page2.is_blank:
            sample_text = page2.full_text[:40]
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=2,
                    message="Halaman 2 (balik kover depan) tidak kosong; ditemukan teks/elemen cetak.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value=f"{len(page2.blocks)} blok teks: '{sample_text}...' ",
                    expected_value="0 blok teks (halaman kosong sempurna)",
                )
            )

        return violations
