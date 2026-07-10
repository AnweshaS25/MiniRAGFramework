class LLMRouterPrompt:
    """
    Builds the prompt used by the LLM Router.
    """

    @staticmethod
    def build(query: str, registry):

        llm_descriptions = ""

        for metadata in registry.list_metadata():

            strengths = ", ".join(metadata.strengths)

            llm_descriptions += f"""
- {metadata.name}
    Description: {metadata.description}
    Strengths: {strengths}
    Local: {metadata.is_local}
    Context Window: {metadata.context_window}

"""

        return f"""
You are an intelligent LLM router.

Your task is to choose the BEST LLM for answering the user's query.

Available LLMs:

{llm_descriptions}

Return ONLY valid JSON.

Example:

{{
    "llm_type": "groq"
}}

User Query:
{query}
"""