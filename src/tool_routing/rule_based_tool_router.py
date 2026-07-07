import re

from src.tool_routing.base_tool_router import BaseToolRouter
from src.core.tool_request import ToolRequest


class RuleBasedToolRouter(BaseToolRouter):
    """
    Simple rule-based tool router.
    """

    CALCULATOR_KEYWORDS = [
        "calculate",
        "calculator",
        "multiply",
        "division",
        "divide",
        "addition",
        "subtract",
        "subtraction",
        "plus",
        "minus",
        "times",
    ]

    DATETIME_KEYWORDS = [
        "date",
        "time",
        "today",
        "day",
        "current time",
        "current date",
    ]

    MATH_PATTERN = re.compile(
        r"\d+\s*[\+\-\*/]\s*\d+"
    )

    def route(self, query: str):

        query_lower = query.lower()

        match = self.MATH_PATTERN.search(query_lower)

        if match:
            return ToolRequest(
                tool_name="calculator",
                arguments={
                    "expression": match.group()
                },
            )

        for keyword in self.CALCULATOR_KEYWORDS:

            if keyword in query_lower:
                return ToolRequest(
                    tool_name="calculator",
                )
            
        for keyword in self.DATETIME_KEYWORDS:
            if keyword in query_lower:
                return ToolRequest(
                    tool_name="datetime",
                )


        return None