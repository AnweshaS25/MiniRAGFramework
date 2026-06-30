from src.strategies.default_token_budget_strategy import DefaultTokenBudgetStrategy


class TokenBudgetStrategyFactory:
    """
    Factory class for creating token budget strategies.
    """

    @staticmethod
    def create():
        return DefaultTokenBudgetStrategy()