from src.memory_retrieval.base_memory_retriever import BaseMemoryRetriever
from src.memory.memory_manager import MemoryManager


class KeywordMemoryRetriever(BaseMemoryRetriever):
    """
    Retrieves conversation messages using simple keyword matching.
    """

    def retrieve(
        self,
        query: str,
        memory: MemoryManager,
    ) -> str:


        messages = memory.get_messages()

        if not messages:
            return ""

        query_words = set(query.lower().split())

        relevant_messages = []

        for message in messages:

            # content = message["content"].lower()
            content = message.content.lower()

            if any(word in content for word in query_words):

                relevant_messages.append(
                    f"{message.metadata['role'].capitalize()}: {message.content}"
                )

        return "\n".join(relevant_messages)