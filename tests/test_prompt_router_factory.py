from src.factories.prompt_router_factory import PromptRouterFactory
from src.constants import PromptRouterTypes

from src.factories.llm_factory import LLMFactory
from src.constants import LLMTypes

from src.prompts.prompt_router_prompt import PromptRouterPrompt


rule_router = PromptRouterFactory.create(
    PromptRouterTypes.RULE_BASED,
)

print(type(rule_router).__name__)


llm = LLMFactory.create(
    LLMTypes.GROQ,
)

llm_router = PromptRouterFactory.create(
    PromptRouterTypes.LLM,
    llm=llm,
    prompt_template=PromptRouterPrompt(),
)

print(type(llm_router).__name__)