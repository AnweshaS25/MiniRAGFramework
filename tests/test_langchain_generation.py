from benchmarks.langchain.langchain_pipeline import LangChainPipeline

pipeline = LangChainPipeline(
    "data/BTechProject1_Final.pdf"
)

documents = pipeline.load_documents()
chunks = pipeline.split_documents(documents)
pipeline.index_documents(chunks)

questions = [
    "What is this project about?",
    "What database is used in the project?",
    "What frontend framework is used?",
]

for question in questions:

    print("=" * 80)
    print("QUESTION:")
    print(question)

    answer = pipeline.generate(question)

    print("\nANSWER:")
    print(answer)
    print("=" * 80)