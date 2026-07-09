from src.llms.llm_manager import LLMManager
from src.llm_routing.rule_based_llm_router import RuleBasedLLMRouter


manager = LLMManager(
    router=RuleBasedLLMRouter(),
)

llm = manager.get_llm(
    # "Give me a brief explanation."
    "Summarize this document."
)

print(type(llm).__name__)