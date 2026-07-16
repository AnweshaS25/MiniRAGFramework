from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.vectorstores.chroma_vector_store import ChromaVectorStore

from src.loaders.pdf_loader import PDFLoader

from src.retrievers.similarity_retriever import SimilarityRetriever

from src.prompts.default_prompt_template import DefaultPromptTemplate

from src.llms.groq_llm import GroqLLM
from src.llms.gemini_llm import GeminiLLM
from src.llms.ollama_llm import OllamaLLM

from src.pipelines.rag_pipeline import RAGPipeline

from src.factories.reranker_factory import RerankerFactory
from src.constants import RerankerTypes

from src.factories.context_strategy_factory import ContextStrategyFactory
from src.factories.token_budget_strategy_factory import TokenBudgetStrategyFactory

from src.factories.security_guard_factory import SecurityGuardFactory
from src.factories.output_guard_factory import OutputGuardFactory
from src.constants import SecurityTypes

from src.tools.tool_registry import ToolRegistry
from src.tools.tool_executor import ToolExecutor
from src.tools.tool_manager import ToolManager
from src.tools.calculator_tool import CalculatorTool
from src.tools.date_time_tool import DateTimeTool

from src.tool_routing.rule_based_tool_router import RuleBasedToolRouter

from src.auth.user import User
from src.factories.role_factory import RoleFactory
from src.constants import RoleTypes
from src.constants import LLMTypes

from src.prompts.prompt_manager import PromptManager
from src.prompt_routing.rule_based_prompt_router import RuleBasedPromptRouter
from src.prompt_routing.llm_prompt_router import LLMPromptRouter

from src.llm_routing.rule_based_llm_router import RuleBasedLLMRouter
from src.llms.llm_manager import LLMManager
from src.prompts.llm_router_prompt import LLMRouterPrompt
from src.llm_routing.llm_llm_router import LLMLLMRouter

from src.prompts.prompt_router_prompt import PromptRouterPrompt

from src.prompts.prompt_registry import PromptRegistry
from src.prompts.default_prompt_template import DefaultPromptTemplate
from src.prompts.summary_prompt_template import SummaryPromptTemplate
from src.prompts.concise_prompt_template import ConcisePromptTemplate
from src.prompts.citation_prompt_template import CitationPromptTemplate

from src.llms.llm_registry import LLMRegistry

from src.llm_strategies.default_fallback_strategy import DefaultFallbackStrategy


from src.strategies.context_registry import ContextRegistry
from src.strategies.context_manager import ContextManager

from src.strategies.default_context_strategy import DefaultContextStrategy
from src.strategies.hybrid_context_strategy import HybridContextStrategy
from src.strategies.lcm_context_strategy import LCMContextStrategy

from src.context_routing.rule_based_context_router import RuleBasedContextRouter

from src.document_store.in_memory_document_store import InMemoryDocumentStore

from src.context_routing.llm_context_router import LLMContextRouter
from src.prompts.context_router_prompt import ContextRouterPrompt


embedding_model = HuggingFaceEmbeddings()

vector_store = ChromaVectorStore(              # Connecting to the already indexed database
    collection_name="test_indexing_pipeline",
    persist_directory="./test_chroma_db",
)

document_store = InMemoryDocumentStore()

loader = PDFLoader("data/BTechProject1_Final.pdf")

original_documents = loader.load()

document_store.add_documents(original_documents)

# Retriever
retriever = SimilarityRetriever(
    embedding_model=embedding_model,
    vector_store=vector_store,
)

# LLM
# llm = GroqLLM()
routing_llm = GroqLLM()

llm_registry = LLMRegistry()

groq_llm = GroqLLM()
gemini_llm = GeminiLLM()
ollama_llm = OllamaLLM()

llm_registry.register_llm(
    LLMTypes.GROQ,
    groq_llm,
)

llm_registry.register_llm(
    LLMTypes.GEMINI,
    gemini_llm,
)

llm_registry.register_llm(
    LLMTypes.OLLAMA,
    ollama_llm,
)

print("\nRegistered LLMs:")
for name in llm_registry.get_all_llms():
    print(name)


prompt_router_prompt = PromptRouterPrompt()

prompt_registry = PromptRegistry()

#Prompt
prompt_router = LLMPromptRouter(
    llm=routing_llm,
    prompt_template=prompt_router_prompt,
    registry=prompt_registry,
)


prompt_registry.register_prompt(
    DefaultPromptTemplate()
)

prompt_registry.register_prompt(
    SummaryPromptTemplate()
)

prompt_registry.register_prompt(
    ConcisePromptTemplate()
)

prompt_registry.register_prompt(
    CitationPromptTemplate()
)

prompt_manager = PromptManager(
    router=prompt_router,
    registry=prompt_registry,
)


llm_router = LLMLLMRouter(
    llm=groq_llm,
    prompt_template=LLMRouterPrompt(),
    registry=llm_registry,
)

fallback_strategy = DefaultFallbackStrategy()

llm_manager = LLMManager(
    router=llm_router,
    registry=llm_registry,
    fallback_strategy=fallback_strategy,
)


context_registry = ContextRegistry()

context_registry.register_strategy(
    "default",
    DefaultContextStrategy(),
)

context_registry.register_strategy(
    "hybrid",
    HybridContextStrategy(),
)

context_registry.register_strategy(
    "lcm",
    LCMContextStrategy(),
)

context_router = LLMContextRouter(
    llm=routing_llm,
    prompt_template=ContextRouterPrompt(),
    registry=context_registry,
)

context_manager = ContextManager(
    router=context_router,
    registry=context_registry,
)

#Reranker
reranker = RerankerFactory.create(RerankerTypes.NONE,)

#Context Strategy
context_strategy = ContextStrategyFactory.create()

#Token Budget
token_budget_strategy = TokenBudgetStrategyFactory.create()

# Security
security_guard = SecurityGuardFactory.create(
    security_type=SecurityTypes.LLM,
    llm=routing_llm
)

# Output Guard
output_guard = OutputGuardFactory.create()

# ---------------- Tools ---------------- #

tool_registry = ToolRegistry()

tool_registry.register_tool(
    CalculatorTool()
)

tool_registry.register_tool(
    DateTimeTool()
)

print("Registered tools:")
for tool in tool_registry.list_tools():
    print("-", tool.name)

tool_executor = ToolExecutor(
    registry=tool_registry,
)

tool_router = RuleBasedToolRouter()

tool_manager = ToolManager(
    router=tool_router,
    executor=tool_executor,
)

# Pipeline
pipeline = RAGPipeline(
    retriever=retriever,
    document_store=document_store,
    prompt_manager=prompt_manager,
    llm_manager=llm_manager,
    reranker=reranker,
    context_manager=context_manager,
    token_budget_strategy=token_budget_strategy,
    security_guard=security_guard,
    output_guard=output_guard,
    tool_manager=tool_manager,
)

current_user = User(
    username="test_user",
    roles=[
        RoleFactory.create(RoleTypes.HR),
    ],
)

response = pipeline.run(
    # query="Are Cart and Wishlist used here?",
    # query="Summarize this PDF.",
    # query="Answer this in one sentence.",
    # query="I need an offline private answer.",
    query="Compare the functional and non-functional requirements.",
    # query="What database is used?",
    user=current_user,
)


#Assertions
assert response.text
assert len(response.text.strip()) > 0
# assert response.model == llm.model_name
assert response.model is not None

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