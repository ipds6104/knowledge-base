"""
Book Page Threshold and Proportions Compliance Rule.
Single Responsibility: Verifies that publication meets minimum book thickness (>= 48 pages),
even preliminary count, and valid ratio between roman and arabic pages.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class BookPageThresholdRule(AuditRule):
    """Memverifikasi ambang tebal buku (>= 48 hal), total halaman prelims genap, dan proporsi romawi vs arab."""

    @property
    def rule_id(self) -> str:
        return "R08_BOOK_PAGE_THRESHOLD"

    @property
    def name(self) -> str:
        return "Ambang Tebal Buku (>= 48 Hal) & Proporsi Halaman Romawi vs Arab"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Bab 1 (Hal. 7) & Subbab 4.1.3 Poin 3 & 10 (Hal. 46-47)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []
        total_p = len(pages)

        # 1. Ambang Tebal Buku (minimal 48-49 halaman untuk kategori buku publikasi resmi)
        if total_p < 48:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    rule_name=self.name,
                    physical_page=total_p,
                    message=f"Ketebalan publikasi ({total_p} hal) di bawah ambang minimal buku resmi BPS (48-49 halaman); dikategorikan sebagai Buklet.",
                    pedoman_ref=self.pedoman_ref,
                    severity=Severity.WARNING,
                    measured_value=f"{total_p} halaman",
                    expected_value=">= 48 halaman",
                )
            )

        # Find transition to Arabic page 1 (Bab 1)
        body_start_idx = -1
        for idx, page in enumerate(pages):
            if "BAB 1:" in page.full_text.upper():
                body_start_idx = idx
                break

        if body_start_idx != -1:
            prelim_count = body_start_idx  # 0 to body_start_idx - 1
            body_count = total_p - prelim_count

            # 2. Total Halaman Pendahuluan WAJIB GENAP [Poin 3, Hal. 46]
            if prelim_count % 2 != 0:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=prelim_count,
                        message=f"Jumlah total lembar pendahuluan ({prelim_count} hal) ganjil. Wajib disisipkan 1 halaman kosong agar genap.",
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value=f"{prelim_count} halaman pendahuluan (ganjil)",
                        expected_value="Jumlah halaman pendahuluan genap",
                    )
                )

            # 3. Batas Jumlah Romawi vs Arab [Poin 10, Hal. 47]: Romawi TIDAK BOLEH LEBIH BANYAK dari Arab
            if prelim_count >= body_count:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=prelim_count,
                        message=f"Jumlah halaman pendahuluan ({prelim_count}) tidak boleh lebih banyak atau sama dengan halaman isi ({body_count}).",
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value=f"Prelims: {prelim_count}, Isi: {body_count}",
                        expected_value="Prelims < Isi",
                    )
                )

        return violations
