from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.vectorstores.chroma_vector_store import ChromaVectorStore

from src.retrievers.similarity_retriever import SimilarityRetriever

from src.prompts.default_prompt_template import DefaultPromptTemplate

from src.llms.groq_llm import GroqLLM

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


#Reranker
reranker = RerankerFactory.create(RerankerTypes.NONE,)

#Context Strategy
context_strategy = ContextStrategyFactory.create()

#Token Budget
token_budget_strategy = TokenBudgetStrategyFactory.create()

# Security
security_guard = SecurityGuardFactory.create(
    security_type=SecurityTypes.LLM,
    llm=llm,
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
    prompt_template=prompt_template,
    llm=llm,
    reranker=reranker,
    context_strategy=context_strategy,
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
    query="Are Cart and Wishlist used here?",
    user=current_user,
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