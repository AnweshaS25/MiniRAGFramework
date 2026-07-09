from src.prompts.base_prompt_template import BasePromptTemplate

class DefaultPromptTemplate(BasePromptTemplate):
    """
    Default prompt template for Retrieval-Augmented Generation (RAG).
    """

    name = "default"
    description = "Use for normal question answering."

    _TEMPLATE = """
You are a helpful AI assistant.

Use only the information provided in the context below to answer the user's question.

If the answer cannot be found in the context, say:
"I don't know based on the provided context."

Do not make up information.

### Conversation History:
{history}

### Context:
{context}

### Question:
{question}

### Answer:
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