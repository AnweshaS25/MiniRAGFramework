from src.memory.conversation_buffer_memory import ConversationBufferMemory
from src.memory.conversation_window_memory import ConversationWindowMemory
from src.memory.summary_memory import SummaryMemory

from src.memory.memory_manager import MemoryManager

from src.constants import MemoryTypes


class MemoryFactory:
    """
    Factory class for creating memory implementations.
    """

    @staticmethod
    def create(memory_type: str, **kwargs):

        if memory_type == MemoryTypes.CONVERSATION_BUFFER:
            memory = ConversationBufferMemory()
            return MemoryManager(memory)
        
        elif memory_type == MemoryTypes.CONVERSATION_WINDOW:
            memory = ConversationWindowMemory(window_size=2) #window_size=2 is temporarily used for testing
            return MemoryManager(memory)

        elif memory_type == MemoryTypes.SUMMARY:
            memory = SummaryMemory(
                llm=kwargs["llm"],
                summarize_after=kwargs.get("summarize_after", 6),
            )

            return MemoryManager(memory)

        raise ValueError(
            f"Unsupported memory: {memory_type}"
        )