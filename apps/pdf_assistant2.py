import sys 

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import os
import tempfile

import streamlit as st

from src.factories.loader_factory import LoaderFactory
from src.factories.splitter_factory import SplitterFactory
from src.factories.embedding_factory import EmbeddingFactory
from src.factories.vector_store_factory import VectorStoreFactory
from src.factories.retriever_factory import RetrieverFactory
from src.prompts.default_prompt_template import DefaultPromptTemplate
from src.factories.llm_factory import LLMFactory
from src.factories.reranker_factory import RerankerFactory
from src.factories.security_guard_factory import SecurityGuardFactory

from src.constants import (
    LoaderTypes,
    SplitterTypes,
    EmbeddingTypes,
    VectorStoreTypes,
    RetrieverTypes,
    LLMTypes,
    RerankerTypes,
    SecurityTypes,
    RoleTypes,
    ToolRouterTypes,
    ContextRouterTypes
)

from src.pipelines.indexing_pipeline import IndexingPipeline
from src.pipelines.rag_pipeline import RAGPipeline
from src.pipelines.conversational_rag_pipeline import ConversationalRAGPipeline

from src.factories.context_strategy_factory import ContextStrategyFactory
from src.factories.token_budget_strategy_factory import TokenBudgetStrategyFactory

from src.factories.security_guard_factory import SecurityGuardFactory
from src.factories.output_guard_factory import OutputGuardFactory


from src.auth.user import User
from src.factories.role_factory import RoleFactory

from src.tools.tool_registry import ToolRegistry
from src.tools.tool_executor import ToolExecutor
from src.tools.calculator_tool import CalculatorTool
from src.tools.date_time_tool import DateTimeTool

from src.tool_routing.rule_based_tool_router import RuleBasedToolRouter
from src.tools.tool_manager import ToolManager

from src.tool_routing.llm_tool_router import LLMToolRouter
from src.prompts.tool_router_prompt import ToolRouterPrompt

from src.prompt_routing.rule_based_prompt_router import RuleBasedPromptRouter
from src.prompts.prompt_manager import PromptManager

from src.factories.prompt_router_factory import PromptRouterFactory
from src.constants import PromptRouterTypes

from src.prompts.prompt_router_prompt import PromptRouterPrompt

from src.document_store.in_memory_document_store import InMemoryDocumentStore

from src.prompts.prompt_registry import PromptRegistry
from src.prompts.default_prompt_template import DefaultPromptTemplate
from src.prompts.summary_prompt_template import SummaryPromptTemplate
from src.prompts.concise_prompt_template import ConcisePromptTemplate
from src.prompts.citation_prompt_template import CitationPromptTemplate

from src.document_store.in_memory_document_store import InMemoryDocumentStore

from src.llms.llm_registry import LLMRegistry
from src.llms.llm_manager import LLMManager

from src.llm_routing.rule_based_llm_router import RuleBasedLLMRouter
from src.llm_strategies.default_fallback_strategy import DefaultFallbackStrategy
from src.factories.llm_manager_factory import LLMManagerFactory

from src.memory.memory_manager import MemoryManager
from src.memory.conversation_buffer_memory import ConversationBufferMemory
from src.memory.conversation_window_memory import ConversationWindowMemory
from src.memory.summary_memory import SummaryMemory

from src.strategies.context_registry import ContextRegistry
from src.strategies.context_manager import ContextManager

from src.strategies.default_context_strategy import DefaultContextStrategy
from src.strategies.hybrid_context_strategy import HybridContextStrategy
from src.strategies.lcm_context_strategy import LCMContextStrategy

from src.context_routing.rule_based_context_router import RuleBasedContextRouter
from src.context_routing.llm_context_router import LLMContextRouter
from src.prompts.context_router_prompt import ContextRouterPrompt

from src.core.context_request import ContextRequest

from src.query_rewriting.rule_based_query_rewriter import RuleBasedQueryRewriter
from src.query_rewriting.query_rewriter_manager import QueryRewriterManager

