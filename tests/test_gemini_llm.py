import os

from src.factories.llm_factory import LLMFactory
from src.constants import LLMTypes

from dotenv import load_dotenv

load_dotenv()


def main():

    print("=" * 80)
    print("Creating Gemini LLM")
    print("=" * 80)

    llm = LLMFactory.create(
        llm_type=LLMTypes.GEMINI,
        api_key=os.getenv("GOOGLE_API_KEY"),
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