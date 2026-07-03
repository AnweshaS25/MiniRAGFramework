from src.security.base_guard import BaseGuard
from src.security.security_result import SecurityResult


class OutputGuard(BaseGuard):
    """
    Checks whether an LLM response contains sensitive information.
    """

    BLOCKED_PATTERNS = [
        "system prompt",
        "developer instructions",
        "api key",
        "secret key",
        "openai_api_key",
        "groq_api_key",
        "password",
        "ignore previous instructions",
        "internal prompt",
    ]

    def validate(self, text: str) -> SecurityResult:

        lowered = text.lower()

        for pattern in self.BLOCKED_PATTERNS:

            if pattern in lowered:
                return SecurityResult(
                    safe=False,
                    reason=(
                        "The generated response contains sensitive "
                        "or internal information and has been blocked."
                    ),
                )

        return SecurityResult(
            safe=True,
        )