from src.memory.conversation_buffer_memory import ConversationBufferMemory
from src.memory.conversation_window_memory import ConversationWindowMemory
from src.memory.summary_memory import SummaryMemory

from src.memory.memory_manager import MemoryManager

from src.llms.groq_llm import GroqLLM


llm = GroqLLM()

buffer = ConversationBufferMemory()

window = ConversationWindowMemory(
    window_size=2,
)

summary = SummaryMemory(
    llm=llm,
    summarize_after=6,
)

manager = MemoryManager(
    buffer_memory=buffer,
    window_memory=window,
    summary_memory=summary,
)


manager.add_message(
    role="user",
    content="Question 1",
)

manager.add_message(
    role="assistant",
    content="Answer 1",
)

manager.add_message(
    role="user",
    content="Question 2",
)

manager.add_message(
    role="assistant",
    content="Answer 2",
)

manager.add_message(
    role="user",
    content="Question 3",
)

manager.add_message(
    role="assistant",
    content="Answer 3",
)


print("\nCombined Context\n")
print(manager.get_context())


print("\nFull History\n")
print(manager.get_full_history())


manager.clear()

assert manager.get_context() == ""
assert manager.get_full_history() == ""

print("\nMemoryManager test passed!")