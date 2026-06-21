from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.vectorstores.chroma_vector_store import ChromaVectorStore

from src.retrievers.similarity_retriever import SimilarityRetriever

from src.prompts.default_prompt_template import DefaultPromptTemplate

from src.llms.groq_llm import GroqLLM

from src.pipelines.rag_pipeline import RAGPipeline


embedding_model = HuggingFaceEmbeddings()

vector_store = ChromaVectorStore(              # Connecting to the already indexed database
    collection_name="test_indexing_pipeline",
    persist_directory="./test_chroma_db",
)

# Retriever
retriever = SimilarityRetriever(
    embedding_model=embedding_model,
    vector_store=vector_store,
)

#Prompt
prompt_template = DefaultPromptTemplate()

# LLM
llm = GroqLLM()

# Pipeline
pipeline = RAGPipeline(
    retriever=retriever,
    prompt_template=prompt_template,
    llm=llm,
)

response = pipeline.run(
    query="Are Cart and Wishlist used here?",
    k=3,
)


#Assertions
assert response.text
assert len(response.text.strip()) > 0
assert response.model == llm.model_name

# Printing Results

print("Answer")
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

print("RAGPipeline test passed!")