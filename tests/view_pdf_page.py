from benchmarks.langchain.langchain_pipeline import LangChainPipeline

pipeline = LangChainPipeline("data/BTechProject1_Final.pdf")

documents = pipeline.load_documents()

PAGE = 4   # change this

doc = documents[PAGE - 1]

print("=" * 80)
print(f"PAGE {PAGE}")
print("=" * 80)
print(doc.page_content)