"""
Early Prelims Physical Number Suppression Compliance Rule.
Single Responsibility: Verifies physical page numbers are suppressed on Hal. i s.d. iv.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class EarlyPrelimsSuppressionRule(AuditRule):
    """Memverifikasi bahwa nomor halaman fisik tidak dicetak pada 4 halaman awal prelims (i, ii, iii, iv)."""

    @property
    def rule_id(self) -> str:
        return "R14_EARLY_PRELIMS_SUPPRESSION"

    @property
    def name(self) -> str:
        return "Penekanan Nomor Fisik Awal Prelims (Hal. i s.d. iv)"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.1.3 Poin 9 (Hal. 47) & Hal. 81"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []

        # Target physical pages 3, 4, 5, 6 (0-indexed indices 2, 3, 4, 5)
        for page_idx in [2, 3, 4, 5]:
            if page_idx >= len(pages):
                break

            page = pages[page_idx]
            footer_text = " ".join(b.text for b in page.footer_blocks).strip().lower()

            forbidden_tokens = ["i", "ii", "iii", "iv"]
            words = footer_text.split()
            for token in forbidden_tokens:
                if token in words or footer_text == token:
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            rule_name=self.name,
                            physical_page=page.page_number,
                            message=(
                                f"Nomor romawi fisik '{token}' tercetak pada footer halaman {page.page_number}. "
                                "Pedoman BPS mewajibkan nomor halaman pada Hal. i s.d. iv disembunyikan (suppressed)."
                            ),
                            pedoman_ref=self.pedoman_ref,
                            severity=Severity.ERROR,
                            measured_value=f"Tercetak '{token}' di footer",
                            expected_value="Footer kosong (nomor fisik disembunyikan)",
                        )
                    )
                    break

        return violations
