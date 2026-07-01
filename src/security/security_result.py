from dataclasses import dataclass
from typing import Optional


@dataclass
class SecurityResult:
    safe: bool
    similarity: Optional[float] = None
    matched_attack: Optional[str] = None
    reason: Optional[str] = None