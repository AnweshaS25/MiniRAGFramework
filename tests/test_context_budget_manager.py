from src.utils.context_budget_manager import ContextBudgetManager

manager = ContextBudgetManager()

budget = manager.compute_budget(
    context_window=12000,
    prompt_tokens=1000,
)

print("Budget:", budget)

assert budget == 9976

print("ContextBudgetManager test passed!")