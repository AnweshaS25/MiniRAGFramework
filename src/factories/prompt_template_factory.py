from src.prompts.default_prompt_template import DefaultPromptTemplate

from src.constants import PromptTemplateTypes


class PromptTemplateFactory:
    """
    Factory class for creating prompt templates.
    """

    @staticmethod
    def create(prompt_template_type: str):

        if prompt_template_type == PromptTemplateTypes.DEFAULT:
            return DefaultPromptTemplate()

        raise ValueError(
            f"Unsupported prompt template: {prompt_template_type}"
        )