from abc import ABC, abstractmethod
from typing import List

from src.core.document import Document
from src.embeddings.base_embeddings import BaseEmbeddings
from src.vectorstores.base_vector_store import BaseVectorStore

from src.auth.user import User

class BaseRetriever(ABC):
    """
    Abstract base class for all retrievers.
    """

    def __init__(self, embedding_model: BaseEmbeddings, vector_store: BaseVectorStore,):

        if embedding_model is None:
            raise ValueError("embedding_model cannot be None.")

        if vector_store is None:
            raise ValueError("vector_store cannot be None.")

        self.embedding_model = embedding_model
        self.vector_store = vector_store

    @abstractmethod
    def retrieve(self, query: str, k: int, metadata_filter: dict | None = None,) -> List[Document]:
        """
        Retrieve relevant documents.

        metadata_filter restricts retrieval to documents
        matching specific metadata.
        """
        pass