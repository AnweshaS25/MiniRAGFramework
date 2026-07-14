from src.memory.summary_memory import SummaryMemory
from src.llms.ollama_llm import OllamaLLM

llm = OllamaLLM(
    model="llama3.2",
)

memory = SummaryMemory(
    llm=llm,
    summarize_after=6,
)


memory.add_message(
    "user",
    "What are the functional requirements of the Grocery Store Management System?"
)

memory.add_message(
    "assistant",
    "The functional requirements include product management, cart management, billing, inventory management..."
)

memory.add_message(
    "user",
    "Can you explain the non-functional requirements?"
)

memory.add_message(
    "assistant",
    "The non-functional requirements include usability, security, reliability..."
)

memory.add_message(
    "user",
    "What database should I use?"
)

memory.add_message(
    "assistant",
    "SQLite is suitable for development, while PostgreSQL is recommended for production."
)


# memory.add_message("user", "Question 1")
# memory.add_message("assistant", "Answer 1")

# memory.add_message("user", "Question 2")
# memory.add_message("assistant", "Answer 2")

# memory.add_message("user", "Question 3")
# memory.add_message("assistant", "Answer 3")


print("\nSummary\n")
print(memory.summary)

print("\nContext\n")
print(memory.get_context())


assert memory.summary != ""
assert len(memory.recent_messages) == 0