from src.tools.calculator_tool import CalculatorTool
from src.tools.tool_registry import ToolRegistry
from src.tools.tool_executor import ToolExecutor


registry = ToolRegistry()

registry.register_tool(
    CalculatorTool()
)

executor = ToolExecutor(registry)

result = executor.execute(
    "calculator",
    expression="25 + 8 * 2",
)

print(result)