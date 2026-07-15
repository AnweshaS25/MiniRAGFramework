import uuid

from src.sessions.base_session_manager import BaseSessionManager
from src.sessions.session import Session


class SessionManager(BaseSessionManager):

    def __init__(
        self,
        memory_factory,
    ):
        self.memory_factory = memory_factory
        self.sessions = {}

    def create_session(self) -> Session:

        session_id = str(uuid.uuid4())

        memory = self.memory_factory()

        session = Session(
            session_id=session_id,
            memory=memory,
        )

        self.sessions[session_id] = session

        return session
    

    def get_session(
        self,
        session_id: str,
    ) -> Session:

        if session_id not in self.sessions:
            raise ValueError(
                f"Session '{session_id}' not found."
            )

        return self.sessions[session_id]
    

    def delete_session(
        self,
        session_id: str,
    ) -> None:

        if session_id in self.sessions:
            del self.sessions[session_id]