from src.constants import SecurityTypes

from src.security.prompt_injection_guard import PromptInjectionGuard
from src.security.semantic_prompt_injection_guard import SemanticPromptInjectionGuard
from src.security.llm_prompt_injection_guard import LLMPromptInjectionGuard

from src.security.attacks.attack_dataset import AttackDataset

from src.embeddings.base_embeddings import BaseEmbeddings
from src.llms.base_llm import BaseLLM


class SecurityGuardFactory:
    """
    Factory for creating security guards.
    """

    @staticmethod
    def create(security_type: str, embedding_model: BaseEmbeddings = None, llm: BaseLLM = None,):

        if security_type == SecurityTypes.RULE_BASED:
            return PromptInjectionGuard()
        

        elif security_type == SecurityTypes.SEMANTIC:

            if embedding_model is None:
                raise ValueError(
                    "embedding_model cannot be None for SemanticPromptInjectionGuard."
                )
            dataset = AttackDataset()
            return SemanticPromptInjectionGuard(embedding_model=embedding_model,dataset=dataset,)
        

        elif security_type == SecurityTypes.LLM:

            if llm is None:
                raise ValueError(
                    "llm cannot be None for LLMPromptInjectionGuard."
                )

            return LLMPromptInjectionGuard(llm=llm,)
        
        raise ValueError(f"Unsupported security guard: {security_type}")
