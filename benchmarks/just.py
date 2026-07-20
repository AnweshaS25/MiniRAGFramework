from benchmarks.langchain.langchain_pipeline import LangChainPipeline

pipeline = LangChainPipeline("data/BTechProject1_Final.pdf")

documents = pipeline.load_documents()

for doc in documents:
    print("=" * 80)
    print(f"PAGE {doc.metadata['page'] + 1}")
    print("=" * 80)
    print(doc.page_content[:1000])   # first 1000 characters
    print()