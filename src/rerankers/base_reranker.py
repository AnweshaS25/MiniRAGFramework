from abc import ABC, abstractmethod
from typing import List

from src.core.document import Document


class BaseReranker(ABC):
    """
    Abstract base class for all rerankers.
    """

    @abstractmethod
    def rerank(self, query: str, documents: List[Document], top_k: int,) -> List[Document]:
        """
        Rerank retrieved documents.
        """
        pass