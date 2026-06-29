from abc import ABC, abstractmethod
from typing import List

from src.core.evaluation_sample import EvaluationSample


class BaseDatasetLoader(ABC):
    """
    Base interface for loading evaluation datasets.
    """

    @abstractmethod
    def load(self) -> List[EvaluationSample]:
        """
        Load evaluation samples.
        """
        pass