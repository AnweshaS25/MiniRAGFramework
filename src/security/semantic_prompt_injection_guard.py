from sentence_transformers import util

from src.security.base_guard import BaseGuard
from src.security.attacks.attack_dataset import AttackDataset
from src.embeddings.base_embeddings import BaseEmbeddings

from src.security.security_result import SecurityResult


class SemanticPromptInjectionGuard(BaseGuard):

    def __init__(self, embedding_model: BaseEmbeddings, dataset: AttackDataset,threshold: float = 0.85,):

        self.embedding_model = embedding_model
        self.dataset = dataset
        self.threshold = threshold

        self.attack_documents = self.dataset.get_documents()

        self.attack_documents = self.embedding_model.embed_documents(self.attack_documents)


        self.attack_embeddings = [
            document.embedding
            for document in self.attack_documents
        ]



    def validate(self, prompt: str) -> SecurityResult:
        query_embedding = self.embedding_model.embed_query(prompt)

        similarities = util.cos_sim(
            query_embedding,
            self.attack_embeddings,
        )[0]

        max_index = similarities.argmax().item()

        max_similarity = similarities[max_index].item()
        matched_attack = self.attack_documents[max_index].content
    
        return SecurityResult(
            safe=max_similarity < self.threshold,
            similarity=max_similarity,
            matched_attack=matched_attack,
            reason=(
                "Semantic prompt injection detected."
                if max_similarity >= self.threshold
                else None
            ),
        )