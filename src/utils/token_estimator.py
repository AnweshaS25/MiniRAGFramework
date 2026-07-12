class TokenEstimator:
    """
    Utility for estimating the number of tokens in text.

    This is a lightweight approximation.

    Later we can replace this with model-specific tokenizers
    like tiktoken or HuggingFace tokenizers.
    """

    @staticmethod
    def estimate(text: str) -> int:

        if not text:
            return 0

        # Approximation:
        # 1 token ≈ 4 characters
        return max(1, len(text) // 4)