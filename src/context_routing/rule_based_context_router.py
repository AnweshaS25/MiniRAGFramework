from src.context_routing.base_context_router import BaseContextRouter
from src.core.context_request import ContextRequest


class RuleBasedContextRouter(BaseContextRouter):

    def route(self, query: str):

        query = query.lower()

        if any(word in query for word in [
            "summarize",
            "summary",
            "entire document",
            "whole document",
            "overall"
        ]):
            # return "lcm"
            return ContextRequest(
                context_strategy="lcm",
            )

        elif any(word in query for word in [
            "compare",
            "analyze",
            "review",
            "explain in detail"
        ]):
            # return "hybrid"
            return ContextRequest(
                context_strategy="hybrid",
            )

        # return "default"
        return ContextRequest(
            context_strategy="default",
        )