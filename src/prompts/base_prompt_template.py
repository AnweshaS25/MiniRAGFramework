from abc import ABC, abstractmethod

class BasePromptTemplate(ABC):
    """
    Abstract base class for all prompt templates.
    """

    @abstractmethod
    def format(self, question: str, context: str, history: str = "",) -> str:
        """
        Format a prompt using the question, retrieved context,
        and optional conversation history.
        """
        pass