from src.query_rewriting.llm_query_rewriter import LLMQueryRewriter

from src.memory_retrieval.keyword_memory_retriever import KeywordMemoryRetriever
from src.memory_retrieval.memory_retriever_manager import MemoryRetrieverManager



from src.config.framework_config import FrameworkConfig
from src.config.core_builder import CoreBuilder
from src.config.framework_builder import FrameworkBuilder

from src.constants import MemoryTypes


current_user = User(
    username="anwesha",
    roles=[
       RoleFactory.create(RoleTypes.ADMIN),
    ],
)


st.set_page_config(
    page_title="MiniRAG PDF Assistant",
    page_icon="📄",
    layout="wide",
)

st.title("📄 MiniRAG PDF Assistant")

st.caption(
    "Upload a PDF and ask questions using Retrieval-Augmented Generation."
)

if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:

    st.header("📂 Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
    )

    st.divider()

    if st.session_state.indexed:

        st.success("✅ Document Indexed")

        st.write(f"**Current PDF:**")
        st.caption(st.session_state.current_file)

        if "num_chunks" in st.session_state:
            st.write(f"**Chunks:** {st.session_state.num_chunks}")

        st.write("**Embedding:**")
        st.caption("Sentence Transformers")

        st.write("**Vector Store:**")
        st.caption("ChromaDB")

        st.write("**LLM:**")
        st.caption("Groq Llama 3.3 70B")


