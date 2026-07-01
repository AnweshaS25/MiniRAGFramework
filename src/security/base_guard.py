from abc import ABC, abstractmethod
from src.security.security_result import SecurityResult


class BaseGuard(ABC):
    """
    Abstract base class for all security guards.
    """

    @abstractmethod
    def validate(self, text: str) -> SecurityResult:
        """
        Validate the given text.

        Returns:
            True  -> safe
            False -> unsafe
        """
        pass