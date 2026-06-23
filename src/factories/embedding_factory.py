from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.embeddings.bge_embeddings import BGEEmbeddings

from src.constants import EmbeddingTypes

class EmbeddingFactory:
    """
    Factory class for creating embedding models.
    """

    @staticmethod
    def create(embedding_type: str):

        if embedding_type == EmbeddingTypes.HUGGINGFACE:
            return HuggingFaceEmbeddings()
        
        elif embedding_type == EmbeddingTypes.BGE:
            return BGEEmbeddings()
        
        raise ValueError(
            f"Unsupported embedding model: {embedding_type}"
        )