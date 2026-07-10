from dataclasses import dataclass
from typing import List


@dataclass
class LLMMetadata:
    """
    Metadata describing an LLM plugin.
    """

    name: str
    description: str
    strengths: List[str]
    is_local: bool
    context_window: int