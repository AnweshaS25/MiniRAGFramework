from src.prompts.base_prompt_template import BasePromptTemplate


class CitationPromptTemplate(BasePromptTemplate):
    """
    Prompt template that encourages grounded answers with citations.
    """

    _TEMPLATE = """
You are a Retrieval-Augmented Generation (RAG) assistant.

Answer ONLY using the provided context.

Requirements:
- Do not invent information.
- If the answer is unavailable, say:
  "I don't know based on the provided context."
- When possible, mention which part of the retrieved context supports your answer.
- Keep the answer factual and grounded.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer:
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