"""
Domain Models and Data Transfer Objects for PDF Layout Compliance Auditing.
Single Responsibility: Encapsulates audit data structures, geometry representations, and violation records.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from enum import Enum


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(frozen=True)
class TextBlock:
    """Represents an extracted text block with bounding box in centimeters."""
    text: str
    x0: float  # Left edge in cm
    y0: float  # Top edge in cm
    x1: float  # Right edge in cm
    y1: float  # Bottom edge in cm

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        return self.y1 - self.y0


@dataclass
class PageGeometry:
    """Physical representation and geometry of a single PDF page."""
    page_number: int  # 1-indexed physical page
    width_cm: float
    height_cm: float
    blocks: List[TextBlock] = field(default_factory=list)

    @property
    def is_recto(self) -> bool:
        """Recto (halaman ganjil / muka kanan)."""
        return self.page_number % 2 != 0

    @property
    def is_verso(self) -> bool:
        """Verso (halaman genap / muka kiri)."""
        return self.page_number % 2 == 0

    @property
    def is_blank(self) -> bool:
        """True if page contains zero printable text blocks."""
        return len(self.blocks) == 0

    @property
    def full_text(self) -> str:
        return " ".join(b.text for b in self.blocks)

    @property
    def header_blocks(self) -> List[TextBlock]:
        """Blocks located within the header zone (y <= 1.4 cm)."""
        return [b for b in self.blocks if b.y0 <= 1.4]

    @property
    def footer_blocks(self) -> List[TextBlock]:
        """Blocks located within the footer zone (y >= 19.4 cm for A5 21.0 cm height)."""
        return [b for b in self.blocks if b.y1 >= 19.4]

    @property
    def body_blocks(self) -> List[TextBlock]:
        """Blocks within the main body area (1.4 cm < y < 19.4 cm)."""
        return [b for b in self.blocks if b.y0 > 1.4 and b.y1 < 19.4]


@dataclass
class Violation:
    """Record of a publishing guideline violation."""
    rule_id: str
    rule_name: str
    physical_page: int
    message: str
    pedoman_ref: str
    severity: Severity = Severity.ERROR
    measured_value: Optional[str] = None
    expected_value: Optional[str] = None


@dataclass
class AuditResult:
    """Consolidated audit result for a single PDF document."""
    file_path: str
    total_pages: int
    violations: List[Violation] = field(default_factory=list)

    @property
    def is_passed(self) -> bool:
        return len([v for v in self.violations if v.severity == Severity.ERROR]) == 0

    @property
    def error_count(self) -> int:
        return len([v for v in self.violations if v.severity == Severity.ERROR])

    @property
    def warning_count(self) -> int:
        return len([v for v in self.violations if v.severity == Severity.WARNING])
