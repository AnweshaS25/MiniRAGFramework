from src.prompts.default_prompt_template import DefaultPromptTemplate

def main():
    print("Inside main")

    template = DefaultPromptTemplate()

    print("DefaultPromptTemplate initialized successfully!\n")

    prompt = template.format(
        question="What is RAG?",
        context="RAG stands for Retrieval-Augmented Generation."
    )

    # Validate return type
    assert isinstance(prompt, str)

    # Validate contents
    assert "What is RAG?" in prompt
    assert "RAG stands for Retrieval-Augmented Generation." in prompt

    print("Formatted Prompt")
    print("-" * 40)
    print(prompt)
    print()

    print("DefaultPromptTemplate test passed!")


if __name__ == "__main__":
    main()