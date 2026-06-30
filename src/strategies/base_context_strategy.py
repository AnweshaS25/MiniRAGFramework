from abc import ABC, abstractmethod


class BaseContextStrategy(ABC):
    """
    Decides how many documents should be retrieved
    based on the LLM context window.
    """

    @abstractmethod
    def get_top_k(self,context_window: int,) -> int:
        pass