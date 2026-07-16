from abc import ABC, abstractmethod

from src.memory.memory_manager import MemoryManager


class BaseQueryRewriter(ABC):
    """
    Base class for converting a follow-up conversational query
    into a standalone query before retrieval.
    """

    @abstractmethod
    def rewrite(
        self,
        query: str,
        memory: MemoryManager,
    ) -> str:
        """
        Returns a rewritten standalone query.
        """
        pass