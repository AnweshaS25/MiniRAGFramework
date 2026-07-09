from src.constants import PromptTemplateTypes


class PromptRouterPrompt:
    """
    Builds the prompt used by the LLM Prompt Router.
    """

    @staticmethod
    def build(query: str) -> str:

        return f"""
You are a prompt routing assistant.

Available prompt templates:

- {PromptTemplateTypes.DEFAULT}
    Use for normal question answering.

- {PromptTemplateTypes.CONCISE}
    Use when the user requests a brief, short, or concise answer.

- {PromptTemplateTypes.SUMMARY}
    Use when the user asks for a summary or overview.

- {PromptTemplateTypes.CITATION}
    Use when the user asks for sources, citations, pages, or evidence.

Your job is to choose the BEST prompt template.

Return ONLY valid JSON.

Example:

{{
    "prompt_type": "summary"
}}

User Query:
{query}
"""