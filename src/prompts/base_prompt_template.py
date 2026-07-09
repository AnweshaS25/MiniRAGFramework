from abc import ABC, abstractmethod

class BasePromptTemplate(ABC):
    """
    Abstract base class for all prompt templates.
    """

    @abstractmethod
    def format(self, **kwargs) -> str:
        """
        Build and return a prompt.
        """
        pass