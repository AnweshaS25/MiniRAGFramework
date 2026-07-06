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
    def similarity_search(self, query_embedding: List[float], k: int, metadata_filter: dict | None = None,) -> List[Document]:
        """
        Retrieve the most similar documents.

        metadata_filter can be used to restrict the search
        to documents matching specific metadata.
        """
        pass 

    @abstractmethod
    def clear(self):
        """
        Remove all documents from the vector store.
        """
        pass