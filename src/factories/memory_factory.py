from src.memory.conversation_buffer_memory import ConversationBufferMemory

from src.constants import MemoryTypes


class MemoryFactory:
    """
    Factory class for creating memory implementations.
    """

    @staticmethod
    def create(memory_type: str, **kwargs):

        if memory_type == MemoryTypes.CONVERSATION_BUFFER:
            return ConversationBufferMemory()

        raise ValueError(
            f"Unsupported memory: {memory_type}"
        )