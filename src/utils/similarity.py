from typing import List

import numpy as np


def cosine_similarity(vector1: List[float], vector2: List[float],) -> float:
    """
    Compute cosine similarity between two vectors.
    """

    if len(vector1) != len(vector2):
        raise ValueError(
            "Vectors must have the same dimensions."
        )

    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = np.dot(
        vector1,
        vector2,
    ) / (norm1 * norm2)

    return float(similarity)