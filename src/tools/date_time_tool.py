from datetime import datetime
from src.tools.base_tool import BaseTool


class DateTimeTool(BaseTool):
    """
    Tool for retrieving the current date and time.
    """

    @property
    def name(self) -> str:
        return "datetime"

    @property
    def description(self) -> str:
        return "Returns the current date, time, and day."

    def execute(self, **kwargs):

        now = datetime.now()

        return {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day": now.strftime("%A"),
        }