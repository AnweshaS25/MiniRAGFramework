from src.memory.base_memory import BaseMemory


class ConversationBufferMemory(BaseMemory):
    """
    Stores the entire conversation history.
    """

    def __init__(self):
        self.messages = []

    
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
            {
                "role": role,
                "content": content,
            }
        )

        print(f"Added {role}: {content}")


    def get_context(self) -> str:
        if not self.messages:
            return ""

        history = []

        for message in self.messages:
            history.append(
                f"{message['role'].capitalize()}: {message['content']}"
            )

        return "\n".join(history)
    

    def clear(self) -> None:
        self.messages.clear()