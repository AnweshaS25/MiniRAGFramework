from src.constants import RerankerTypes

from src.rerankers.no_reranker import NoReranker
from src.rerankers.cross_encoder_reranker import (CrossEncoderReranker,)

class RerankerFactory:
    """
    Factory class for creating rerankers.
    """

    @staticmethod
    def create(reranker_type: str, **kwargs,):

        if reranker_type == RerankerTypes.NONE:
            return NoReranker()
        
        elif reranker_type == RerankerTypes.CROSS_ENCODER:
            return CrossEncoderReranker(
                model_name=kwargs.get(
                    "model_name",
                    "cross-encoder/ms-marco-MiniLM-L-6-v2",
                ),
            )

        raise ValueError(
            f"Unsupported reranker: {reranker_type}"
        )