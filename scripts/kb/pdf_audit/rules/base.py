"""
Abstract Base Class for PDF Publishing Compliance Rules.
Single Responsibility: Defines the interface contract for layout audit rules.
"""

from abc import ABC, abstractmethod
from typing import List
from ..models import PageGeometry, Violation


class AuditRule(ABC):
    """Contract for an independent compliance audit rule."""

    @property
    @abstractmethod
    def rule_id(self) -> str:
        """Unique machine-readable identifier (e.g., 'R01_FLYLEAF')."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable rule name."""
        pass

    @property
    @abstractmethod
    def pedoman_ref(self) -> str:
        """Citation in Pedoman Pembuatan Publikasi BPS Edisi 2023."""
        pass

    @abstractmethod
    def evaluate(self, pages: List[PageGeometry]) -> List[Violation]:
        """Evaluates document pages against this rule and returns a list of violations."""
        pass
