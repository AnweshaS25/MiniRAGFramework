from dataclasses import dataclass

#A permission represents one specific action that a user is allowed to perform.

@dataclass(frozen=True)
class Permission:
    """
    Represents a permission that can be granted to a role.
    """

    name: str