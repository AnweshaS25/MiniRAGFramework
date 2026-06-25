from abc import ABC, abstractmethod


class BaseMemory(ABC):
    """
    Abstract base class for conversation memory.
    """

    @abstractmethod
    def add_message(self, role: str, content: str,) -> None:
        """
        Add a message to memory.
        """
        pass

    @abstractmethod
    def get_context(self) -> str:
        """
        Return the conversation history as a string.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clear all stored conversation history.
        """
        pass