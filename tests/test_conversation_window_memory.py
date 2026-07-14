from src.memory.conversation_window_memory import ConversationWindowMemory

from src.factories.memory_factory import MemoryFactory
from src.constants import MemoryTypes



# memory = ConversationWindowMemory()

# memory = MemoryFactory.create(
#     MemoryTypes.CONVERSATION_WINDOW,
# )

memory = ConversationWindowMemory(window_size=2)


memory.add_message(
    role="user",
    content="Question 1",
)

memory.add_message(
    role="assistant",
    content="Answer 1",
)

memory.add_message(
    role="user",
    content="Question 2",
)

memory.add_message(
    role="assistant",
    content="Answer 2",
)

memory.add_message(
    role="user",
    content="Question 3",
)

memory.add_message(
    role="assistant",
    content="Answer 3",
)

print("\nConversation Context\n")
print(memory.get_context())

assert "Question 1" not in memory.get_context()
assert "Answer 1" not in memory.get_context()

assert "Question 2" in memory.get_context()
assert "Answer 2" in memory.get_context()

assert "Question 3" in memory.get_context()
assert "Answer 3" in memory.get_context()

assert len(memory.messages) == 4  #when window_size=2

print("\nConversationWindowMemory test passed!")