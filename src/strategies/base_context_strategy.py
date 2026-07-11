from abc import ABC, abstractmethod
from typing import List

from src.core.document import Document


class BaseContextStrategy(ABC):
    """
    Decides how many documents should be retrieved
    based on the LLM context window.
    """

    @abstractmethod
    def get_top_k(self,context_window: int,) -> int:
        pass

    @abstractmethod
    def build_context(self, documents: List[Document],) -> str:
        """
        Build the final context that will be sent to the LLM.
        """
        pass


    @abstractmethod
    def requires_retrieval(self) -> bool:
        """
        Whether this strategy needs semantic retrieval.
        """
        pass