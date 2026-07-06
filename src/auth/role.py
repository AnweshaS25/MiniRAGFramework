from dataclasses import dataclass
from typing import List

from src.auth.permission import Permission

#Roles should be immutable because they represent fixed identities within the authorization system.

@dataclass(frozen=True)  
class Role:
    """
    Represents a user role.
    """

    name: str
    permissions: List[Permission]
    