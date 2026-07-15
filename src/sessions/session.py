from src.memory.memory_manager import MemoryManager


class Session:
    """
    Represents one user conversation session.
    """

    def __init__(
        self,
        session_id: str,
        memory: MemoryManager,
    ):
        self.session_id = session_id
        self.memory = memory