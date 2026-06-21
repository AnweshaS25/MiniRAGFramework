from abc import ABC, abstractmethod
from typing import Any


class BasePipeline(ABC):
    """
    Abstract base class for all pipelines.
    """

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """
        Execute the pipeline.
        """
        pass