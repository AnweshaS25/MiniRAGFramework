from transformers import AutoTokenizer


class TokenEstimator:
    """
    Estimates tokens using the same tokenizer
    family as the embedding model.
    """

    _tokenizer = AutoTokenizer.from_pretrained(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    @classmethod
    def estimate(cls, text: str) -> int:
        if not text:
            return 0

        return len(
            cls._tokenizer.encode(
                text,
                add_special_tokens=False,
            )
        )