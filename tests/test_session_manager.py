from src.sessions.session_manager import SessionManager

from src.memory.memory_manager import MemoryManager

from src.memory.conversation_buffer_memory import ConversationBufferMemory
from src.memory.conversation_window_memory import ConversationWindowMemory
from src.memory.summary_memory import SummaryMemory

from src.llms.groq_llm import GroqLLM


llm = GroqLLM()


def create_memory():

    return MemoryManager(
        summary_memory=SummaryMemory(
            llm=llm,
            summarize_after=6,
        ),
        window_memory=ConversationWindowMemory(
            window_size=2,
        ),
        buffer_memory=ConversationBufferMemory(),
    )


session_manager = SessionManager(
    memory_factory=create_memory,
)


# Create two independent sessions

session1 = session_manager.create_session()

session2 = session_manager.create_session()


# Add conversation only to session1

session1.memory.add_message(
    role="user",
    content="Hello from Session 1",
)

session1.memory.add_message(
    role="assistant",
    content="Hi Session 1",
)

session1_context = session1.memory.get_context()
session2_context = session2.memory.get_context()

print("\nSession 1\n")
print(session1_context)

print("\nSession 2\n")
print(session2_context)


# Session IDs should be different

assert session1.session_id != session2.session_id


# Session 1 should contain its messages

assert "Hello from Session 1" in session1.memory.get_context()


# Session 2 should be empty

# assert session2.memory.get_context() == ""
assert session2_context == ""


print("\nSessionManager test passed!")