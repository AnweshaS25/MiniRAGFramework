from src.prompts.base_prompt_template import BasePromptTemplate


class SummaryPromptTemplate(BasePromptTemplate):
    """
    Prompt template optimized for document summarization.
    """

    _TEMPLATE = """
You are an expert document summarizer.

Use ONLY the provided context.

Produce a clear and structured summary.

Requirements:
- Focus on the main ideas.
- Do not invent information.
- Ignore irrelevant details.
- Use bullet points where appropriate.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Summary:
"""

    def format(self, **kwargs) -> str:

        question = kwargs["question"]
        context = kwargs["context"]
        history = kwargs.get("history", "")

        if not question.strip():
            raise ValueError("question cannot be empty.")

        if context is None:
            raise ValueError("context cannot be None.")

        return self._TEMPLATE.format(
            question=question,
            context=context,
            history=history,
        )