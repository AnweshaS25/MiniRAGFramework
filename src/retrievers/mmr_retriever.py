from typing import List

from src.embeddings.base_embeddings import BaseEmbeddings
from src.vectorstores.base_vector_store import BaseVectorStore

from src.core.document import Document
from src.retrievers.base_retriever import BaseRetriever

from src.utils.similarity import cosine_similarity


class MMRRetriever(BaseRetriever):
    """
    Retriever that performs Maximal Marginal Relevance (MMR) retrieval.
    """

    def __init__(self, embedding_model: BaseEmbeddings, vector_store: BaseVectorStore, lambda_param: float = 0.5,fetch_k: int = 20,):

        super().__init__(embedding_model, vector_store,)

        if not 0 <= lambda_param <= 1:
            raise ValueError(
                "lambda_param must be between 0 and 1."
            )

        if fetch_k <= 0:
            raise ValueError(
                "fetch_k must be greater than 0."
            )

        self.lambda_param = lambda_param
        self.fetch_k = fetch_k

    def retrieve(self, query: str, k: int,) -> List[Document]:

        if not query.strip():
            raise ValueError("query cannot be empty.")

        if k <= 0:
            raise ValueError(
                "k must be greater than 0."
            )
        
        if k > self.fetch_k:
            raise ValueError(
                "k cannot be greater than fetch_k."
            )
        
        query_embedding = self.embedding_model.embed_query(query)

        candidate_documents = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            k=self.fetch_k,
        )

        if not candidate_documents:
            return []

        selected_documents = []

        remaining_documents = candidate_documents.copy()

        # Select the most relevant document first
        selected_documents.append(remaining_documents.pop(0))

        if k == 1:
            return selected_documents

        while (
            len(selected_documents) < k
            and remaining_documents
        ):

            best_document = None
            best_score = float("-inf")

            for candidate in remaining_documents:

                score = self._compute_mmr_score(
                    query_embedding=query_embedding,
                    candidate_document=candidate,
                    selected_documents=selected_documents,
                )

                if score > best_score:
                    best_score = score
                    best_document = candidate

            selected_documents.append(best_document)

            remaining_documents.remove(best_document)

        return selected_documents
    

    def _compute_mmr_score(self, query_embedding: List[float], candidate_document: Document,selected_documents: List[Document],) -> float:
        """
        Compute the MMR score for a candidate document.
        """

        # Similarity with the query
        query_similarity = cosine_similarity(
            query_embedding,
            candidate_document.embedding,
        )

        # If nothing has been selected yet
        if not selected_documents:
            return query_similarity

        # Maximum similarity with already selected documents
        max_similarity = max(
            cosine_similarity(
                candidate_document.embedding,
                selected.embedding,
            )
            for selected in selected_documents
        )

        # MMR Score
        mmr_score = (
            self.lambda_param * query_similarity
            - (1 - self.lambda_param) * max_similarity
        )

        return mmr_score
