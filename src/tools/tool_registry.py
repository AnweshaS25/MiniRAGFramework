from src.tools.base_tool import BaseTool


class ToolRegistry:
    """
    Registry that stores all available tools.
    """

    def __init__(self):
        self._tools = {}

    def register_tool(self, tool: BaseTool) -> None:
        """
        Register a tool.
        """

        if not isinstance(tool, BaseTool):
            raise TypeError(
                "tool must inherit from BaseTool."
            )

        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

    def get_tool(self, tool_name: str) -> BaseTool:
        """
        Retrieve a registered tool by name.
        """

        if tool_name not in self._tools:
            raise ValueError(
                f"Unknown tool: {tool_name}"
            )

        return self._tools[tool_name]

    def list_tools(self) -> list[BaseTool]:
        """
        Return all registered tools.
        """

        return list(self._tools.values())