


class PromptRouterPrompt:
    """
    Builds the prompt used by the LLM Prompt Router.
    """

    @staticmethod
    def build(query: str, registry) -> str:

        prompt_descriptions = []

        for prompt in registry.list_prompts():

            prompt_descriptions.append(
                f"- {prompt.name}: {prompt.description}"
            )

        prompts = "\n".join(prompt_descriptions)

        return f"""
You are a prompt routing assistant.

Available prompt templates:

{prompts}

Your job is to choose the BEST prompt template.

Return ONLY valid JSON.

Example:

{{
    "prompt_type": "summary"
}}

User Query:
{query}
"""