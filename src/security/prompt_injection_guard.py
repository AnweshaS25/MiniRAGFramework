import re

from src.security.base_guard import BaseGuard
from src.security.security_result import SecurityResult


class PromptInjectionGuard(BaseGuard):
    """
    Detects simple prompt injection attempts.
    """

    BLOCKED_PATTERNS = [
        "ignore previous instructions",
        "forget previous instructions",
        "system prompt",
        "developer instructions",
        "act as",
        "you are now",
        "bypass",
        "override",
        "jailbreak",
    ]

    STOP_WORDS = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "to",
        "of",
        "for",
        "please",
        "all",
    }

    def _normalize(self, text: str) -> str:
        """
        Normalize text before checking.
        """

        text = text.lower()

        text = re.sub(r"[^\w\s]", "", text)

        words = [
            word
            for word in text.split()
            if word not in self.STOP_WORDS
        ]

        return " ".join(words)

    def validate(self, text: str) -> bool:

        normalized = self._normalize(text)

        for pattern in self.BLOCKED_PATTERNS:

            if self._normalize(pattern) in normalized:
                return SecurityResult(safe=False, reason="Rule-based prompt injection detected.",)

        return SecurityResult(safe=True,)