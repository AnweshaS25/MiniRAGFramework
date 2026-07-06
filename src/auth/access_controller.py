from src.auth.user import User


class AccessController:
    """
    Responsible for checking whether a user
    has a particular permission.
    """

    @staticmethod
    def has_permission(user: User, permission_name: str, ) -> bool:

        for role in user.roles:

            for permission in role.permissions:

                if permission.name == permission_name:
                    return True

        return False