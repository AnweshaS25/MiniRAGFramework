from src.memory.base_memory import BaseMemory
from src.memory_retrieval.memory_document import MemoryDocument


class ConversationBufferMemory(BaseMemory):
    """
    Stores the entire conversation history.
    """

    def __init__(self):
        self.messages = []


    def get_messages(self):
        return self.messages

    
    def add_message(self, role: str, content: str,) -> None:

        if role not in ("user", "assistant"):
            raise ValueError(
                "role must be either 'user' or 'assistant'."
            )

        if not content.strip():
            raise ValueError(
                "content cannot be empty."
            )

        self.messages.append(
             MemoryDocument(
                 content=content,
                 metadata={
                     "role": role,
                }
            )
        )

        print(f"Added {role}: {content}")


    def get_context(self) -> str:
        if not self.messages:
            return ""

        history = []

        for message in self.messages:
            history.append(
                f"{message.metadata['role'].capitalize()}: {message.content}"
            )
        return "\n".join(history)
    

    def clear(self) -> None:
        self.messages.clear()