from abc import ABC, abstractmethod
from typing import Optional

from src.core.tool_request import ToolRequest


class BaseToolRouter(ABC):
    """
    Base interface for deciding which tool should handle
    a user query.
    """

    @abstractmethod
    def route(self, query: str) -> ToolRequest | None:
        """
        Decide which tool should be used.
        """
        pass