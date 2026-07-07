from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolRequest:
    """
    Represents a request to execute a tool.
    """

    tool_name: str

    arguments: dict[str, Any] = field(default_factory=dict)