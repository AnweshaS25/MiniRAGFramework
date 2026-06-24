from src.vectorstores.in_memory_vector_store import InMemoryVectorStore
from src.vectorstores.chroma_vector_store import ChromaVectorStore

from src.constants import VectorStoreTypes

class VectorStoreFactory:
    """
    Factory class for creating vector stores.
    """

    @staticmethod
    def create(vector_store_type: str, **kwargs,):

        if vector_store_type == VectorStoreTypes.IN_MEMORY:
            return InMemoryVectorStore()
        
        elif vector_store_type == VectorStoreTypes.CHROMA:
            return ChromaVectorStore(
                collection_name=kwargs.get(
                    "collection_name",
                    "default_collection",
                ),
                persist_directory=kwargs.get(
                    "persist_directory",
                    "./chroma_db",
                ),
            )
        
        raise ValueError(
            f"Unsupported vector store: {vector_store_type}"
        )