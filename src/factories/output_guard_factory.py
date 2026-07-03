from src.security.output_guard import OutputGuard


class OutputGuardFactory:
    """
    Factory for creating output guards.
    """

    @staticmethod
    def create():
        return OutputGuard()