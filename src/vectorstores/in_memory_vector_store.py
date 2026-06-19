from typing import List

import numpy as np

from src.core.document import Document
from src.vectorstores.base_vector_store import BaseVectorStore

class InMemoryVectorStore(BaseVectorStore):
    """
    Simple in-memory vector store.
    """
    def __init__(self):
        self.documents: List[Document] = []

    def add_documents(self, documents: List[Document]) -> None:

        if not isinstance(documents, list):
            raise TypeError("documents must be a list of Document objects.")
        
        for document in documents:
            if not isinstance(document, Document):
                raise TypeError("All items must be Document objects.")
        
        for document in documents:
            if document.embedding is None:
                raise ValueError("All documents must have embeddings before being added.")
            
        self.documents.extend(documents)

    def _cosine_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """
        Compute cosine similarity between two vectors.
        """

        if len(vector1) != len(vector2):
            raise ValueError("Vectors must have the same dimensions.")
        
        vector1 = np.array(vector1)
        vector2 = np.array(vector2)

        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)

        if norm1 == 0 or norm2 == 0:
            raise ValueError("Cosine similarity is undefined for zero vectors.")

        similarity = np.dot(vector1, vector2) / (norm1 * norm2)

        return float(similarity)

    def similarity_search(self,query_embedding: List[float], k: int) -> List[Document]:
        if not isinstance(query_embedding, list):
            raise TypeError("query_embedding must be a list of floats.")

        if k <= 0:
            raise ValueError("k must be greater than 0.")

        if not self.documents:
            return []
        
        similarity_scores = []

        for document in self.documents:

            score = self._cosine_similarity(
                query_embedding,
                document.embedding
            )

            similarity_scores.append(
                (score, document)
            )

        similarity_scores.sort(
            key=lambda item: item[0],
            reverse=True
        )

        top_k = similarity_scores[:k]

        return [
            document
            for _, document in top_k
        ]