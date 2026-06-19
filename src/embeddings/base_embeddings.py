from abc import ABC, abstractmethod
from typing import List

from src.core.document import Document


class BaseEmbeddings(ABC):
    """
    Abstract base class for embedding models.
    """

    @abstractmethod
    def embed_documents(self, documents: List[Document]) -> List[Document]:
        """
        Generates embeddings for a list of documents.
        Args:
            documents: List of Document objects.

        Returns:
            List of Document objects with embeddings added.
        """
        pass

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """
        Generate an embedding for a query string.
        """
        pass