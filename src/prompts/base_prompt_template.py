from abc import ABC, abstractmethod

class BasePromptTemplate(ABC):
    """
    Abstract base class for all prompt templates.
    """

    @abstractmethod
    def format(self, question: str, context: str,) -> str:
        """
        Format a prompt using the question and retrieved context.
        """
        pass