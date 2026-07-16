from src.llms.llm_manager import LLMManager


class LLMManagerFactory:

    @staticmethod
    def create(router, registry, fallback_strategy):

        return LLMManager(
            router=router,
            registry=registry,
            fallback_strategy=fallback_strategy,
        )