"""
Explanatory Notes and Standard Symbols Compliance Rule.
Single Responsibility: Verifies Penjelasan Umum exists on Recto and documents official BPS statistical symbols.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class ExplanatoryNotesRule(AuditRule):
    """Memverifikasi kehadiran Penjelasan Umum dan pendefinisian notasi statistik baku BPS."""

    @property
    def rule_id(self) -> str:
        return "R17_EXPLANATORY_NOTES"

    @property
    def name(self) -> str:
        return "Standarisasi Penjelasan Umum & Notasi Statistik Baku"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.3 Poin 11 (Hal. 87) & Hal. 325-337"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        found_notes = False
        notes_page = None

        for page in pages[:15]:
            if "PENJELASAN UMUM" in page.full_text.upper() or "EXPLANATORY NOTES" in page.full_text.upper():
                found_notes = True
                notes_page = page
                break

        if not found_notes or notes_page is None:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=9,
                    message="Halaman Penjelasan Umum (Explanatory Notes) tidak ditemukan pada bagian prelims.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value="Tidak ditemukan",
                    expected_value="Ada halaman Penjelasan Umum",
                )
            )
            return violations

        # 1. Verifikasi dimulai di halaman ganjil (Rekto)
        if notes_page.is_verso:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=notes_page.page_number,
                    message=f"Penjelasan Umum berada di halaman fisik genap ({notes_page.page_number}). Pedoman BPS mewajibkan di halaman ganjil (Rekto).",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.ERROR,
                    measured_value=f"Halaman {notes_page.page_number} (Verso)",
                    expected_value="Halaman Rekto (Ganjil)",
                )
            )

        # 2. Verifikasi simbol statistik baku ('…' atau '...' dan '–' atau '-')
        has_dots = ("…" in notes_page.full_text or "..." in notes_page.full_text)
        has_dash = ("–" in notes_page.full_text or "-" in notes_page.full_text)
        if not (has_dots and has_dash):
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=notes_page.page_number,
                    message="Penjelasan Umum belum mendefinisikan secara lengkap notasi statistik baku ('…' data belum tersedia dan '–' data nol).",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.WARNING,
                    measured_value=notes_page.full_text[:60],
                    expected_value="Memuat notasi '…' dan '–'",
                )
            )

        return violations
