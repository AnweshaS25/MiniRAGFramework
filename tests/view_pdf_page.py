from benchmarks.langchain.langchain_pipeline import LangChainPipeline

pipeline = LangChainPipeline("data/BTechProject1_Final.pdf")

documents = pipeline.load_documents()

for page_number, doc in enumerate(documents, start=1):

    print("=" * 80)
    print(f"PAGE {page_number}")
    print("=" * 80)
    print(doc.page_content)
    print("\n\n")