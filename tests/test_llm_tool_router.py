from src.llms.groq_llm import GroqLLM

from src.prompts.tool_router_prompt import ToolRouterPrompt

from src.tool_routing.llm_tool_router import LLMToolRouter

from src.tools.tool_registry import ToolRegistry

from src.tools.calculator_tool import CalculatorTool
from src.tools.date_time_tool import DateTimeTool


# LLM
llm = GroqLLM()

# Tool Registry
tool_registry = ToolRegistry()

tool_registry.register_tool(
    CalculatorTool()
)

tool_registry.register_tool(
    DateTimeTool()
)

# Prompt
prompt_template = ToolRouterPrompt()

# Router
router = LLMToolRouter(
    llm=llm,
    prompt_template=prompt_template,
    registry=tool_registry,
)


query = "What time is it?"
tool_request = router.route(query)
print(tool_request)


queries = [
    "What time is it?",
    "Calculate 15*8",
    "Summarize this PDF",
]

for query in queries:

    print("-" * 40)
    print("Query:", query)

    tool_request = router.route(query)

    print(tool_request)