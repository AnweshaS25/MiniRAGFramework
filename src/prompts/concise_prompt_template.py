from src.prompts.base_prompt_template import BasePromptTemplate


class ConcisePromptTemplate(BasePromptTemplate):
    """
    Prompt template that produces short, concise answers.
    """

    name = "concise"
    description = "Use when the user requests a brief or short answer."

    _TEMPLATE = """
You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer cannot be found in the context, say:

"I don't know based on the provided context."

Answer in no more than 2-3 sentences.

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