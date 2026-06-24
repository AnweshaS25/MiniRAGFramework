from src.retrievers.similarity_retriever import SimilarityRetriever
from src.retrievers.mmr_retriever import MMRRetriever

from src.constants import RetrieverTypes

class RetrieverFactory:
    """
    Factory class for creating retrievers.
    """

    @staticmethod
    def create(retriever_type: str, **kwargs,):

        if retriever_type == RetrieverTypes.SIMILARITY:
            return SimilarityRetriever(
                embedding_model=kwargs["embedding_model"],
                vector_store=kwargs["vector_store"],
            )
        
        elif retriever_type == RetrieverTypes.MMR:
            return MMRRetriever(
                embedding_model=kwargs["embedding_model"],
                vector_store=kwargs["vector_store"],
                lambda_param=kwargs.get("lambda_param", 0.5),
                fetch_k=kwargs.get("fetch_k", 20),
            )
            

        raise ValueError(
            f"Unsupported retriever: {retriever_type}"
        )