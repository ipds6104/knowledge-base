"""
Running Title Content Compliance Rule.
Single Responsibility: Verifies bilingual running titles (Book Title on Even/Verso, Chapter Title on Odd/Recto)
and ensures total absence of running titles on preliminary pages.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class RunningTitleContentRule(AuditRule):
    """Memverifikasi isi dan penempatan running title bilingual sesuai Subbab 4.1.4 Pedoman BPS 2023."""

    @property
    def rule_id(self) -> str:
        return "R07_RUNNING_TITLE_CONTENT"

    @property
    def name(self) -> str:
        return "Konten & Penempatan Running Title (Buku di Genap, Bab di Ganjil)"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.1.4 Poin 1-3 & Poin 6a (Hal. 49-52)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []

        # Find transition page from prelims to body (Page 1 Arab)
        # In our KCDA, Page 1 Arab starts with BAB 1: GEOGRAFI DAN IKLIM
        body_start_idx = -1
        for idx, page in enumerate(pages):
            if "BAB 1:" in page.full_text.upper():
                body_start_idx = idx
                break

        if body_start_idx == -1:
            return violations

        # 1. Check that preliminary pages have NO running title
        for idx in range(body_start_idx):
            page = pages[idx]
            # Page 1 (Cover) and Page 2 (Flyleaf) are handled by other rules
            if page.page_number in [1, 2]:
                continue
            if page.header_blocks:
                header_text = " | ".join(b.text.replace("\n", " ") for b in page.header_blocks)
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=page.page_number,
                        message="Halaman pendahuluan (romawi) dilarang memuat running title pada kepala halaman.",
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.ERROR,
                        measured_value=header_text[:40],
                        expected_value="Tanpa running title pada halaman romawi",
                    )
                )

        # 2. Check Body Pages (from body_start_idx to second-to-last page)
        # Skip the back cover (last page)
        for idx in range(body_start_idx, len(pages) - 1):
            page = pages[idx]

            # Skip divider pages, back matter openers, and blank pages (they have no headers by definition)
            if (
                "BAB " in page.full_text.upper()
                or "DAFTAR PUSTAKA" in page.full_text.upper()
                or page.is_blank
            ):
                continue

            # Must have a running header
            if not page.header_blocks:
                # If page is completely empty filler, BlankPageRule handles it
                if not page.body_blocks:
                    continue
                # For non-divider content pages, a running header is expected
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        physical_page=page.page_number,
                        message="Halaman isi batang tubuh harus memiliki running header.",
                        pedoman_ref=self.pedoman_ref,
                        severity=Severity.WARNING,
                        measured_value="Tidak ada header block",
                        expected_value="Running header aktif",
                    )
                )
                continue

            header_text = " ".join(b.text for b in page.header_blocks).upper()

            if page.is_verso:
                # Even / Verso page must contain publication title: "DALAM ANGKA 2026"
                if "DALAM ANGKA" not in header_text:
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            rule_name=self.name,
                            physical_page=page.page_number,
                            message="Halaman Genap (Verso) harus memuat Judul Publikasi (misal: 'Kecamatan ... Dalam Angka 2026').",
                            pedoman_ref=self.pedoman_ref,
                            severity=Severity.ERROR,
                            measured_value=header_text[:45],
                            expected_value="Memuat frasa 'DALAM ANGKA 2026'",
                        )
                    )
            else:
                # Odd / Recto page must contain chapter title or BPS Kabupaten Mempawah
                valid_recto = any(
                    ch in header_text
                    for ch in [
                        "GEOGRAFI",
                        "PEMERINTAHAN",
                        "KEPENDUDUKAN",
                        "SOSIAL",
                        "PERTANIAN",
                        "PARIWISATA",
                        "PERBANKAN",
                        "DAFTAR PUSTAKA",
                        "BPS",
                    ]
                )
                if not valid_recto:
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            rule_name=self.name,
                            physical_page=page.page_number,
                            message="Halaman Ganjil (Rekto) harus memuat Judul Bab yang sedang aktif.",
                            pedoman_ref=self.pedoman_ref,
                            severity=Severity.ERROR,
                            measured_value=header_text[:45],
                            expected_value="Memuat Judul Bab aktif",
                        )
                    )

        return violations