if uploaded_file is not None: 

    file_changed = (
        uploaded_file.name != st.session_state.current_file
    )

    if file_changed:

        st.session_state.messages = []

        st.session_state.indexed = False
        st.session_state.rag_pipeline = None
        st.session_state.current_file = None

        with st.spinner("📄 Saving uploaded PDF..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as temp_file:

                temp_file.write(uploaded_file.getbuffer())
                pdf_path = temp_file.name

        st.success("PDF uploaded successfully!")



        config = FrameworkConfig(
            loader_type=LoaderTypes.PDF,
            splitter_type=SplitterTypes.RECURSIVE,
            embedding_type=EmbeddingTypes.HUGGINGFACE,
            vector_store_type=VectorStoreTypes.CHROMA,
            retriever_type=RetrieverTypes.SIMILARITY,

            llm_types=[
                LLMTypes.GROQ,
                LLMTypes.GEMINI,
                LLMTypes.OLLAMA,
            ],

            conversation_window_size=2,

            summarize_after=6,

            prompt_router_type=PromptRouterTypes.RULE_BASED,

            tool_router_type=ToolRouterTypes.LLM,

            context_router_type=ContextRouterTypes.RULE_BASED,
        )

        builder = FrameworkBuilder(config)



        framework = builder.build(pdf_path)

        tool_manager = framework.tool_manager

        prompt_manager = framework.prompt_manager

        memory = framework.memory

        context_manager = framework.context_manager

        st.write(type(framework))

        st.write(type(framework.core))

        st.write(type(framework.llm_manager))



        core = builder.build_core(pdf_path)


        loader = core["loader"]
        splitter = core["splitter"]
        embedding_model = core["embedding_model"]
        vector_store = core["vector_store"]
        retriever = core["retriever"]

        print("\n========== FRAMEWORK BUILDER TEST ==========")
        print(type(core["loader"]))
        print(type(core["splitter"]))
        print(type(core["embedding_model"]))
        print(type(core["vector_store"]))
        print(type(core["retriever"]))
        print("===========================================\n")  





        # loader = LoaderFactory.create(LoaderTypes.PDF, file_path=pdf_path,)

        # splitter = SplitterFactory.create(SplitterTypes.RECURSIVE,)

        # embedding_model = EmbeddingFactory.create(EmbeddingTypes.HUGGINGFACE,)

        # vector_store = VectorStoreFactory.create(
        #     VectorStoreTypes.CHROMA,
        #     collection_name="streamlit_pdf_assistant",
        #     persist_directory="./streamlit_chroma_db",
        # )

        vector_store.clear()

        document_store = InMemoryDocumentStore()

        indexing_pipeline = IndexingPipeline(
            loader=loader,
            splitter=splitter,
            embedding_model=embedding_model,
            vector_store=vector_store,
            document_store=document_store,
        )
        try: 
            with st.spinner("🧠 Indexing document..."):
                chunks = indexing_pipeline.run(
                    metadata={
                        "permission": "VIEW_HR_DOCUMENTS"
                    }
                )
        except Exception as e:
            st.error(f"Indexing failed: {e}")
            st.stop()
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)



        # retriever = RetrieverFactory.create(
        #     RetrieverTypes.SIMILARITY,
        #     embedding_model=embedding_model,
        #     vector_store=vector_store,
        # )

        # llm = LLMFactory.create(LLMTypes.GROQ,)

        # llm_registry = LLMRegistry()

        # groq_llm = LLMFactory.create(
        #     LLMTypes.GROQ,
        # )

        # gemini_llm = LLMFactory.create(
        #     LLMTypes.GEMINI,
        # )

        # ollama_llm = LLMFactory.create(
        #     LLMTypes.OLLAMA,
        # )

        # llm_registry.register_llm(
        #     LLMTypes.GROQ,
        #     groq_llm,
        # )

        # llm_registry.register_llm(
        #     LLMTypes.GEMINI,
        #     gemini_llm,
        # )

        # llm_registry.register_llm(
        #     LLMTypes.OLLAMA,
        #     ollama_llm,
        # )


        reranker = RerankerFactory.create(RerankerTypes.NONE,)

        # prompt_registry = PromptRegistry()

        # prompt_registry.register_prompt(
        #     DefaultPromptTemplate()
        # )

        # prompt_registry.register_prompt(
        #     SummaryPromptTemplate()
        # )

        # prompt_registry.register_prompt(
        #     ConcisePromptTemplate(),
        # )

        # prompt_registry.register_prompt(
        #     CitationPromptTemplate(),
        # )

        # prompt_router = PromptRouterFactory.create(
        #     prompt_router = RuleBasedPromptRouter(),
        #     llm=groq_llm,
        #     prompt_template=PromptRouterPrompt(),
        #     registry=prompt_registry,
        # )

        # prompt_router = RuleBasedPromptRouter()

        # prompt_manager = PromptManager(
        #     router=prompt_router,
        #     registry=prompt_registry,
        #     # llm=llm,
        #     # prompt_template=PromptRouterPrompt(),
        # )

        # llm_router = RuleBasedLLMRouter()

        # fallback_strategy = DefaultFallbackStrategy()

        # llm_manager = LLMManagerFactory.create(
        #     router=llm_router,
        #     registry=llm_registry,
        #     fallback_strategy=fallback_strategy,
        # )

        llm_manager = builder.build_llm()
        


        # tool_router_prompt = ToolRouterPrompt()


        # ---------------- Tools ---------------- #

        # tool_registry = ToolRegistry()

        # tool_registry.register_tool(
        #     CalculatorTool()
        # )

        # tool_executor = ToolExecutor(
        #     registry=tool_registry,
        # )

        # tool_registry.register_tool(
        #     DateTimeTool()
        # )

        # tool_router = LLMToolRouter(
        #     llm_manager=llm_manager,
        #     prompt_template=tool_router_prompt,
        #     registry=tool_registry,
        # )

        # tool_manager = ToolManager(
        #     router=tool_router,
        #     executor=tool_executor,
        # )

        # llm_router = RuleBasedLLMRouter()

        # fallback_strategy = DefaultFallbackStrategy()

        # llm_manager = LLMManagerFactory.create(
        #     router=llm_router,
        #     registry=llm_registry,
        #     fallback_strategy=fallback_strategy,
        # )


        security_guard = SecurityGuardFactory.create(
            security_type=SecurityTypes.LLM,
            llm_manager=llm_manager,
        )

        output_guard = OutputGuardFactory.create()

        # context_strategy = ContextStrategyFactory.create()

        token_budget_strategy = TokenBudgetStrategyFactory.create()

        # llm_router = RuleBasedLLMRouter()

        # fallback_strategy = DefaultFallbackStrategy()

        # llm_manager = LLMManagerFactory.create(
        #     router=llm_router,
        #     registry=llm_registry,
        #     fallback_strategy=fallback_strategy,
        # )


        # buffer_memory = ConversationBufferMemory()

        # window_memory = ConversationWindowMemory(
        #     window_size=2,
        # )

        # summary_memory = SummaryMemory(
        #     llm_manager=llm_manager,
        #     summarize_after=6,
        # )

        # memory = MemoryManager(
        #     buffer_memory=buffer_memory,
        #     window_memory=window_memory,
        #     summary_memory=summary_memory,
        # )


        memory_retriever = MemoryRetrieverManager(
            retriever=KeywordMemoryRetriever(),
        )

        query_rewriter = QueryRewriterManager(
            rewriter=LLMQueryRewriter(
                llm_manager=llm_manager,
            ),
        )


        # context_registry = ContextRegistry()

        # context_registry.register_strategy(
        #     "default",
        #     DefaultContextStrategy(),
        # )

        # context_registry.register_strategy(
        #     "hybrid",
        #     HybridContextStrategy(),
        # )

        # context_registry.register_strategy(
        #     "lcm",
        #     LCMContextStrategy(),
        # )

