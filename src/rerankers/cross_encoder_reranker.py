from typing import List
from src.core.document import Document
from src.rerankers.base_reranker import BaseReranker
from sentence_transformers import CrossEncoder

class CrossEncoderReranker(BaseReranker):
    """
    Reranker based on a Cross Encoder model.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",):

        if not model_name.strip():
            raise ValueError("model_name cannot be empty.")

        self.model_name = model_name
        self.model = CrossEncoder(model_name,)


    def rerank(self, query: str, documents: List[Document], top_k: int,) -> List[Document]:
        """
        Rerank retrieved documents.
        """

        if not query.strip():
            raise ValueError("query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        if not documents:
            return []


        pairs = [
            (
                query,
                document.content,
            )
            for document in documents
        ]

        scores = self.model.predict(pairs,)

        scored_documents = list(
            zip(
                documents,
                scores,
            )
        )

        scored_documents.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        top_k = min(top_k, len(documents))

        return [
            document
            for document, _ in scored_documents[:top_k]
        ]