from typing import Any

from src.tools.tool_executor import ToolExecutor
from src.tool_routing.base_tool_router import BaseToolRouter


class ToolManager:
    """
    Coordinates tool routing and execution.
    """

    def __init__(self, router: BaseToolRouter, executor: ToolExecutor, ):
        if router is None:
            raise ValueError("router cannot be None.")

        if executor is None:
            raise ValueError("executor cannot be None.")

        self.router = router
        self.executor = executor

    def process(self, user_query: str, **kwargs, ) -> tuple[bool, Any]:
        """
        Decide whether a tool should be used and execute it.

        Returns:
            (True, result) if a tool was executed.

            (False, None) if no tool was selected.
        """

        tool_request = self.router.route(user_query)

        print("Router returned:", tool_request)

        # if tool_request is None:
        #     return False, None
        if not tool_request or not tool_request.tool_name:
            return False, None

        tool_kwargs = dict(kwargs)

        tool_kwargs.update(tool_request.arguments)

        print("Executing tool:", tool_request.tool_name)

        result = self.executor.execute(
            tool_request.tool_name,
            **tool_kwargs,
        )
        return True, result