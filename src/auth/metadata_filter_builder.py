from src.auth.user import User


class MetadataFilterBuilder:
    """
    Builds metadata filters from a user's permissions.
    """

    @staticmethod
    def build(user: User) -> dict:

        permissions = set()

        for role in user.roles:
            for permission in role.permissions:
                permissions.add(permission.name)

        if "VIEW_ALL_DOCUMENTS" in permissions:
            return None

        return {
            "permission": {
                "$in": list(permissions)
            }
        }