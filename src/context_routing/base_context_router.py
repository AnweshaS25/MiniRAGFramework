from abc import ABC, abstractmethod


class BaseContextRouter(ABC):
    """
    Decides which context strategy should be used
    for the current query.
    """

    @abstractmethod
    def route(self, query: str):
        pass