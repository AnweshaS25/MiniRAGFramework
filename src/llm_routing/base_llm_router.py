from abc import ABC, abstractmethod


class BaseLLMRouter(ABC):
    """
    Base class for all LLM routers.
    """

    @abstractmethod
    def route(self, query: str) -> str:
        """
        Return the LLM type that should answer the query.
        """
        pass