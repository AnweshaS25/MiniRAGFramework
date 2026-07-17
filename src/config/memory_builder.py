from src.memory.memory_manager import MemoryManager

from src.memory.conversation_buffer_memory import ConversationBufferMemory
from src.memory.conversation_window_memory import ConversationWindowMemory
from src.memory.summary_memory import SummaryMemory


class MemoryBuilder:

    def __init__(self, config):
        self.config = config


    def build(
        self,
        llm_manager,
    ):
        buffer_memory = ConversationBufferMemory()

        window_memory = ConversationWindowMemory(
            window_size=self.config.conversation_window_size,
        )

        summary_memory = SummaryMemory(
            llm_manager=llm_manager,
            summarize_after=self.config.summarize_after,
        )

        return MemoryManager(
            buffer_memory=buffer_memory,
            window_memory=window_memory,
            summary_memory=summary_memory,
        )