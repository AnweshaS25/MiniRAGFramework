from src.memory.base_memory import BaseMemory


class ConversationWindowMemory(BaseMemory):
    """
    Stores only the last N messages.
    """

    def __init__(self, window_size: int = 6):
        self.window_size = window_size
        self.messages = []



    def add_message(self, role: str, content: str) -> None:

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

        # Keep only the last `window_size` messages

        max_messages = self.window_size * 2
        if len(self.messages) > max_messages:
            self.messages = self.messages[-max_messages:]


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