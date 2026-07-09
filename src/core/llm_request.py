from dataclasses import dataclass, field


@dataclass
class LLMRequest:
    """
    Represents a request to use a particular LLM.
    """

    llm_type: str

    arguments: dict = field(default_factory=dict)