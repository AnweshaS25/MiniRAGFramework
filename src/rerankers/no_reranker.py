from typing import List

from src.core.document import Document

from src.rerankers.base_reranker import BaseReranker

class NoReranker(BaseReranker):
    """
    Default reranker that performs no reranking.
    """

    def rerank(self, query: str, documents: List[Document], top_k: int,) -> List[Document]:

        if not query.strip():
            raise ValueError("query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        if not documents:
            return []

        return documents[:top_k]