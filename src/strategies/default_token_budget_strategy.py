from src.strategies.base_token_budget_strategy import BaseTokenBudgetStrategy


class DefaultTokenBudgetStrategy(BaseTokenBudgetStrategy):
    """
    Default strategy for allocating the LLM context window.

    We reserve some tokens for:
    - the prompt
    - the generated answer

    The remaining tokens can be used for retrieved context.
    """

    def __init__(self, prompt_tokens: int = 2000, response_tokens: int = 4000,):
        self.prompt_tokens = prompt_tokens
        self.response_tokens = response_tokens

    def get_context_token_budget(self, context_window: int,) -> int:

        budget = (
            context_window
            - self.prompt_tokens
            - self.response_tokens
        )

        return max(budget, 0)