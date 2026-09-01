from abc import ABC, abstractmethod
from typing import Any, Dict

class ProviderAdapter(ABC):
    """Abstract base class for tool providers."""

    @abstractmethod
    def execute(self, capability_code: str, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the capability against a target."""
        pass

    @abstractmethod
    def validate_target(self, target: str) -> bool:
        """Validate that the target is within allowed scope."""
        pass

    @abstractmethod
    def normalize_result(self, raw_output: Any) -> Dict[str, Any]:
        """Convert raw provider output to a standard format."""
        pass