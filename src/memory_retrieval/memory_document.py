from dataclasses import dataclass
from typing import Dict


@dataclass
class MemoryDocument:
    """
    Represents one conversational memory entry.
    """

    content: str
    metadata: Dict