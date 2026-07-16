from abc import ABC, abstractmethod

from src.memory.memory_manager import MemoryManager


class BaseMemoryRetriever(ABC):
    """
    Base class for all memory retrievers.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        memory: MemoryManager,
    ) -> str:
        """
        Return only the relevant memory for the query.
        """
        pass