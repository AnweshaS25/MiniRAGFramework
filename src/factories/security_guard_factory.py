from src.constants import SecurityTypes

from src.security.prompt_injection_guard import PromptInjectionGuard
from src.security.semantic_prompt_injection_guard import SemanticPromptInjectionGuard

from src.security.attacks.attack_dataset import AttackDataset

from src.embeddings.base_embeddings import BaseEmbeddings


class SecurityGuardFactory:
    """
    Factory for creating security guards.
    """

    @staticmethod
    def create(security_type: str, embedding_model: BaseEmbeddings = None,):

        if security_type == SecurityTypes.RULE_BASED:
            return PromptInjectionGuard()
        
        elif security_type == SecurityTypes.SEMANTIC:
            if embedding_model is None:
                raise ValueError(
                    "embedding_model cannot be None for SemanticPromptInjectionGuard."
                )
        
            dataset = AttackDataset()
            return SemanticPromptInjectionGuard(embedding_model=embedding_model,dataset=dataset,)
        
        raise ValueError(f"Unsupported security guard: {security_type}")
