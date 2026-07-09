from abc import ABC, abstractmethod

from src.core.prompt_request import PromptRequest


class BasePromptRouter(ABC):
    """
    Base class for all prompt routers.
    """

    @abstractmethod
    def route(self, query: str) -> PromptRequest | None:
        """
        Decide which prompt template should be used.
        """
        pass