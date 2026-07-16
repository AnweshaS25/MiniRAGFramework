from src.memory.base_memory import BaseMemory
from src.memory.conversation_buffer_memory import ConversationBufferMemory
from src.memory.conversation_window_memory import ConversationWindowMemory
from src.memory.summary_memory import SummaryMemory


class MemoryManager:
    """
    Coordinates conversation memory.

    Initially delegates to a single memory implementation.
    """

    def __init__(
        self, 
        buffer_memory: ConversationBufferMemory,
        window_memory: ConversationWindowMemory,
        summary_memory: SummaryMemory,
    ):
        
        if buffer_memory is None:
            raise ValueError("buffer_memory cannot be None.")

        if window_memory is None:
            raise ValueError("window_memory cannot be None.")

        if summary_memory is None:
            raise ValueError("summary_memory cannot be None.")
        
        self.buffer_memory = buffer_memory
        self.window_memory = window_memory
        self.summary_memory = summary_memory


    def add_message(
        self, 
        role: str, 
        content: str
    ) -> None:
        
        self.buffer_memory.add_message(
            role=role, 
            content=content
        )

        self.window_memory.add_message(
            role=role, 
            content=content
        )

        self.summary_memory.add_message(
            role=role, 
            content=content
        )


    def get_context(self) -> str:

        # print("MemoryManager.get_context() called")

        parts = []

        summary = self.summary_memory.get_context()

        if summary:
            parts.append(summary)

        recent = self.window_memory.get_context()

        if recent:
            parts.append(
                "Recent Conversation:\n" + recent
            )

        return "\n\n".join(parts)


    def clear(self) -> None:
        self.buffer_memory.clear()
        self.window_memory.clear()
        self.summary_memory.clear()


    def get_full_history(self) -> str:
        return self.buffer_memory.get_context()
    
    def get_messages(self):
        return self.buffer_memory.get_messages()