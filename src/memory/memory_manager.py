from src.memory.base_memory import BaseMemory


class MemoryManager:
    """
    Coordinates conversation memory.

    Initially delegates to a single memory implementation.
    """

    def __init__(self, memory: BaseMemory):

        if memory is None:
            raise ValueError("memory cannot be None.")

        self.memory = memory


    def add_message(self, role: str, content: str) -> None:
        self.memory.add_message(role, content)


    def get_context(self) -> str:
        return self.memory.get_context()


    def clear(self) -> None:
        self.memory.clear()