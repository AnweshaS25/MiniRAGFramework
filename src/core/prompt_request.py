from dataclasses import dataclass


@dataclass
class PromptRequest:
    """
    Represents the prompt template selected for a query.
    """

    prompt_type: str