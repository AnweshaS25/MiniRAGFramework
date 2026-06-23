from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings

class EmbeddingFactory:
    """
    Factory class for creating embedding models.
    """

    @staticmethod
    def create(embedding_type: str):

        if embedding_type == "huggingface":
            return HuggingFaceEmbeddings()
        
        raise ValueError(
            f"Unsupported embedding model: {embedding_type}"
        )