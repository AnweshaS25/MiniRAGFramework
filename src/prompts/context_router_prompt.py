class ContextRouterPrompt:
    """
    Builds the prompt used by the Context Router.
    """

    @staticmethod
    def build(query: str, registry):

        strategy_descriptions = ""

        for strategy in registry.list_strategies():

            strategy_descriptions += f"""
- {strategy.name}
    Description: {strategy.description}
"""

        return f"""
You are an intelligent Context Strategy Router.

Your task is to choose the BEST context strategy for answering the user's query.

Available Context Strategies:

{strategy_descriptions}

Return ONLY valid JSON.

Example:

{{
    "context_strategy": "default"
}}

User Query:
{query}
"""