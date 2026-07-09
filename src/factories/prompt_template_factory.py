from src.prompts.default_prompt_template import DefaultPromptTemplate
from src.prompts.concise_prompt_template import ConcisePromptTemplate
from src.prompts.summary_prompt_template import SummaryPromptTemplate
from src.prompts.citation_prompt_template import CitationPromptTemplate

from src.constants import PromptTemplateTypes


class PromptTemplateFactory:
    """
    Factory class for creating prompt templates.
    """

    @staticmethod
    def create(prompt_template_type: str):

        if prompt_template_type == PromptTemplateTypes.DEFAULT:
            return DefaultPromptTemplate()
        
        if prompt_template_type == PromptTemplateTypes.CONCISE:
            return ConcisePromptTemplate()
        
        if prompt_template_type == PromptTemplateTypes.SUMMARY:
            return SummaryPromptTemplate()

        if prompt_template_type == PromptTemplateTypes.CITATION:
            return CitationPromptTemplate()

        raise ValueError(
            f"Unsupported prompt template: {prompt_template_type}"
        )