from abc import ABC, abstractmethod

from src.sessions.session import Session


class BaseSessionManager(ABC):

    @abstractmethod
    def create_session(self) -> Session:
        pass

    @abstractmethod
    def get_session(
        self,
        session_id: str,
    ) -> Session:
        pass

    @abstractmethod
    def delete_session(
        self,
        session_id: str,
    ) -> None:
        pass