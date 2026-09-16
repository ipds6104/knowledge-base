"""
PDF Compliance Auditor and Report Formatter.
Single Responsibility: Orchestrates rules evaluation against PDF geometries and formats human-readable reports.
"""

from pathlib import Path
from typing import List, Union, Optional
from .models import AuditResult, Violation, Severity
from .inspector import PdfInspector
from .rules import AuditRule, get_default_kcda_rules


class KcdaPdfAuditor:
    """Orchestrator for evaluating PDF documents against BPS publishing guidelines."""

    def __init__(self, rules: Optional[List[AuditRule]] = None):
        self.rules = rules or get_default_kcda_rules()

    def audit_file(self, pdf_path: Union[str, Path]) -> AuditResult:
        """Audits a single PDF file against registered rules."""
        inspector = PdfInspector(pdf_path)
        pages = inspector.inspect_pages()

        violations: List[Violation] = []
        for rule in self.rules:
            rule_violations = rule.evaluate(pages)
            violations.extend(rule_violations)

        # Sort violations by physical page number
        violations.sort(key=lambda v: v.physical_page)

        return AuditResult(
            file_path=str(pdf_path),
            total_pages=len(pages),
            violations=violations,
        )

    def audit_multiple(self, pdf_paths: List[Union[str, Path]]) -> List[AuditResult]:
        """Audits multiple PDF documents sequentially."""
        return [self.audit_file(p) for p in pdf_paths]

    @staticmethod
    def format_cli_report(result: AuditResult) -> str:
        """Formats an AuditResult into a clear, structured terminal string."""
        path_obj = Path(result.file_path)
        file_name = path_obj.name
        kec_name = path_obj.parent.name

        lines = [
            f"📄 Berkas: {file_name} ({kec_name})",
            f"   Total Halaman: {result.total_pages} hal | Status: {'✅ LULUS' if result.is_passed else '❌ GAGAL'}",
        ]

        if not result.violations:
            lines.append("   🎉 100% Sesuai Pedoman Publikasi BPS 2023 (0 pelanggaran)")
            return "\n".join(lines)

        lines.append(
            f"   ⚠️  Ditemukan: {result.error_count} kesalahan (Error), {result.warning_count} peringatan (Warning):"
        )
        lines.append("   " + "-" * 70)

        for v in result.violations:
            prefix = "🔴 ERROR" if v.severity == Severity.ERROR else "🟡 WARN "
            lines.append(f"   {prefix} [Hal. {v.physical_page:02d}] {v.rule_name}")
            lines.append(f"      Pesan   : {v.message}")
            lines.append(f"      Rujukan : {v.pedoman_ref}")
            if v.measured_value:
                lines.append(f"      Terukur : {v.measured_value}")
            if v.expected_value:
                lines.append(f"      Standar : {v.expected_value}")
            lines.append("")

        return "\n".join(lines)
