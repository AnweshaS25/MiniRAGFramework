from dataclasses import dataclass
from typing import List

from src.auth.role import Role


@dataclass
class User:
    """
    Represents an authenticated user.
    """

    username: str
    roles: List[Role]