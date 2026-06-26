from abc import ABC, abstractmethod
from typing import Any


class BaseEvaluator(ABC):
    """
    Abstract base class for all evaluators.
    """

    @abstractmethod
    def evaluate(self, *args, **kwargs) -> Any:
        """
        Evaluate a component and return evaluation results.
        """
        pass