from src.prompts.base_prompt_template import BasePromptTemplate

class DefaultPromptTemplate(BasePromptTemplate):
    """
    Default prompt template for Retrieval-Augmented Generation (RAG).
    """

    _TEMPLATE = """
You are a helpful AI assistant.

Use only the information provided in the context below to answer the user's question.

If the answer cannot be found in the context, say:
"I don't know based on the provided context."

Do not make up information.

### Context:
{context}

### Question:
{question}

### Answer:
"""

    def format(self, question: str, context: str) -> str:

        if not question.strip():
            raise ValueError("question cannot be empty.")

        if not context.strip():
            raise ValueError("context cannot be empty.")

        return self._TEMPLATE.format(
            context=context,
            question=question,
        )