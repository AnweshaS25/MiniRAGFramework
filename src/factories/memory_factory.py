from src.memory.conversation_buffer_memory import ConversationBufferMemory
from src.memory.conversation_window_memory import ConversationWindowMemory

from src.constants import MemoryTypes


class MemoryFactory:
    """
    Factory class for creating memory implementations.
    """

    @staticmethod
    def create(memory_type: str, **kwargs):

        if memory_type == MemoryTypes.CONVERSATION_BUFFER:
            return ConversationBufferMemory()
        
        elif memory_type == MemoryTypes.CONVERSATION_WINDOW:
            return ConversationWindowMemory(window_size=2) #window_size=2 is temporarily used for testing

        raise ValueError(
            f"Unsupported memory: {memory_type}"
        )