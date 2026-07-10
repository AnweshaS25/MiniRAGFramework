from abc import ABC, abstractmethod


class BaseFallbackStrategy(ABC):
    """
    Decides the order in which LLMs should be tried.
    """

    @abstractmethod
    def order(self, preferred_llm, available_llms):
        pass