from src.memory.base_memory import BaseMemory
from src.llms.base_llm import BaseLLM
from src.llms.llm_manager import LLMManager

from src.memory_retrieval.memory_document import MemoryDocument


class SummaryMemory(BaseMemory):
    """
    Stores a running summary of the conversation.
    """

    def __init__(
        self,
        llm_manager:LLMManager,
        summarize_after: int = 6,
    ):
        
        if llm_manager is None:
            raise ValueError(
                "llm_manager cannot be None."
            )

        self.llm_manager = llm_manager
        self.summary = ""
        self.recent_messages = []
        self.summarize_after = summarize_after


    def add_message(self, role: str, content: str) -> None:
        if role not in ("user", "assistant"):
            raise ValueError(
                "role must be either 'user' or 'assistant'."
            )

        if not content.strip():
            raise ValueError(
                "content cannot be empty."
            )

        self.recent_messages.append(
            MemoryDocument(
                content=content,
                metadata={
                    "role": role,
                }
            )
        )

        # TODO:
        # Summarize every 6 messages
        if len(self.recent_messages) >= self.summarize_after:
            self._summarize_recent_messages()


    def get_context(self) -> str:
        sections = []

        if self.summary:
            sections.append(
                f"Conversation Summary:\n{self.summary}"
            )

        if self.recent_messages:

            history = []

            for message in self.recent_messages:
                history.append(
                    f"{message.metadata['role'].capitalize()}: {message.content}"
                )

            sections.append(
                "Recent Conversation:\n"
                + "\n".join(history)
            )

        return "\n\n".join(sections)


    def clear(self) -> None:
        self.summary = ""
        self.recent_messages.clear()


    def _summarize_recent_messages(self):
        conversation = []

        for message in self.recent_messages:
            conversation.append(
                f"{message.metadata['role'].capitalize()}: {message.content}"
            )

        conversation = "\n".join(conversation)

        prompt = f"""
        You are maintaining a conversation summary.

        Your job is to update the existing summary with the recent conversation.

        Current Summary:
        {self.summary}

        Recent Conversation:
        {conversation}

        Write an updated conversation summary.

        The summary is for another AI assistant, not for the user.

        Include:
        - user goals
        - important facts
        - decisions made
        - ongoing tasks (if any)

        Write only the summary.

        Do NOT write:
        - introductions
        - conclusions
        - explanations
        - phrases like "Here is the summary..."
        - phrases like "There were no ongoing tasks..."

        Keep it under 150 words.
        """

        response = self.llm_manager.generate(
            query="conversation summary",
            prompt=prompt,
        )

        self.summary = response.text.strip() 

        self.recent_messages.clear()