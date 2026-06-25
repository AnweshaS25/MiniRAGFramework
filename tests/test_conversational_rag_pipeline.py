from src.constants import (EmbeddingTypes, VectorStoreTypes, RetrieverTypes,)

from src.factories.embedding_factory import EmbeddingFactory
from src.factories.vector_store_factory import VectorStoreFactory
from src.factories.retriever_factory import RetrieverFactory

from src.prompts.default_prompt_template import DefaultPromptTemplate

from src.llms.ollama_llm import OllamaLLM

from src.memory.conversation_buffer_memory import ConversationBufferMemory

from src.pipelines.conversational_rag_pipeline import (
    ConversationalRAGPipeline,
)

from src.core.document import Document

print("=" * 80)
print("Creating embedding model")
print("=" * 80)

embedding_model = EmbeddingFactory.create(
    EmbeddingTypes.HUGGINGFACE,
)

documents = [
    Document(
        content="Retrieval-Augmented Generation combines retrieval with language models."
    ),
    Document(
        content="RAG retrieves documents before generating answers."
    ),
    Document(
        content="Vector databases store embeddings."
    ),
]


documents = embedding_model.embed_documents(
    documents,
)


vector_store = VectorStoreFactory.create(
    VectorStoreTypes.IN_MEMORY,
)

vector_store.add_documents(
    documents,
)


retriever = RetrieverFactory.create(
    RetrieverTypes.SIMILARITY,
    embedding_model=embedding_model,
    vector_store=vector_store,
)


prompt_template = DefaultPromptTemplate()


llm = OllamaLLM(
    model="llama3.2",
)


memory = ConversationBufferMemory()


pipeline = ConversationalRAGPipeline(
    retriever=retriever,
    prompt_template=prompt_template,
    llm=llm,
    memory=memory,
)


print("\n")
print("=" * 80)
print("Question 1")
print("=" * 80)

response = pipeline.run(
    query="What is RAG?",
    k=2,
)

print(response.text)


print("\n")
print("=" * 80)
print("Question 2")
print("=" * 80)

response = pipeline.run(
    query="Can you explain that more simply?",
    k=2,
)

print(response.text)


#Verify Memory
print("\n")
print("=" * 80)
print("Conversation Memory")
print("=" * 80)

print(memory.get_context())