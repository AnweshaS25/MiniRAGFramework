from abc import ABC, abstractmethod
from typing import List

from src.core.document import Document
from src.embeddings.base_embeddings import BaseEmbeddings
from src.vectorstores.base_vector_store import BaseVectorStore

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
    def retrieve(self, query: str, k: int,) -> List[Document]:
        """
        Retrieve the k most relevant documents for the given query.
        """
        pass