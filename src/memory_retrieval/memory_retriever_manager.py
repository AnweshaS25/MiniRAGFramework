from src.memory_retrieval.base_memory_retriever import BaseMemoryRetriever
from src.memory.memory_manager import MemoryManager


class MemoryRetrieverManager:
    """
    Wrapper around a memory retriever.

    Makes it easy to swap different memory retrieval strategies.
    """

    def __init__(
        self,
        retriever: BaseMemoryRetriever,
    ):
        self.retriever = retriever

    def retrieve(
        self,
        query: str,
        memory: MemoryManager,
    ) -> str:

        return self.retriever.retrieve(
            query=query,
            memory=memory,
        )