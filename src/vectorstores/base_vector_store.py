from abc import ABC, abstractmethod
from typing import List

from src.core.document import Document

class BaseVectorStore(ABC):
    """
    Abstract base class for all vector stores.
    """

    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        """
        Store documents and their embeddings.
        """
        pass

    @abstractmethod
    def similarity_search(self, query_embedding: List[float],k: int) -> List[Document]:
        """
        Return the k most similar documents.
        """
        pass