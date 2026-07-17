from src.tools.tool_registry import ToolRegistry
from src.tools.tool_executor import ToolExecutor
from src.tools.tool_manager import ToolManager

from src.tools.calculator_tool import CalculatorTool
from src.tools.date_time_tool import DateTimeTool

from src.tool_routing.rule_based_tool_router import RuleBasedToolRouter
from src.tool_routing.llm_tool_router import LLMToolRouter

from src.prompts.tool_router_prompt import ToolRouterPrompt

from src.constants import ToolRouterTypes


class ToolBuilder:
    """
    Builds the tool subsystem.
    """

    def __init__(self, config):

        self.config = config

    def build(
        self,
        llm_manager,
    ):
        tool_registry = ToolRegistry()

        tool_registry.register_tool(
            CalculatorTool()
        )

        tool_registry.register_tool(
            DateTimeTool()
        )

        tool_executor = ToolExecutor(
            registry=tool_registry,
        )

        if self.config.tool_router_type == ToolRouterTypes.RULE_BASED:

            tool_router = RuleBasedToolRouter()

        elif self.config.tool_router_type == ToolRouterTypes.LLM:

            tool_router = LLMToolRouter(
                llm_manager=llm_manager,
                prompt_template=ToolRouterPrompt(),
                registry=tool_registry,
            )

        else:

            raise ValueError(
                f"Unsupported tool router: {self.config.tool_router_type}"
            )

        tool_manager = ToolManager(
            router=tool_router,
            executor=tool_executor,
        )

        return tool_manager