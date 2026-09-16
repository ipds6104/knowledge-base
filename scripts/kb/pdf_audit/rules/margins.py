"""
Margins and Safety Trim Compliance Rule.
Single Responsibility: Verifies mirror margins and distance of running headers/footers to paper edges.
"""

from typing import List
from ..models import PageGeometry, Violation, Severity
from .base import AuditRule


class SafetyTrimMarginRule(AuditRule):
    """Memverifikasi batas margin kertas A5 dan jarak aman pisau cetak (trim safety zone)."""

    @property
    def rule_id(self) -> str:
        return "R05_SAFETY_TRIM_MARGINS"

    @property
    def name(self) -> str:
        return "Margin Cermin & Jarak Aman Pisau Cetak (Trim Safety Zone)"

    @property
    def pedoman_ref(self) -> str:
        return "Pedoman Publikasi BPS 2023 Subbab 4.2.1 & 4.2.2 (Hal. 49-51)"

    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        violations: List[Violation] = []

        # Standard A5: width ~14.8 cm, height ~21.0 cm
        # Minimum safe distance from outer sheet edge for header/footer is 0.85 cm (ideal: 1.00 cm)
        MIN_EDGE_DIST = 0.85  # cm

        for page in pages:
            # Skip outer cover pages (page 1 and last page)
            if page.page_number == 1 or page.page_number == len(pages):
                continue

            # Check Header Trim Distance (Top Edge: y=0)
            for block in page.header_blocks:
                if block.y0 < MIN_EDGE_DIST:
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            rule_name=self.name,
                            physical_page=page.page_number,
                            message=f"Running header terlalu dekat ke tepi atas kertas ({block.y0:.2f} cm < {MIN_EDGE_DIST} cm). Berisiko terpotong percetakan.",
                            pedoman_ref=self.pedoman_ref,
                            severity=Severity.ERROR,
                            measured_value=f"y0 = {block.y0:.2f} cm",
                            expected_value=f"y0 >= {MIN_EDGE_DIST} cm (standar 1.00 cm)",
                        )
                    )
                    break

            # Check Footer Trim Distance (Bottom Edge: y=page.height_cm)
            for block in page.footer_blocks:
                dist_from_bottom = page.height_cm - block.y1
                if dist_from_bottom < MIN_EDGE_DIST:
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            rule_name=self.name,
                            physical_page=page.page_number,
                            message=f"Running footer terlalu dekat ke tepi bawah kertas ({dist_from_bottom:.2f} cm < {MIN_EDGE_DIST} cm). Berisiko terpotong percetakan.",
                            pedoman_ref=self.pedoman_ref,
                            severity=Severity.ERROR,
                            measured_value=f"Jarak bawah = {dist_from_bottom:.2f} cm",
                            expected_value=f"Jarak bawah >= {MIN_EDGE_DIST} cm (standar 1.00 cm)",
                        )
                    )
                    break

            # Check Inside / Outside Margins for Body Text
            # On Rekto (odd): Inside (left) >= 1.95 cm, Outside (right) text <= 13.4 cm
            # On Verso (even): Outside (left) text >= 1.45 cm, Inside (right) text <= 12.9 cm
            for block in page.body_blocks:
                # Disregard full-width tables or background blocks slightly touching edges
                if page.is_recto:
                    # Spine is left on recto
                    if block.x0 < 1.85 and block.width < 12.0:
                        violations.append(
                            Violation(
                                rule_id=self.rule_id,
                                rule_name=self.name,
                                physical_page=page.page_number,
                                message=f"Teks menabrak margin punggung/jilid pada lembar Rekto.",
                                pedoman_ref=self.pedoman_ref,
                                severity=Severity.WARNING,
                                measured_value=f"x0 = {block.x0:.2f} cm",
                                expected_value="x0 >= 2.00 cm",
                            )
                        )
                        break
                else:
                    # Outer cut is left on verso
                    if block.x0 < 1.35 and block.width < 12.0:
                        violations.append(
                            Violation(
                                rule_id=self.rule_id,
                                rule_name=self.name,
                                physical_page=page.page_number,
                                message=f"Teks menabrak margin luar pada lembar Verso.",
                                pedoman_ref=self.pedoman_ref,
                                severity=Severity.WARNING,
                                measured_value=f"x0 = {block.x0:.2f} cm",
                                expected_value="x0 >= 1.50 cm",
                            )
                        )
                        break

        return violations
