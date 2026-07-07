from typing import Any

from src.tools.tool_registry import ToolRegistry


class ToolExecutor:
    """
    Responsible for executing registered tools.
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, tool_name: str, **kwargs,) -> Any:
        """
        Execute a registered tool.
        """

        print("Executor received:", tool_name)

        tool = self.registry.get_tool(tool_name)

        return tool.execute(**kwargs)