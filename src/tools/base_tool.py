from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Base interface for all tools/plugins that can be used by the framework.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique name of the tool.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Short description of what the tool does.
        """
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        #**kwargs makes the interface flexible while keeping the framework generic
        """
        Execute the tool.

        Returns:
            The result produced by the tool.
        """
        pass