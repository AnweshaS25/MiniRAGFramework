class ContextBudgetManager:
    """
    Computes how many tokens are available
    for retrieved context.

    Formula:

    Context Window
    - Reserved Output Tokens
    - Prompt Tokens
    = Context Budget
    """

    def __init__(
        self,
        reserved_output_tokens: int = 1024,
    ):
        self.reserved_output_tokens = reserved_output_tokens

    def compute_budget(
        self,
        context_window: int,
        prompt_tokens: int,
    ) -> int:

        budget = (
            context_window
            - self.reserved_output_tokens
            - prompt_tokens
        )

        return max(0, budget)