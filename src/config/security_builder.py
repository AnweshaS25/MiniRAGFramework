from src.factories.security_guard_factory import SecurityGuardFactory
from src.factories.output_guard_factory import OutputGuardFactory
from src.factories.token_budget_strategy_factory import TokenBudgetStrategyFactory
from src.factories.reranker_factory import RerankerFactory


class SecurityBuilder:
    """
    Builds security-related components.
    """

    def __init__(self, config):

        self.config = config

    def build(
        self,
        llm_manager,
    ):
        security_guard = SecurityGuardFactory.create(
            security_type=self.config.security_type,
            llm_manager=llm_manager,
        )

        output_guard = OutputGuardFactory.create()

        token_budget_strategy = TokenBudgetStrategyFactory.create()

        reranker = RerankerFactory.create(
            self.config.reranker_type,
        )

        return {
            "security_guard": security_guard,
            "output_guard": output_guard,
            "token_budget_strategy": token_budget_strategy,
            "reranker": reranker,
        }