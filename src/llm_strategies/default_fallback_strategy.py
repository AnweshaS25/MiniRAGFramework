from src.llm_strategies.base_fallback_strategy import BaseFallbackStrategy


class DefaultFallbackStrategy(BaseFallbackStrategy):
    """
    Default fallback strategy.

    Keeps the preferred LLM first,
    then tries every other registered LLM.
    """

    def order(self, preferred_llm, available_llms):

        ordered = [preferred_llm]

        for llm in available_llms.values():

            if llm is not preferred_llm:
                ordered.append(llm)

        return ordered