from src.context_routing.base_context_router import BaseContextRouter


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
            return "lcm"

        elif any(word in query for word in [
            "compare",
            "analyze",
            "review",
            "explain in detail"
        ]):
            return "hybrid"

        return "default"