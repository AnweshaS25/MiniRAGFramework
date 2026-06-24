from src.factories.llm_factory import LLMFactory
from src.constants import LLMTypes


def main():

    print("=" * 80)
    print("Creating Ollama LLM")
    print("=" * 80)

    llm = LLMFactory.create(
        llm_type=LLMTypes.OLLAMA,
        model="llama3.2",
    )

    print("\nGenerating response...\n")

    response = llm.generate(
        "Explain Retrieval-Augmented Generation in one sentence."
    )

    print("Response:")
    print(response.text)

    print("\nModel:")
    print(response.model)


if __name__ == "__main__":
    main()