from src.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """
    Tool for evaluating simple mathematical expressions.
    """

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Evaluates mathematical expressions."

    def execute(self, **kwargs):

        expression = kwargs.get("expression")

        if expression is None:
            raise ValueError(
                "Missing required argument: expression."
            )

        try:
            result = eval(
                expression,
                {"__builtins__": {}},
                {},
            )

        except Exception as e:
            raise ValueError(
                f"Invalid mathematical expression: {e}"
            )

        return result