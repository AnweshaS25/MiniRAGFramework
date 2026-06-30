from abc import ABC, abstractmethod


class BaseTokenBudgetStrategy(ABC):
    """
    Strategy for deciding how much retrieved context
    can fit inside an LLM.
    """

    @abstractmethod
    def get_context_token_budget(self, context_window: int,) -> int:
        pass