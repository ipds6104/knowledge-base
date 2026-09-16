"""
Duplex Printability and Page Count Rule.
Single Responsibility: Verifies even total page count and verso positioning of back cover for duplex printing.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class DuplexPrintabilityRule(AuditRule):
    """Memverifikasi kesiapan cetak bolak-balik (duplex): total halaman genap & kover belakang di Verso."""

    @property
    def rule_id(self) -> str:
        return "R06_DUPLEX_PRINTABILITY"

    @property
    def name(self) -> str:
        return "Kesiapan Cetak Dupleks (Total Halaman Genap & Kover Belakang Verso)"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.1.1 & Subbab 4.4.2 (Hal. 44, 91)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        total_p = len(pages)

        # 1. Check Even Total Pages
        if total_p % 2 != 0:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=total_p,
                    message="Total halaman buku berjumlah ganjil; berisiko merusak pencetakan bolak-balik (duplex).",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value=f"{total_p} halaman (ganjil)",
                    expected_value="Jumlah halaman genap",
                )
            )

        # 2. Check Back Cover on Verso (Even Page)
        if total_p > 0:
            last_page = pages[-1]
            if not last_page.is_verso:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=total_p,
                        message="Kover belakang berada pada lembar Rekto (ganjil). Harus selalu berada di lembar Verso (genap).",
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value=f"Halaman {total_p} (Rekto)",
                        expected_value="Halaman genap (Verso)",
                    )
                )

        return violations
