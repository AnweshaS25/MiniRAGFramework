from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings

from src.constants import EmbeddingTypes

class EmbeddingFactory:
    """
    Factory class for creating embedding models.
    """

    @staticmethod
    def create(embedding_type: str):

        if EmbeddingTypes.HUGGINGFACE:
            return HuggingFaceEmbeddings()
        
        raise ValueError(
            f"Unsupported embedding model: {embedding_type}"
        )