#         context_router = LLMContextRouter(
#               llm_manager=llm_manager,
#               prompt_template=context_prompt_template,
#               registry=context_registry,
#         )

        # context_router = RuleBasedContextRouter()

        # context_manager = ContextManager(
        #     router=context_router,
        #     registry=context_registry,
        # )


        rag_pipeline = ConversationalRAGPipeline(
            retriever=retriever,
            prompt_manager=prompt_manager,
            document_store=document_store,
            llm_manager=llm_manager,
            reranker=reranker,
            context_manager=context_manager,
            token_budget_strategy=token_budget_strategy,
            security_guard=security_guard,
            output_guard=output_guard,
            tool_manager=tool_manager,
            memory=memory,
            query_rewriter=query_rewriter,
            memory_retriever=memory_retriever,
        )

        st.session_state.rag_pipeline = rag_pipeline
        st.session_state.indexed = True
        st.session_state.current_file = uploaded_file.name
        st.session_state.num_chunks = len(chunks)

        st.rerun()

        st.success(f"✅ Successfully indexed {len(chunks)} chunks!")



# ---------------- Chat ---------------- #

if st.session_state.indexed:

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_question = st.chat_input(
        "Ask a question about the PDF..."
    )

    if user_question:

        # Display user message immediately
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question,
            }
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        # Generate assistant response
        with st.chat_message("assistant"):

            with st.spinner("🤖 Thinking..."):

                try:

                    llm_response = st.session_state.rag_pipeline.run(
                        query=user_question,
                        user=current_user,
                    )

                    assistant_answer = llm_response.text

                except PermissionError as e:
                    assistant_answer = f"🔒 {e}"

                except Exception as e:

                    import traceback

                    st.code(traceback.format_exc())

                    assistant_answer = f"❌ Error: {e}"

                st.markdown(assistant_answer)

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_answer,
            }
        )




# if st.session_state.indexed:

#     st.success(
#         f"Current document: {st.session_state.current_file}"
#     )

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     user_question = st.chat_input(
#         "Ask a question about the PDF..."
#     )

#     if user_question:
#         st.session_state.messages.append(
#             {
#                 "role": "user",
#                 "content": user_question,
#             }
#         )

#         with st.chat_message("user"):
#             st.markdown(user_question)

#         with st.chat_message("assistant"):

#             with st.spinner("Thinking..."):

#                 response = st.session_state.rag_pipeline.run(
#                     query=user_question,
#                 )

#                 assistant_answer = response.text

#                 st.markdown(assistant_answer)

#         st.session_state.messages.append(
#             {
#                 "role": "assistant",
#                 "content": assistant_answer,
#                 }
#         )