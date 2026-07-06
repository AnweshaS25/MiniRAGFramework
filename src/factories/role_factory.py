from src.auth.role import Role
from src.auth.permission import Permission

from src.constants import RoleTypes


class RoleFactory:
    """
    Factory for creating predefined roles.
    """

    @staticmethod
    def create(role_name: str) -> Role:

        role_name = role_name.lower()

        if role_name == RoleTypes.ADMIN:
            return Role(
                name="Admin",
                permissions=[
                    Permission("VIEW_ALL_DOCUMENTS"),
                    Permission("UPLOAD_DOCUMENTS"),
                    Permission("DELETE_DOCUMENTS"),
                ],
            )

        elif role_name == RoleTypes.HR:
            return Role(
                name="HR",
                permissions=[
                    Permission("VIEW_HR_DOCUMENTS"),
                ],
            )

        elif role_name == RoleTypes.FINANCE:
            return Role(
                name="Finance",
                permissions=[
                    Permission("VIEW_FINANCE_DOCUMENTS"),
                ],
            )

        elif role_name == RoleTypes.ENGINEERING:
            return Role(
                name="Engineering",
                permissions=[
                    Permission("VIEW_ENGINEERING_DOCUMENTS"),
                ],
            )

        raise ValueError(
            f"Unsupported role: {role_name}"
        )