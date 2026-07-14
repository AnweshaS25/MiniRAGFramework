from src.memory.conversation_buffer_memory import ConversationBufferMemory
from src.memory.conversation_window_memory import ConversationWindowMemory
from src.memory.summary_memory import SummaryMemory

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

        elif memory_type == MemoryTypes.SUMMARY:
            return SummaryMemory(
                llm=kwargs["llm"],
                summarize_after=kwargs.get("summarize_after", 6),
            )

        raise ValueError(
            f"Unsupported memory: {memory_type}"
        )