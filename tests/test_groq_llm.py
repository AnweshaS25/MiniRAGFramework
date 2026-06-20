from src.core.llm_response import LLMResponse
from src.llms.groq_llm import GroqLLM

def main():
    print("Inside main")

    # Initialize the LLM
    llm = GroqLLM()

    print("GroqLLM initialized successfully!\n")

    # Generate a response
    response = llm.generate(
        "What is the capital of France?"
    )

    # Validate return type
    assert isinstance(response, LLMResponse)

    # Validate response text
    assert response.text.strip()

    print("Response")
    print("-" * 40)
    print(response.text)
    print()

    print("Model")
    print("-" * 40)
    print(response.model)
    print()

    print("Prompt Tokens")
    print("-" * 40)
    print(response.prompt_tokens)
    print()

    print("Completion Tokens")
    print("-" * 40)
    print(response.completion_tokens)
    print()

    print("Total Tokens")
    print("-" * 40)
    print(response.total_tokens)
    print()

    print("GroqLLM test passed!")


if __name__ == "__main__":
    main()