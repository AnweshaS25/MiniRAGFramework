from src.retrievers.similarity_retriever import SimilarityRetriever

class RetrieverFactory:
    """
    Factory class for creating retrievers.
    """

    @staticmethod
    def create(retriever_type: str, **kwargs,):

        if retriever_type == "similarity":
            return SimilarityRetriever(
                embedding_model=kwargs["embedding_model"],
                vector_store=kwargs["vector_store"],
            )
            

        raise ValueError(
            f"Unsupported retriever: {retriever_type}"
        )