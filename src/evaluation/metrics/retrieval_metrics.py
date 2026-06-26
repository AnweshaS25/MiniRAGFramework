from typing import Set

def precision_at_k(retrieved_ids: list[str], relevant_ids: Set[str], k: int,) -> float:
    """
    Compute Precision@k.
    """

    if k <= 0:
        raise ValueError("k must be greater than 0.")
    
    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0
    
    relevant_count = sum(
        doc_id in relevant_ids
        for doc_id in retrieved
    )

    return relevant_count / len(retrieved)



def recall_at_k(retrieved_ids: list[str], relevant_ids: Set[str], k: int,) -> float:
    """
    Compute Recall@k.
    """

    if k <= 0:
        raise ValueError("k must be greater than 0.")

    if not relevant_ids:
        return 0.0
    
    retrieved = retrieved_ids[:k]

    relevant_count = sum(
        doc_id in relevant_ids
        for doc_id in retrieved
    )

    return relevant_count / len(relevant_ids)



def hit_rate(retrieved_ids: list[str], relevant_ids: Set[str], k: int,) -> float:
    """
    Compute Hit Rate@k.
    """

    if k <= 0:
        raise ValueError("k must be greater than 0.")
    
    if not relevant_ids:
        return 0.0

    retrieved = retrieved_ids[:k]

    return float(
        any(
            doc_id in relevant_ids
            for doc_id in retrieved
        )
    )



def mean_reciprocal_rank(retrieved_ids: list[str], relevant_ids: Set[str], k: int,) -> float:
    """
    Compute Reciprocal Rank (RR) for a single query.
    """

    if k <= 0:
        raise ValueError("k must be greater than 0.")

    if not relevant_ids:
        return 0.0
    
    retrieved = retrieved_ids[:k]

    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
        
    return 0.0 
