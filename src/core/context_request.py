from dataclasses import dataclass


@dataclass
class ContextRequest:
    """
    Represents the context strategy selected by a context router.
    """

    context_strategy: str