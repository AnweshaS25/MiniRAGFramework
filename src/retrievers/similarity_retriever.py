from typing import List

from src.core.document import Document
from src.retrievers.base_retriever import BaseRetriever

class SimilarityRetriever(BaseRetriever):
    """
    Retriever that performs similarity search using the configured
    embedding model and vector store.
    """

    def retrieve(self, query: str, k: int,) -> List[Document]:
        if not query.strip():
            raise ValueError("query cannot be empty.")

        if k <= 0:
            raise ValueError("k must be greater than 0.")
        
        query_embedding = self.embedding_model.embed_query(query)

        documents = self.vector_store.similarity_search(query_embedding=query_embedding,k=k,)

        return documents