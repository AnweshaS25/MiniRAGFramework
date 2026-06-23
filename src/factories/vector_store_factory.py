from src.vectorstores.in_memory_vector_store import InMemoryVectorStore
from src.vectorstores.chroma_vector_store import ChromaVectorStore

class VectorStoreFactory:
    """
    Factory class for creating vector stores.
    """

    @staticmethod
    def create(vector_store_type: str, **kwargs,):

        if vector_store_type == "inmemory":
            return InMemoryVectorStore()
        
        if vector_store_type == "chroma":
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